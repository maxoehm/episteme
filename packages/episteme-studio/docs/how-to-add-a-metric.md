# How to Add a Metric to GLP Studio

This guide explains how to implement, register, and visualize a new graph metric or community detection algorithm in `glp-studio`.

GLP Studio provides a declarative, dual-engine metrics architecture capable of running local sub-second evaluations, in-memory `igraph` computations, and distributed Neo4j Graph Data Science (GDS) procedures, rendered on an interactive AntV G6 canvas.

---

## 1. Metric Architecture Overview

Metrics in GLP Studio follow a modular pattern that bridges the frontend workbench with backend graph analytics:

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend UI                           │
│  - MetricsDrawer.tsx (dynamic JSON schema parameters)       │
│  - OverlaySwitcher.tsx (categorical / continuous switcher)  │
│  - GraphCanvas.tsx (AntV G6 states & Hull contours)         │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST / SSE
┌──────────────────────────────▼──────────────────────────────┐
│                    FastAPI Endpoints                        │
│  - GET  /api/metrics/definitions                            │
│  - POST /api/metric-executions (fast-path <= 250ms)         │
│  - GET  /api/metric-executions/{id} (async polling)         │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                      MetricService                          │
│  - Descriptor registry & live engine capability probing     │
│  - Fast-path execution & async task cancellation            │
└──────────────┬──────────────────────────────┬───────────────┘
               │ GDS                          │ In-Memory Fallback
┌──────────────▼──────────────┐┌──────────────▼───────────────┐
│        Neo4jReader          ││       metrics_adapter        │
│  - Ephemeral projection     ││  - igraph algorithms         │
│  - GDS stream execution     ││  - QBAF gradual semantics    │
│  - Guaranteed drop cleanup  ││  - Weakly connected comps    │
└─────────────────────────────┘└──────────────────────────────┘
```

### Key Concepts

- **Scope (`MetricScope`)**:
  - `single_node`: Evaluated upstream/downstream of a specific focus node (e.g., local gradual strength $\rho$).
  - `global`: Evaluated across the entire graph snapshot or Neo4j database (e.g., PageRank, Degree, Leiden clustering).
- **Execution Engine**:
  - `"gds"`: Uses Neo4j Graph Data Science procedures with ephemeral projections and fallback to `"igraph"`.
  - `"cypher"`: Runs custom Cypher path traversals against Neo4j.
  - `"igraph"` / `"python"`: In-memory calculations executed over `GraphView`.
- **Fast-Path Lifecycle**:
  Sub-250ms computations immediately return `200 OK` with the complete `MetricResult`. Computations exceeding 250ms return `202 Accepted` with an `execution_id` for background status polling and cooperative client cancellation.
- **Canvas Presentation**:
  Metrics can color nodes (`scale="continuous"` or `scale="categorical"`), draw causal paths on edges (`affected_edges`), or draw bounding hulls around clusters (`type: "hull"` in AntV G6).

---

## 2. Step-by-Step Implementation Guide

### Step 1: Define Overlay Kinds & Domain Models

If your metric can also be toggled as an epistemic or structural overlay, register its identifier in `glp_studio.domain.overlays.OverlayKind`:

```python
# packages/glp-studio/src/glp_studio/domain/overlays.py

class OverlayKind(StrEnum):
    GRADUAL_STRENGTH = "gradual_strength"
    INTERNAL_CORRELATION = "internal_correlation"
    DEGREE = "degree"
    COMPONENT = "component"
    PAGERANK = "pagerank"
    LEIDEN = "leiden"  # <-- Register new overlay kind
    B_CONSISTENCY = "b_consistency"
    STABLE_EXTENSION = "stable_extension"
```

Also update the frontend TypeScript definition in `packages/glp-studio/frontend/src/api/types.ts`:

```typescript
export type OverlayKind =
  | "gradual_strength"
  | "internal_correlation"
  | "degree"
  | "component"
  | "pagerank"
  | "leiden" // <-- Add here
  | "b_consistency"
  | "stable_extension";
```

---

### Step 2: Implement In-Memory / Fallback Adapter

In `glp_studio.adapters.metrics_adapter`, write a pure function accepting a `GraphView` snapshot and algorithmic parameters. All functions must include NumPy-style docstrings.

```python
# packages/glp-studio/src/glp_studio/adapters/metrics_adapter.py

