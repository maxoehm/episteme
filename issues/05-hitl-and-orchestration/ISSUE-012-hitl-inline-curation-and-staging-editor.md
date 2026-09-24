# [ISSUE-012] Human-in-the-Loop (HITL) Inline Curation & Staging Editor

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-012` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/panels/`, `api/`) |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §5.3](issues/shared/requirements_glp_project.md#L241-L253), [docs/TODO_FUTURE.md §3](docs/TODO_FUTURE.md#L36-L45) |

---

## 1. Problem Statement & Motivation
Automated LLM graph extraction inevitably produces occasional errors: conflated concepts, incorrect relation polarities (e.g. marking an attack as support), or spurious triples. 

Currently, GLP Studio includes [`PolarityInversionModal.tsx`](packages/episteme-studio/frontend/src/panels/PolarityInversionModal.tsx) for reversing dialectical polarities, but lacks a full **Human-in-the-Loop (HITL) Curation Workbench**:
1. **Interactive Curation Actions**: Merging synonym/duplicate nodes, splitting conflated concepts, pruning spurious edges, or manually injecting missing inferential bridges.
2. **Non-Destructive Staging & Commit Flow**: Edits must never destructively mutate raw machine extraction artifacts. Instead, they should stage in a provisional local diff and commit as versioned human curation layers on top of the immutable machine run.
3. **High-Centrality & Anomaly Flagging**: Per [`docs/TODO_FUTURE.md` §3](docs/TODO_FUTURE.md#L36-L45), the pipeline should automatically prioritize expert review for high-centrality bottleneck claims and numerical results.

---

## 2. Functional Requirements
1. **Curator Action Toolbar**:
   - Add inline editing controls to [`NodeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx) and [`EdgeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/EdgeInspectorPanel.tsx):
     - `Merge with Node...`: Merges two nodes while consolidating aliases and provenance chunks.
     - `Split Concept...`: Divides an entity into two distinct theoretical claims.
     - `Invert Polarity`: Toggles `SUPPORT` $\leftrightarrow$ `ATTACK`.
     - `Mark Spurious / Delete`: Soft-deletes an edge with an audit justification note.
2. **Staging & Commit Ledger**:
   - Create a `StagingDrawer.tsx` displaying pending human adjustments as a diff preview ($A \Delta B$).
   - Provide a "Commit Curation" action that writes a `curation_manifest.json` artifact attached to the run.
3. **Targeted HITL Review Queue**:
   - Filter queue prioritizing:
     - Nodes with high betweenness centrality (inferential bottlenecks).
     - Nodes with tenability violations ($TS_{\text{local}} < 0.5$).
     - Claims with numerical or empirical assertions.

---

## 3. Acceptance Criteria
- [ ] Researchers can merge nodes and toggle edge polarities directly within the UI.
- [ ] Edits are non-destructive and tracked in a provisional curation staging ledger.
- [ ] Committing curation creates a versioned fork of the run with full provenance.
- [ ] Review queue correctly highlights high-centrality and low-tenability claims for priority verification.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/NodeInspectorPanel.tsx)
- [`packages/episteme-studio/frontend/src/panels/EdgeInspectorPanel.tsx`](packages/episteme-studio/frontend/src/panels/EdgeInspectorPanel.tsx)
- [`packages/episteme-studio/frontend/src/panels/PolarityInversionModal.tsx`](packages/episteme-studio/frontend/src/panels/PolarityInversionModal.tsx)
- [`packages/episteme-studio/src/glp_studio/api/runs.py`](packages/episteme-studio/src/glp_studio/api/runs.py)
