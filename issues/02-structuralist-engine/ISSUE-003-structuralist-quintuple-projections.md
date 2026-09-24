# [ISSUE-003] Complete Structuralist Quintuple Filter Projections ($M_p, M, M_{pp}, GC, GL$)

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-003` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/store/viewOverlayStore.ts`, `panels/ViewOverlayDrawer.tsx`), `packages/episteme-pipeline` |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §2.1](issues/shared/requirements_glp_project.md#L92-L103), [ADR 0015](docs/adr/0015-theoretical-enrichment-and-tenability-evaluation.md) |

---

## 1. Problem Statement & Motivation
Under the formal structuralist philosophy of science ([Balzer, Moulines, Sneed 1987]; [Stegmüller 1976]), a scientific theory is formalized as a pair $T = \langle K, I \rangle$, where the theoretical core $K$ is a five-tuple:
$$K = \langle M_p, M, M_{pp}, GC, GL \rangle$$
1. $M_p$: Potential Models (the conceptual and parametric framework).
2. $M$: Actual Models (subsets of $M_p$ satisfying fundamental laws).
3. $M_{pp}$: Partial Potential Models (the non-theoretical empirical base).
4. $GC$: Global Constraints (cross-application constraints linking instances across distinct domains).
5. $GL$: Global Intertheoretical Links (directed bridges connecting parameters to foundational/external theories).

Currently, GLP Studio's [`viewOverlayStore.ts`](packages/episteme-studio/frontend/src/store/viewOverlayStore.ts) only implements lenses for:
- `empirical_base` ($M_{pp}$, Partition B)
- `theoretical_core` ($M$, Partition A)

The remaining three structural components—**Potential Models ($M_p$)**, **Global Constraints ($GC$)**, and **Global Links ($GL$)**—are extracted during pipeline enrichment ([ADR 0015](docs/adr/0015-theoretical-enrichment-and-tenability-evaluation.md)) but lack first-class visual filter toggles and dedicated projection overlays in the user interface.

---

## 2. Functional Requirements
1. **Curated Lenses Expansion**:
   - Add explicit lenses to `CURATED_LENSES` in [`viewOverlayStore.ts`](packages/episteme-studio/frontend/src/store/viewOverlayStore.ts):
     - `potential_models` ($M_p$): Isolates conceptual predicates, parameter dimensions, and typing boundaries before law validation.
     - `global_constraints` ($GC$): Highlights inter-domain parameter equality and boundary constraints.
     - `intertheoretical_links` ($GL$): Isolates cross-theory dependency links (`CONSTRAINS`, `REDUCES_TO`, `COHERES_WITH`).
2. **Overlay Drawer Controls**:
   - In [`ViewOverlayDrawer.tsx`](packages/episteme-studio/frontend/src/panels/ViewOverlayDrawer.tsx), provide a dedicated "Structuralist Quintuple ($K$)" section enabling researchers to toggle each component on/off independently or as combined sets.
3. **Graph Node/Edge Styling**:
   - Differentiate $GC$ edges (dashed orange constraint links) and $GL$ edges (double-line inter-paradigm bridges) in [`edgeStyling.ts`](packages/episteme-studio/frontend/src/graph/styling/edgeStyling.ts).

---

## 3. Acceptance Criteria
- [ ] `viewOverlayStore.ts` defines complete masks for $M_p$, $M$, $M_{pp}$, $GC$, and $GL$.
- [ ] Users can toggle individual components of $K$ in the View Overlay Drawer and observe immediate canvas filtering.
- [ ] $GL$ links connecting distinct theoretical clusters are visually distinguished from intra-theory argumentative edges.
- [ ] Unit tests in `packages/episteme-studio/frontend/src/panels/viewOverlay.test.ts` pass with full coverage for all five structuralist masks.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/store/viewOverlayStore.ts`](packages/episteme-studio/frontend/src/store/viewOverlayStore.ts)
- [`packages/episteme-studio/frontend/src/panels/ViewOverlayDrawer.tsx`](packages/episteme-studio/frontend/src/panels/ViewOverlayDrawer.tsx)
- [`packages/episteme-studio/frontend/src/graph/styling/edgeStyling.ts`](packages/episteme-studio/frontend/src/graph/styling/edgeStyling.ts)
