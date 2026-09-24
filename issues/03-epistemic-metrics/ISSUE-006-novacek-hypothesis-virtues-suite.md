# [ISSUE-006] Nováček Formal Hypothesis Virtues Suite in Epistemetrics

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-006` |
| **Component(s)** | `packages/epistemetrics` (`graph/algorithms/`), `packages/episteme-studio` |
| **Roadmap Horizon** | **Horizon 1 & 2** (Platform Stabilization & Dialectical Modeling) |
| **Priority** | High |
| **Status** | In Progress (Foundations Laid) |
| **Source Ref** | [requirements_glp_project.md §3.2](issues/shared/requirements_glp_project.md#L145-L150), [`docs/concepts/theory/metrics/`](docs/concepts/theory/metrics/) |

---

## 1. Problem Statement & Motivation
Vit Nováček (2015) formalized epistemological hypothesis virtues directly within knowledge graphs. Rather than judging scientific theories purely on empirical accuracy, formal philosophy of science evaluates structural virtues such as:
1. **Modesty**: Minimizing speculative, ungrounded paths relative to total possible simple paths ($\frac{|\Pi(H_\omega)|}{|\Pi(H)|}$).
2. **Structural Elegance / Simplicity**: Maximizing inferential parsimony and minimizing superfluous structural cycles.
3. **Structural Refutability**: Measuring the vulnerability of the theory graph to falsification by calculating whether invalidation of key bottleneck claims causes the claim volume to collapse.
4. **Conservatism**: Minimizing semantic and topological jump distances between grounding premises and radical conclusions.

While the mathematical formulations are documented in detail in [`docs/concepts/theory/metrics/`](docs/concepts/theory/metrics/), their executable implementations need to be completed in the `epistemetrics` library and exposed via GLP Studio.

---

## 2. Functional Requirements
1. **Epistemetrics Algorithm Implementations**:
   - Implement in `packages/epistemetrics/src/epistemetrics/graph/algorithms/`:
     - `modesty.py`: Structural approximation of simple path ratios over bounded random walks.
     - `structural_elegance.py`: Ratio of informative inferential paths to cyclic graph entropy.
     - `structural_refutability.py`: Articulation point and bridge bottleneck analysis measuring graph collapse under node ablation.
     - `conservatism.py`: Shortest-path semantic embedding divergence between premise anchors and conclusion leaves.
2. **Dual-Engine Execution**:
   - Support both pure Python (NetworkX) and Neo4j async Cypher execution modes via `epistemetrics.adapters`.
3. **Studio Service Integration**:
   - Register the four Nováček metrics in [`glp_studio/services/metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py) with standardized `MetricDescriptor` schemas.

---

## 3. Acceptance Criteria
- [ ] `epistemetrics.graph.algorithms` exports `compute_modesty`, `compute_structural_elegance`, `compute_refutability`, and `compute_conservatism`.
- [ ] Deterministic unit tests with known synthetic graphs verify scoring fidelity against Nováček (2015) baselines in `packages/epistemetrics/tests/`.
- [ ] Studio API (`/api/metrics/definitions`) returns descriptors for all four virtues.
- [ ] Running a virtue computation via Studio executes asynchronously and renders score distribution charts in [`EpistemicCharts.tsx`](packages/episteme-studio/frontend/src/panels/EpistemicCharts.tsx).

---

## 4. Key Target Files
- `packages/epistemetrics/src/epistemetrics/graph/algorithms/`
- [`packages/episteme-studio/src/glp_studio/services/metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py)
- [`packages/episteme-studio/frontend/src/panels/EpistemicCharts.tsx`](packages/episteme-studio/frontend/src/panels/EpistemicCharts.tsx)
