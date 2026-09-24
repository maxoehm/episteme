# glp-studio — Architecture Specification

Read in this order: `DECISIONS.md` → this file → `CONTRACT.md` → `ONTOLOGY.md` → `MILESTONES.md`.

---

## 1. What this is

> A **run-oriented workbench** over an artifact-producing, fingerprint-invalidated batch
> pipeline. The graph is one view among several — not the product.

The framing matters because it contradicts the obvious one. `glp-studio` is not a Neo4j
browser. `ExecutionConfig.project_artifacts_to_graph` defaults to `False`, so Neo4j holds
an *optional projection* of a system of record that lives on disk in
`../../../.pipeline_artifacts`. A Neo4j-first tool would show an empty canvas on a machine with
117 runs of results already on it.

For the first release the Studio is scoped as a **diagnostic instrument** (D-17): inspect
and debug what the pipeline produced. That is the honest framing of the current data —
zero theory atoms persisted, argumentative weights null throughout — and it turns the
defect into the value proposition. A provenance-and-artifact inspector is exactly the
tool for finding out why Phase 4 emits no atoms.

### Read and write model

| | Source | Availability | Authority |
|---|---|---|---|
| Run / artifact store | `../../../.pipeline_runs`, `../../../.pipeline_artifacts` | always, offline | **authoritative**, per-run, immutable |
| Neo4j | bolt | only when projection is on | derived, cross-run, queryable |
| epistemetrics | computed | on demand | derived overlays |
| *write* | `POST /api/runs` | — | the only mutation |

### Dependency direction

```
glp_studio ──► pipeline
           └─► epistemetrics
```

Strictly one-way. The pipeline never learns the Studio exists, and requires **no changes**
to be observed — `EventObserver` is already a Protocol.

---

## 2. Package layout

```
packages/glp-studio/
├── DECISIONS.md · SPEC.md · CONTRACT.md · ONTOLOGY.md · MILESTONES.md · README.md
├── pyproject.toml           # glp-studio; workspace deps grund-glp + epistemetrics
│                            #   [project.scripts] glp-studio = "glp_studio.__main__:main"
│                            #   hatch build hook: vite build -> src/glp_studio/static/
├── archive/                 # superseded planning docs — provenance only
├── src/glp_studio/
│   ├── __main__.py          # CLI: serve --host --port --env-file --profile --demo
│   ├── settings.py          # StudioSettings(BaseSettings) — the ONLY os.environ reader
│   ├── app.py               # FastAPI factory: routers, static mount, SPA fallback
│   ├── lifespan.py          # AsyncDriver, RunRegistry, ArtifactReader — one each
│   │
│   ├── domain/              # the wire contract. MUST NOT import pipeline.* (D-01)
│   │   ├── graph.py         #   GraphView, StudioNode, StudioEdge, Layer
│   │   ├── runs.py          #   RunSummary, RunDetail, PhaseStatus
│   │   ├── events.py        #   StudioEvent
│   │   ├── overlays.py      #   Overlay, OverlayKind
│   │   ├── config.py        #   ConfigView, ConfigPatch, InvalidationPreview
│   │   └── errors.py        #   ProblemDetail
│   │
│   ├── adapters/            # anti-corruption layer — the ONLY pipeline.* importers
│   │   ├── artifact_reader.py   # .pipeline_runs / .pipeline_artifacts -> domain
│   │   ├── neo4j_reader.py      # async read-only Cypher -> GraphView
│   │   ├── schema_mapper.py     # SchemaConfig -> polarity/partition resolution
│   │   ├── config_mapper.py     # PipelineConfig <-> ConfigView, fingerprint diffing
│   │   ├── event_mapper.py      # PipelineEvent -> StudioEvent
│   │   └── metrics_adapter.py   # epistemetrics -> Overlay
│   │
│   ├── runtime/             # execution & streaming
│   │   ├── observer.py      #   StudioEventObserver — enqueue only, never IO
│   │   ├── broker.py        #   per-run ring buffer, seq, SSE fan-out, replay
│   │   ├── executor.py      #   subprocess launch, IPC bridge, cancellation
│   │   └── registry.py      #   RunHandle lifecycle
│   │
│   ├── services/            # orchestration; no FastAPI imports -> unit-testable
│   │   ├── graph_service.py     # seed -> subgraph -> expand, node budget
│   │   ├── run_service.py
│   │   ├── overlay_service.py   # cache on (graph_version, kind, params)
│   │   └── config_service.py    # profiles, patch validation, invalidation preview
│   │
│   ├── api/
│   │   ├── deps.py · errors.py
│   │   ├── system.py        #   /api/health, /api/capabilities, /api/schema
│   │   ├── runs.py · stream.py · graph.py · overlays.py · config.py
│   │
│   ├── security.py          # loopback default, token guard, read-only Cypher
│   ├── fixtures/            # demo run — FE develops with no Neo4j and no LLM
│   └── static/              # vite output; gitignored; shipped in the wheel
│
├── frontend/                # JS package. NOT an npm workspace root (D-02)
│   ├── package.json · vite.config.ts · tsconfig.json
│   └── src/
│       ├── api/             #   generated.d.ts, client.ts, sse.ts
│       ├── store/           #   zustand slices: selection, view, runs, overlays
│       ├── graph/           #   GraphCanvas.tsx (G6 ref wrapper), styles, layouts
│       ├── panels/          #   Inspector, Evidence, Overlays, RunTimeline, ConfigEditor
│       ├── console/         #   Cypher editor + virtualized LogStream
│       └── shell/           #   AppShell, resizable panels, command palette
└── tests/
```