def compute_leiden(
    graph: GraphView,
    params: dict[str, Any] | None = None,
) -> Overlay:
    """Compute Leiden community detection across the graph view using igraph.

    Partitions the graph nodes into disjoint communities maximizing modularity
    via the Leiden algorithm. Takes into account edge weights when present.

    Parameters
    ----------
    graph : GraphView
        The graph snapshot view to analyze.
    params : dict of str to Any, optional
        Optional algorithmic parameters:
        - gamma / resolution : float, default 1.0
        - max_levels / n_iterations : int, default 10
        - objective_function : str, default "modularity"

    Returns
    -------
    Overlay
        Computed Leiden community overlay with categorical scale.
    """
    opts = params or {}
    resolution = float(opts.get("gamma", opts.get("resolution", 1.0)))
    n_iterations = int(opts.get("max_levels", opts.get("n_iterations", 10)))
    objective = str(opts.get("objective_function", "modularity"))

    if not graph.nodes:
        return Overlay(
            id=f"overlay-leiden-{uuid4().hex[:8]}",
            kind=OverlayKind.LEIDEN,
            params={"gamma": resolution, "max_levels": n_iterations, **opts},
            node_values={},
            edge_values={},
            scale="categorical",
            domain=[],
            computed_at=datetime.now(timezone.utc),
            graph_version=graph.graph_version,
            incomplete_inputs=0,
        )

    g = ig.Graph(directed=False)
    g.add_vertices(len(graph.nodes))
    node_id_to_idx = {node.id: idx for idx, node in enumerate(graph.nodes)}
    g.vs["name"] = [node.id for node in graph.nodes]

    edges_to_add: list[tuple[int, int]] = []
    weights: list[float] = []
    for edge in graph.edges:
        src_idx = node_id_to_idx.get(edge.source)
        tgt_idx = node_id_to_idx.get(edge.target)
        if src_idx is not None and tgt_idx is not None:
            edges_to_add.append((src_idx, tgt_idx))
            w = float(edge.weight) if edge.weight is not None else 1.0
            weights.append(max(0.01, w))
    g.add_edges(edges_to_add)

    try:
        partition = g.community_leiden(
            objective_function=objective,
            weights=weights if weights else None,
            resolution=resolution,
            n_iterations=n_iterations,
        )
        membership = partition.membership
    except Exception as exc:
        logger.warning("igraph community_leiden failed, falling back to components: %s", exc)
        cl = g.connected_components()
        membership = cl.membership

    node_values: dict[str, float | str | None] = {
        node.id: str(membership[idx])
        for idx, node in enumerate(graph.nodes)
    }
    unique_communities = sorted(list({str(v) for v in node_values.values() if v is not None}))

    return Overlay(
        id=f"overlay-leiden-{uuid4().hex[:8]}",
        kind=OverlayKind.LEIDEN,
        params={"gamma": resolution, "max_levels": n_iterations, **opts},
        node_values=node_values,
        edge_values={},
        scale="categorical",
        domain=unique_communities,
        computed_at=datetime.now(timezone.utc),
        graph_version=graph.graph_version,
        incomplete_inputs=0,
    )
```

Register this adapter in `glp_studio.services.overlay_service.OverlayService`:

```python
# packages/glp-studio/src/glp_studio/services/overlay_service.py

self._plugins = {
    ...
    OverlayKind.LEIDEN: compute_leiden,
}
```

---

### Step 3: Implement Neo4j GDS Driver Execution

When executing against Neo4j, implement the GDS algorithm with an **ephemeral projection lifecycle** in `glp_studio.adapters.neo4j_reader.Neo4jReader`.

> [!IMPORTANT]
> GDS projections consume in-memory database resources. Always guarantee projection destruction in a `finally` block with `CALL gds.graph.drop('{proj_name}', false)`.

```python
# packages/glp-studio/src/glp_studio/adapters/neo4j_reader.py

