# Langfuse Integration

Langfuse observability is optional and decoupled via the event system: it is **not injected by default**.

When injected, telemetry flows through two coordinated pathways:

1. **Run-level root span and session grouping** via `run_observability_context`, which bundles all nested phase spans,
   component traces, and LLM generations into a searchable session in the Langfuse dashboard.
2. **Event-level observations** via `LangfuseObserver`, which translates domain events into spans, LLM completions into
   native **generations** (with full prompt, response, latency, and token metrics), and evaluation metrics into **scores**.

## Setup & Injection

To use Langfuse:

1. **Configure credentials**: Set `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and optionally `LANGFUSE_HOST` in your environment or `.env` file.
2. **Inject the observer**: Instantiate `LangfuseObserver` and register it on your `EventEmitter` (such as `SimpleEventEmitter`). If Langfuse is not needed, simply omit this step.
3. **Wrap in root context (optional)**: Wrap the pipeline execution in `run_observability_context` to correlate all traces under a unified root span and session ID.

```python
import os
from pipeline import Pipeline
from pipeline.events import SimpleEventEmitter, LangfuseObserver
from pipeline.runs.observability import run_observability_context

# 1. Instantiate the event emitter and inject LangfuseObserver
emitter = SimpleEventEmitter()

try:
    langfuse_observer = LangfuseObserver()
    emitter.register_observer(langfuse_observer)
except RuntimeError:
    # Safely skipped if the optional langfuse package is not installed
    pass

# 2. Optionally wrap execution to bind root session and trace context
with run_observability_context(
        name="pipeline.run",
        session_id="experiment-kg-01",  # Groups traces into a searchable session
        run_id="run-123",  # Correlates trace and events
        version="0.1.0",
        tags=["dataset:scierc", "mode:production"],
):
    pipeline = Pipeline(config=config, event_emitter=emitter)
    # execute pipeline...
