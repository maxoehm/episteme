# [ISSUE-029] Missing `TheoryGraph` Domain Architecture & Broken Contract in `epistemetrics`

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-029` |
| **Component(s)** | `packages/epistemetrics` (`core/models.py`, `graph/theory_graph.py`, `__init__.py`), `packages/episteme-pipeline` (`evaluation/adapters/neo4j_to_epistemetrics.py`) |
| **Roadmap Horizon** | **Horizon 1** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | Critical / Blocker |
| **Status** | Open |
| **Source Ref** | [`test_neo4j_to_epistemetrics.py`](../../packages/episteme-pipeline/tests/test_neo4j_to_epistemetrics.py#L8-L55), [`packages/epistemetrics/README.md`](../../packages/epistemetrics/README.md#L40-L61), [`packages/epistemetrics/ARCHITECTURE_DECISIONS.md`](../../packages/epistemetrics/ARCHITECTURE_DECISIONS.md#L41-L55) |

---

## 1. Problem Statement & Motivation

Executing the test suite via `rtk uv run --offline pytest packages/episteme-pipeline/tests/test_neo4j_to_epistemetrics.py` currently crashes with an immediate failure:
```
FAILED packages/episteme-pipeline/tests/test_neo4j_to_epistemetrics.py::TestNeo4jToEpistemetricsAdapter::test_export_neo4j_to_theory_graph
AttributeError: module 'epistemetrics' has no attribute 'TheoryGraph'
```

### 1.1 The Specification-Implementation Chasm
Both [`packages/epistemetrics/README.md`](../../packages/epistemetrics/README.md) and [`packages/epistemetrics/ARCHITECTURE_DECISIONS.md`](../../packages/epistemetrics/ARCHITECTURE_DECISIONS.md) explicitly define the public API for the library:
```python
import epistemetrics as em

tg = em.TheoryGraph()
tg.add_node("A1", name="Newtonian Mechanics", node_type=em.NodeType.AXIOM, epistemic_status=em.EpistemicStatus.HARD_CORE)
tg.add_edge("A1", "P1", relation_type=em.RelationType.EXPLAINS)
report = em.analyze_theory_graph(tg)
```

Furthermore, [`evaluation/adapters/neo4j_to_epistemetrics.py`](../../packages/episteme-pipeline/evaluation/adapters/neo4j_to_epistemetrics.py) was written against this exact API contract.

However, in `packages/epistemetrics/src/epistemetrics/`:
1. **`TheoryGraph` does not exist.**
2. **`NodeType`, `EpistemicStatus`, and `RelationType` enums do not exist.**
3. **`analyze_theory_graph` and `EpistemicReport` do not exist.**
4. The package only provides generic graph data science centrality and clustering algorithms (betweenness, eigenvector, louvain, pagerank, wcc) imported from NetworkX and Neo4j GDS.

Because `epistemetrics` lacks its core domain object, any pipeline component attempting to perform epistemic theory evaluation fails.

---

## 2. Functional Requirements

### 2.1 Core Domain Enums & Models (`epistemetrics.core.models`)
Implement the formal domain primitives:
1. **`NodeType(str, Enum)`**:
   - Members: `AXIOM`, `HYPOTHESIS`, `CLAIM`, `CONCEPT`, `PHENOMENON`, `EVIDENCE`, `THEORY_ELEMENT`, `POTENTIAL_MODEL`, `ACTUAL_MODEL`, `PARTIAL_POTENTIAL_MODEL`, `CONSTRAINT`, `PARADIGM`.
   - Method `from_str(cls, val: str) -> NodeType` with case-insensitive normalization and safe fallback.
2. **`EpistemicStatus(str, Enum)`**:
   - Members: `HARD_CORE`, `PROTECTIVE_BELT`, `NEUTRAL`, `ANOMALOUS`.
   - Method `from_str(cls, val: str) -> EpistemicStatus`.
3. **`RelationType(str, Enum)`**:
   - Members: `EXPLAINS`, `SUPPORTS`, `ATTACKS`, `SPECIALIZES`, `REDUCES_TO`, `CONSTRAINS`, `PRESUPPOSES`, `COHERES_WITH`, `EQUIVALENT_TO`.
   - Method `from_str(cls, val: str) -> RelationType`.
4. **`TheoryNode` & `TheoryEdge`**:
   - Typed Pydantic or frozen dataclass structures preserving node attributes, confidence, epistemic status, layer tags, and provenance anchors.

### 2.2 `TheoryGraph` Runtime Model (`epistemetrics.graph.theory_graph`)
Implement `TheoryGraph`:
- Backed by an internal `nx.DiGraph` (or `nx.MultiDiGraph`).
- Methods:
  - `add_node(node_id: str, name: str, node_type: NodeType, epistemic_status: EpistemicStatus = EpistemicStatus.NEUTRAL, confidence: float = 1.0, description: str = None, provenance: list[str] = None, attributes: dict = None) -> None`
  - `add_edge(source: str, target: str, relation_type: RelationType, confidence: float = 1.0, weight: float = 1.0, attributes: dict = None) -> None`
  - `get_node(node_id: str) -> TheoryNode | None`
  - `get_edge(source: str, target: str) -> list[TheoryEdge]`
  - Properties: `num_nodes`, `num_edges`, `nodes`, `edges`, `nx_graph`.
  - Export/Import: `to_dict()`, `from_dict()`, `to_networkx()`, `from_networkx()`.

### 2.3 `analyze_theory_graph` & `EpistemicReport`
Implement baseline analytical dispatch in `epistemetrics`:
- Calculates graph summary stats (node/edge counts, density, connectivity).
- Dispatches to epistemic virtue and structural algorithms.
- Returns `EpistemicReport` with markdown serialization helper `.to_markdown()`.

### 2.4 Top-Level Package Exports (`epistemetrics/__init__.py`)
Export all core domain constructs directly at the root:
```python
from epistemetrics.core.models import NodeType, EpistemicStatus, RelationType
from epistemetrics.graph.theory_graph import TheoryGraph
from epistemetrics.analysis import analyze_theory_graph, EpistemicReport
```

---

## 3. Acceptance Criteria

- [ ] `packages/epistemetrics/src/epistemetrics/graph/theory_graph.py` implements `TheoryGraph` with NetworkX encapsulation.
- [ ] `NodeType`, `EpistemicStatus`, `RelationType` enums support `.from_str()` parsing.
- [ ] Root `epistemetrics` exports `TheoryGraph`, `NodeType`, `EpistemicStatus`, `RelationType`, `analyze_theory_graph`, and `EpistemicReport`.
- [ ] `rtk uv run --offline pytest packages/episteme-pipeline/tests/test_neo4j_to_epistemetrics.py` passes without error.
- [ ] Unit tests in `packages/epistemetrics/tests/` verify `TheoryGraph` lifecycle, serialization, and immutability guards.

---

## 4. Key Target Files

- `packages/epistemetrics/src/epistemetrics/graph/theory_graph.py`
- `packages/epistemetrics/src/epistemetrics/core/models.py`
- `packages/epistemetrics/src/epistemetrics/analysis.py`
- `packages/epistemetrics/src/epistemetrics/__init__.py`
- `packages/episteme-pipeline/tests/test_neo4j_to_epistemetrics.py`
