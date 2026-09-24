# [0014] Deterministic Identity Diffing and Progression Workbench

Status: Accepted (2026-09-08)

## Context

Researchers executing the Episteme knowledge graph pipeline regularly evaluate variations in model capability (e.g. compact open-source models like Llama 3 8B vs. frontier reasoning systems like Claude 3.5 Sonnet / o1), prompt template formulations, and hyperparameter thresholds (reranker cutoff, temperature, ACC decoding strategies). 

Because `L2Entity` identifiers (`entity_<14 hex>`), argument components (`ac_<14 hex>`), and `ArtifactEnvelope.identity_key`s are deterministically hashed from canonical linguistic representations and source chunk context (Decision D-18), pipeline runs over identical source documents exhibit 100% semantic identity stability. 

However, `episteme-studio` was previously architected around single-run inspection. Evaluating the progression or degeneration of results between two runs required tedious manual switching between run IDs, resulting in severe cognitive friction:
1. **Spatial Disorientation**: Independent force-directed layouts on separate canvases scramble $(x, y)$ node coordinates, destroying the researcher's mental map of the domain.
2. **Visual Clutter**: Overlaying two separate graphs with arbitrary color scales leads to visual overload ("rainbow explosion") on top of existing layer (L1/L2/L3) and partition (B/A) styles.
3. **Semantic Inversion Blindness**: Critical philosophical divergences—such as a claim relation changing from `SUPPORTS (+1)` to `REFUTES (-1)`—were easily lost in aggregate node/edge counts.

## Decision

Implement a **Deterministic Run-to-Run Diff Engine** and a **Low-Cognitive-Load Visual Workbench**:

1. **Union Ghost Layout (Tied Spatial Coordinates)**:
   - When diffing baseline Run A and candidate Run B, layout calculation is executed over the **union graph** $G_{\text{union}} = (V_A \cup V_B, E_A \cup E_B)$.
   - Every entity shared between the runs maintains the identical $(x, y)$ coordinate across views, preserving spatial landmarks in the researcher's memory.

2. **The "Diff Lens" 3-State Scrub & Blink Comparator**:
   - The canvas HUD provides a 3-state temporal scrubber: `[ Run A: Baseline ] ── [ Diff Lens ] ── [ Run B: Candidate ]`.
   - Researchers can activate **A/B Blink Mode** (via `Space`), rapidly alternating between Run A and Run B. This leverages the human visual cortex's innate motion-detection capabilities (the astronomical comparator technique) to spot additions, dropouts, and link modifications without cognitive color decoding.

3. **Multi-Tier Divergence Filtering**:
   - Rather than displaying all changes simultaneously, the canvas HUD provides high-salience divergence filters:
     - `All Changes`
     - `⚡ Polarity Inversions` (highlights contradictory claim relations)
     - `Gained Entities (+)` (new discoveries in Run B)
     - `Lost Entities (-)` (dropped entities/pruned hallucinations)
     - `Argument Drift (|Δρ| > threshold)` (Theory Atoms with significant epistemic acceptability divergence)

4. **Dedicated Polarity Inversion & Configuration Diff Drawers**:
   - Polarity contradictions ($polarity_A \times polarity_B < 0$) are surfaced with dual-tone stippled edges and a `⚡` glyph.
   - Clicking an inversion opens a side-by-side inspection modal showing source quotes, confidence scores, and relation types from both runs.
   - The **Config Delta Drawer** isolates parameter divergences (models, temperatures, prompts, thresholds) while filtering out the 90%+ identical settings.

5. **Clean Layered Architecture (D-01)**:
   - Wire contracts defined in `Episteme_studio.domain.diff` (`GraphDiffView`, `NodeDiffStatus`, `EdgeDiffStatus`, `PolarityInversion`, `ConfigDeltaItem`, `DiffKPIs`).
   - Pure service layer in `Episteme_studio.services.diff_service.DiffService` operating over `ArtifactReader`.
   - Endpoint: `GET /api/diff/runs?base_id={run_a}&target_id={run_b}`.

## Alternatives Considered

- **Dual Split-Screen Canvases**: Placing Run A on the left and Run B on the right. Rejected due to saccadic eye movement fatigue and divergent node positions from separate force layouts.
- **Color-Coded Overlap Overlay**: Using green/red/blue color tinting directly on standard node fills. Rejected because it directly clashes with L1/L2/L3 semantic layer coloring and community hulls.
- **Tabular Triple Diff Table**: Displaying added/removed relations purely in a table. Rejected because it destroys structural graph topology and path relationships.

## Consequences

- **Instant Progression Auditing**: Researchers can immediately verify if a frontier reasoning model gained critical intermediate argument steps or simply extracted redundant entities.
- **Direct Epistemic Alignment**: Contradictory model conclusions are surfaced in one click rather than remaining hidden in graph statistics.
- **Cognitive Clarity**: Spatial continuity and progressive disclosure prevent visual fatigue during detailed pipeline evaluations.

## Related

- [ADR 0011: Declarative Graph Metrics and QBAF Semantics](0011-declarative-graph-metrics-and-qbaf-semantics.md)
- [ADR 0010: Dual-Driver Graph Preview](0010-graph-preview-driver-selection-neo4j.md)
- [DECISIONS.md: D-18 Stable Identity Key Diffing](../../packages/episteme-studio/docs/DECISIONS.md)