**The `adapters/` rule is the load-bearing one.** Only that directory may import
`pipeline.*` or `epistemetrics.*`. With the ontology under active revision and the
relation vocabulary unstable (D-15), routers importing `pipeline.contracts.domain`
directly would propagate every ontology change into the HTTP API and on into TypeScript.

---

## 3. Configuration

Three planes, with a rule for each.

| Plane | Contents | Source | Fingerprinted | Studio may edit |
|---|---|---|---|---|
| **Environment** | `HF_TOKEN`, `LITELLM_API_KEY`, `LITELLM_API_BASE`, `NEO4J_*`, `LANGFUSE_*`, `OLLAMA_HOST` | `.env` / process env | no | no — shown redacted |
| **Run config** | `PipelineConfig`: thresholds, prompts, schema, decoding, **models** | JSON profile + patch | yes | yes → new run |
| **Studio config** | host, port, node budget, query timeout, flags | `GLP_STUDIO_*` | no | yes, session-local |

### Rules

- **`StudioSettings(BaseSettings)` with `env_prefix="GLP_STUDIO_"` is the only place in
  `glp_studio` that touches `os.environ`.** No scattered `os.getenv`.
- Precedence: CLI flag → process env → `--env-file` → repo-root `.env`. Documented, and
  surfaced per-field in the UI.
- **The Studio never resolves `LLM_MODEL` itself.** It calls `PipelineConfig.from_env()`,
  the same resolver the CLI and example scripts use. One path, or you get "works in
  `../../../examples/pipeline_full_run.py`, fails in the Studio".
- `GET /api/config/effective` returns the resolved config with **per-field provenance**
  (`default | env | profile | override`), secrets redacted. "Why did this run use that
  model?" answered in one click.
- Profiles are `configs/*.json` via `config.model_dump_json()`. `POST /api/runs` takes
  `{profile_id, patch}`.
- `POST /api/config/invalidation-preview` reports which phases a patch would invalidate
  **before** the run starts, using machinery that already exists. Highest value per line
  of code in the whole Studio.

### `ModelConfig` (implemented — D-14)

`../../../pipeline/config.py` now carries a `models: ModelConfig` block: `llm_model`,
`embedding_model`, `reranker_model`, `temperature`, `seed`, `llm_api_base`, plus
`ModelConfig.from_env()` and `PipelineConfig.from_env()`. `default_embedding_model` and
`default_reranker_model` survive as deprecated read-only properties for the three
in-tree callers.

It is **not** folded into `phase_config_fingerprints` — model identity already reaches
invalidation through `fingerprint_method`, and folding it in would invalidate all 117
existing runs for no added coverage. See D-14 for the full rationale, including a
correction to an earlier claim in the archived analysis.

---

## 4. The four integration seams

### Events — zero pipeline changes

`StudioEventObserver` implements the existing `EventObserver` Protocol and registers
alongside the progress and Langfuse observers. `ContextualEventEmitter` already injects
`run_id` and `phase`; reuse it.

**The critical constraint:** `SimpleEventEmitter.emit()` is synchronous and calls
`observer.on_event(event)` inline on the pipeline thread. `on_event` must therefore do
nothing but `serialize_event()` and a non-blocking put onto a bounded queue — drop-oldest,
carrying a `dropped_before` count so the console can show a gap marker honestly. Any IO
there stalls the pipeline.

`event_mapper` maps `get_event_type_name(e)` to a stable `kind` and passes unknown types
through generically. There are ~28 event classes today and there will be more; an
unrecognised one must never 500.

### Execution — subprocess (D-05)

`nest_asyncio` is a project dependency and patching uvicorn's loop is corrupting; torch
holds the GIL and memory; cancellation needs a process boundary; a pipeline crash must
not kill the server. Events return over a `multiprocessing.Queue` with the same observer
protocol on the child side.

`RunRegistry` tracks `queued | running | failed | succeeded`, and a failed run must expose
its traceback through the API — pipelines with LLM calls fail routinely, and a stepper
that just stops is useless.

### Graph reads — artifacts first (D-04)

`ArtifactReader` reads `.pipeline_runs/run-<uuid>.json` manifests and
`.pipeline_artifacts/run-<uuid>/artifact::<identity_key>.json` envelopes. Works offline,
today, over existing data.

