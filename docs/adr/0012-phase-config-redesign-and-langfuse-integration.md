# [0012] Phase Configuration Redesign, Staged Epistemic Pipeline Flow, and Langfuse Governance

Status: Accepted (2026-09-07)

## Context

The construction of theory graphs from scientific texts is governed by [`pipeline/config.py`](../../pipeline/config.py), which defines granular hyperparameters, model stacks, decoding strategies, structured prompt templates, and execution/caching policies across eight sequential phases:
- Phase 1: Data Foundation
- Phase 2: Entity & Local Relation Discovery
- Phase 3: Global Relation Extraction
- Phase 3b: Latent Graph Consolidation
- Phase 4: Entity Maturation (Batch Epistemic Synthesis)
- Phase 4: Argument Mining
- Phase 5: Inter-Document Argument Web & Fusion
- Phase 6: Epistemic Consolidation

Prior to this decision, `packages/episteme-studio` had several significant deficiencies:
1. **Unrepresented Pipeline Options**: `ConfigEditor.tsx` only exposed six hardcoded parameters. Key controls such as gleaning cycles, Jaccard overlap thresholds, decoding strategies (`direct_constrained`, `nl_to_format`), random seeds, chunk overlap, and theory fusion were inaccessible.
2. **Blind Execution UX**: Clicking "Run Pipeline" in `AppShell.tsx` immediately launched a background demo run with no pre-flight inspection of active settings, corpus input selection, or cache impact.
3. **Fragmented Prompt Governance**: While the core library supports `LangfusePromptProvider` with versioning, labels, and local fallbacks, the Studio provided no way to inspect or switch between built-in default prompts and Langfuse-managed prompts.
4. **Subprocess Deserialization Mismatch**: In `run_service.py`, patch overrides containing dot-notation paths (e.g. `phase3.global_relation_confidence_threshold`) were forwarded directly to the worker process without unflattening, causing Pydantic validation failures in real pipeline executions.

## Decision

We implement a cohesive **Epistemic Experiment Staging Workbench** across `Episteme_studio` and `packages/episteme-studio/frontend`:

### 1. Purpose-Built Staged DAG Pipeline Flow Strip (Rejection of React Flow)
- We explicitly reject introducing `@xyflow/react` (`react-flow`) or generic node-graph canvas libraries.
- **Rationale**: In Episteme, the phase topology is a strict, staged epistemic progression ($L1 \to L2 \to L3 \to L4$). Artifacts flow through strictly typed `ArtifactCollection` containers. An unconstrained canvas with arbitrary draggable wires provides false affordances while adding ~120KB+ bundle weight and canvas gesture collisions with the existing `@antv/g6` explorer.
- Instead, we implement a lightweight, responsive SVG/CSS **Staged Epistemic Pipeline DAG Strip** displaying the 8 phases with real-time invalidation aura badges (`🟢 Reused` vs `🟠 Re-executing`), modification counters, conditional phase toggles, and direct master-detail selection.

### 2. Unified Staging & Execution Navigation
- Clicking "Run Pipeline" in the top navigation header transitions the user directly to the **Phase Config / Staging Workbench** with an active staging state.
- The workbench integrates corpus document selection, profile presets, prompt resolution, and live invalidation previews, culminating in a prominent "Launch Pipeline Run" action.

### 3. Eager Langfuse Prompt Management & Telemetry Governance
- We add prompt resolution capabilities (`POST /api/config/prompts/resolve`) backed by `LangfusePromptProvider` and `DefaultPromptProvider`.
- **Eager Resolution**: Prompt bundles (direct, reasoning, format, gleaning templates) and version tags are resolved before run execution and populated into `PipelineConfig`.
- **Fingerprinting & Invalidation**: Resolved prompt texts are hashed into phase fingerprints; switching prompt versions in Langfuse automatically triggers phase invalidation for only the affected pipeline phases.
- **Telemetry Hook**: When `LANGFUSE_PUBLIC_KEY` is present, the subprocess worker automatically registers `LangfuseObserver` and binds `run_observability_context(session_id=run_id, run_id=run_id)`.
- Studio links runs directly to Langfuse sessions (`${langfuse_host}/traces?search=${run_id}`).

### 4. Robust Configuration Unflattening & Validation
- `ConfigAdapter.apply_patch` safely unflatters dot-delimited paths into nested dictionaries, validating updates against the full `PipelineConfig` Pydantic model before starting subprocess execution.

## Alternatives Considered

- **React Flow (`@xyflow/react`)**: Rejected as heavyweight, redundant with AntV G6, and ill-suited for dense hyperparameter tuning on fixed-topology pipelines.
- **Modal-only configuration**: Rejected because researchers require high-density visual space to review prompts, thresholds, and invalidation cascades simultaneously.
- **Python-only Langfuse configuration**: Rejected because researchers using the GUI should not be locked out of managed prompt versioning or cost/trace telemetry.

## Consequences

- **Positive**:
  - Full transparency into all pipeline hyperparameters and cache invalidations before executing runs.
  - Seamless interoperability between Studio GUI staging and cluster execution via one-click CLI command export (`uv run python pipeline/pipeline.py --config ...`).
  - Native Langfuse prompt versioning and session tracking with zero-config offline fallback.
- **Negative / Trade-offs**:
  - Studio backend requires additional endpoint for prompt resolution.
