# [ISSUE-008] Extended Newman Centrality & Topological Metrics Suite

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-008` |
| **Component(s)** | `packages/epistemetrics` (`graph/algorithms/`), `packages/episteme-studio` |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §3.1](issues/shared/requirements_glp_project.md#L138-L144) |

---

## 1. Problem Statement & Motivation
Network centrality identifies inferential bottlenecks, foundational axioms, and bridging terms in scientific graphs. While PageRank, Degree Centrality, Weakly Connected Components (WCC), Betweenness Centrality, and Eigenvector Centrality have been implemented in `epistemetrics` and exposed in GLP Studio, several classical Newman network metrics are still missing:
1. **Closeness Centrality**: Shortest-path distance to all other concepts in the theory graph.
2. **Katz Centrality**: Attenuated walk-based centrality with parameter $\alpha < 1/\lambda_{\max}$.
3. **Kleinberg's HITS (Hubs and Authorities)**: Distinguishing foundational authorities ($a_i$) from literature hubs ($h_i$).
4. **Local Clustering Coefficient ($C_i$) & Global Transitivity**: Quantifying triadic closure and local modular density.

---

## 2. Functional Requirements
1. **Algorithm Implementation in Epistemetrics**:
   - Add modules to `packages/epistemetrics/src/epistemetrics/graph/algorithms/`:
     - `closeness.py`: Closeness with disconnected component handling (Wasserman-Faust harmonic formula).
     - `katz.py`: Attenuated walk centrality with automatic spectral radius bounds check.
     - `hits.py`: Mutual authority and hub score convergence.
     - `clustering.py`: Local clustering coefficient and directed transitivity.
2. **Studio Integration**:
   - Register the new algorithms in [`metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py).
   - Expose them in [`AlgorithmPicker.tsx`](packages/episteme-studio/frontend/src/panels/AlgorithmPicker.tsx) and [`MetricsDrawer.tsx`](packages/episteme-studio/frontend/src/panels/MetricsDrawer.tsx).

---

## 3. Acceptance Criteria
- [ ] Closeness, Katz, HITS, and Clustering algorithms implemented with NetworkX and Cypher/GDS adapters in `epistemetrics`.
- [ ] Standard unit tests verifying mathematical invariants on benchmark graphs in `packages/epistemetrics/tests/`.
- [ ] Users can execute each metric asynchronously from the Studio Metrics Drawer and view results mapped to node sizes and colors.

---

## 4. Key Target Files
- `packages/epistemetrics/src/epistemetrics/graph/algorithms/`
- [`packages/episteme-studio/src/glp_studio/services/metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py)
- [`packages/episteme-studio/frontend/src/panels/AlgorithmPicker.tsx`](packages/episteme-studio/frontend/src/panels/AlgorithmPicker.tsx)
