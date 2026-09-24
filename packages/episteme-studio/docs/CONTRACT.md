# Wire Contract

The interface between `glp_studio` (Python) and `frontend` (TypeScript). These models
live in `../src/glp_studio/domain` and **must not import from `pipeline.*` or
`epistemetrics.*`** — that translation is `adapters/`' job (D-01).

TypeScript types are generated, never hand-written:

```bash
openapi-typescript http://127.0.0.1:8000/openapi.json -o frontend/src/api/generated.d.ts
```

CI fails if regeneration produces a diff.

---

## 1. Conventions

- **Prefix** `/api`, unversioned (D-03).
- **Casing** `snake_case` on the wire, matching Python. Do not camelize.
- **Time** RFC 3339 UTC with `Z`.
- **Absent vs. zero** `null` means *unknown*. `0` means *measured as zero*. This
  distinction is load-bearing for `polarity`, `weight` and `plausibility` — never
  coalesce a null to a zero (D-12, D-15).
- **Unknown enum values must render.** Every open string field below is open on
  purpose; a value the client has not seen must degrade to neutral styling, never throw.

---

## 2. Graph

```python
class Layer(IntEnum):
    L1 = 1
    L2 = 2
    L3 = 3


class StudioNode(BaseModel):
    id: str                       # stable identity_key where available (D-18)
    layer: Layer
    type: str                     # OPEN. Schema-declared or not; never a closed enum.
    label: str
    partition: Literal["B", "A"] | None = None   # from schema.component_partitions; L3 only
    degree: int = 0
    plausibility: float | None = None            # tau. null = unknown, not 0.0
    confidence: float | None = None
    resolved: bool = True         # False -> referenced but never persisted (D-16)
    synthetic: bool = False       # True -> reified Inference node (D-21)
    props: dict[str, Any] = Field(default_factory=dict)


class StudioEdge(BaseModel):
    id: str
    source: str
    target: str
    target_kind: Literal["node", "edge"] = "node"   # reserved; see D-21
    type: str                     # OPEN. The raw predicate, e.g. "WIDERSPRICHT".
    layer: Layer
    polarity: int | None = None   # -1 | 0 | 1 from schema; null = UNMAPPED (D-15)
    weight: float | None = None   # phi. null = unknown, not 0.0
    confidence: float | None = None
    props: dict[str, Any] = Field(default_factory=dict)


class GraphView(BaseModel):
    nodes: list[StudioNode]
    edges: list[StudioEdge]
    source: Literal["artifacts", "neo4j", "fixture"]
    run_id: str | None = None
    graph_version: str            # cache + staleness key
    schema_version: str
    truncated: bool = False
    dropped_count: int = 0        # how many elements the budget excluded
    unmapped_predicates: dict[str, int] = Field(default_factory=dict)
    unresolved_count: int = 0
    layer_counts: dict[int, int] = Field(default_factory=dict)   # drives the L1/L2/L3 toggles
```

`truncated`/`dropped_count` are mandatory, not optional politeness. A view that silently
drops elements reads as complete and is worse than one that admits its budget.

`comboId` is deliberately absent — grouping is a G6 rendering concern the client derives
(D-09).

---

## 3. Runs

Mirrors `../../../pipeline/runs/models.py` without importing it.

