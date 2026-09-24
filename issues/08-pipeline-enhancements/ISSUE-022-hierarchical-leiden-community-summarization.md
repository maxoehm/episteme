# [ISSUE-022] Hierarchical Leiden Community Summarization & Theory Synthesis

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-022` |
| **Component(s)** | `packages/episteme-pipeline` (`pipeline/phases/phase5_fusion/`, `pipeline/phases/phase6_theorynet/`) |
| **Roadmap Horizon** | **Horizon 2** (Dialectical Modeling & Theory Synthesis) |
| **Priority** | Medium |
| **Status** | Open |
| **Source Ref** | [`review/07/04_graph_construction_and_optimization.md §4`](review/07/04_graph_construction_and_optimization.md#L35-L48) |

---

## 1. Problem Statement & Motivation
In [`pipeline/phases/phase5_fusion/leiden_clustering.py`](packages/episteme-pipeline/episteme_pipeline/phases/phase5_fusion/leiden_clustering.py), hierarchical community detection is performed on the entity graph and theory graph using the Leiden algorithm (`graspologic.partition.hierarchical_leiden`).

The detected clusters are assigned community IDs and stored in Neo4j as `Community` nodes. However, the system currently lacks a **generative community summarization** mechanism (analogous to Microsoft GraphRAG community reports). As a result:
1. Macro-level theoretical clusters remain uninterpreted collections of node IDs and edge pointers.
2. Global questions regarding the overarching themes, argumentative clusters, or dialectical camps within the corpus cannot be answered without reading through all constituent nodes individually.
3. The bridge between structural graph partitioning and high-level epistemological synthesis remains incomplete.

---

## 2. Functional Requirements
1. **Community Summarization Protocol & Engine**:
   - Introduce a `CommunitySummarizer` interface in `pipeline/protocols/` and implement `LLMCommunitySummarizer` in `phase5_fusion/`.
   - For each detected Leiden community (or communities meeting a minimum size threshold, e.g. $\ge 3$ nodes):
     - Extract member entities/atoms, their descriptions, textual envelopes, and internal interconnecting relations.
     - Prompt the structured LLM to generate a `CommunityReport` containing:
       - `title`: Short title of the theoretical sub-domain or debate.
       - `summary`: Comprehensive synthesis of the claims, arguments, and positions represented in the cluster.
       - `key_propositions`: List of central propositions or hypotheses.
       - `internal_tensions`: Known critiques, refutations, or dialectical tensions within the community.
2. **Artifact & Graph Persistence**:
   - Store generated community summaries as properties on the corresponding `Community` nodes in Neo4j (`title`, `summary`, `report_json`).
   - Emit `CommunityReportArtifact` instances into the pipeline `ArtifactCollection` so summaries participate in artifact invalidation and provenance tracking.
3. **Studio Integration**:
   - Expose community summaries in GLP Studio's cluster view or hull overlays so users can inspect macro-level summaries by clicking on community hulls.

---

## 3. Acceptance Criteria
- [ ] `LeidenTheoryClustering` optionally executes LLM community summarization when configured in `Phase5Config`.
- [ ] `CommunityReport` Pydantic models are validated and emitted as run artifacts.
- [ ] Neo4j `Community` nodes store synthesized summary and title properties.
- [ ] Unit tests with mock LLM confirm summarization runs without schema errors.

---

## 4. Key Target Files
- [`packages/episteme-pipeline/episteme_pipeline/phases/phase5_fusion/leiden_clustering.py`](packages/episteme-pipeline/episteme_pipeline/phases/phase5_fusion/leiden_clustering.py)
- [`packages/episteme-pipeline/episteme_pipeline/config.py`](packages/episteme-pipeline/episteme_pipeline/config.py)
- [`packages/episteme-pipeline/episteme_pipeline/artifacts/models.py`](packages/episteme-pipeline/episteme_pipeline/artifacts/models.py)
