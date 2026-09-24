# Phase 3: Global Relation Extraction

## Overview

Phase 3 discovers semantic relations between entity pairs across chunk and document boundaries. Where Phase 2 extracts
local (within-chunk) triples, Phase 3 identifies global relations whose evidence is distributed across the corpus.

The default SOTA implementation uses **`DenseRetrievalGlobalRelationExtractor`** (Retrieve $\to$ Rerank $\to$ Extract),
combining dense vector retrieval, Text-Attributed Graph (TAG) subgraph envelopes, Cross-Encoder joint-attention
reranking, and structured LLM decoding.

Processing is crash-resilient: entities are read from the graph store (or from the Phase 2 artifact view on first run).
Each committed global triple carries `scope="global"` to distinguish it from Phase 2 local triples.

## Goals

- Identify semantically meaningful relations between entity pairs across different documents and chunks.
- Break chunk boundaries via dense vector candidate generation rather than relying solely on co-occurrence.
- Filter candidate pairs with high precision using Cross-Encoder joint attention before invoking LLM decoding.
- Retrieve coherent evidence envelopes (subgraph context) per candidate pair.
- Validate all extracted relation types against `SchemaConfig`.
- Provide a reusable `GlobalRelationExtractor` interface shared with Phase 4b ARC.

## Steps (Retrieve $\to$ Rerank $\to$ Extract)

1. **Entity Loading**: All Layer 2 entities are loaded from the graph store via `get_entities()` (falling back to
   `Phase2ArtifactsView` on first run).
2. **Dense Candidate Generation (The Prior)**:
    - Entities are embedded globally using their name and description.
    - Pairwise cosine similarities are computed across the corpus.
    - Pairs exceeding `Phase3Config.dense_similarity_threshold` form the candidate set, capped at
      `max_candidates_per_entity_pair` per entity hub.
3. **Subgraph Envelope Retrieval (`get_subgraph_envelope`)**:
    - For each candidate entity in a pair, the graph store is queried for up to `subgraph_depth` hops of contextual
      neighborhood (chunk nodes and adjacent entities).
    - Envelopes for entity A and entity B are merged, deduplicated, and formatted into compact context strings.
4. **Cross-Encoder Precision Reranking (`RelationReranker`)**:
    - The candidate entity pair and their merged envelope context are evaluated jointly by `RelationReranker` (e.g.
      `Alibaba-NLP/gte-reranker-modernbert-base`).
    - Cross-encoders perform full cross-attention between entity contexts, filtering spurious semantic matches.
    - Pairs scoring below `Phase3Config.reranker_threshold` are discarded.
5. **LLM Relation Decoding**:
    - Candidate pairs passing the reranker threshold are passed to the LLM via `astructured_predict` against
      `GlobalRelationOutput`.
    - The LLM outputs: `relation: str | None`, `confidence: float`, `direction: Literal["A_to_B", "B_to_A"]`, and
      `reasoning: str`.
6. **Schema Validation & Graph Commit**:
    - If `relation` is not in `SchemaConfig.relation_types`, it is dropped.
    - Valid triples are committed to Neo4j via MERGE with `scope="global"` and `source_chunk_id=None`.

## Phase Data Flow

- **Input:** `Phase2ArtifactsView` (or graph store on resume).
- **Output:** Phase 3 global relation artifact collection.
- **Graph updates:**
    - Relation edges (`SchemaConfig.relation_types`): `confidence`, `scope: "global"`, `source_chunk_id: None`

## GlobalRelationExtractor — Shared Interface

`GlobalRelationExtractor(ABC)` defines the pluggability seam for global relation discovery. It is **shared with Phase 4b
ARC**: the same extractor instance created in `Pipeline.for_task()` is injected into both `Phase3Runner` and
`Phase4Runner`. This guarantees consistent evidence retrieval across the pipeline.

The interface exposes:

- `extract(entities, graph_store, schema) -> list[L2Triple]`: Full batch extraction (Phase 3).
- `get_subgraph_envelope(entity, graph_store, depth) -> SubGraph`: Per-entity contextual envelope retrieval (used by
  Phase 4b ARC for argument component pairs).

### Implementations:

- **`DenseRetrievalGlobalRelationExtractor`** (`pipeline/phases/phase3_global_relations/dense_retrieval_extractor.py`):
  Default SOTA implementation using dense retrieval and Cross-Encoder reranking.
- **`TAGRelationExtractor`** (`pipeline/phases/phase3_global_relations/tag_extractor.py`): Alternative implementation
  utilizing chunk-co-occurrence structural blocking.

## Pluggability

- **Extractor**: Implement `GlobalRelationExtractor(ABC)` and pass via `Phase3Runner(global_extractor=MyExtractor())`.
- **Reranker**: Pass any `RelationReranker` or `CrossEncoder` to `Pipeline.for_task(relation_reranker=...)`.
- **Schema**: Validated dynamically against `SchemaConfig`.

## ADR References

- [ADR 0002: TAG Reranker Global Relation Extraction](../../adr/0002-tag-reranker-global-relation-extraction.md)

## Implementation

- `pipeline/phases/phase3_global_relations/__init__.py` — `Phase3Runner`
- `pipeline/phases/phase3_global_relations/dense_retrieval_extractor.py` — `DenseRetrievalGlobalRelationExtractor`
- `pipeline/phases/phase3_global_relations/tag_extractor.py` — `TAGRelationExtractor`
- `pipeline/phases/phase3_global_relations/rerankers.py` — `CrossEncoderRelationReranker`
- `pipeline/phases/phase3_global_relations/models.py` — `GlobalRelationOutput`
- `pipeline/protocols/extractors.py` — `GlobalRelationExtractor(ABC)`, `RelationReranker(ABC)`