```python
class RunStatus(StrEnum):
    PLANNED = "planned"; RUNNING = "running"; COMPLETED = "completed"
    FAILED = "failed"; ABORTED = "aborted"


class PhaseStatus(BaseModel):
    phase_name: str               # NOT unique — two phases are both "Phase 4" (D-22)
    phase_ordinal: int            # the React key
    status: RunStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    reused: bool = False
    artifact_count: int = 0


class RunSummary(BaseModel):
    run_id: str
    status: RunStatus
    created_at: datetime
    completed_at: datetime | None = None
    pipeline_version: str
    schema_version: str | None = None
    input_sources: list[str] = Field(default_factory=list)
    models: dict[str, str] = Field(default_factory=dict)   # from config_snapshot.models (D-14)
    artifact_count: int = 0
    size_bytes: int = 0
    tags: list[str] = Field(default_factory=list)
    parent_run_id: str | None = None


class RunDetail(RunSummary):
    phase_records: list[PhaseStatus]
    artifact_counts_by_kind: dict[str, int]
    graph_schema: dict[str, Any]        # the run's OWN schema — render against this
    config_snapshot: dict[str, Any]     # secrets already redacted
    fingerprints: dict[str, Any]
    unresolved_count: int = 0
    failure: ProblemDetail | None = None
```

The stepper renders from `phase_records` as returned. Never a compiled-in list of six
(D-22).

---

## 4. Events

```python
class StudioEvent(BaseModel):
    seq: int                      # monotonic per run; the SSE id
    run_id: str
    ts: datetime
    kind: str                     # OPEN. Mapped from get_event_type_name()
    level: Literal["debug", "info", "warning", "error"] = "info"
    phase: str | None = None
    message: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    dropped_before: int = 0       # events the bounded queue discarded before this one
```

`kind` is open: `../../../pipeline/events/models.py` defines ~28 event classes and will gain more.
`event_mapper` maps known names and passes unknown ones through as `kind` with the raw
payload — it must never 500 on an event class it has not seen (D-01).

`dropped_before` exists because the observer queue is bounded and drop-oldest: the
pipeline thread must never block on a slow browser. When it is non-zero, the console
shows a gap marker rather than pretending the stream was continuous.

---

## 5. Overlays

```python
class OverlayKind(StrEnum):
    GRADUAL_STRENGTH = "gradual_strength"       # rho, per theorynet_concept.md §4
    INTERNAL_CORRELATION = "internal_correlation"
    DEGREE = "degree"
    COMPONENT = "component"
    B_CONSISTENCY = "b_consistency"             # reserved -> 501 (D-12)
    STABLE_EXTENSION = "stable_extension"       # reserved -> 501 (D-12)


class Overlay(BaseModel):
    id: str
    kind: OverlayKind
    params: dict[str, Any] = Field(default_factory=dict)
    node_values: dict[str, float | str | None] = Field(default_factory=dict)
    edge_values: dict[str, float | str | None] = Field(default_factory=dict)
    scale: Literal["continuous", "categorical", "ordinal"] = "continuous"
    domain: list[float] | list[str] | None = None
    computed_at: datetime
    graph_version: str
    incomplete_inputs: int = 0    # nodes/edges skipped for null tau or phi
```

`incomplete_inputs` matters right now: τ and φ are null throughout the current data
(D-12), so `gradual_strength` over today's graphs would be computed from almost nothing.
The overlay must report that rather than present a confident-looking result.

Reserved kinds return `501 Not Implemented`; the UI greys them out rather than offering
a button that fails (ONTOLOGY §7).

---

## 6. Config

```python
class FieldProvenance(StrEnum):
    DEFAULT = "default"; ENV = "env"; PROFILE = "profile"; OVERRIDE = "override"


class ConfigView(BaseModel):
    values: dict[str, Any]                       # secrets redacted as "***"
    provenance: dict[str, FieldProvenance]       # dotted path -> where it came from
    profile_id: str | None = None
    schema_version: str


class ConfigPatch(BaseModel):
    profile_id: str | None = None
    patch: dict[str, Any] = Field(default_factory=dict)   # dotted paths


class InvalidationPreview(BaseModel):
    invalidated_phases: list[int]
    reused_phases: list[int]
    changed_fingerprints: dict[str, tuple[str | None, str | None]]
    reason: str
    estimated_artifact_loss: int
```

`InvalidationPreview` is the highest-value endpoint in the Studio: it answers *"what will
this config change cost me?"* before a run starts, using invalidation machinery that
already exists. Note that `_phase_config_fingerprints` hashes only per-phase sub-configs,
so a change to `config.models` correctly shows **no** invalidation (D-14).

