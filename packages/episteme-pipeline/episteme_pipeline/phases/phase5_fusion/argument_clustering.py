"""
EmbeddingArgumentClustering — global argument resolution via Key Point Analysis.

Groups semantically equivalent argument components across chunks/documents.
Each cluster represents arguments that are logically the same claim or premise,
possibly restated in different sections.

Strategy:
  1. Retrieve all TheoryAtom nodes from the graph
  2. Embed their texts using the embedding_model (async, batched)
  3. Compute pairwise cosine similarity
  4. Find connected components where any pair exceeds the similarity threshold
     (single-linkage clustering — fast, O(N²) which is fine for V1)
  5. Return clusters of size ≥ 2 (singletons need no merging)

The caller (`Phase5bTheoryFusionRunner.run`) receives the cluster list and can use it
to merge or link canonical nodes. No graph mutations are performed here — the
cluster structure is returned for the caller to act on.

This is intentionally simple. More sophisticated approaches (HDBSCAN, Key Point
Analysis from IBM, or a fine-tuned cross-encoder for argument similarity) can be
plugged in by subclassing ArgumentClustering and injecting the new implementation.
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict

from episteme_pipeline.protocols.fusion import ArgumentClustering
from episteme_pipeline.protocols.graph_store import GraphReader

logger = logging.getLogger(__name__)


def _union_find_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Union-find connected components from a list of (i, j) edges."""
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


class EmbeddingArgumentClustering(ArgumentClustering):
    """
    Cosine-similarity connected-components clustering over L3 argument components.

    Requires an embedding_model to be injected. Falls back to empty clusters if
    no embedding_model is available (safe for pipelines without argument mining).
    """

    def __init__(
        self,
        embedding_model=None,
        similarity_threshold: float = 0.85,
        max_components: int = 10000,
    ) -> None:
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.max_components = max_components

    async def cluster(
        self,
        graph_store: GraphReader,
    ) -> list[list[str]]:
        if self.embedding_model is None:
            logger.warning(
                "EmbeddingArgumentClustering: no embedding_model — skipping clustering."
            )
            return []

        components = await graph_store.get_theory_atoms()
        n = len(components)

        if n < 2:
            return []

        if n > self.max_components:
            logger.warning(
                "Phase 5b: %d components exceeds max_components=%d — clustering skipped to avoid O(%.0f) memory usage",
                n,
                self.max_components,
                n * n,
            )
            return []

        logger.info("Phase 5b: clustering %d argument components.", n)

        # Embed all component texts (concurrent)
        texts = [c.text for c in components]
        # The EmbeddingModel contract is async-only; no sync fallback needed.
        raw_embeddings = await self.embedding_model.aget_text_embedding_batch(texts)

        import numpy as np

        matrix = np.array(raw_embeddings, dtype=np.float32)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        matrix = matrix / norms

        # Pairwise cosine similarity (N×N, vectorized)
        sim = matrix @ matrix.T

        # Collect edges where similarity ≥ threshold (upper triangle only)
        edges = [
            (i, j)
            for i in range(n)
            for j in range(i + 1, n)
            if sim[i, j] >= self.similarity_threshold
        ]

        if not edges:
            return []

        groups = _union_find_components(n, edges)
        ids = [c.id for c in components]

        clusters = [[ids[i] for i in group] for group in groups if len(group) > 1]

        logger.info(
            "Phase 5b: found %d argument clusters (threshold=%.2f).",
            len(clusters),
            self.similarity_threshold,
        )
        return clusters
