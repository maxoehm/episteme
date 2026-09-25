"""In-memory graph store implementation conforming to ProcessingGraph.

Enables pure in-memory execution of the pipeline and evaluation harness without
requiring a running Neo4j instance or network connectivity.
"""

from __future__ import annotations

from typing import Any

from episteme_pipeline.contracts.domain import (
    L1Chunk,
    L2Entity,
    L2Triple,
    PhaseItemRecord,
    SearchResult,
    SubGraph,
    TheoryAtom,
    TheoryRelation,
)
from episteme_pipeline.protocols.graph_store import ProcessingGraph


class InMemoryGraphStore(ProcessingGraph):
    """In-memory graph store for offline execution and evaluation."""

    def __init__(self) -> None:
        self._chunks: dict[str, L1Chunk] = {}
        self._entities: dict[str, L2Entity] = {}
        self._triples: list[L2Triple] = []
        self._theory_atoms: dict[str, TheoryAtom] = {}
        self._theory_relations: list[TheoryRelation] = []
        self._generic_relations: list[dict[str, Any]] = []
        self._processed_chunks: dict[str, set[str]] = {}  # chunk_id -> set of phase tags
        self._processed_items: dict[str, dict[str, PhaseItemRecord]] = {}
        self._nodes: dict[str, dict[str, Any]] = {}

    async def close(self) -> None:
        """Close handle (no-op for in-memory)."""
        pass

    async def get_chunks(
        self, filters: dict | None = None, limit: int | None = None
    ) -> list[L1Chunk]:
        chunks = list(self._chunks.values())
        if limit:
            chunks = chunks[:limit]
        return chunks

    async def get_entities(
        self,
        labels: list[str] | None = None,
        filters: dict | None = None,
    ) -> list[L2Entity]:
        entities = list(self._entities.values())
        if labels:
            entities = [e for e in entities if e.label in labels]
        return entities

    async def get_all_entity_triples(self) -> list[L2Triple]:
        return list(self._triples)

    async def get_neighborhood(self, node_id: str, depth: int = 1) -> SubGraph:
        neighbor_nodes = [
            e for e in self._entities.values() if e.id != node_id
        ][:10]
        neighbor_triples = [
            t for t in self._triples if t.subject_id == node_id or t.object_id == node_id
        ]
        return SubGraph(
            center_id=node_id,
            nodes=neighbor_nodes,
            triples=neighbor_triples,
            depth=depth,
        )

    async def vector_search(
        self,
        embedding: list[float],
        top_k: int,
        node_label: str | None = None,
    ) -> list[SearchResult]:
        results: list[SearchResult] = []
        for ent in list(self._entities.values())[:top_k]:
            results.append(
                SearchResult(
                    node_id=ent.id,
                    score=1.0,
                    node_label=ent.label,
                    node_name=ent.name or ent.id,
                )
            )
        return results

    async def get_theory_atoms(self) -> list[TheoryAtom]:
        return list(self._theory_atoms.values())

    async def get_all_theory_relations(self) -> list[TheoryRelation]:
        return list(self._theory_relations)

    async def find_entities_by_name(
        self, name: str, label: str | None = None
    ) -> list[L2Entity]:
        name_lower = name.lower()
        matches = []
        for ent in self._entities.values():
            if ent.name and ent.name.lower() == name_lower:
                if label is None or ent.label == label:
                    matches.append(ent)
        return matches

    async def get_entity_envelopes(self, entity_id: str) -> list[str]:
        ent = self._entities.get(entity_id)
        if ent and ent.textual_envelope:
            return [ent.textual_envelope]
        return []

    async def get_chunk_entities(self, chunk_id: str) -> list[L2Entity]:
        return [
            e
            for e in self._entities.values()
            if chunk_id in (e.source_chunk_ids or [])
        ]

    async def upsert_node(
        self,
        label: str,
        node_id: str,
        properties: dict,
        *,
        extra_labels: tuple[str, ...] = (),
        create_only_properties: dict | None = None,
    ) -> None:
        self._nodes[node_id] = {
            "label": label,
            "extra_labels": extra_labels,
            **properties,
        }

    async def prune_document_children(
        self,
        document_id: str,
        *,
        keep_chunk_ids: list[str],
        keep_chapter_ids: list[str],
    ) -> dict[str, int]:
        keep = set(keep_chunk_ids)
        dead = [
            cid
            for cid, chunk in self._chunks.items()
            if chunk.source_doc_id == document_id and cid not in keep
        ]
        for cid in dead:
            del self._chunks[cid]
        return {"chunks": len(dead), "chapters": 0}

    async def upsert_relation(
        self,
        from_id: str,
        relation_type: str,
        to_id: str,
        properties: dict | None = None,
    ) -> None:
        rel_dict = {
            "from_id": from_id,
            "relation_type": relation_type,
            "to_id": to_id,
            "properties": properties or {},
        }
        self._generic_relations.append(rel_dict)
        self._theory_relations.append(
            TheoryRelation(
                source_id=from_id,
                target_id=to_id,
                relation_type=relation_type,
                confidence=float(properties.get("confidence", 1.0)) if properties else 1.0,
                scope=properties.get("scope", "global") if properties else "global",
                weight=float(properties.get("weight", 1.0)) if properties else 1.0,
            )
        )

    async def upsert_relations(self, relations: list[dict]) -> None:
        for r in relations:
            await self.upsert_relation(
                from_id=r["from_id"],
                relation_type=r["relation_type"],
                to_id=r["to_id"],
                properties=r.get("properties"),
            )

    async def upsert_chunk(self, chunk: L1Chunk) -> None:
        self._chunks[chunk.id] = chunk

    async def upsert_chunks(self, chunks: list[L1Chunk]) -> None:
        for c in chunks:
            await self.upsert_chunk(c)

    async def upsert_entity(self, entity: L2Entity) -> None:
        self._entities[entity.id] = entity

    async def upsert_entities(self, entities: list[L2Entity]) -> None:
        for e in entities:
            await self.upsert_entity(e)

    async def upsert_triple(self, triple: L2Triple) -> None:
        self._triples.append(triple)

    async def upsert_triples(self, triples: list[L2Triple]) -> None:
        for t in triples:
            await self.upsert_triple(t)

    async def upsert_argument_component(self, component: TheoryAtom) -> None:
        self._theory_atoms[component.id] = component

    async def upsert_argument_components(
        self, components: list[TheoryAtom]
    ) -> None:
        for comp in components:
            await self.upsert_argument_component(comp)

    async def upsert_community(
        self, community_id: str, level: int, entity_ids: list[str]
    ) -> None:
        for e_id in entity_ids:
            self._generic_relations.append(
                {
                    "from_id": e_id,
                    "relation_type": "IN_COMMUNITY",
                    "to_id": community_id,
                    "properties": {"level": level},
                }
            )

    async def upsert_communities(self, communities: list[dict]) -> None:
        for c in communities:
            await self.upsert_community(c["community_id"], c["level"], c["entity_ids"])

    async def mark_chunk_processed(self, chunk_id: str, phase: str) -> None:
        self._processed_chunks.setdefault(chunk_id, set()).add(phase)

    async def mark_chunks_processed(self, chunk_ids: list[str], phase: str) -> None:
        for cid in chunk_ids:
            await self.mark_chunk_processed(cid, phase)

    async def get_unprocessed_chunks(
        self, phase: str, limit: int | None = None
    ) -> list[L1Chunk]:
        unprocessed = [
            c
            for c in self._chunks.values()
            if phase not in self._processed_chunks.get(c.id, set())
        ]
        if limit:
            unprocessed = unprocessed[:limit]
        return unprocessed

    async def filter_unprocessed_items(
        self, item_keys: list[str], phase: str
    ) -> list[str]:
        phase_items = self._processed_items.get(phase, {})
        return [k for k in item_keys if k not in phase_items]

    async def commit_phase_batch(
        self,
        phase: str,
        triples: list[L2Triple],
        items: list[PhaseItemRecord],
    ) -> None:
        await self.upsert_triples(triples)
        phase_items = self._processed_items.setdefault(phase, {})
        for record in items:
            phase_items[record.key] = record

    async def clear_phase_checkpoints(self, phase: str) -> None:
        if phase in self._processed_items:
            del self._processed_items[phase]
        for tags in self._processed_chunks.values():
            tags.discard(phase)