---

## 7. Endpoints

| Method | Path | Returns | Milestone |
|---|---|---|---|
| `GET` | `/api/health` | liveness | M2 |
| `GET` | `/api/capabilities` | `{artifacts, neo4j, execution, overlays[]}` | M2 |
| `GET` | `/api/schema` | active `SchemaConfig` | M2 |
| `GET` | `/api/runs` | `list[RunSummary]`, paginated | M3 |
| `GET` | `/api/runs/{run_id}` | `RunDetail` | M3 |
| `GET` | `/api/runs/{run_id}/graph` | `GraphView` | M4 |
| `GET` | `/api/runs/{run_id}/artifacts` | `list[ArtifactRef]`, filter by kind | M4 |
| `GET` | `/api/runs/{run_id}/evidence/{node_id}` | provenance chain + chunk text + spans | M4 |
| `POST` | `/api/runs` | start a run → `RunSummary` | M5 |
| `POST` | `/api/runs/{run_id}/cancel` | `RunSummary` | M5 |
| `GET` | `/api/runs/{run_id}/events` | SSE `StudioEvent` stream | M5 |
| `GET` | `/api/graph/view` | `GraphView` from Neo4j | M6 |
| `GET` | `/api/graph/expand` | `GraphView` (k-hop from seeds) | M6 |
| `POST` | `/api/graph/cypher` | `CypherResult` | M6 |
| `GET` | `/api/overlays` | `list[Overlay]` (cached) | M7 |
| `POST` | `/api/overlays` | compute → `Overlay` | M7 |
| `GET` | `/api/metrics/definitions` | `list[MetricDescriptor]` | Metrics Framework |
| `POST` | `/api/metric-executions` | execute → `MetricResult` (200) or queued (202) | Metrics Framework |
| `GET` | `/api/metric-executions/{id}` | `ExecutionStatusResponse` | Metrics Framework |
| `DELETE` | `/api/metric-executions/{id}` | cancel → `{ "execution_id", "status": "cancelled" }` | Metrics Framework |
| `GET` | `/api/config/effective` | `ConfigView` | M7 |
| `GET` | `/api/config/profiles` | `list[str]` | M7 |
| `POST` | `/api/config/invalidation-preview` | `InvalidationPreview` | M7 |

`/api/capabilities` is what lets the frontend grey out the Cypher console when Neo4j is
absent, instead of erroring (D-04).

### SSE

`GET /api/runs/{run_id}/events` emits `id: {seq}` per event and honours `Last-Event-ID`
on reconnect, replaying from the per-run ring buffer. `?since={seq}` does the same for
an initial mount. `EventSource` cannot set headers, so when a token is required it goes
in the query string (D-23).

---

## 8. Errors

RFC 7807 `application/problem+json` for every non-2xx (D-24):

```python
class ProblemDetail(BaseModel):
    type: str        # stable slug, the machine-readable part
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)
```

| `type` | Status | When |
|---|---|---|
| `run-not-found` | 404 | Unknown `run_id` |
| `artifact-store-unavailable` | 503 | `artifacts_dir` missing or unreadable |
| `neo4j-unavailable` | 503 | No driver, or connection failed |
| `neo4j-read-only-violation` | 403 | Write attempted through the Cypher console |
| `query-timeout` | 504 | Transaction exceeded its budget |
| `result-too-large` | 413 | Row or node cap exceeded |
| `overlay-not-implemented` | 501 | Reserved `OverlayKind` |
| `run-already-active` | 409 | Concurrent start rejected |
| `invalid-config-patch` | 422 | Patch failed `PipelineConfig` validation |
| `frontend-not-built` | 503 | `static/index.html` absent — says to run `npm run build` |

`frontend-not-built` is a served page, not a crash at import (D-11).
