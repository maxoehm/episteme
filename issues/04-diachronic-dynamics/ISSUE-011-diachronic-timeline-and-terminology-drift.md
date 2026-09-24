# [ISSUE-011] Diachronic Timeline Scrubber & Terminology Drift Inspector

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-011` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/panels/`, `frontend/src/graph/`) |
| **Roadmap Horizon** | **Horizon 3** (Epistemic Frontiers & Scientific Research) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §4.2](issues/shared/requirements_glp_project.md#L200-L208) |

---

## 1. Problem Statement & Motivation
Scientific and philosophical discourse unfolds over decades or centuries. As theories mature:
1. **Temporal Birth, Mutation, and Retirement**: Core concepts undergo progressive specialization or abandonment over time.
2. **Terminology Drift**: The linguistic terms denoting a theoretical role often shift (e.g., "vis viva" shifting to "kinetic energy", or "caloric" shifting to "internal thermal energy") while the underlying mathematical or inferential role in the graph remains invariant.

Currently, GLP Studio presents static graph snapshots corresponding to single execution runs. It lacks a **temporal timeline scrubber** to play through historical time slices, and a **terminology drift inspector** to track semantic shifts without corrupting historical provenance.

---

## 2. Functional Requirements
1. **Timeline Scrubber Control**:
   - Provide a temporal scrubber slider at the bottom of the graph canvas, indexed by publication year or document chronology ($t_0 \to t_{\text{final}}$).
   - Moving the scrubber animates node and edge appearances, mutations, and retirements.
2. **Terminology Drift Inspector**:
   - For stable theoretical roles, maintain an alias progression ledger:
     $$\text{Role}_{id} \to [(\text{"vis viva"}, 1686), (\text{"kinetic energy"}, 1849)]$$
   - Surface label evolution in [`NodeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx) under an "Evolution" tab.
3. **Non-Destructive Temporal State Preservation**:
   - Preserve temporal metadata without mutating original entity IDs or raw extraction envelopes.

---

## 3. Acceptance Criteria
- [ ] Timeline scrubber allows users to scrub across historical epochs and observe graph growth.
- [ ] Nodes that are retired or replaced in later epochs visually fade or display retirement badges.
- [ ] Terminology drift table tracks historical aliases for invariant structural roles.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/panels/RunTimeline.tsx`](packages/episteme-studio/frontend/src/panels/RunTimeline.tsx)
- [`packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx)
- [`packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx)
