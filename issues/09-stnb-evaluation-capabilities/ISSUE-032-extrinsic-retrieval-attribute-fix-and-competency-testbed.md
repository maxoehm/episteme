# [ISSUE-032] Extrinsic Retrieval Scorer Attribute Crash & STNB Competency Testbed

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-032` |
| **Component(s)** | `packages/episteme-pipeline` (`evaluation/scorers/retrieval_scorer.py`, `evaluation/run_eval.py`, `evaluation/data/`) |
| **Roadmap Horizon** | **Horizon 1** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [`retrieval_scorer.py`](../../packages/episteme-pipeline/evaluation/scorers/retrieval_scorer.py#L52-L57), [`run_eval.py`](../../packages/episteme-pipeline/evaluation/run_eval.py#L192-L200), [`contracts/domain.py`](../../packages/episteme-pipeline/episteme_pipeline/contracts/domain.py#L245-L250) |

---

## 1. Problem Statement & Motivation

Downstream extrinsic evaluation measures whether the constructed theory graph provides practical utility for scientific question-answering and structured retrieval.

Currently, extrinsic evaluation is broken by an unhandled attribute error and lacks a scientific competency query testbed:

### 1.1 Critical Path AttributeError in `retrieval_scorer.py`
In [`evaluation/scorers/retrieval_scorer.py`](../../packages/episteme-pipeline/evaluation/scorers/retrieval_scorer.py#L52-L57):
```python
results = await self.graph_reader.vector_search(
    embedding=query_embedding, top_k=top_k
)
retrieved_ids = [res.id for res in results]
```
However, the domain contract [`episteme_pipeline.contracts.domain.SearchResult`](../../packages/episteme-pipeline/episteme_pipeline/contracts/domain.py#L245-L250) is defined as:
```python
class SearchResult(BaseModel):
    node_id: str
    score: float
    node_label: str
    node_name: str
```
Because `SearchResult` has `node_id` instead of `id`, calling `retrieval_evaluator.evaluate_query(...)` immediately raises `AttributeError: 'SearchResult' object has no attribute 'id'`. The extrinsic evaluation scorer cannot execute a single query.

### 1.2 Uninformative Dummy Queries in `run_eval.py`
When running STNB (where no SciFact path is supplied), `run_eval.py` lines 192–200 fall back to a hardcoded placeholder:
```python
dummy_query = "What is the main argument?"
dummy_gold_ids = {"doc_0"}
if 'gold_data' in locals() and gold_data.get("l2_entities"):
    dummy_gold_ids = {ent.id for ent in gold_data["l2_entities"][:3]}

metrics = await retrieval_evaluator.evaluate_query(dummy_query, dummy_gold_ids)
self.report.extrinsic_metrics = metrics
```
This dummy test evaluates a generic query against arbitrary entity IDs, producing fabricated or uninterpretable IR numbers that have no bearing on scientific graph quality.

### 1.3 Absence of Theory Competency Benchmarks
A valid Theory Graph evaluation must test domain competencies:
1. **Law Identification Queries:** *"Which governing principle accounts for planetary orbits?"* $\to$ Gold Node: Law of Universal Gravitation ($M_{\text{CPM\_Grav}}$).
2. **Structural Derivation Queries:** *"How does Hooke's Law specialize general particle mechanics?"* $\to$ Gold Node: Harmonic Oscillator Specialization ($T_{\text{CPM\_Harmonic}}$).
3. **Invariance Queries:** *"What empirical property is constrained to remain invariant across multiple bodies?"* $\to$ Gold Node: Mass Invariance Constraint ($GC_{\text{CPM\_Mass}}$).

---

## 2. Functional Requirements

### 2.1 Fix `SearchResult` Property Reference
Update line 56 in `retrieval_scorer.py`:
```python
retrieved_ids = [res.node_id for res in results]
```

### 2.2 Scoped Run-Slice Retrieval
Support `run_id` parameter in `GraphReader.vector_search` and `ExtrinsicRetrievalEvaluator` to ensure retrieval only scans nodes generated during the evaluated run.

### 2.3 Curate STNB Competency Query Testbed (`stnb_cpm_queries.yaml`)
Create `packages/episteme-pipeline/evaluation/data/stnb_cpm_queries.yaml`:
```yaml
queries:
  - id: "cpm_q01"
    query: "What governing law establishes the proportionality between impressed force and change of motion?"
    gold_target_ids: ["str:M_CPM_Newton2"]
    category: "core_law"
  - id: "cpm_q02"
    query: "Which invariance constraint demands that body mass remains constant across different experimental setups?"
    gold_target_ids: ["str:GC_CPM_Mass"]
    category: "constraint"
  - id: "cpm_q03"
    query: "Which theoretical specialization describes restoring force in a spring?"
    gold_target_ids: ["str:T_CPM_Harmonic", "str:M_CPM_Hooke"]
    category: "specialization"
```

### 2.4 Wire STNB Competency Queries into `run_eval.py`
When `dataset_type == "structuralist"`, load `stnb_cpm_queries.yaml`, run batch retrieval over the generated Neo4j TheoryNet, and report mean MRR, Hits@1, Hits@3, Hits@10, and nDCG.

---

## 3. Acceptance Criteria

- [ ] `retrieval_scorer.py` accesses `res.node_id` without `AttributeError`.
- [ ] `packages/episteme-pipeline/evaluation/data/stnb_cpm_queries.yaml` contains at least 5 competency queries with gold target IDs.
- [ ] `run_eval.py` executes competency evaluation for STNB and records IR metrics in the evaluation report.
- [ ] Unit tests in `packages/episteme-pipeline/tests/` verify ranking calculation against mock `SearchResult` collections.

---

## 4. Key Target Files

- `packages/episteme-pipeline/evaluation/scorers/retrieval_scorer.py`
- `packages/episteme-pipeline/evaluation/data/stnb_cpm_queries.yaml`
- `packages/episteme-pipeline/evaluation/run_eval.py`
- `packages/episteme-pipeline/tests/test_extrinsic_metrics.py`
