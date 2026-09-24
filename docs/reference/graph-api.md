# Graph API

This page documents the pipeline-facing graph contracts.

The important boundary is the protocol and DTO layer, not the Neo4j backend.
`GraphReader.get_neighborhood()` returns a `SubGraph`, which is the canonical transport object for structural context
passed into Phase 3, Phase 4, and fusion logic.

## Key Semantics

- `SubGraph` is a serializable neighborhood snapshot, not a live graph handle.
- `center_id` identifies the query center; the center node does not need to be duplicated in `nodes`.
- `nodes` and `triples` expose the retrieved local context in pipeline-native types.
- Storage backends may vary, but callers should rely only on the documented
  `SubGraph` and `GraphReader` contracts.

### Envelope Construction and Traversal

When `GraphReader.get_neighborhood()` constructs a `SubGraph` envelope (e.g., for Phase 3 and Phase 4 LLM context), it
explicitly **filters out structural nodes** (`Chunk`, `Chapter`, `Document`).

**Why filter structural nodes?**

- Structural nodes like `Chunk` carry heavy metadata payloads (e.g., 4096-dimensional dense embeddings,
  `phase2_processed` flags, source IDs).
- If traversed, these nodes would leak into the LLM prompt via the envelope formatting (`format_envelope`), causing
  severe context window overflows and diluting the semantic reasoning task.
- By ignoring structural nodes during the `apoc.path.subgraphAll` traversal, the resulting `SubGraph` strictly contains
  semantic entity-to-entity and component-to-component relationships, which is the exact context needed for LLM relation
  extraction and argument mining.

### Batch Persistence and Bulk I/O

The write interface [`GraphWriter`](#pipeline.protocols.graph_store.GraphWriter) exposes explicit plural persistence contracts (`upsert_chunks`, `upsert_entities`, `upsert_triples`, `upsert_relations`, `upsert_argument_components`, `upsert_communities`) alongside singular operations.

Key write invariants:

- **Single-Transaction Bulk Writes:** Plural write operations execute within a single Cypher transaction using `UNWIND $batch AS ...`. This reduces transaction management and round-trip network overhead by up to $95\%$ during large ingestions.
- **DRY Singular Delegation:** To avoid query duplication and ensure consistent label/property mapping, singular methods (`upsert_entity`, `upsert_triple`, `upsert_chunk`, etc.) wrap inputs in single-element lists and delegate to the plural batch implementations.
- **Explicit Contracts over Global Flags:** There is no global `enable_batching` flag. Phases decide whether to batch data (typically via Python's standard `itertools.batched`) based on their algorithmic constraints.

For the architectural rationale and benchmarks, see [ADR 0017: Explicit Batch Contracts & Bulk I/O](../adr/0017-explicit-batch-contracts-and-bulk-io.md).

## Contracts

::: episteme_pipeline.contracts.domain.SubGraph

::: episteme_pipeline.protocols.graph_store.GraphReader

::: episteme_pipeline.protocols.graph_store.GraphWriter

::: episteme_pipeline.protocols.graph_store.PhaseCheckpointStore
