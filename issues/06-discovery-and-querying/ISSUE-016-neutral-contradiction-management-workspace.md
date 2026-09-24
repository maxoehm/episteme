# [ISSUE-016] Neutral Contradiction Management Workspace (3-State Belief Indicator)

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-016` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/panels/`), `packages/episteme-pipeline` |
| **Roadmap Horizon** | **Horizon 3** (Epistemic Frontiers & Scientific Research) |
| **Priority** | Medium |
| **Status** | Planned / Research |
| **Source Ref** | [requirements_glp_project.md §6.3](issues/shared/requirements_glp_project.md#L287-L293), [docs/TODO_FUTURE.md §6](docs/TODO_FUTURE.md#L70-L79) |

---

## 1. Problem Statement & Motivation
In standard knowledge graphs, contradictions are treated as database errors to be resolved or purged. However, in scientific and philosophical literature, competing paradigms legitimately contradict one another without objective consensus. 

Per the philosophical doctrine of **Epistemic Contextualism**, the system must never forcibly merge or auto-resolve conflicting theoretical paradigms. Instead, the platform requires a **Neutral Contradiction Management Workspace**:
1. Managing `WIDERSPRICHT` / `ATTACKS` relationships neutrally as framework-relative assertions.
2. Formalizing an explicit 3-state belief indicator:
   $$\vec{b} = \langle \text{Belief}, \text{Disbelief}, \text{Uncertainty} \rangle$$
   ensuring that conflicting claims remain mutually observable without synthetic homogenization.

---

## 2. Functional Requirements
1. **3-State Epistemic Valuation**:
   - Model belief vectors $\langle B, D, U \rangle$ where $B + D + U = 1.0$ (Dempster-Shafer or Subjective Logic).
   - Tag conflicting claims with paradigm context anchors (e.g. `theory_scope: "Copenhagen"` vs `theory_scope: "Bohmian"`).
2. **Contradiction Workspace Panel**:
   - Provide a specialized view in GLP Studio isolating conflicting subgraphs connected by `ATTACKS` and `INCOMPATIBLE_WITH` edges.
   - Display a side-by-side claim ledger comparing the empirical grounding, citation evidence, and internal coherence of both sides neutrally.
3. **Dynamic Admissibility Valuation ($\kappa$)**:
   - Per [`docs/TODO_FUTURE.md` §6](docs/TODO_FUTURE.md#L77-L79), integrate structural correspondence scores into downstream evaluation metrics for external paradigm compatibility.

---

## 3. Acceptance Criteria
- [ ] Contradictory claims are displayed in a dedicated Contradiction Workspace without forced resolution.
- [ ] Nodes display 3-state belief distributions $\langle B, D, U \rangle$ rather than simple binary truth values.
- [ ] Paradigm boundaries are visually preserved across conflicting claim pairs.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/panels/`](packages/episteme-studio/frontend/src/panels/)
- `packages/episteme-pipeline/episteme_pipeline/post_processing/`
