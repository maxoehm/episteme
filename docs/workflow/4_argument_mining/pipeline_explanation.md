# Phase 4b: Argument Mining

## Overview

Phase 4b extracts argumentative structure from each chunk: it segments text into Argumentative Discourse Units (ADUs),
classifies each ADU and its local relations (ACC + ARI), and then evaluates global cross-chunk argument relations (ARC).
The output populates Layer 3 of the knowledge graph with `ArgumentComponent` nodes and `SUPPORTS`/`ATTACKS` edges.

Processing is crash-resilient: each chunk is marked `phase4_processed` only after its components and local relations are
committed. ARC runs once globally after all per-chunk processing completes.

## Goals

- Segment each chunk into typed ADUs (Claim, MajorClaim, Premise).
- Extract local (within-chunk) argument relations between ADUs in a single LLM pass (ADR 0004).
- Identify global (cross-chunk) argument relations between components using TAG context.
- Map the resulting argument graph structure to a Theoriennetz (TF) representation.
- Commit all argument structures incrementally and crash-safely.

## Steps

1. **ADU Segmentation** (`LLMADUSegmenter`):
    - The LLM receives the chunk text and returns it re-annotated with `<AC id="...">...</AC>` markup tags.
    - If no ADUs are identified, the chunk is skipped cleanly.
2. **ACC Classification** (`LLMACCClassifier`):
    - The annotated text and extracted ADU spans are passed to a second LLM call against `ACCOutput`.
    - The LLM returns: per-ADU `component_type` (`CLAIM | MAJOR_CLAIM | PREMISE`) and local relation triples
      `(source_id, relation, target_id, confidence)`.
    - **ACC and ARI are fused in one pass** (ADR 0004) — the classifier outputs both types and local relations together.
3. **Stable ID Assignment**:
    - `_stable_component_id(chunk_id, ac_tag) = "ac_" + sha256("{chunk_id}:{ac_tag}")[:14]`.
    - The same ADU appearing across retries maps to the same graph ID.
4. **Schema Validation**:
    - `component_type` is validated against `schema.component_types`.
    - `relation` is validated against `schema.argument_relation_types`.
    - Unknown values outside the schema are dropped.
5. **Graph Commit (Per Chunk)**:
    - `ArgumentComponent` nodes upserted via MERGE.
    - Local `SUPPORTS`/`ATTACKS` edges committed.
    - `EXTRACTED_FROM` edges created from component to Chunk (`confidence: 1.0`).
    - Chunk marked `phase4_processed = true`.
6. **ARC Classification** (`TAGARCClassifier`):
    - After all chunks are processed, cross-chunk argument pairs are formed (components from different chunks only).
    - For each pair, `global_extractor.get_subgraph_envelope()` retrieves TAG context.
    - The LLM classifies the stance (`SUPPORTS` or `ATTACKS`).
    - Valid global relations are committed with `source="global"`.
7. **Theoriennetz (TF) Mapping**:
    - The complete argument graph is mapped to `TF(atoms, relations)` where atoms are all `ArgumentComponent` nodes
      typed by `component_type` and relations are all `SUPPORTS`/`ATTACKS` edges (ADR 0007).

## Phase Data Flow

- **Input:** `Phase3ArtifactsView` over global relations — used to confirm Phase 3 completion; per-chunk content is read
  directly from the graph via `get_unprocessed_chunks("phase4")`.
- **Output:** Phase 4 argument component / relation artifact collection.
- **Graph updates:**
    - `ArgumentComponent` nodes: `id`, `text`, `component_type`, `source_chunk_id`
    - `SUPPORTS` / `ATTACKS` edges: `confidence`, `source: "local" | "global"`
    - `EXTRACTED_FROM` edges: ArgumentComponent $\to$ Chunk (`confidence: 1.0`)
    - `Chunk.phase4_processed = true` after each successful chunk

## ACC + ARI Fusion

ADU Classification (ACC) and local Argument Relation Identification (ARI) are handled in a single LLM call. The ACC
prompt asks the model to output both typed components and the local relations between them. This eliminates an extra
round-trip LLM call per chunk.

The `ARIIdentifier(ABC)` override point is preserved for advanced use cases where a dedicated relation identification
step is preferable (see ADR 0004).

## ARC and GlobalRelationExtractor

ARC (Argument Relation Classification) reuses `GlobalRelationExtractor` — the same instance injected into Phase 3. For
each cross-chunk component pair, `get_subgraph_envelope()` retrieves TAG context, grounding stance classification in
document structure rather than raw text proximity.

Cross-chunk pair formation is capped by `Phase4Config.arc_max_candidates_per_component` to prevent combinatorial blowup.

## Pluggability

- **ADU Segmenter**: Implement `ADUSegmenter(ABC)` and inject via `Phase4Runner(adu_segmenter=MySegmenter())`.
- **ACC Classifier**: Implement `ACCClassifier(ABC)` and inject via `Phase4Runner(acc_classifier=MyClassifier())`.
- **ARC Classifier**: Implement `ARCClassifier(ABC)` and inject via `Phase4Runner(arc_classifier=MyClassifier())`.
- **ARI (Dedicated Pass)**: Implement `ARIIdentifier(ABC)` for documents requiring separate relation identification.
- **Global Extractor**: Shared with Phase 3; inject via `Phase4Runner(global_extractor=MyExtractor())`.
- **Schema**: Validated against `SchemaConfig`.

## ADR References

- [ADR 0004: ACC Outputs Triples Single Pass](../../adr/0004-acc-outputs-triples-single-pass.md)
- [ADR 0007: TF Structural Correspondence](../../adr/0007-tf-structural-correspondence.md)

## Implementation

- `pipeline/phases/phase4_argument_mining/__init__.py` — `Phase4Runner`
- `pipeline/phases/phase4_argument_mining/adu_segmenter.py` — `LLMADUSegmenter`
- `pipeline/phases/phase4_argument_mining/acc_classifier.py` — `LLMACCClassifier`
- `pipeline/phases/phase4_argument_mining/arc_classifier.py` — `TAGARCClassifier`
- `pipeline/phases/phase4_argument_mining/models.py` — `ADUSegmentationOutput`, `ACCOutput`, `ARCRelationOutput`
- `pipeline/protocols/argument_mining.py` — `ADUSegmenter(ABC)`, `ACCClassifier(ABC)`, `ARCClassifier(ABC)`,
  `ARIIdentifier(ABC)`
