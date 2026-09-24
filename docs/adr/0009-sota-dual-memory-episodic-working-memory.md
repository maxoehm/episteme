# ADR 0009: SOTA Dual-Memory Architecture & Episodic Working Memory

## Status

Accepted

## Context

In dense scientific and philosophical texts (e.g., Kant, Carnap, Hegel), arguments and theoretical concepts span across
multiple chapters. Processing document chunks in isolation leads to severe issues:

1. **Implicit Reference Ambiguity:** References such as "this assumption" or "the second premise" cannot be resolved by
   isolated chunk extractors or vector search alone.
2. **Lossy Text Summarization:** Naive memory prompting ("summarize what was learned in these pages") acts like a lossy
   compression algorithm, leading to semantic drift over long texts.
3. **Arbitrary Token Boundaries:** Sliding FIFO token buffers cut off logical contexts based on token counts rather than
   semantic boundaries.

We need a state-of-the-art context memory model that bridges local chunk extraction with global knowledge graph store
without overflowing LLM context windows or introducing semantic drift.

## Decision

We adopt a **SOTA Dual-Memory Architecture** consisting of:

1. **Short-Term Memory (STM / RAM):** A stateful, short-lived memory context carried sequentially across document chunks
   ($C_{i-1} \to C_i$).
    - **Global Structural Anchor:** Ingests the book's global Table of Contents (ToC) or chapter outlines as a static
      coordinate system in the prompt.
    - **Structured State Machine:** Replaces free-text summaries with explicit state variable updates
      (`active_entities`, `unresolved_references`, `current_argument_branch`).
    - **State Interface Decoupling:** Decouples the state machine interface from underlying serialization formats (JSON
      patches, Pydantic schemas, key-value dicts) to allow empirical evaluation of optimal state formats.
2. **Long-Term Memory (LTM / Disk):** The Neo4j property graph holding canonical entities, formal relations, and
   argument components.
3. **Episodic Eviction (Boundary-Based Reset):** LLM detects semantic boundaries (sub-chapter end, argument shift)
   during sequential ingestion. Extracted entities and relations ($\Delta G_i$) are committed to Neo4j LTM. The STM
   state itself is **never committed to Neo4j**; its short-lived variables are purged from runtime memory (RAM) upon
   boundary detection, retaining only the Global Structural Anchor (ToC) and immediate transitional context for the next
   episode.
4. **Strict Phase Isolation:** Short-Term Memory handles localized context bridging in Phase 2 (Entity Discovery) and
   Phase 3 (Global Relations). Leiden community detection and macro-level summarization remain strictly reserved for
   Phase 5 (Alignment & Fusion).

## Consequences

### Positive

- **Precise Reference Resolution:** Resolves demonstratives ("this theory") locally into canonical identifiers before
  querying LTM.
- **No Semantic Drift:** Explicit state variables eliminate the lossy compression of unstructured text summaries.
- **Semantic Boundary Alignment:** Flushes knowledge to LTM based on logical section boundaries rather than arbitrary
  token lengths.
- **Architectural Modularity:** Keeps Phase 2/3 extraction independent of Phase 5 Leiden clustering.

### Negative

- **Sequential Dependency:** Chunk processing within a section becomes strictly sequential, limiting parallelization of
  Phase 2 across chunks of the same chapter.
- **State Machine Overhead:** Requires state extraction schema parsing and boundary check evaluation per chunk.

## Implementation Plan

1. Define `WorkingMemoryState` abstract interface and state schema representations in
   `pipeline/phases/phase2_entity_discovery/`.
2. Implement ToC parser / Global Structural Anchor prompt injection.
3. Implement boundary detection and episodic eviction flush handler.
4. Document the model in `docs/concepts/episodic_working_memory.md` and track tasks in `docs/TODO_unifying_llm.md` and
   `docs/TODO.md`.

## Related ADRs

- [ADR 0003: Coreference Absorbed Into Fusion](0003-coreference-absorbed-into-fusion.md)
- [ADR 0005: Two-Pass Fusion Strategy](0005-two-pass-fusion-strategy.md)
- [ADR 0008: Diátaxis Documentation Framework](0008-diataxis-documentation-framework.md)

## Implementation Date

2026-08-05