Two behaviours are mandatory from the start:

- **Render each run under its own schema.** `RunDetail.graph_schema` comes from that run's
  `config_snapshot.graph_schema`, never from the current `DEFAULT_SCHEMA` (D-13).
- **Materialise placeholders for dangling references.** 72 argument-relations point at
  components that were never persisted; surfacing them is the point (D-16).

`Neo4jReader` is added at M6 and gated by `/api/capabilities` so the frontend greys out
the Cypher console rather than erroring.

Every `GraphView` carries `source`, `run_id` and `graph_version` so overlays cache
correctly and stale views are detectable.

### Metrics — overlays (D-08)

`metrics_adapter` wraps `epistemetrics` and returns `Overlay` objects cached on
`(graph_version, kind, params)`.

Scope warning: `epistemetrics` currently exports exactly two functions
(`internal_correlation`, `neo4j_result_to_igraph`). The overlay registry is a plugin table
of `OverlayKind → callable`; unimplemented kinds return `501` and the UI greys them out.

---

## 5. Frontend

### State boundary

G6 owns graph data and layout positions. Zustand owns **selection and view configuration
only** — never a mirror of node data. Subscribe with selectors; use
`subscribeWithSelector` plus imperative `store.subscribe` to push into G6 rather than
re-rendering React around a heavy canvas.

### Rendering rules

- **No hardcoded type names** (D-13). All styling derives from the schema fetched at
  runtime. Unknown types render neutral and labelled, never throw.
- **`polarity: null` ≠ `polarity: 0`.** Unknown renders as grey dashed; neutral as grey
  solid. Conflating them would present an unmapped attack relation as harmless (D-15).
- **Null weight is a visual state**, not zero (D-12).
- **Per-layer toggles** in explore mode — L1/L2/L3 independently, each with its count.
  L1 defaults off on cardinality grounds only (D-20).
- **Dagre only for acyclic projections.** Argument graphs are cyclic by construction —
  that is the point of the formalism. Dagre silently breaks cycles. Use force or
  `combo-combined` for the argument web; reserve dagre for the `DEDUCES` subgraph.
- **G6 v5 API**: `graph.setElementState(id, states)`, `setData` / `updateNodeData`. The
  archived plan used the v4 `setItemState`, which does not exist in v5.
- **StrictMode double-mounts.** Guard the effect and call `graph.destroy()` on cleanup.
  Lazy-load G6; it is a large bundle.

### Reproducibility

This is a research instrument, so: view state (run, filters, layer toggles, overlay,
layout seed) is URL-encoded; positions persist per saved view keyed on `identity_key`
(D-18); export to SVG and GraphML alongside PNG. Force layouts are non-deterministic —
without a seed the same graph looks different on every load, which is unusable for a
figure in a paper.

### Stack

Vite + React + TypeScript, `@antv/g6` v5, zustand, TanStack Query/Table/Virtual,
`react-resizable-panels`, Tailwind + shadcn/ui, CodeMirror 6 with
`@neo4j-cypher/react-codemirror` (D-07), recharts for metric distributions.

Evaluate if it is worth it using shadcn.

**Regenerate `package.json` from the registry at scaffold time.** The archived manifest
was partly stale and partly unverified: `@xterm/*` must be dropped entirely (D-06);
`@tanstack/react-table ^9` sits oddly beside `@tanstack/react-virtual ^3`; and
`@tailwindcss/vite` plus the shadcn prerequisites (`class-variance-authority`, Radix,
`tailwindcss-animate`) were missing while both archived documents assumed shadcn.

---

## 6. Packaging and serving

`hatchling` with a build hook running `npm ci && npm run build` into
`../src/glp_studio/static`, resolved at runtime via
`importlib.resources.files("glp_studio") / "static"` — **never a CWD-relative path**.

Dev: `vite dev` on 5173 proxying `/api` to uvicorn:8000. Prod: single origin with an SPA
catch-all for non-`/api` paths — `StaticFiles(html=True)` alone 404s on deep links.

If `static/index.html` is missing, serve the `frontend-not-built` problem page telling the
user to run `npm run build`. Never crash at import.

Two repo-level gaps to close: the root `../../glp-pipeline/pyproject.toml` has no `[build-system]` and no
`[project.scripts]`, and pytest's `pythonpath` / `testpaths` need
`../src` and `../tests` added.

---

## 7. Security

Bind `127.0.0.1` by default; any non-loopback bind requires `GLP_STUDIO_TOKEN` or the
server refuses to start. Cypher runs through `session(default_access_mode=READ)` against
a read-only role where available, with a transaction timeout and a row cap — never
regex-blocking of `DELETE`. Secrets redacted in `/api/config/effective`. `EventSource`
cannot set headers, so the SSE token travels in the query string.

Unrelated housekeeping: `../../../examples/.env` and `../../../evaluation/.env` hold live credentials.
Confirm they are gitignored; rotate if ever committed.

---

## 8. Known constraints