# [ISSUE-005] Sneedian $T$-Theoreticity Criterion & Symbolic Ramsey-Sentence Verification

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-005` |
| **Component(s)** | `packages/episteme-pipeline` (`post_processing/theoretical_enrichment/`), `packages/epistemetrics` |
| **Roadmap Horizon** | **Horizon 3** (Epistemic Frontiers & Scientific Research) |
| **Priority** | Low |
| **Status** | Research / Future Target |
| **Source Ref** | [requirements_glp_project.md §2.3](issues/shared/requirements_glp_project.md#L125-L132) |

---

## 1. Problem Statement & Motivation
Joseph D. Sneed's seminal problem of theoretical terms establishes that the meaning and measurement of theoretical concepts often presupposes the very theory in which they appear (e.g., measuring gravitational mass requires Newton's laws). 

To avoid vicious circularity and verify that a theory makes genuine empirical claims rather than vacuous analytical tautologies, computational metatheory requires:
1. **Automated Sneedian Classification**: Classifying predicates and terms as $T$-theoretical or $T$-non-theoretical depending on whether their determination requires an application of theory $T$.
2. **Ramsey-Sentence Reduction ($r(K)$)**: Stripping $T$-theoretical functions via existential quantification over relations to extract the non-theoretical empirical assertion $\text{Cn}(K)$, and mathematically verifying that the theory's empirical content is non-empty.

---

## 2. Functional Requirements
1. **Sneedian Term Classifier**:
   - Analyze dependency chains in the knowledge graph: if term $X$'s measurement or derivation edge strictly originates from an axiom of theory $T$, label $X$ as $T$-theoretical. If $X$ can be grounded independently in pre-theoretical observations (Layer 1 chunks or external theories), label $X$ as $T$-non-theoretical ($M_{pp}$).
2. **Ramsey Sentence Eliminator**:
   - Implement symbolic second-order term elimination over extracted first-order constraints in `epistemetrics`.
   - Compute the empirical projection $r(M) \subseteq M_{pp}$.
   - Verify whether $r(M)$ places non-trivial restrictions on the empirical base ($r(M) \subsetneq M_{pp}$).

---

## 3. Acceptance Criteria
- [ ] Pipeline post-processor assigns `is_theoretical: bool` to parameters in `TheoryNet`.
- [ ] Symbolic module verifies whether the empirical claim contains non-vacuous content.
- [ ] Unit tests validate classical test cases (e.g. Sneed's formulation of Classical Particle Mechanics).

---

## 4. Key Target Files
- `packages/episteme-pipeline/episteme_pipeline/post_processing/theoretical_enrichment/`
- `packages/epistemetrics/src/epistemetrics/core/models.py`
