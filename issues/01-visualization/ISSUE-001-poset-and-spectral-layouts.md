# [ISSUE-001] Topological Poset / Specialization Tree & Spectral Graph Layouts

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-001` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/graph/`) |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §1.2](issues/shared/requirements_glp_project.md#L52-L63) |

---

## 1. Problem Statement & Motivation
Currently, GLP Studio supports force-directed layouts (`d3-force`), basic geometric layouts (`concentric`, `radial`, `circular`, `grid`), and hierarchical DAGs (`antv-dagre`) in [`GraphCanvasHud.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx). 

However, formal theory graphs—specifically Theory-Nets—exhibit structural hierarchies that generic DAG algorithms cannot render cleanly:
1. **Theory Specialization Posets ($T_b \to T_i$)**: Structuralist theory-nets are strictly partially ordered sets (posets) rooted in invariant basic theory elements ($T_b$) that specialize monotonically downwards into terminal applications. Standard DAG layouts produce excessive edge crossings and do not emphasize horizontal specialization tiers or parent-child invariants.
2. **Structural Bottlenecks & Community Bridges**: Force layouts often tangle dense theoretical clusters. A **Spectral / Graph Laplacian layout** (computing coordinates via the Fiedler vector / second-smallest Laplacian eigenvalue) is required to expose natural structural communities and bridge bottlenecks mathematically.

---

## 2. Functional Requirements
1. **Poset / Specialization Tree Layout**:
   - Provide a dedicated `poset-tree` layout option in [`GraphCanvasHud.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx) and [`useG6Instance.ts`](packages/episteme-studio/frontend/src/graph/hooks/useG6Instance.ts).
   - Recognize `CONSTRAINS`, `SPECIALIZES`, and `EXTENDS` directed edges to compute topological rank tiers.
   - Root nodes ($T_b$) must anchor at the top tier; terminal intended applications ($I$) anchor at the bottom tier.
2. **Spectral / Laplacian Layout**:
   - Provide a `spectral-laplacian` option.
   - For smaller subgraphs ($N \le 1500$), calculate the normalized Laplacian matrix $L = I - D^{-1/2} A D^{-1/2}$ and use eigenvectors $v_2$ (Fiedler vector) and $v_3$ as 2D spatial coordinates.
   - For larger graphs, request 2D spectral coordinates from the backend metric adapter or fall back to high-damping force layout.
3. **Layout Stability & Warm Restart**:
   - Integrate with the position caching mechanism in [`useG6Instance.ts`](packages/episteme-studio/frontend/src/graph/hooks/useG6Instance.ts) (`savedPositionsRef`) to avoid canvas jitter when switching between layouts.

---

## 3. Acceptance Criteria
- [ ] `poset-tree` and `spectral-laplacian` appear as selectable options in the Canvas HUD layout dropdown.
- [ ] Selecting `poset-tree` on a Theory-Net subgraph cleanly separates hierarchical specialization levels with top-to-bottom edge alignment.
- [ ] Selecting `spectral-laplacian` positions structural bridge nodes along the central axis between disconnected clusters.
- [ ] Node positions are safely cached, allowing seamless toggling between layouts without reset artifacts.
- [ ] Unit tests added verifying layout configuration generation in `packages/episteme-studio/frontend/src/graph/styling/styling.test.ts`.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx)
- [`packages/episteme-studio/frontend/src/graph/hooks/useG6Instance.ts`](packages/episteme-studio/frontend/src/graph/hooks/useG6Instance.ts)
- [`packages/episteme-studio/frontend/src/graph/styling/types.ts`](packages/episteme-studio/frontend/src/graph/styling/types.ts)
