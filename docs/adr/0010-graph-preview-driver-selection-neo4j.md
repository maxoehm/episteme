# [0010] Dual-Driver Graph Preview (Artifact Store vs. Live Neo4j) and Calculation Overlays

Status: Accepted (2026-09-07)

## Context

Episteme Studio provides an interactive graph visualization canvas powered by AntV G6 (`GraphCanvas.tsx`).
Initially, graph materialization was tied exclusively to pipeline execution run directories via `ArtifactReader`
(per decision D-04). However, users and researchers require:

1. **Global cross-run visibility**: Examining the accumulated multi-document theory graph directly from the
   active Neo4j database rather than only inspecting frozen individual run artifacts.
2. **Interactive exploration**: Incrementally expanding node neighborhoods (lazy k-hop expansion) from seeds
   on the canvas without loading the entire graph into memory at once.
3. **Complex graph analytics**: Triggering and visualizing structural and epistemic graph algorithms
   (e.g., PageRank centrality, degree centrality, weakly connected components, gradual strength semantics)
   directly against the live Neo4j store or active graph views.
4. **Resilient UX**: Switching drivers seamlessly while providing inline connection management and fallback
   when Neo4j is offline or credentials need reconfiguration.

## Decision

Implement a **Dual-Driver Graph Preview Architecture** centered on the unified `GraphView` domain model:

1. **Driver Switcher in Graph Explorer UI**:
   - The primary toolbar presents a segmented driver selector: **Artifact Store (Run)** vs **Neo4j Database (Live)**.
   - In Artifact Store mode, graphs are loaded from the selected pipeline run snapshot via `/api/runs/{run_id}/graph`.
   - In Neo4j Database mode, graphs are queried live via `/api/graph/view` and independent of individual run selection.
   - When Neo4j is offline or disconnected, an inline banner and embedded connection modal prompt the user to
     input credentials or reconnect.

2. **Interactive Lazy Neighborhood Expansion**:
   - Double-clicking (`NodeEvent.DBLCLICK`) or right-clicking (`NodeEvent.CONTEXT_MENU`) any node on the canvas in
     Neo4j mode triggers `/api/graph/expand` (1-hop traversal).
   - The returned sub-graph projection is merged into the active canvas data structure, dynamically preserving
     existing layout coordinates while rendering new neighbors and edges.
   - The Node Inspector panel exposes a dedicated "Expand Neighbors (+1 hop)" button for accessibility and keyboard navigation.

3. **Overlay & Complex Calculation Integration**:
   - The backend `ComputeOverlayRequest` and frontend `OverlaySwitcher` support a `source` parameter (`"artifacts"` or `"neo4j"`).
   - In Neo4j mode, overlays (such as PageRank, degree centrality, connected components, and gradual strength)
     resolve their graph snapshot directly from the active Neo4j projection.
   - Added `OverlayKind.PAGERANK` backed by the `igraph` directed PageRank engine, allowing instant epistemic
     centrality calculations projected as continuous scale overlays on canvas nodes.

4. **Connection Status Endpoint**:
   - Added `GET /api/graph/status` returning current connection liveness, Bolt URI, and active database name.

## Alternatives Considered

- **Neo4j-only graph visualization**: Dropping artifact-based graph preview would break offline usability
  and make it impossible to inspect historical run artifacts when Neo4j is not provisioned (violating D-04).
- **Client-side only expansion**: Re-querying the whole database on every expansion would degrade canvas
  performance and exceed node budgets on large graphs; server-side k-hop traversal via `Neo4jReader.expand_graph`
  ensures deterministic latency and budget enforcement.
- **Separate Cypher-only algorithm pipeline**: Requiring users to write raw Cypher/GDS queries to see metrics
  introduces friction; integrating standard graph metrics into the existing `OverlayService` allows 1-click
  visual rendering on the canvas.

## Consequences

- The AntV G6 canvas renders graphs from both drivers interchangeably without divergence in rendering logic.
- Both drivers produce standard RFC 7807 problem details when unavailable (`neo4j-unavailable` with HTTP 503).
- Researchers can alternate between immutable run provenance and live graph experimentation in a single unified interface.

## Related

- `../../packages/episteme-studio/docs/DECISIONS.md` — D-04 (Artifact Store primary, Neo4j secondary)
- `packages/episteme-studio/src/Episteme_studio/adapters/neo4j_reader.py` — Neo4j query & expansion adapter
- `packages/episteme-studio/src/Episteme_studio/services/overlay_service.py` — Metric overlay dispatch table
- `packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx` — Dual-driver canvas implementation
