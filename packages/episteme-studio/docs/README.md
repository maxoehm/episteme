# glp-studio

A run-oriented workbench over the Grund GLP pipeline: browse and configure runs and artifacts, trace
grounding from theory atoms back to source text, watch pipeline execution live, query the
projected graph, and apply epistemic overlays.

---

## Read in this order

| Document | What it settles |
|---|---|
| **[SPEC.md](SPEC.md)** | Architecture, package layout, configuration, the four integration seams |
| **[CONTRACT.md](CONTRACT.md)** | Wire models, endpoints, error shape — what Python and TypeScript agree on |
| **[ONTOLOGY.md](ONTOLOGY.md)** | Node and relation types, and what may *not* be assumed about them |
| **[docs/](index.md)** | Developer how-to guides and architecture walkthroughs |

`archive/` holds the earlier planning documents. They contradict the above on thirteen
points and two of them are corrupted. Do not implement from them.

---

## Five things that will surprise you

Verified against the repository, not assumed. Full detail in `SPEC.md` §8.

1. **Neo4j is optional.** `project_artifacts_to_graph` defaults to `False`. The system of
   record is `../../../.pipeline_artifacts` on disk. Build the artifact reader
   first (D-04).
2. **The declared schema is not the extracted vocabulary.** Real predicates are
   open-vocabulary German (`WIDERSPRICHT`, `FALSIFIZIERT`, `IMPLIZIERT`, …) with an *empty*
   intersection against `L2_RELATION_TYPES`. Every polarity lookup misses (D-15).
3. **There are eight phases, not six** — including a `3b` and two both named "Phase 4".
   Render the stepper from `phase_records`, keyed on ordinal (D-22).
4. **`epistemetrics` exports two functions.** Most metric buttons in the archived plan
   have nothing behind them (ONTOLOGY §7).

---
