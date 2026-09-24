# [0005] Pipeline Consolidation and Fusion Sequence: Phase 3b Before Argument Mining, Phase 5b After

Status: Accepted (Amended to reflect Phase 3b Latent Graph Consolidation and 7-runner pipeline)

## Context

Argument mining (Phase 4) operates on entity-tagged text. If the Knowledge Graph still contains alias entities or
duplicate parallel extractions ("Kant" and "Immanuel Kant" as separate nodes), argument components extracted from
different sections will fail to unify structurally — e.g., a claim about "Kant" and a claim about "Immanuel Kant" will
produce disconnected argument subgraphs even if they refer to the same person.

Conversely, argument clustering (Key Point Analysis) and global theory fusion can only run *after* all ADUs have been
extracted and committed to the graph by Phase 4.

This creates a two-boundary constraint:

1. *"Foundational entity structures must be consolidated prior to Argument Component Extraction."*
2. *"Theory-level argument alignment and clustering evaluate the explicitly extracted Layer 3 theory arguments
   post-extraction."*

## Decision

The pipeline execution flow in `Pipeline.for_task()` orchestrates 7 sequential runners:

```
Phase 1 → Phase 2 → Phase 3 → [Phase 3b] → [Phase 4 Maturation] → Phase 4 → [Phase 5b]
```

**Phase 3b: Latent Graph Consolidation** (before Phase 4):

- Runs `LatentGraphConsolidation` — non-generative, fast mathematical sweep over dense vector embeddings combined with
  Jaccard overlap of 1-hop relation signatures.
- Input: `Phase3ArtifactsView`; output: `Canonicalization` artifacts.
- Result: Knowledge Graph L2 entity duplicates are unified into canonical nodes before argument components are
  extracted.

**Phase 4 Entity Maturation** (before Phase 4 Argument Mining):

- Synthesizes canonical descriptions and resolves entity-level epistemic drift from accumulated empirical envelopes.

**Phase 5b: Theory Fusion & Argument Clustering** (after Phase 4):

- Runs `EmbeddingArgumentClustering` — groups semantically equivalent L3 argument components.
- Runs `TheoryFusion` / `LeidenTheoryClustering` if enabled.
- Input: `Phase4ArtifactsView`; output: Phase 5b fusion-decision artifacts.

## Alternatives considered

- **LLM-based Phase 5a before Phase 4** — replaced by Phase 3b non-generative mathematical sweep, which avoids redundant
  LLM calls and achieves faster, deterministic topological consolidation over dense vectors and 1-hop relation edges.
- **Single fusion pass at the very end** — simpler DAG, but argument mining on an un-consolidated KG produces
  structurally inconsistent argument graphs. Rejected on correctness grounds.
- **Entity fusion inside Phase 2** — would require the full KG to be built first, which contradicts Phase 2's
  incremental per-chunk model. Phase 3b is the correct position for post-Phase 3 global operations.

## Consequences

- `Pipeline.for_task()` executes 7 sequential runners: `Phase1Runner`, `Phase2Runner`, `Phase3Runner`,
  `Phase3bLatentConsolidationRunner`, `Phase4EntityMaturationRunner`, `Phase4Runner`, `Phase5ArgumentWebRunner`.
- Pre-Phase 4 consolidation emits `Canonicalization` artifacts that update entity identities in the graph store before
  Phase 4 executes.
- `Phase5ArgumentWebRunner` handles post-Phase 4 argument clustering and structural correspondence.

## Related

- `pipeline/pipeline.py` — `Pipeline.for_task()`
- `pipeline/phases/phase3b_consolidation/` — `Phase3bLatentConsolidationRunner`
- `../../pipeline/phases/phase5_fusion/argument_web.py` — `Phase5ArgumentWebRunner`
- `docs/workflow/3b_consolidation/index.md` — Phase 3b Latent Graph Consolidation
- `docs/concepts/dense_alignment.md` — Epistemic Grounding and Dense Alignment
- ADR 0003 — Coreference resolution absorbed into Phase 3b

