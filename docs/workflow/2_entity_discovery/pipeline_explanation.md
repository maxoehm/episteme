# Phase 2: Entity & Local Relation Discovery

## Overview

Phase 2 processes each chunk from Phase 1 through Named Entity Recognition, entity linking, and local triple extraction.
It populates Layer 2 of the knowledge graph with typed entity nodes and semantically labelled edges derived from
within-chunk co-occurrences.

Processing is crash-resilient: each chunk is marked as `phase2_processed` only after its entities and triples are
committed. Restarting after a failure resumes from the last uncommitted chunk.

## Goals

- Extract named entities of the domain schema types from each chunk
- Assign stable, deterministic graph IDs (same entity name + label = same ID across chunks)
- Link extracted entities to existing canonical nodes where possible (prevent fragmentation)
- Extract local (within-chunk) semantic triples
- Commit all extractions to the graph incrementally

## Steps

1. **NER + local relation extraction** (`LLMNERExtractor`) — structured LLM prediction (`astructured_predict`) against
   `NERExtractionOutput` schema. If `max_gleanings > 0`, the extractor runs an iterative "gleaning" loop, re-prompting
   the LLM with previously extracted entities to capture any missed concepts or relations. Unknown labels are silently
   dropped. See `prompting.md` for the CoT strategy.
2. **Stable ID assignment** — `_stable_entity_id(label, name)` =
   `"entity_" + sha256("{LABEL}::{normalized_name}")[:14]`. The same entity name appearing in multiple chunks maps to
   the same graph ID, enabling MERGE deduplication automatically.
3. **Entity linking** (`NameEntityLinker`) — queries the graph for existing entities with overlapping names (containment
   check, case-insensitive, ≥4 chars). If a match is found, the extracted entity's ID is redirected to the canonical ID,
   and the canonical entity accumulates an additional `source_chunk_id`.
4. **ID redirect propagation** — triples whose `subject_id` or `object_id` was redirected are updated before commit.
5. **Graph commit** — entity nodes (MERGE), local triples (MERGE), and `EXTRACTED_FROM` edges (entity → chunk)
   committed. Chunk marked `phase2_processed`.

## Phase Data Flow

- **Input:** Phase 1 artifact view over documents/chunks — used as fallback if no unprocessed chunks exist in the graph
  (first run). On resume, chunks are read from `get_unprocessed_chunks("phase2")`.
- **Output:** Phase 2 entity mention / linked entity / local relation artifact collection.
- **Graph updates:**
    - Entity nodes (labelled with `SchemaConfig.node_types`): `id`, `name`, `description`, `source_chunk_ids`
    - Relation edges (`SchemaConfig.relation_types`): `confidence`, `scope="local"`, `source_chunk_id`
    - `EXTRACTED_FROM` edges: entity → Chunk (`confidence: 1.0`)
    - `Chunk.phase2_processed = true` after each successful chunk

## Coreference handling

Local coreferences (pronouns, within-chunk aliases) are resolved implicitly by the NER LLM prompt. Cross-chunk aliases
are resolved by Phase 3b Latent Graph Consolidation. See `docs/adr/0003-coreference-absorbed-into-fusion.md`.

## Episodic Working Memory (Short-Term Memory / RAM)

To solve chunk isolation and implicit reference ambiguity across sequential text chunks, `Phase2Runner` integrates
**Episodic Working Memory**:

- **Global Structural Anchor (`GlobalStructuralAnchor`)**: Injects document Table of Contents (ToC) or section outlines
  as a static global coordinate system in `NER_EXTRACTION_PROMPT`. Can be explicitly user-provided or auto-discovered
  from `L1Chunk` metadata.
- **Decoupled State Machine (`WorkingMemoryState`)**: Tracks short-lived variables (`active_entities`,
  `unresolved_references`, `current_argument_branch`) across sequential chunk iterations ($S_{i-1} \to S_i$). The state
  object resides strictly in RAM and is **never** committed to Neo4j.
- **Boundary-Based Eviction (`EpisodicEvictionHandler`)**: Monitors structural triggers (section/header changes) and
  semantic triggers (`boundary_detected: bool = True` from LLM output). On boundary detection, short-lived variables are
  purged from RAM while retaining the Global Structural Anchor and a transitional summary bridge for the start of the
  next episode.

See: [Episodic Working Memory Concept](../../concepts/episodic_working_memory.md)
and [ADR 0009](../../adr/0009-sota-dual-memory-episodic-working-memory.md).

## Pluggability

- **NER extractor:** implement `NERExtractor(ABC)` and inject via `Phase2Runner(ner_extractor=MyExtractor())`.
- **Entity linker:** implement `EntityLinker(ABC)` for bi-encoder + cross-encoder linking; inject via
  `Phase2Runner(entity_linker=MyLinker())`.
- **Working Memory:** inject custom `EpisodicWorkingMemoryManager` or strategy (`json_patch`, `pydantic`, `key_value`)
  via `Phase2Runner(working_memory_manager=MyManager())`.
- **Schema:** all entity and relation types come from `SchemaConfig` injected at construction. Unknown types returned by
  the LLM are silently dropped.

## Implementation

`pipeline/phases/phase2_entity_discovery/__init__.py` — `Phase2Runner`  
`pipeline/phases/phase2_entity_discovery/ner_extractor.py` — `LLMNERExtractor`  
`pipeline/phases/phase2_entity_discovery/working_memory.py` — `EpisodicWorkingMemoryManager`,
`EpisodicEvictionHandler`  
`pipeline/phases/phase2_entity_discovery/entity_linker.py` — `NameEntityLinker`  
`pipeline/phases/phase2_entity_discovery/models.py` — `NERExtractionOutput`, `ExtractedEntity`, `ExtractedTriple`  
`pipeline/protocols/memory.py` — `GlobalStructuralAnchor`, `WorkingMemoryState`, `EvictionSignal`
