# [ISSUE-007] Pareto Frontier Multi-Virtue Evaluation & Tradeoff Visualizer

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-007` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/panels/`) |
| **Roadmap Horizon** | **Horizon 2** (Scalability, Benchmarking & Dialectical Modeling) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §3.2](issues/shared/requirements_glp_project.md#L148-L150) |

---

## 1. Problem Statement & Motivation
No single epistemic metric determines whether a theory is optimal; theoretical virtues naturally trade off against one another (e.g., maximizing empirical content and refutability often reduces modesty and conservatism). 

Currently, GLP Studio visualizes individual metric distributions in isolation. To evaluate competing theoretical frameworks or subgraphs, researchers require a **Pareto Frontier Analytics View** that computes multi-objective efficiency frontiers across virtues (e.g., plotting Refutability vs. Simplicity vs. Tenability).

---

## 2. Functional Requirements
1. **Multi-Objective Tradeoff Scatterplot**:
   - Provide an interactive multi-axis scatterplot using ECharts in [`EpistemicCharts.tsx`](packages/episteme-studio/frontend/src/panels/EpistemicCharts.tsx).
   - Allow users to select any two or three metrics for the X, Y, and Z (size/color) axes (e.g., $X = \text{Refutability}$, $Y = \text{Conservatism}$, $\text{Size} = \text{Tenability}$).
2. **Pareto Dominance Calculation**:
   - Calculate non-dominated points: theory subgraph $A$ dominates $B$ ($A \succ B$) iff $A$ is strictly better than $B$ on at least one virtue and no worse on all others.
   - Draw the computed Pareto efficiency frontier boundary line/surface.
3. **Subgraph Highlighting from Scatter Points**:
   - Clicking any point on the Pareto frontier highlights its corresponding TheoryNet sub-element and intended applications on the main AntV G6 canvas.

---

## 3. Acceptance Criteria
- [ ] Users can configure multi-metric axes and view competing theories on a 2D/3D scatterplot.
- [ ] Non-dominated theories along the Pareto frontier are visually distinguished with gold boundary highlights.
- [ ] Clicking points cross-filters the graph canvas and opens the Theory Inspector.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/panels/EpistemicCharts.tsx`](packages/episteme-studio/frontend/src/panels/EpistemicCharts.tsx)
- [`packages/episteme-studio/frontend/src/panels/echarts.ts`](packages/episteme-studio/frontend/src/panels/echarts.ts)
- [`packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx)
