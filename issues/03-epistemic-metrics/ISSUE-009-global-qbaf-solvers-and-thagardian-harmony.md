# [ISSUE-009] Global QBAF Gradual Semantics Solvers & Thagardian Harmony (ECHO)

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-009` |
| **Component(s)** | `packages/epistemetrics` (`graph/algorithms/`), `packages/episteme-studio` |
| **Roadmap Horizon** | **Horizon 2** (Scalability, Benchmarking & Dialectical Modeling) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §3.3](issues/shared/requirements_glp_project.md#L151-L162), [ADR 0011](docs/adr/0011-declarative-graph-metrics-and-qbaf-semantics.md), [docs/roadmap.md Horizon 2](docs/roadmap.md#L160-L175) |

---

## 1. Problem Statement & Motivation
Under [ADR 0011](docs/adr/0011-declarative-graph-metrics-and-qbaf-semantics.md), GLP Studio supports *local* gradual strength semantics (`compute_local_gradual_strength`) over bounded neighborhoods upstream of a single focus node.

However, full dialectical theory evaluation requires global network solvers:
1. **Global Gradual Argumentation Semantics (QBAF)**: Iterative global convergence over arbitrary directed, cyclic graphs $Q = \langle A, R^-, R^+, w \rangle$. Requires implementing Eulerian semantics, quadratic energy models, and categorization models to compute equilibrium justification degrees $\tau(a)$ for all arguments simultaneously.
2. **Thagardian Coherence (ECHO Solver)**: Paul Thagard's Explanatory Coherence Model computes system harmony $H$ via connectionist constraint relaxation over positive (`COHERES_WITH`, `EXPLAINS`) and negative (`INCOHERENT_WITH`, `CONTRADICTS`) constraints, settling node activations $a_i \in [-1, 1]$.

---

## 2. Functional Requirements
1. **Epistemetrics Solvers**:
   - `qbaf_gradual.py`:
     - Implement DF-QuAD and Euler-based gradual semantics with user-configurable damping ($\alpha$) and belief decay ($\theta$).
     - Guarantee convergence on cyclic networks using Banach fixed-point contraction mappings.
   - `thagard_echo.py`:
     - Implement Thagardian network relaxation updating activations $a_i(t+1) = a_i(t)(1 - \theta) + \text{net}_i( \max - a_i(t) )$.
     - Compute global System Harmony $H = \sum_{i, j} w_{ij} a_i a_j$.
2. **Studio Integration & Visualization**:
   - Add `qbaf_global` and `thagard_harmony` descriptors to [`metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py).
   - In GLP Studio, display settled node activations with multi-channel color gradients (blue for belief, red for disbelief) and visualize mutual coherence loops on the canvas.

---

## 3. Acceptance Criteria
- [ ] Global QBAF solver converges deterministically on benchmark cyclic argumentation topologies.
- [ ] Thagard ECHO solver calculates System Harmony $H$ and outputs stable activation vectors.
- [ ] Users can trigger global QBAF and ECHO from the Studio Metrics Drawer and inspect edge contribution flows.
- [ ] Unit tests in `packages/epistemetrics/tests/` verify mathematical convergence bounds.

---

## 4. Key Target Files
- `packages/epistemetrics/src/epistemetrics/graph/algorithms/`
- [`packages/episteme-studio/src/glp_studio/services/metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py)
- [`packages/episteme-studio/frontend/src/panels/MetricsDrawer.tsx`](packages/episteme-studio/frontend/src/panels/MetricsDrawer.tsx)
