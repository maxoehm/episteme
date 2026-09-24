"""
LatentGraphConsolidation — fast mathematical sweep for parallel collisions (Phase 3b).

Uses vector embeddings of minted Layer 2 nodes to find and merge duplicates
caused by parallel processing. Two nodes are merged if they are within a strict
Euclidean/Cosine distance threshold and share highly overlapping Phase 3 relation edges.
"""

from __future__ import annotations

import logging
from collections import defaultdict

import numpy as np

from episteme_pipeline.contracts.domain import L2Entity
from episteme_pipeline.protocols.fusion import InstanceFusion
from episteme_pipeline.protocols.graph_store import FusionGraph

logger = logging.getLogger(__name__)


def _union_find_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Compute connected components of a graph using Union-Find.

    Parameters
    ----------
    n : int
        The number of nodes in the graph (indexed from 0 to n-1).
    edges : list[tuple[int, int]]
        A list of undirected edges represented as pairs of node indices.

    Returns
    -------
    list[list[int]]
        A list of lists, where each sublist contains the node indices belonging to
        the same connected component.
    """
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        parent[find(x)] = find(y)

    for i, j in edges:
        union(i, j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)
    return list(groups.values())


class LatentGraphConsolidation(InstanceFusion):
    """Mathematical sweep over dense vectors to merge duplicate Layer 2 nodes.

    Parameters
    ----------
    embedding_model : object, optional
        The embedding model used to project textual envelopes into vector space.
    dense_similarity_threshold : float, default 0.85
        The minimum cosine similarity required to consider two nodes as duplicates.
    relation_overlap_threshold : float, default 0.8
        The minimum Jaccard similarity threshold for 1-hop relation edge overlap.
    """

    def __init__(
        self,
        embedding_model=None,
        dense_similarity_threshold: float = 0.85,
        relation_overlap_threshold: float = 0.8,
    ) -> None:
        self.embedding_model = embedding_model
        self.dense_similarity_threshold = dense_similarity_threshold
        self.relation_overlap_threshold = relation_overlap_threshold

    async def _get_relations_for_entity(self, entity_id: str, graph_store: FusionGraph) -> set[str]:
        """Fetch the relation signatures for a given entity.

        Parameters
        ----------
        entity_id : str
            The unique identifier of the entity.
        graph_store : FusionGraph
            The graph store containing the entity neighborhood.

        Returns
        -------
        set[str]
            A set of string signatures representing incoming and outgoing relations.
        """
        env = await graph_store.get_neighborhood(entity_id, depth=1)
        if not env.nodes and not env.triples:
            return set()
        
        signatures = set()
        for t in env.triples:
            if t.subject_id == entity_id:
                signatures.add(f"OUT:{t.predicate}:{t.object_id}")
            elif t.object_id == entity_id:
                signatures.add(f"IN:{t.predicate}:{t.subject_id}")
        return signatures

    def _jaccard(self, set1: set[str], set2: set[str]) -> float:
        """Compute the Jaccard similarity coefficient between two sets.

        Parameters
        ----------
        set1 : set[str]
            The first set of strings.
        set2 : set[str]
            The second set of strings.

        Returns
        -------
        float
            The Jaccard similarity index, ranging from 0.0 to 1.0. Returns 1.0 if
            both sets are empty.
        """
        if not set1 or not set2:
            # If both are empty, Jaccard is mathematically 1.0, but semantically 
            # we return 0.0 for graph merging (isolated nodes aren't automatically identical).
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return float(intersection) / union

    async def fuse(self, graph_store: FusionGraph) -> dict[str, str]:
        """Find and merge duplicate Layer 2 nodes in the graph.

        Finds groups of entities with the same label that meet both the dense similarity
        threshold and structural relation overlap threshold, then maps duplicates to a
        canonical entity.

        Parameters
        ----------
        graph_store : FusionGraph
            The graph store containing Layer 2 entities and relation edges.

        Returns
        -------
        dict[str, str]
            A dictionary mapping duplicate entity IDs to their canonical entity ID.
        """
        if self.embedding_model is None:
            logger.warning("LatentGraphConsolidation: no embedding_model — returning empty map.")
            return {}

        entities = await graph_store.get_entities()
        if len(entities) < 2:
            return {}

        # 1. Embed textual envelopes
        texts = [e.textual_envelope or e.name for e in entities]
        embeddings_list = await self.embedding_model.aget_text_embedding_batch(texts)
        embeddings = np.array(embeddings_list)

        # Normalize for cosine similarity via dot product
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0] = 1e-10
        embeddings_normalized = embeddings / norms
        sim_matrix = np.dot(embeddings_normalized, embeddings_normalized.T)

        n = len(entities)
        edges = []

        # 2. Find candidates passing dense threshold
        for i in range(n):
            for j in range(i + 1, n):
                # Only compare entities of the same label
                if entities[i].label != entities[j].label:
                    continue
                
                if sim_matrix[i, j] >= self.dense_similarity_threshold:
                    # 3. Check structural overlap
                    rel_i = await self._get_relations_for_entity(entities[i].id, graph_store)
                    rel_j = await self._get_relations_for_entity(entities[j].id, graph_store)
                    
                    overlap = self._jaccard(rel_i, rel_j)
                    if overlap >= self.relation_overlap_threshold:
                        edges.append((i, j))

        # 4. Cluster connected components
        clusters = _union_find_components(n, edges)

        # 5. Build fused map (map all to the most grounded entity in cluster)
        fused_map: dict[str, str] = {}
        for cluster in clusters:
            if len(cluster) < 2:
                continue
            
            # Elect canonical: most grounded (most source chunks)
            cluster_entities = [entities[idx] for idx in cluster]
            cluster_entities.sort(key=lambda e: len(e.source_chunk_ids), reverse=True)
            canonical = cluster_entities[0]
            
            for e in cluster_entities[1:]:
                fused_map[e.id] = canonical.id
                
        return fused_map
