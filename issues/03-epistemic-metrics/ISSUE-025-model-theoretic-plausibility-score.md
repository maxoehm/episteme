# [ISSUE-025] Model-Theoretic Plausibility Score ($p$) on Evidentiary Edges

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-025` |
| **Component(s)` | `packages/epistemetrics` (`graph/models.py`), `packages/episteme-pipeline` (`pipeline/contracts/domain.py`, `phases/phase6_theorynet/`), `packages/episteme-studio` |
| **Roadmap Horizon** | **Horizon 2** (Dialectical Modeling & Epistemic Metrics) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | Formerly tracked in `docs/concepts/theory/metrics/TODO.md` |

---

## 1. Problem Statement & Motivation
In structuralist philosophy of science (Sneed, Stegmüller, Balzer & Moulines), an empirical application $I$ is intended to be subsumed under a theoretical model core $M_p$. When extracting natural-language claims from scholarly literature, empirical observations rarely map with binary certainty to formal model cores.

To formally capture the degree of fit between concrete observation units and abstract law hypotheses, the graph schema requires an explicit **Plausibility Score** ($p$):
- **Definition:** A continuous metric $p(i, x) \in [0, 1]$ quantifying the epistemic confidence that an empirical observation node $i \in I$ is a valid instantiation of a theoretical model component $x \in X$ (where $X \subseteq M_p$).
- **Epistemic Function:** It serves as a hermeneutic proxy for structural fit when evaluating natural language claims against formal theory cores:
  - $p \to 1.0$: High likelihood that $i$ fits the theoretical claim of $x$ (e.g., $i$: *"Observed perihelion shift of Mercury"*, $x$: *"Geodesic equation in Schwarzschild metric"*).
  - $p \to 0.0$: Lack of fit, irrelevance, or empirical contradiction.

---

## 2. Functional Requirements
1. **Schema & Domain Contract Representation**:
   - Verify and standardize the `plausibility: float` property on `:EVIDENCED_BY`, `:INSTANTIATES`, and `:APPLIES_TO` relationships in `pipeline/contracts/domain.py` and Neo4j projection graphs.
   - Differentiate edge plausibility ($p$) from node prior plausibility ($\tau$), ensuring clear semantic distinction in serialization and schema validation.

2. **Extraction & Inference Support**:
   - In `Phase 6: TheoryNet` and `post_processing/theoretical_enrichment/`, compute or propagate empirical fit scores when linking Layer 1/2 observation instances to Layer 3 theoretical hypotheses.

3. **Epistemetrics & Studio Visualization**:
   - Support edge-level plausibility weighting in `epistemetrics` tenability calculations ($TS_{\text{edge}}$) and LPG-ECHO evidentiary input clamping.
   - Display edge plausibility in GLP Studio edge inspection panels and edge weight stroke representations.

---

## 3. Acceptance Criteria
- [ ] Domain contracts in `pipeline/contracts/domain.py` explicitly validate edge-level `plausibility: float | None` bounded in $[0.0, 1.0]$.
- [ ] Projection to Neo4j persists `plausibility` property on `:EVIDENCED_BY` and `:INSTANTIATES` relationships.
- [ ] Epistemetrics tenability evaluators incorporate edge plausibility into structural fit metrics.
- [ ] Unit tests verify serialization, deserialization, and edge score validation.

---

## 4. Key Target Files
- `packages/episteme-pipeline/episteme_pipeline/contracts/domain.py`
- `packages/episteme-pipeline/episteme_pipeline/phases/phase6_theorynet/`
- `packages/epistemetrics/src/epistemetrics/`
- `packages/episteme-studio/src/glp_studio/adapters/neo4j_reader.py`
