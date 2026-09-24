# [0013] Per-Run Neo4j Credentials and Automatic Graph Fallback

Status: Accepted (2026-09-07)

## Context

In ADR 0010, Episteme Studio established a Dual-Driver Graph Preview architecture supporting both Artifact Store snapshots (`/api/runs/{run_id}/graph`) and Live Neo4j databases (`/api/graph/view`). However, real-world research usage revealed critical friction points:

1. **Global Mode Lock-In & Stale Data**:
   Once connected to Neo4j, the frontend remained locked in Neo4j mode globally. Switching to a different run in the left sidebar continued querying the active Neo4j database, which typically did not contain that run's graph (yielding an empty graph or misleading stale data) instead of displaying the run's actual artifact output.
2. **Canvas Clutter vs. Global Shell Controls**:
   Exposing driver toggles directly inside the graph canvas HUD overloaded the analytical viewport. The global connection and driver state belongs naturally in the application shell and system connectivity indicators.
3. **Multi-Database & Per-Run Epistemic Projections**:
   Different pipeline runs often write to distinct Neo4j databases or instances. When inspecting an older run, researchers need to reconnect to that specific run's database projection.
4. **Zero Server-Side Secret Storage**:
   Storing database credentials (especially plaintext or reversibly hashed passwords) in pipeline run directories (`.pipeline_runs/{run_id}/run.json`) or server configs introduces substantial security and privacy risks when artifacts or repositories are shared.

## Decision

Implement **Default Artifact Store Loading**, **Top-Level Shell Connectivity Management**, and **Per-Run Client-Side Credential Storage**:

1. **Clean Canvas HUD & Default to Artifact Store**:
   - The graph canvas HUD (`GraphCanvasHud.tsx`) is stripped of driver switchers, keeping the HUD dedicated strictly to layout, viewport navigation, layers, overlays, and metrics.
   - If no specific live Neo4j connection is active or established, the graph automatically defaults to the **Artifact Store**, loading the immutable artifact graph for the active run via `/api/runs/{runId}/graph` (preserving architectural decision D-04: Artifact Store primary, Neo4j secondary).

2. **Unchanged Status Element with Submenu Controls in AppShell**:
   - The connectivity status element in `AppShell.tsx` preserves its exact design and styling:
     - When using artifacts (default): displays `Artifact Store` with an amber status dot.
     - When using live Neo4j: displays `Neo4j Live` with a glowing green status dot.
   - Its hover/click submenu exposes comprehensive storage controls:
     - If Neo4j is offline: displays a direct `+ Add Neo4j Connection...` trigger opening the connection modal.
     - If Neo4j is connected: displays active graph source, a 1-click toggle between `Switch to Artifact Store` and `Switch to Neo4j Live`, a `Configure Connection...` trigger, and a `Disconnect` button.
   - A dedicated key button (`Key` icon) is placed adjacent to the status dropdown in the top navigation bar for immediate 1-click access to the connection modal.

3. **Secure Client-Side Browser Storage (`localStorage`)**:
   - Credentials (`url`, `user`, `password`, `database`, `savedAt`) are persisted exclusively in the client's browser `localStorage` under `episteme-studio-run-neo4j-credentials` via `useCredentialStore`.
   - Passwords and connection secrets are **never sent to or stored on the backend filesystem**, eliminating secret leakage in manifests or version control.
   - When launching a new pipeline execution (`startNewRun`), the frontend automatically links the user's `lastUsedCredentials` to the newly minted run ID, providing seamless zero-click credential continuity for new runs.

4. **Lifecycle Panel Visibility in RunDetailView**:
   - The `Corpus & Lifecycle` panel in `RunDetailView` displays the active Neo4j database mapping with inline "Configure" or "Edit" modal controls.

5. **Backend Session Disconnect Endpoint**:
   - Added `POST /api/graph/disconnect` to `Episteme_studio.api.graph` to cleanly close active async driver connection pools and reset runtime state on demand.

## Alternatives Considered

- **Embedding driver toggles in the Graph HUD**: Rejected because it cluttered the viewport and created confusing disconnects between global app connectivity and local canvas view state.
- **Server-Side Credential Vault**: Storing credentials in SQLite or JSON manifests in the backend artifact directory. Rejected due to security risks and credential leakage when sharing run folders.
- **Global Neo4j Mode without Run Fallback**: Retaining Neo4j mode across run switches. Rejected because it frequently produced blank canvases or displayed graphs from different runs.

## Consequences

- **Viewport Clarity**: The graph canvas HUD is focused entirely on graph visualization and analysis.
- **Predictable Exploration**: The system always defaults safely to the immutable artifact graph when no specific Neo4j connection is provided.
- **Intuitive Shell Navigation**: Connectivity and driver switching are centralized in `AppShell.tsx` without altering the status element design.
- **Security & Privacy**: Zero server-side persistence of database passwords. All credentials reside strictly in the researcher's local browser storage.

## Related

- `docs/adr/0010-graph-preview-driver-selection-neo4j.md` — Dual-Driver Graph Preview architecture
- `../../packages/episteme-studio/docs/DECISIONS.md` — D-04 (Artifact Store primary, Neo4j secondary)
- `packages/episteme-studio/frontend/src/shell/AppShell.tsx` — Top navbar status dropdown, submenu actions, and key button
- `packages/episteme-studio/frontend/src/store/credentialStore.ts` — Client-side credential store
- `packages/episteme-studio/src/Episteme_studio/api/graph.py` — Disconnect and connect endpoints
