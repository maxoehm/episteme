# [0001] Neo4j with Async Driver as Default Graph Backend

Status: Accepted

## Context

The pipeline requires a property graph store that supports:

- Idempotent node and edge writes (crash-resilient incremental processing)
- Vector similarity search on chunk embeddings (Phase 3 TAG envelope retrieval)
- Per-chunk processing state tracking (`{phase}_processed` flags)
- Flexible schema: node labels and relation types determined at runtime by `SchemaConfig`
- Async I/O compatible with Python `asyncio` (all phase runners are async)

The graph layer is the single shared state between all pipeline phases and between pipeline runs; its reliability and
query expressiveness are the dominant constraints.

## Decision

Use **Neo4j** (community or enterprise) as the default graph backend, accessed via the official `neo4j` async Python
driver. The graph abstraction is now split in `pipeline/protocols/graph_store.py` into `GraphReader`, `GraphWriter`, and
`PhaseCheckpointStore`, plus focused composites such as `EntityGraph`, `ProcessingGraph`, `ProjectionGraph`, and
`FusionGraph`.

All writes use `MERGE` semantics throughout, making every graph commit idempotent. A chunk is committed only after all
its extractions are written; the `{phase}_processed = true` flag on the Chunk node is set last, making crash recovery
automatic: re-running any phase picks up from the last committed chunk.

## Alternatives considered

- **LlamaIndex PropertyGraphIndex** — provides a higher-level abstraction but hides the Cypher layer, making per-chunk
  phase tracking and custom MERGE patterns difficult to express. Also ties the graph implementation to LlamaIndex's
  storage model, reducing portability.
- **NetworkX (in-memory)** — no persistence, no vector search, not suitable for multi-session incremental processing.
  Useful only as a test double (the `InMemoryGraphStore` in tests serves this purpose).
- **Apache TinkerPop / Gremlin-compatible stores** — more portable API but weaker vector search support and less common
  in the philosophy NLP research community.
- **RDF triple stores (Stardog, GraphDB)** — correct semantics for knowledge representation, but Python async driver
  ecosystem is immature and SPARQL queries are more verbose for the graph traversal patterns needed here.

## Consequences

- Neo4j must be running and reachable before any phase beyond Phase 1 executes.
- `ensure_indexes()` must be called once after the store is created to install the `chunk_embedding` vector index and
  any uniqueness constraints.
- Tests use `InMemoryGraphStore` (no external service required). Integration tests against a real Neo4j instance are out
  of scope for V1.
- Switching to a different graph backend now means implementing only the narrower interfaces a consumer needs. The Neo4j
  implementations in `pipeline/graph/neo4j_store.py` provide separate reader/writer/checkpoint/processing classes
  directly.

## Related

- `pipeline/protocols/graph_store.py` — abstract interface
- `pipeline/graph/neo4j_store.py` — Neo4j implementation
- `tests/conftest.py` — `InMemoryGraphStore` test double
