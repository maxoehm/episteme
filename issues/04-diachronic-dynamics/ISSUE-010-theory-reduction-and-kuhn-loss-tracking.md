# [ISSUE-010] Diachronic Theory Dynamics, Reduction Matrices ($\rho$), & Kuhn-Loss Tracking

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-010` |
| **Component(s)** | `packages/episteme-pipeline` (`post_processing/`), `packages/episteme-studio` (`frontend/src/panels/`) |
| **Roadmap Horizon** | **Horizon 3** (Epistemic Frontiers & Scientific Research) |
| **Priority** | High (Research Target) |
| **Status** | Research / Planned |
| **Source Ref** | [requirements_glp_project.md §4.1](issues/shared/requirements_glp_project.md#L181-L199), [docs/roadmap.md Horizon 3](docs/roadmap.md#L295-L303) |

---

## 1. Problem Statement & Motivation
Scientific theories evolve diachronically through specialization, paradigm shifts, and reduction (e.g., Classical Mechanics reducing to Relativistic Mechanics, or Phlogiston chemistry being displaced by Lavoisier's Oxygen framework).

While GLP Studio currently implements deterministic run-to-run identity diffing ([ADR 0014](docs/adr/0014-deterministic-identity-diffing-and-progression-workbench.md)) to track set-theoretic differences ($A \setminus B$, $B \setminus A$), this only tracks syntactic changes between pipeline executions. It does not model formal **structuralist theory reduction**:
1. **Reduction Relation ($\rho: T' \to T$)**: Mapping intended applications and models of successor theory $T'$ into predecessor theory $T$.
2. **Kuhn-Loss Tracking ($L_{\text{lost}}$)**: Identifying empirical problems or phenomena that were successfully explained by predecessor theory $T$ ($I_T$) but are abandoned, displaced, or unexplainable by successor theory $T'$ ($I_T \setminus \rho(I_{T'})$).

---

## 2. Functional Requirements
1. **Structuralist Reduction Analyzer**:
   - Create a post-processing module in `packages/episteme-pipeline/episteme_pipeline/post_processing/theory_reduction/`.
   - Calculate the reduction matrix $\rho$ between two distinct theoretical frameworks extracted from historical corpora.
   - Flag domain-level subsumption vs. incommensurability.
2. **Kuhn-Loss Ledger**:
   - Detect empirical applications ($y \in I_T$) whose tenability collapses or which lack representation in $T'$.
   - Compute the Kuhn-Loss metric:
     $$L_{\text{lost}}(T, T') = \frac{|I_T \setminus \rho(I_{T'})|}{|I_T|}$$
3. **Theory Dynamics Studio View**:
   - Provide a dedicated **Theory Dynamics / Reduction Studio** panel in GLP Studio visualizing the asymmetric specialization lattice ($T_b \to T_i$) and side-by-side empirical domain displacement maps.

---

## 3. Acceptance Criteria
- [ ] Pipeline computes reduction mappings ($\rho$) and flags lost empirical applications ($L_{\text{lost}}$).
- [ ] GLP Studio displays a Kuhn-Loss matrix comparing competing or historical theories.
- [ ] Verification on historical benchmark cases (e.g. Newtonian mechanics vs. Special Relativity).

---

## 4. Key Target Files
- `packages/episteme-pipeline/episteme_pipeline/post_processing/theory_reduction/`
- `packages/episteme-studio/frontend/src/panels/`
- [`packages/episteme-studio/src/glp_studio/api/diff.py`](packages/episteme-studio/src/glp_studio/api/diff.py)
