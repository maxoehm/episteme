# [0011] Declarative Graph Metrics Framework, Async Lifecycles, and Gradual Strength Semantics

Status: Accepted (2026-09-07)

## Context

Theory graphs and epistemic argument structures (e.g., TheoryNet, Quantitative Bipolar Argumentation Frameworks / QBAF) require both local and global quantitative analysis to be interpretable by domain researchers. 

Previously, graph analytics in Episteme Studio were limited to synchronous node overlays (via `OverlayService`), with several key limitations:
1. **Lack of Causal Edge Explanations**: Argumentative influence flows along directed relations (supports, attacks, rebuttals). Visualizing metric values solely on nodes fails to convey *why* a claim has low or high epistemic strength, which edges transmitted support or attack, and their proportional contributions.
2. **Execution Latency Discrepancy & UX Blocking**: Local metric calculations on small neighborhoods execute in <10ms, while global structural metrics (such as PageRank across thousands of live Neo4j nodes) can take multiple seconds. Blocking the UI or timing out HTTP connections degrades the interactive research experience.
3. **Canvas State Collisions & Race Conditions**: Overwriting node and edge states on the AntV G6 canvas would wipe user selection (`selected`) and hover states. Furthermore, switching focus nodes rapidly or modifying parameter forms while background calculations were in flight could lead to stale asynchronous results overwriting newer queries.
4. **Accessibility (WCAG 2.1 AA Compliance)**: Relying strictly on red/green node colors to denote attack and support paths makes the graph unusable for users with color vision deficiencies.
5. **Infrastructure Heterogeneity**: Neo4j Graph Data Science (GDS) library is not guaranteed to be installed on every deployment, risking query failures when running heavy graph algorithms.

## Decision

We implement an end-to-end declarative metrics architecture across `Episteme_studio` and `packages/episteme-studio/frontend`:

### 1. Declarative Metric Registry & Parameter Schemas
- Defined `MetricDescriptor` with metadata, scope (`global` vs `single_node`), execution engine (`gds`, `python`), availability flags, and JSON Schema definitions for parameters.
- Exposed `GET /api/metrics/definitions` dynamically querying live engine availability (e.g., probing Neo4j for GDS procedures `gds.pageRank.stream`).

### 2. Hybrid Async Execution Lifecycle with Stale Protection
- `POST /api/metric-executions`: Fast-path heuristic executes calculations within a 250ms deadline.
  - Sub-250ms calculations return `200 OK` with the completed `MetricResult` payload immediately.
  - Computations exceeding 250ms return `202 Accepted` with an `execution_id` and polling endpoint `/api/metric-executions/{id}`.
  - Long-running tasks support cooperative cancellation via `DELETE /api/metric-executions/{id}`.
- Client-side Zustand store tracks monotonic `request_sequence` IDs and active `AbortController` handles. Stale responses from previous runs or focus nodes are discarded when newer requests resolve.

### 3. Local Gradual Strength Semantics (QBAF)
- Implemented bounded iterative semantics (`compute_local_gradual_strength`) over subgraphs upstream of a focus node.
- Cycles are prevented from locking by bounded convergence iterations with tolerance $\epsilon$.
- Pathway polarity analysis traces upstream influences and categorizes nodes and edges into `support`, `attack`, or `support + attack` (dual-influence).
- Computes marginal ablation impact $\Delta(u) = \rho(focus) - \rho_{-u}(focus)$ to measure the true causal contribution of each upstream claim.
- Returns detailed `affected_edges` and `affected_nodes` dictionaries.

### 4. Ephemeral Neo4j GDS Projections with Resilient Fallback
- `Neo4jReader.run_gds_pagerank` generates ephemeral in-memory graph projections with unique UUIDs (`pr-proj-<uuid>`).
- Guaranteed projection cleanup is enforced via Python `try ... finally` calling `gds.graph.drop(..., false)`.
- When GDS is unavailable or errors, execution seamlessly falls back to Python in-memory `igraph` PageRank, decorating the result with transparent provenance warnings.

### 5. Canvas Composite States and WCAG Multi-Channel Styling
- AntV G6 canvas utilizes composable states (`metric-focus`, `metric-affected`, `metric-role-support`, `metric-role-attack`, `metric-role-dual`, `metric-dimmed`) without mutating or clearing user `selected` states.
- Multi-channel visual differentiation:
  - Node & Edge badges: `[▲]` for Support, `[▼]` for Attack, `[▲/▼]` for Dual.
  - Stroke patterns: solid for Support, dashed (`[4, 4]`) for Attack, dash-dotted for Dual.
  - Focus node: cyan double-halo focus ring (`#06b6d4`).
  - Unaffected elements: dimmed with 0.6 opacity to maintain WCAG contrast and readability.
- "Clear Metric / Reset View" removes metric visual states while preserving node positions, camera zoom, and loaded subgraphs.

### 6. Dual Context Menus & Edge Inspector Modal
- Added context menu listeners on canvas:
  - Right-clicking nodes opens `NodeContextMenu.tsx` with options to inspect, run local metrics, expand neighbors, or focus camera.
  - Right-clicking edges opens `EdgeContextMenu.tsx` with options to inspect relationship properties, polarity provenance, and highlight source/target claims.
- `EdgeInspectorModal.tsx` provides deep causal inspection of weights $\phi$, epistemic polarities, and contribution shares.

## Alternatives Considered

- **Synchronous-only execution**: Rejected because global analytics on large knowledge graphs cause browser timeouts and freeze user interactions.
- **WebSocket/SSE-only transport for metrics**: Rejected to preserve lightweight stateless REST semantics matching the existing API architecture, while using short polling only for jobs exceeding 250ms.
- **Node-only metric visual explanations**: Rejected because epistemic argument graphs derive meaning from relational inferences; without edge contribution annotations, users cannot verify the reasoning path.

## Consequences

- Researchers can explore quantitative argument metrics with full causal path transparency.
- Graph analytics scale gracefully between sub-millisecond local queries and distributed GDS runs.
- Canvas state management is robust against async race conditions and accessible under WCAG guidelines.

## Related

- `../../packages/episteme-studio/docs/CONTRACT.md` — API contracts for metrics and execution endpoints
- `packages/episteme-studio/src/Episteme_studio/domain/metrics.py` — Domain models for metrics
- `packages/episteme-studio/src/Episteme_studio/services/metric_service.py` — Metric registry and lifecycle manager
- `packages/episteme-studio/src/Episteme_studio/adapters/metrics_adapter.py` — QBAF gradual strength semantics engine
- `packages/episteme-studio/frontend/src/panels/MetricsDrawer.tsx` — Dynamic schema metrics drawer
