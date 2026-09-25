# [ISSUE-031] Specialization Poset Hierarchies ($\alpha$) & Theoretical Dynamics Verification

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-031` |
| **Component(s)** | `packages/epistemetrics` (`epistemic/poset_evaluation.py`, `epistemic/dynamics.py`), `packages/episteme-pipeline` |
| **Roadmap Horizon** | **Horizon 1 & 2** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [`docs/research/structuralist_theory_benchmark.md §Task 2, 4, 5`](../../docs/research/structuralist_theory_benchmark.md#L231-L264), [`docs/concepts/theory/metrics/theory_dynamics/`](../../docs/concepts/theory/metrics/theory_dynamics/) |

---

## 1. Problem Statement & Motivation

While [`ISSUE-030`](ISSUE-030-intrinsic-model-component-and-property-evaluation.md) verifies the local model-theoretic components ($\mathcal{M}_p, \mathcal{M}, \mathcal{M}_{pp}, GC, I_0$) and property-by-property alignment, scientific theories are organized globally as:
1. **Vertical Specialization Trees (Posets $\alpha$):** A Directed Acyclic Graph (DAG) ordered by specialization where specialized elements inherit models from parent theories while introducing restrictive laws.
2. **Intertheoretical Reduction Links ($\rho$):** Inter-net mappings connecting distinct theories (e.g. Collision Mechanics $\to$ Particle Mechanics).
3. **Diachronic Dynamics ($TN_t \to TN_{t+1}$):** Historical theory trajectories where the theoretical core ($T_0$) remains invariant while auxiliary belts adapt to empirical anomalies.

Currently, the evaluation suite has zero capability to test whether:
- The predicted specialization relations form a valid cycle-free poset DAG.
- The fundamental root law is unique and conforms to the gold standard ($B(TN) = \{T_0\}$).
- Specialized theories correctly inherit parent models.
- Theory evolution avoids Lakatosian degeneration.

---

## 2. Functional Requirements

### 2.1 Poset Specialization Hierarchy Verification (Task 2)
Implement in `packages/epistemetrics/src/epistemetrics/epistemic/poset_evaluation.py`:
1. **DAG & Acyclicity Verification:**
   - Computes cycle detection over the `str:specializes` subgraph.
   - Asserts strict partial order properties (transitivity, irreflexivity, antisymmetry).
2. **Root Element Conformity:**
   - Verifies whether the graph possesses a unique greatest lower bound $T_0$ matching the reference root theory element:
     $$B(TN_{\text{pred}}) = \{ T_{0, \text{gold}} \}$$
3. **Hierarchical Model Inheritance Subsumption:**
   - Verifies that for every specialization edge $T_i \xrightarrow{\alpha} T_j$, model classes satisfy inclusion:
     $$\mathcal{M}_p(T_j) \subseteq \mathcal{M}_p(T_i) \quad \text{and} \quad \mathcal{M}(T_j) \subset \mathcal{M}(T_i)$$
4. **Poset Transitive Reduction F1:**
   - Computes transitive reduction of predicted and reference specialization trees to compute Precision, Recall, and Poset F1.

### 2.2 Intertheoretical Link Prediction & Reduction (Task 4)
Implement in `packages/epistemetrics/src/epistemetrics/epistemic/reduction_evaluation.py`:
1. Evaluates directed cross-theory links (`str:reducesTo`, `str:presupposes`) between distinct Theory Elements.
2. Computes relational link precision, recall, and reduction F1.

### 2.3 Diachronic Dynamics & Lakatosian Degeneration (Task 5)
Implement in `packages/epistemetrics/src/epistemetrics/epistemic/dynamics.py`:
1. **Lakatosian Degeneration Index ($DI$):**
   $$DI = \frac{\Delta |\text{Auxiliary Hypotheses}| + |\text{Anomalies}|}{\Delta |\text{Empirical Content}| + \epsilon}$$
2. **Hard-Core Invariance Checker:**
   - Asserts that root axioms $T_0$ remain invariant across successive editions/epochs ($TN_t \to TN_{t+1}$).

---

## 3. Acceptance Criteria

- [ ] `poset_evaluation.py` detects cycles and flags non-DAG specialization structures.
- [ ] Root conformity evaluator verifies unique $T_0$ identity against reference graphs.
- [ ] Specialization reachability verifies that all reference derivation paths exist in the prediction.
- [ ] Computes Lakatosian Degeneration Index and tracks immunization shifts across multi-epoch datasets.
- [ ] Deterministic unit tests in `packages/epistemetrics/tests/` verify acyclicity and reachability containment.

---

## 4. Key Target Files

- `packages/epistemetrics/src/epistemetrics/epistemic/poset_evaluation.py`
- `packages/epistemetrics/src/epistemetrics/epistemic/dynamics.py`
- `packages/epistemetrics/src/epistemetrics/epistemic/reduction_evaluation.py`
- `packages/epistemetrics/src/epistemetrics/__init__.py`