async def run_gds_leiden(
    self,
    gamma: float = 1.0,
    theta: float = 0.01,
    tolerance: float = 1e-4,
    max_levels: int = 10,
    timeout: float = 60.0,
) -> tuple[dict[str, int | str], dict[str, Any]]:
    """Execute Leiden community detection using the Neo4j GDS library.

    Creates an ephemeral projection, streams Leiden community assignments,
    and guarantees projection cleanup in a finally block.
    """
    if self._driver is None:
        raise Neo4jUnavailableError("Neo4j driver is not configured.")

    has_gds = await self.check_gds_availability()
    if not has_gds:
        raise Neo4jUnavailableError("Neo4j GDS library is not installed or available.")

    proj_name = f"leiden-proj-{uuid4().hex[:8]}"

    try:
        # 1. Project ephemeral in-memory graph
        project_cypher = (
            f"CALL gds.graph.project.cypher('{proj_name}', "
            "'MATCH (n) RETURN id(n) AS id, labels(n) AS labels', "
            "'MATCH (s)-[r]->(t) RETURN id(s) AS source, id(t) AS target, coalesce(r.weight, 1.0) AS weight')"
        )
        await self.execute_cypher(project_cypher, timeout=timeout)

        # 2. Stream GDS algorithm output
        stream_cypher = (
            f"CALL gds.leiden.stream('{proj_name}', {{"
            f"  gamma: {gamma}, "
            f"  theta: {theta}, "
            f"  tolerance: {tolerance}, "
            f"  maxLevels: {max_levels}, "
            f"  relationshipWeightProperty: 'weight'"
            f"}}) "
            "YIELD nodeId, communityId "
            "RETURN coalesce(gds.util.asNode(nodeId).id, elementId(gds.util.asNode(nodeId))) AS id, communityId "
            "ORDER BY communityId ASC"
        )
        res = await self.execute_cypher(stream_cypher, limit=10000, timeout=timeout)

        communities: dict[str, int | str] = {}
        for row in res.rows:
            nid = row.get("id")
            comm_id = row.get("communityId")
            if nid is not None and comm_id is not None:
                communities[str(nid)] = comm_id

        unique_communities = set(communities.values())
        summary = {
            "community_count": len(unique_communities),
            "node_count": len(communities),
            "gamma": gamma,
            "theta": theta,
            "max_levels": max_levels,
            "engine": "gds",
        }
        return communities, summary

    finally:
        # 3. Always drop ephemeral projection in finally block
        try:
            drop_cypher = f"CALL gds.graph.drop('{proj_name}', false)"
            await self.execute_cypher(drop_cypher, timeout=10.0)
        except Exception as drop_err:
            logger.warning("Failed to drop GDS ephemeral projection %s: %s", proj_name, drop_err)
```

---

### Step 4: Register Descriptor and Execution Logic in MetricService

In `glp_studio.services.metric_service.MetricService`:

1. **Declare Descriptor in `list_descriptors()`**:
   Provide the JSON Schema for parameters so the frontend `MetricsDrawer` can dynamically generate form controls (sliders, input fields, defaults).

```python
MetricDescriptor(
    id="leiden_global",
    label="Global Leiden Community Detection",
    description=(
        "Partitions the graph into densely connected modular communities using the Leiden algorithm "
        "via Neo4j GDS, with seamless igraph fallback."
    ),
    scope=MetricScope.GLOBAL,
    available=has_gds,
    unavailable_reason=None if has_gds else "Neo4j GDS plugin is not installed in the active Neo4j instance.",
    engine="gds",
    param_schema={
        "type": "object",
        "properties": {
            "gamma": {
                "type": "number",
                "title": "Resolution (Gamma)",
                "description": "Resolution parameter controlling community granularity",
                "default": 1.0,
                "minimum": 0.01,
                "maximum": 10.0,
            },
            "theta": {
                "type": "number",
                "title": "Randomness (Theta)",
                "description": "Randomness parameter for the refinement phase",
                "default": 0.01,
                "minimum": 0.0,
                "maximum": 1.0,
            },
            "tolerance": {
                "type": "number",
                "title": "Tolerance",
                "description": "Convergence threshold delta",
                "default": 0.0001,
                "minimum": 0.00001,
                "maximum": 0.1,
            },
            "max_levels": {
                "type": "integer",
                "title": "Max Levels",
                "description": "Maximum number of hierarchical clustering levels",
                "default": 10,
                "minimum": 1,
                "maximum": 50,
            },
        },
    },
)
```

2. **Handle Execution with Fallback in `execute_metric()`**:
   Attempt the GDS execution first. If Neo4j is absent or errors out, fall back to `compute_leiden()` and append an informative warning:

```python
elif metric_id in ("leiden_global", "leiden"):
    gamma = float(opts.get("gamma", opts.get("resolution", 1.0)))
    theta = float(opts.get("theta", 0.01))
    tolerance = float(opts.get("tolerance", 1e-4))
    max_levels = int(opts.get("max_levels", opts.get("n_iterations", 10)))
    warnings = []

    gds_available = await self.probe_gds_available()
    if self._neo4j_reader is not None and gds_available:
        try:
            communities, summary = await self._neo4j_reader.run_gds_leiden(
                gamma=gamma, theta=theta, tolerance=tolerance, max_levels=max_levels
            )
            affected_nodes = {
                nid: AffectedNodeDetail(
                    roles=["cluster"],
                    net_contribution=None,
                    metadata={"community": str(comm_id), "cluster": str(comm_id)},
                )
                for nid, comm_id in communities.items()
            }
            return MetricResult(
                execution_id=exec_id,
                metric_id=metric_id,
                scope=MetricScope.GLOBAL,
                result_value=summary.get("community_count", len(set(communities.values()))),
                graph_revision=graph_view.graph_version,
                duration_ms=max(1, int((datetime.now(timezone.utc) - start).total_seconds() * 1000)),
                summary=summary,
                affected_nodes=affected_nodes,
                affected_edges=[],
                warnings=warnings,
                computed_at=datetime.now(timezone.utc),
            )
        except Exception as exc:
            logger.warning("GDS Leiden execution failed, falling back to igraph: %s", exc)
            warnings.append("Executed via in-memory igraph fallback (GDS execution error)")

    # Fallback to in-memory igraph
    overlay = compute_leiden(graph_view, params={"gamma": gamma, "max_levels": max_levels, **opts})
    ...