```

## Observation Mapping

`LangfuseObserver` listens for events emitted across the pipeline lifecycle and maps them to corresponding Langfuse observation primitives:

### Pipeline Lifecycle & Components

| Pipeline Event | Observation Type | Observation Name | Captured Fields & Metadata |
|:---|:---|:---|:---|
| `ComponentStarted` | `span` | `component.<name>` | Component name, input description |
| `ComponentCompleted` | `span` | `component.<name>` | Execution duration (`duration_seconds`), success status, output description |
| `PhaseCompleted` | `span` | `phase.<name>` | Artifact count, duration (`duration_seconds`), success status, error message |

### LLM & Embedding Generations

| Pipeline Event | Observation Type | Observation Name | Captured Fields & Metadata |
|:---|:---|:---|:---|
| `LLMGenerationCompleted` | `generation` | `llm.<operation>` | Model name, model parameters, prompt input, JSON/text completion output, token usage (`prompt_tokens`, `completion_tokens`, `total_tokens`), latency, cache status, prompt metadata (`prompt_name`, `prompt_version`, `prompt_label`) |
| `EmbeddingGenerationCompleted` | `generation` | `embed.<operation>` | Model name, batch size (`text_count`), total characters, token usage (`prompt_tokens`, `total_tokens`), vector dimension (`vector_dim`), latency, cache status |
| `LLMDurationMeasured` | `generation` | `llm.<operation>` | Fallback latency measurement if detailed generation event is unavailable |

### Phase Domain Spans

| Pipeline Event | Phase | Observation Type | Observation Name | Captured Fields & Metadata |
|:---|:---|:---|:---|:---|
| `ChunksGenerated` | Phase 1 (Chunking) | `span` | `phase1.chunking` | `document_id`, `document_title`, `chunk_count`, `token_count` |
| `EntityLinkingCandidatesRetrieved` | Phase 2 (Linking) | `span` | `phase2.linking.candidates` | `mention_id`, `mention_name`, `candidate_count`, top candidate list |
| `EntityLinkingReranked` | Phase 2 (Linking) | `span` | `phase2.linking.rerank` | `mention_id`, `mention_name`, `candidate_id`, `candidate_name`, cross-encoder `score`, `accepted` flag, `threshold` |
| `DenseCandidatesGenerated` | Phase 3 (Dense Extract) | `span` | `phase3.dense.candidates` | `entities_count`, `candidate_count`, top candidate pairs |
| `RerankerScoreAssigned` | Phase 3 (Dense Extract) | `span` | `phase3.dense.rerank` | `candidate_pair`, `entity_a`, `entity_b`, payloads, reranker `score`, `accepted` flag, `threshold`, recovery attempts |
| `LLMRelationDecoded` | Phase 3 (Dense Extract) | `span` | `phase3.dense.llm_extract` | `candidate_pair`, extracted `relation`, `direction`, extraction `confidence` |
| `EntityMaturationSynthesized` | Phase 4 (Maturation) | `span` | `phase4.maturation.synthesize` | `entity_id`, `entity_name`, `envelope_count`, `top_k_used`, `synthesized_description` |
| `FusionDecisionMade` | Phase 5 (Fusion) | `span` | `phase5.fusion.decision` | `entities_fused`, `fusion_type`, `confidence`, decision `reason` / rationale |

### Evaluation & Metrics

| Pipeline Event | Observation Type | Observation Name | Captured Fields & Metadata |
|:---|:---|:---|:---|
| `EvaluationScoreLogged` | `score` + `span` | `eval.score.<metric_name>` | Langfuse numeric score (`metric_name`, `value`, `comment`), span with `target_id`, `metric_name`, `score`, and `comment` |
| `EvaluationCompleted` | `score`(s) + `span` | `evaluation.<evaluation_id>` | Langfuse numeric scores for each evaluation metric, summary span with `evaluation_id`, metrics dictionary, and `outcome` |

## Session Bundling & Run Searchability

To bundle an entire multi-phase execution into a single, cohesive, searchable session in Langfuse:

1. Specify or generate a `session_id` (defaults to `run_id` if omitted).
2. All child spans, retrieval observations, and LLM generations automatically inherit the active trace ID and
   `session_id`.
3. In the Langfuse Dashboard under **Sessions**, search by `session_id` to inspect the total token consumption,
   aggregated costs, and end-to-end latency across all pipeline phases.

## Disk Cache Observability

When `DiskCachedStructuredLLM` serves a prediction from local cache:

- An `LLMGenerationCompleted` event is emitted with `cached=True` and `prompt_tokens=0, completion_tokens=0`.
- Langfuse records a generation with 0 billable tokens and <1ms latency, enabling direct visualization of cache hit
  rates and monetary cost savings in the dashboard.

## Prompt Management with Langfuse

Episteme supports managing and versioning prompt bundles in Langfuse via `LangfusePromptProvider`.

```python
from pipeline.prompts import LangfusePromptProvider
from pipeline.config import PipelineConfig

# 1. Initialize prompt provider (with automatic fallback to local defaults)
prompt_provider = LangfusePromptProvider()

# 2. Populate PipelineConfig with managed prompts by label (e.g. 'production')
config = PipelineConfig()
config = prompt_provider.populate_config(config, label_or_version="production")

# Or fetch specific bundles:
ner_bundle = prompt_provider.get_bundle("ner_extraction", label_or_version="production")
```

### Prompt Lifecycle & Reproducibility

- **Eager Resolution**: Prompts and their version metadata are fetched before the pipeline run starts and populated into
  `PipelineConfig`.
- **Run Manifests & Fingerprints**: Run manifests capture the prompt text, version, and name in method fingerprints.
  Updating a prompt version in Langfuse invalidates only the affected pipeline phase.
- **Trace Linking**: When generating structured predictions, `LangfuseObserver` records the `prompt_name`,
  `prompt_version`, and `prompt_label` on the Langfuse generation observation.

## Operational Notes

- Spans and generations are automatically closed and updated.
- Observability is non-blocking and strictly best-effort: network or logging failures will never disrupt pipeline
  execution.
- Sensitive or large fields (e.g. oversized candidate lists) are truncated to keep dashboard views clean and performant.
