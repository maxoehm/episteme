# [0017] Explicit Batch Contracts, Cypher UNWIND Bulk I/O, and Decoupled Embedding Operations

Status: Accepted (2026-08-18)

## Context

Constructing theory graphs from extensive scientific literature requires persisting tens of thousands of text chunks, named entities, cross-chunk relations, and argument components (theory atoms) into Neo4j, while concurrently computing dense vector embeddings.

In early pipeline iterations, node and edge persistence relied on singular methods (`upsert_chunk`, `upsert_entity`, `upsert_triple`). Each invocation opened an independent session and committed a distinct transaction against the database. For monographs yielding thousands of entities and relations, this created severe transactional overhead:

1. **Transaction Overhead Dominance:** The primary performance bottleneck was not connection acquisition but transaction management overhead—repeated network round-trips, transaction coordinator handshakes, and individual lock acquisitions for every node and relation write.
2. **Global Configuration Antipatterns:** Introducing global configuration flags (e.g., `enable_batching: bool`) in `PipelineConfig` was considered. However, global switches pollute phase implementations with conditional branches (`if self.config.enable_batching: ... else: ...`), obscuring core domain algorithms and creating combinatorial testing complexity.
3. **Misconceptions Around Connection Pooling:** Suggestions arose to implement custom connection pooling or caching. However, the official Neo4j Python driver (`AsyncGraphDatabase.driver`) natively maintains a thread-safe, asynchronous connection pool. Implementing custom pooling was redundant.
4. **Conflation of Database and Embedding I/O:** While both benefit from batching, database persistence and embedding inference operate under entirely different constraints:
   - Database writes are constrained by Cypher query compilation, lock contention, and transaction log flushes.
   - Embedding API calls are bounded by provider rate limits, token window limits, and tensor batch dimensions.
   Coupling their batching mechanics into a unified infrastructure creates brittle cross-dependencies.

## Decision

We introduce explicit batching contracts across the graph store and embedding protocols, implement Cypher `UNWIND` single-transaction persistence in the Neo4j backend, and standardize high-throughput phases around the `collect -> batched -> persist` pattern.

### 1. Connection Pool Retention and Transaction-Level Optimization

We rely exclusively on the `neo4j.AsyncGraphDatabase.driver` connection pool managed inside `_Neo4jConnection`. Rather than optimizing connection lifetimes, optimization targets transaction overhead by minimizing transaction counts through Cypher bulk queries.

### 2. Explicit Protocol Contracts Over Configuration Flags

We reject global `enable_batching` flags. The capability to batch is declared explicitly in the protocol contracts, leaving individual Phase authors to select the execution strategy appropriate for their data dependencies.

`GraphWriter` in `pipeline/protocols/graph_store.py` is extended with explicit plural methods:

```python
class GraphWriter(GraphHandle, ABC):
    # Sequential / Singular methods
    @abstractmethod
    async def upsert_chunk(self, chunk: L1Chunk) -> None: ...

    @abstractmethod
    async def upsert_entity(self, entity: L2Entity) -> None: ...

    @abstractmethod
    async def upsert_triple(self, triple: L2Triple) -> None: ...

    # Explicit Batch methods
    @abstractmethod
    async def upsert_chunks(self, chunks: list[L1Chunk]) -> None: ...

    @abstractmethod
    async def upsert_entities(self, entities: list[L2Entity]) -> None: ...

    @abstractmethod
    async def upsert_triples(self, triples: list[L2Triple]) -> None: ...

    @abstractmethod
    async def upsert_relations(self, relations: list[dict]) -> None: ...

    @abstractmethod
    async def upsert_argument_components(self, components: list[TheoryAtom]) -> None: ...

    @abstractmethod
    async def upsert_communities(self, communities: list[dict]) -> None: ...
```

### 3. Cypher `UNWIND` Implementation with DRY Delegation

In `pipeline/graph/neo4j_store.py`, `_Neo4jWriteMixin` implements bulk methods using Cypher's `UNWIND $batch AS item` clause. This allows Neo4j to execute hundreds of merges within a single transaction:

```cypher
UNWIND $batch AS entity
MERGE (n:`Entity` {id: entity.id})
SET n += entity.props
```

To eliminate code duplication, singular methods (`upsert_entity`, `upsert_triple`, `upsert_chunk`, etc.) wrap their single input in a list and delegate to their plural counterparts:

```python
async def upsert_entity(self, entity: L2Entity) -> None:
    await self.upsert_entities([entity])
```

### 4. Decoupled Embedding Protocol

Embedding components strictly maintain separate batching contracts on `EmbeddingModel`:

```python
class EmbeddingModel(ABC):
    @abstractmethod
    async def aget_text_embedding(self, text: str) -> list[float]: ...

    @abstractmethod
    async def aget_text_embedding_batch(self, texts: list[str]) -> list[list[float]]: ...
```

This ensures that LLM/embedding batch sizes (tuned for token counts and GPU memory) remain decoupled from database write batch sizes (tuned for Cypher lock retention).

### 5. Phase Refactoring: The `collect -> batched -> persist` Pattern

Phases accumulating substantial entities, triples, or components use Python 3.12+'s standard `itertools.batched` to chunk in-memory collections into safe increments (default 500) before persisting:

```python
from itertools import batched

class ExamplePhase(PhaseRunner):
    async def run(self, input_data: PhaseInput, context: PipelineContext) -> PhaseOutput:
        # 1. Process items and accumulate results in memory
        extracted_entities = [await self._extract(item) for item in input_data.items]

        # 2. Persist in bounded chunks to prevent transaction memory spikes
        for entity_batch in batched(extracted_entities, 500):
            await self.graph_store.upsert_entities(list(entity_batch))
```

This pattern is applied uniformly across:
- **Phase 1 (Foundation):** Text chunks batched into Neo4j (`upsert_chunks`).
- **Phase 2 (Entity Discovery):** Extracted entities, initial triples, and processed chunk IDs batched in 500-item chunks.
- **Phase 3 (Global Relations):** Candidate batches and verified relation triples batched into single Cypher transactions.
- **Phase 4 (Maturation & Argument Mining):** Synthesized entity envelopes, theory atoms, and dialectical relations batched.
- **Phase 5 (Fusion):** Hierarchical community memberships batched (`upsert_communities`).
- **Phase 6 (TheoryNet) & Post-Processing:** Projection atoms, relations, and theoretical parameter updates batched in 500-item chunks.

## Consequences

### Positive

- **Performance Gain:** Reduces Neo4j write transaction overhead by up to $95\%$ on multi-thousand entity corpora.
- **Clean Architecture:** Eliminates combinatorial `if enable_batching` flags in domain and runner logic.
- **DRY Query Logic:** Singular write methods delegate to plural methods, ensuring single sources of truth for Cypher mutation queries.
- **Independent Scaling:** Database batch sizing (typically $500$) and embedding batch sizing (typically $10\text{--}64$) can be tuned independently without impedance mismatch.

### Negative / Trade-offs

- **Memory Consumption in Memory-Constrained Runners:** Collecting items before persisting requires intermediate list allocations, though bounded by phase boundaries and chunk sizes ($O(N)$ within phase scope).
- **Interface Surface Expansion:** Protocols declare both singular and plural variants, increasing mock requirements in testing fixtures.
