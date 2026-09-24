# [ISSUE-014] Neuro-Symbolic Hybrid Vector & Graph Search Engine

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-014` |
| **Component(s)** | `packages/episteme-pipeline` (`graph/`), `packages/episteme-studio` (`frontend/src/shell/GlobalCommandOmnibar.tsx`, `api/`) |
| **Roadmap Horizon** | **Horizon 2** (Scalability, Benchmarking & Dialectical Modeling) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §6.1](issues/shared/requirements_glp_project.md#L257-L264), [docs/TODO_FUTURE.md §5](docs/TODO_FUTURE.md#L56-L69) |

---

## 1. Problem Statement & Motivation
Currently, GLP Studio features two separate search mechanisms:
1. Pure Cypher queries in [`CypherConsole.tsx`](packages/episteme-studio/frontend/src/console/CypherConsole.tsx).
2. Client-side memory string filtering in [`GlobalCommandOmnibar.tsx`](packages/episteme-studio/frontend/src/shell/GlobalCommandOmnibar.tsx) (`⌘K`).

Neither fulfills the neuro-symbolic retrieval vision detailed in [`docs/TODO_FUTURE.md` §5](docs/TODO_FUTURE.md#L56-L69): querying the Theory Graph with natural language, where dense vector similarity across textual envelopes is combined with structural graph traversal and topological centrality constraints.

---

## 2. Functional Requirements
1. **Hybrid Retrieval Endpoint**:
   - Create `POST /api/search/hybrid` in `packages/episteme-studio/src/glp_studio/api/graph.py`.
   - Pipeline:
     - Dispatches semantic query text to the active dense embedding model (e.g. `text-embedding-3-large`).
     - Queries Neo4j vector index for top-$k$ nearest entity and chunk candidates.
     - Combines vector scores with topological graph weight:
       $$\text{Score}(u) = \lambda \cdot \text{CosineSim}(q, u) + (1 - \lambda) \cdot \text{PageRank}(u)$$
     - Filters by user-specified structural constraints (e.g. `layer == 3`, `partition == 'A'`, or paths connected to a specific theoretical concept).
2. **Omnibar Natural Language Integration**:
   - Enhance [`GlobalCommandOmnibar.tsx`](packages/episteme-studio/frontend/src/shell/GlobalCommandOmnibar.tsx) so typing freeform questions or conceptual prompts queries the hybrid search backend and returns ranked entity clusters with matching provenance snippets.

---

## 3. Acceptance Criteria
- [ ] Hybrid endpoint accepts natural language queries and returns vector-similarity-ranked nodes filtered by graph schema.
- [ ] Omnibar triggers backend search when queries do not match local client keywords.
- [ ] Clicking a search result centers the AntV G6 camera on the target node and selects its neighborhood.
- [ ] Automated integration tests verify hybrid ranking logic.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/shell/GlobalCommandOmnibar.tsx`](packages/episteme-studio/frontend/src/shell/GlobalCommandOmnibar.tsx)
- [`packages/episteme-studio/src/glp_studio/api/graph.py`](packages/episteme-studio/src/glp_studio/api/graph.py)
- `packages/episteme-pipeline/episteme_pipeline/graph/`
