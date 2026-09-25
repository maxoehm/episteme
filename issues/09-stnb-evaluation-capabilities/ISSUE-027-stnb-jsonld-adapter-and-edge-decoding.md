# [ISSUE-027] STNB JSON-LD Adapter Schema Inconsistencies & Edge Decoding Bugs

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-027` |
| **Component(s)** | `packages/episteme-pipeline` (`evaluation/adapters/structuralist.py`) |
| **Roadmap Horizon** | **Horizon 1** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | Critical / Blocker |
| **Status** | Open |
| **Source Ref** | [`evaluation/adapters/structuralist.py`](../../packages/episteme-pipeline/evaluation/adapters/structuralist.py#L71-L116), [`scorers/gm_gbs.py`](../../packages/episteme-pipeline/evaluation/scorers/gm_gbs.py#L60) |

---

## 1. Problem Statement & Motivation

In [`evaluation/adapters/structuralist.py`](../../packages/episteme-pipeline/evaluation/adapters/structuralist.py), the `load_structuralist_benchmark` function is responsible for parsing STNB JSON-LD envelopes into pipeline `L1Chunk` instances and a ground-truth `nx.DiGraph`.

Inspection of the implementation reveals multiple critical bugs that prevent accurate graph loading and cause immediate runtime crashes during scoring:

### 1.1 Edge Attribute Naming Mismatch (`relation` vs `label`)
In `structuralist.py` lines 104–115, edges are added with the attribute `relation`:
```python
if "str:specializes" in item:
    gold_graph.add_edge(node_id, item["str:specializes"], relation="specializes")
```
However, in [`evaluation/scorers/gm_gbs.py`](../../packages/episteme-pipeline/evaluation/scorers/gm_gbs.py#L60), the intrinsic scorer queries edge labels using `data="label"`:
```python
gold_edges = list(gold_graph.edges(data="label"))
gold_labels = [str(data) for _, _, data in gold_edges]
```
Because the edge attribute is named `relation` instead of `label`, `gold_graph.edges(data="label")` yields `None` for every single edge. As a result, `gold_labels` becomes `['None', 'None', ...]`, corrupting semantic embedding calculations.

### 1.2 Unhandled Array Targets (`TypeError: unhashable type: 'list'`)
In valid JSON-LD graph models, relational properties such as `str:hasActualModel`, `str:hasPotentialModel`, and `str:specializes` frequently link a `TheoryElement` to multiple models or multiple sub-theories:
```json
{
  "@id": "str:T_CPM_Base",
  "@type": "TheoryElement",
  "str:hasActualModel": ["str:M_CPM_Newton2", "str:M_CPM_Newton3"]
}
```
In `structuralist.py`, `item["str:hasActualModel"]` is passed directly as the target node without checking whether it is a string or a list. When an array is present, NetworkX attempts to hash the list as a node identifier and crashes:
```
TypeError: unhashable type: 'list'
```

### 1.3 Text-Anchor Namespace Mismatch
Line 71 extracts anchors via:
```python
anchor = item.get("glp:textAnchor")
```
However, the canonical STNB data card and JSON-LD specification ([`docs/research/structuralist_theory_benchmark.md`](../../docs/research/structuralist_theory_benchmark.md#L82-L114)) define:
```json
"Episteme:textAnchor": {
  "sourceDocId": "newton_principia_1687",
  "chunkId": "chunk_principia_law_02", ...
}
```
If an envelope uses `"Episteme:textAnchor"` or `"textAnchor"`, the adapter extracts zero text chunks, causing `chunks` to be empty and starving the evaluation pipeline of input.

### 1.4 Missing Relational Properties & Directed Poset Inversion
1. The adapter completely ignores core structuralist edge types:
   - `str:presupposes` ($\pi$ - pre-theoreticity and measurement dependency).
   - `str:empiricallyEquivalent` ($\varepsilon$ - structural equivalence between theoretical formulations).
   - `str:hasParadigm` ($I_0$ - paradigmatic applications).
2. Specialization directionality: In structuralism, $\alpha$ denotes vertical specialization (Parent core $\to$ Child specialization: e.g., General CPM $\to$ Hookean Oscillator). If a child node specifies `"str:specializes": "str:T_CPM_Base"`, naive edge insertion creates an edge Child $\to$ Parent, inverting the specialization DAG topology.

---

## 2. Functional Requirements

1. **Dual Edge Attribute Standardization**:
   - Set both `label` and `relation` on every edge added to `gold_graph`:
     ```python
     gold_graph.add_edge(u, v, label=rel_name, relation=rel_name, weight=1.0)
     ```
2. **List and String Target Normalization**:
   - Helper function `_as_list(val)` to normalize both scalar string IDs and JSON arrays:
     ```python
     def _as_list(value: Any) -> list[str]:
         if isinstance(value, list):
             return [str(v) for v in value]
         if isinstance(value, str):
             return [value]
         return []
     ```
3. **Resilient Text Anchor Resolution**:
   - Check all supported namespaces in order: `"Episteme:textAnchor"`, `"glp:textAnchor"`, and `"textAnchor"`.
4. **Complete Edge Type Coverage**:
   - Parse all 8 structuralist edge types: `specializes`, `reducesTo`, `hasConstraint`, `hasActualModel`, `hasPotentialModel`, `hasPartialPotentialModel`, `presupposes`, `empiricallyEquivalent`.
5. **Poset Orientation Normalization**:
   - Standardize specialization edges so directed paths flow from Root Theory Core $\to$ Specialized Sub-theory ($T_0 \xrightarrow{\alpha} T_1$), preserving DAG hierarchical levels.

---

## 3. Acceptance Criteria

- [ ] `load_structuralist_benchmark` parses JSON-LD graphs with list-valued relations without `TypeError`.
- [ ] Nodes and edges in `gold_graph` include both `label` and `relation` attributes.
- [ ] `gold_graph.edges(data="label")` returns valid string labels (never `None`).
- [ ] Resolves anchors under `"Episteme:textAnchor"`, `"glp:textAnchor"`, and `"textAnchor"`.
- [ ] Unit tests in `packages/episteme-pipeline/tests/` verify parsing of multi-target edges, anchor variations, and DAG edge orientations.

---

## 4. Key Target Files

- `packages/episteme-pipeline/evaluation/adapters/structuralist.py`
- `packages/episteme-pipeline/tests/test_evaluation_scaffolding.py`
