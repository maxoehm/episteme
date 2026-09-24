# [ISSUE-017] Visual Metamodel & Ontology Schema Designer

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-017` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/panels/configEditor/`), `packages/episteme-pipeline` (`schema/`) |
| **Roadmap Horizon** | **Horizon 1 & 2** (Platform Stabilization & Usability) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §6.3](issues/shared/requirements_glp_project.md#L294-L298) |

---

## 1. Problem Statement & Motivation
The pipeline supports customizable schema taxonomies via `SchemaConfig` and `DEFAULT_SCHEMA` (Phase 0). While GLP Studio includes a text-based configuration editor ([`ConfigEditor.tsx`](packages/episteme-studio/frontend/src/panels/ConfigEditor.tsx)) and phase drawers ([`PhaseCatalogDrawer.tsx`](packages/episteme-studio/frontend/src/panels/PhaseCatalogDrawer.tsx)), there is no **visual graphical designer** for ontologies.

Researchers in specialized scientific disciplines (e.g. cognitive science, economics) need to define custom entity classes, permissible edge types, domain-range cardinality constraints, and inverse relationships visually before executing pipeline runs on novel corpora.

---

## 2. Functional Requirements
1. **Interactive Schema Canvas**:
   - Provide a visual drag-and-drop ontology editor within the Studio Config / Engine tab.
   - Nodes represent entity types (with color, layer assignment L1/L2/L3, and mandatory property fields).
   - Edges represent permitted relational predicates (with allowed source/target types and polarity constraints).
2. **Schema Export & Pipeline Integration**:
   - Export custom visual designs directly to standard `schema_config.yaml` or JSON schemas ingested by `PipelineConfig`.
   - Prevent database migrations by compiling schema rules into dynamic prompt instructions and Neo4j Cypher constraints.
3. **Corpus Profile Library**:
   - Save and load pre-configured domain profiles (e.g. "Philosophy of Science", "Biomedical Literature", "Normative Ethics").

---

## 3. Acceptance Criteria
- [ ] Graphical node-and-wire interface for designing custom entity and relation schemas.
- [ ] Exporting produces valid `SchemaConfig` objects recognized by `episteme-pipeline`.
- [ ] Real-time validation warns against invalid inter-layer connections or missing inverse rules.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/panels/configEditor/`](packages/episteme-studio/frontend/src/panels/configEditor/)
- [`packages/episteme-studio/frontend/src/panels/PhaseCatalogDrawer.tsx`](packages/episteme-studio/frontend/src/panels/PhaseCatalogDrawer.tsx)
- `packages/episteme-pipeline/episteme_pipeline/schema/`
