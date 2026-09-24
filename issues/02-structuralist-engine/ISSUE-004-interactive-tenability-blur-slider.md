# [ISSUE-004] Real-Time Tenability Blur Slider ($\delta^*$) & Interactive Anomaly Lensing

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-004` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/graph/`, `panels/`) |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §2.2](issues/shared/requirements_glp_project.md#L104-L124), [ADR 0015](docs/adr/0015-theoretical-enrichment-and-tenability-evaluation.md) |

---

## 1. Problem Statement & Motivation
Under [ADR 0015](docs/adr/0015-theoretical-enrichment-and-tenability-evaluation.md), empirical observations $y \in I \subseteq M_{pp}$ are evaluated against theoretical laws $M$ using Bourbaki uniform spaces and admissible blurs $\mathcal{A}$:
$$TS_{\text{local}}(y, M) = \sup \{ 1 - \delta \mid \exists x^* \in M : (\Phi(y), x^*) \in u_\delta \}$$
When an empirical claim deviates from theoretical constraints, it incurs an inaccuracy blur $\delta^*$. If $TS < 0.5$, it is flagged as an epistemic anomaly.

Currently, tenability thresholds can be configured inside backend parameter forms (`tenability_threshold: 0.5` in [`metric_service.py`](packages/episteme-studio/src/glp_studio/services/metric_service.py#L390-L397)), but the canvas lacks an **interactive real-time slider control**. Researchers cannot dynamically scrub through blur radii ($\delta^* \in [0.0, 1.0]$) to inspect boundary conditions and watch theories transition from tenable to falsified in real time.

---

## 2. Functional Requirements
1. **Interactive Blur HUD Control**:
   - Add a floating slider control $\delta^*$ directly to [`GraphCanvasHud.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx) when the Tenability overlay is active.
   - Adjusting the slider updates the threshold in real time (debounced to 30fps for smooth canvas animation).
2. **Visual Anomaly Callouts**:
   - Nodes dropping below the active cutoff ($TS_{\text{local}} < \delta^*$) are rendered with an anomaly warning ring (pulsing amber/red border) and dimmed fill.
   - Edges violating inter-domain constraints ($TS_{\text{edge}} < \delta^*$) display a jagged/dashed line pattern.
3. **Explanatory Violation Drawer**:
   - Clicking an anomalous node opens [`NodeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx), showing the exact symbolic law equation, observed empirical values, and the distance metric driving down the tenability score.

---

## 3. Acceptance Criteria
- [ ] Canvas HUD displays a reactive slider for blur radius $\delta^*$ when Tenability mode is enabled.
- [ ] Nodes dynamically transition to "anomalous" visual states as $\delta^*$ increases.
- [ ] Node inspector displays the mathematical constraint formula and violation delta for flagged nodes.
- [ ] Performance benchmark: Canvas maintains $> 50\text{ fps}$ during continuous slider scrubbing on graphs with up to 1,000 active nodes.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvasHud.tsx)
- [`packages/episteme-studio/frontend/src/graph/styling/nodeStyling.ts`](packages/episteme-studio/frontend/src/graph/styling/nodeStyling.ts)
- [`packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx)