```

---

### Step 5: Visualizing Clusters with AntV G6 "Hull"

AntV G6 includes a built-in `hull` extension that renders convex or smooth polygon contours around groups of nodes.

In `packages/glp-studio/frontend/src/graph/GraphCanvas.tsx`:

1. **Extract cluster groups from `activeMetricResult` or `activeOverlay`**:
```typescript
const clusters: Record<string, string[]> = {};
for (const [nodeId, detail] of Object.entries(activeMetricResult.affected_nodes)) {
  const comm = detail.metadata?.community ?? detail.metadata?.cluster;
  if (comm !== undefined && comm !== null) {
    const key = String(comm);
    if (!clusters[key]) clusters[key] = [];
    clusters[key].push(nodeId);
  }
}
```

2. **Configure G6 Hull Plugins**:
Instantiate a `hull` plugin entry for each community using a categorical color palette:

```typescript
const hullPlugins = Object.entries(clusters)
  .map(([commKey, members], idx) => {
    const validMembers = members.filter((id) => renderedNodeIds.has(id));
    if (validMembers.length === 0) return null;
    const palette = HULL_PALETTE[idx % HULL_PALETTE.length];
    return {
      key: `hull-${commKey}`,
      type: "hull",
      members: validMembers,
      padding: 18,
      corner: "smooth",
      fill: palette.fill,
      stroke: palette.stroke,
      fillOpacity: isDark ? 0.18 : 0.12,
      strokeOpacity: 0.7,
      lineWidth: 2,
      labelText: `Community ${commKey} (${validMembers.length})`,
      labelFill: isDark ? "#f1f5f9" : "#1e293b",
      labelFontSize: 11,
      labelBackground: true,
      labelBackgroundFill: isDark ? "#0f172a" : "#ffffff",
      labelBackgroundOpacity: 0.8,
      labelBackgroundPadding: [2, 6],
    };
  })
  .filter(Boolean);

// Update plugins and trigger render
graph.setPlugins(hullPlugins);
graph.render().catch(() => {});
```

3. **Cleanup**:
When clearing the metric or switching overlays, call `graph.setPlugins([])` and `graph.render()` to remove all hull contours from the canvas.

---

### Step 6: Testing Your Metric

Ensure full automated test coverage for your new metric:
1. **Unit tests for the in-memory adapter**: Test on sample/empty graphs in `packages/glp-studio/tests/test_<metric>_metric.py`.
2. **Mock GDS tests**: Verify ephemeral projection creation and guaranteed drop in `finally`.
3. **Fallback tests**: Verify that missing GDS automatically falls back with transparent warnings.
4. **Fast-path & REST API tests**: Verify `POST /api/metric-executions` succeeds with `200 OK`.

Run tests:
```bash
uv run pytest packages/glp-studio/tests/test_leiden_metric.py -v
```

Rebuild frontend assets:
```bash
cd packages/glp-studio/frontend && npm run build
```

---

## 3. Grounding & Theoretical References

- **Leiden Community Algorithm**:
  Traag, V. A., Waltman, L., & van Eck, N. J. (2019). *From Louvain to Leiden: guaranteeing well-connected communities*. Scientific Reports, 9(1), 5233. [doi:10.1038/s41598-019-41695-z](https://doi.org/10.1038/s41598-019-41695-z)
- **Quantitative Bipolar Argumentation Frameworks (QBAF)**:
  Cayrol, C., & Lagasquie-Schiex, M.-C. (2005). *Gradual valuation in argumentation frameworks*. In European Conference on Symbolic and Quantitative Approaches to Reasoning with Uncertainty (ECSQARU), pp. 480-491.
- **GLP Studio ADR 0011**:
  *Declarative Graph Metrics Framework, Async Lifecycles, and Gradual Strength Semantics* (`docs/adr/0011-declarative-graph-metrics-and-qbaf-semantics.md`).
