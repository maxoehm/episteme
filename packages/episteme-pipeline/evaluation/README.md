# Evaluation Blueprint: Knowledge‑Graph Construction

Date: 2026-06-07
Status: Plan for implementation
Owner: Grund GLP

---

## 1. Purpose and Scope

This blueprint operationalizes our evaluation strategy for the pipeline’s core: knowledge‑graph (KG) construction. It documents what we aim to prove, how we will measure it, and which artifacts we will persist so results are reusable for the paper and future work.

Focus:
- Construction phases up to and including fusion/normalization.
- Argument/Theory projections are evaluated separately; for now we add minimal coherence checks behind a semantics gate (to be decided in the theory layer docs).

Non‑goals:
- End‑user task performance and downstream reasoning quality are out of scope for this phase.

References:
- Target methodology: `docs/evaluation/methodology.md` (2026‑06‑01).
- Critical review priorities: `../../../review/2026-06-critical-architecture-and-implementation-review.md`.

---

## 2. Hypotheses and Research Questions

H1. With a fixed LLM, pipeline choices (chunking, retrieval, linking thresholds, fusion) materially change task‑level quality (NER, EL, RE) and graph integrity.

H2. On established gold benchmarks, the pipeline achieves competitive results against strong open baselines; any deficits are explainable by retrievable evidence gaps or clear error buckets.

H3. The constructed graph maintains high provenance coverage and satisfies schema/uniqueness/existence constraints in Neo4j.

RQ1. How sensitive are results to chunking parameters and retrieval windows?  
RQ2. What are the dominant error modes per phase (missed mentions, false merges, unsupported relations, etc.)?  
RQ3. How stable are results across runs with fixed seeds and across model/prompt versions?

---

## 3. Evaluation Modes

- Closed‑Book: Only dataset text/context. No external retrieval beyond the provided document(s).
- Retrieval‑Assisted: Allow retrieval (e.g., collection‑scoped). Log sources; report candidate recall and evidence sufficiency.
- Stability: Repeat runs with fixed seeds; report variance across 3 runs (min).

Guardrails:
- Freeze model name/version and prompt IDs per run.
- Disallow external web retrieval on closed‑book sets.
- LLM‑as‑judge only as a secondary signal with correlation to human judgments on sampled items.

---

## 4. Datasets Strategy (No Large In‑House Gold)

Policy: Prefer established public gold standards and use adapters to our schema. Maintain only a tiny domain review set (200–500 items) for edge cases (DE/EN scholarly philosophy/science, long‑range references, ambiguous names).

Selection principles:
- Coverage: EN and DE for NER; at least one EL and one RE set.
- Licensing: Redistributable or runnable via public instructions.
- Task clarity: Unambiguous label spaces and evaluation scripts.

Adapters:
- Each dataset gets an `evaluation/adapters/<dataset>/` folder with: loader, label mapping, and prediction normalizer.

---

## 5. Metrics and Checks

Per `docs/evaluation/methodology.md` with added specifics for graph-level evaluation:

- **Graph Structural Matching (GM-GBS):** Graph BERTScore with similarity thresholds (e.g., 95%) to evaluate structural and semantic alignment, abstracting away from exact string matches.
- **Hallucination & Omission Rates (OEP):** Optimal Edit Paths to calculate the precise percentage of fabricated or missing triples compared to the benchmark.
- **Reference-Free Evaluation (LLM-as-a-Judge):** Faithfulness (is the graph supported by the source text?) and Comprehensiveness (does the graph cover all major claims?).
- **Graph Integrity (Neo4j):**
  - Schema consistency against the abstracted pipeline schema.
  - Provenance coverage (% nodes/edges with source offsets + doc IDs).
- **Cost/Performance:** tokens, latency, memory footprint.
- **Stability:** cross‑run deltas with fixed seeds.

---

## 6. Artifacts and Run Manifests

Every evaluation is tied to a run manifest (`evaluation/run_manifest.schema.yaml`). Persist phase artifacts to enable re‑scoring:

- Phase 1: chunked text + provenance map.
- Phase 2: entity mentions (spans, types), candidate links, resolved links.
- Phase 3: relation candidates and final relations (with evidence refs).
- Phase 5: clusters/merges and decisions (scores, thresholds).

Reporting: One Markdown report per run in `experiments/` using `evaluation/templates/report_template.md`.

---

## 7. Baselines and Ablations

- Baselines: At least one strong open baseline per task (classical or smaller LM), plus simple heuristics where applicable.
- Ablations: Fix the LLM; vary chunking, retrieval scope, linker thresholds, and fusion parameters to quantify pipeline lift.

---

## 8. Human and LLM Review

- **Scope:** difficult global relations and ambiguous entity links in the domain review set, especially for scholarly philosophy/science texts.
- **LLM-as-a-Judge (Core):** used to automatically assess reference-free metrics (Faithfulness and Comprehensiveness). See `evaluation/rubrics/llm_judge_prompts.md` for zero-shot/few-shot prompts.
- **Human Review:** rubric‑based judgments to calibrate the LLM-judge; compute inter‑annotator agreement on a subset.
- **Storage:** structured judgments under `experiments/<run_id>/review/`.

Rubrics: see `evaluation/rubrics/README.md` and `evaluation/rubrics/llm_judge_prompts.md`.

---

## 9. Contamination and Ethics

- Document any pretraining overlap concerns and retrieval sources.  
- Closed‑book by default for public benchmarks.  
- No PII or sensitive content beyond dataset terms.

---

## 10. Milestones (First 4 Weeks)

1. Manifests + Artifacts
   - Finalize run‑manifest schema with language tracking; implement artifact persistence contracts.
   - Wire graph-level constraint checks into reports.
2. Graph Scorers + Adapters
   - Implement formatting adapters (syntactic normalization only).
   - Implement GM-GBS and OEP structural scorers; first runs and reports.
3. LLM-as-a-Judge + Retrieval
   - Implement reference-free metrics (Faithfulness/Comprehensiveness); implement candidate recall diagnostics.
4. Human Review Pilot
   - Draft rubrics; sample domain cases; calibrate the LLM‑judge with human scores; publish comparative report.

---

## 11. Paper‑Facing Outputs

Each report includes:
- Datasets and splits, model/prompt/seed, schema snapshot.
- Full metric tables and confidence intervals where applicable.
- Error analysis with exemplars per bucket.
- Graph integrity summary and constraint status.
- Cost metrics and stability analysis.

We will maintain a table of SOTA/baseline comparisons with citations in the paper appendix; the repo will link to reproducible run folders.

---

## 12. Risks and Mitigations

- LLM variance → fix seeds; report variance; repeat critical runs.
- Schema mismatch → adapters normalize outputs to each label space.
- Overreliance on LLM‑judge → human correlation checks; limit judge influence.
- Retrieval leakage on closed‑book → enforce mode flags at run time.

---

## 13. Implementation Handover

This document is the ground truth for the next implementation step. See:
- `evaluation/run_manifest.schema.yaml` — manifest contract.
- `evaluation/templates/report_template.md` — reporting skeleton.
- `evaluation/neo4j/constraints_checklist.md` — integrity checks to wire into CI.
- `evaluation/rubrics/README.md` — reviewer guidance.

