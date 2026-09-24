# [ISSUE-013] Retrieval MIPS Distributions & Cross-Encoder Rerank Decision Auditing

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-013` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/panels/StageProvenancePane.tsx`, `panels/StageArtifactsView.tsx`), `packages/episteme-pipeline` |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §5.1](issues/shared/requirements_glp_project.md#L229-L233) |

---

## 1. Problem Statement & Motivation
In Phase 3 (Global Relations) and Phase 3b (Consolidation), relations are discovered through a two-stage retrieval pipeline:
1. **Bi-encoder Maximum Inner Product Search (MIPS)**: Rapid dense similarity candidate blocking generating top-$k$ candidate pairs.
2. **Cross-Encoder Reranker**: Deep cross-attention scoring assigning confidence scores and applying an acceptance threshold cutoff ($\tau$).

Currently, [`StageArtifactsView.tsx`](packages/episteme-studio/frontend/src/panels/StageArtifactsView.tsx) and [`StageProvenancePane.tsx`](packages/episteme-studio/frontend/src/panels/StageProvenancePane.tsx) display the finalized triples and text provenance. However, developers and researchers cannot inspect the **decision boundary**: why a specific candidate was dropped, the distribution of cross-encoder confidence scores, or what happens when threshold $\tau$ is altered.

---

## 2. Functional Requirements
1. **Candidate Retrieval Score Spectra**:
   - In [`StageProvenancePane.tsx`](packages/episteme-studio/frontend/src/panels/StageProvenancePane.tsx), render an interactive histogram of candidate pair similarity scores.
   - Display a vertical marker indicating the active acceptance threshold $\tau$.
2. **Dropped Candidate Triage**:
   - Provide a toggle to view "Rejected Candidates" (candidates scoring just below $\tau$) alongside accepted triples to diagnose false negatives and borderline extractions.
3. **Threshold Sensitivity Simulation**:
   - Allow users to simulate moving $\tau$ to preview how many relations would be added or pruned without re-running the full LLM pipeline.

---

## 3. Acceptance Criteria
- [ ] Stage 3 provenance pane displays MIPS distance distributions and cross-encoder score histograms.
- [ ] Users can inspect rejected/dropped candidate pairs that fell below the threshold.
- [ ] Acceptance threshold $\tau$ is visualized clearly on the distribution curve.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/panels/StageProvenancePane.tsx`](packages/episteme-studio/frontend/src/panels/StageProvenancePane.tsx)
- [`packages/episteme-studio/frontend/src/panels/StageArtifactsView.tsx`](packages/episteme-studio/frontend/src/panels/StageArtifactsView.tsx)
