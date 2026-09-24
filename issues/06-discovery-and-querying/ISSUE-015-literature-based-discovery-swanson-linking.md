# [ISSUE-015] Literature-Based Discovery (LBD) & Swanson Linking Workbench

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-015` |
| **Component(s)** | `packages/episteme-pipeline` (`post_processing/`), `packages/episteme-studio` (`frontend/src/panels/`) |
| **Roadmap Horizon** | **Horizon 3** (Epistemic Frontiers & Scientific Research) |
| **Priority** | Low (Research Target) |
| **Status** | Research / Future Target |
| **Source Ref** | [requirements_glp_project.md §6.2](issues/shared/requirements_glp_project.md#L268-L285) |

---

## 1. Problem Statement & Motivation
Don R. Swanson pioneered Literature-Based Discovery (LBD), demonstrating that undiscovered public knowledge exists in the cross-disciplinary gaps between disconnected literatures:
$$A \longrightarrow C \quad \text{and} \quad C \longrightarrow B \implies A \overset{?}{\dashrightarrow} B$$
If literature $A$ shares an intermediate theoretical bridge $C$ with literature $B$, but researchers in communities $A$ and $B$ do not cite or communicate with each other, $A \dashrightarrow B$ constitutes a candidate scientific hypothesis.

Currently, extraction is restricted to explicit co-occurrences and direct discourse relations within single documents. A discovery informatics engine is needed to mine indirect inferential pathways across literature silos.

---

## 2. Functional Requirements
1. **Swanson Bridge Mining Algorithm**:
   - Traverse Neo4j for pairs of concepts $(A, B)$ belonging to separate literature clusters (measured by Louvain/Leiden modularity) that share significant intermediate theoretical bridges $C_1, \dots, C_k$.
2. **Discovery Multi-Scorer**:
   - Score each candidate discovery along four formal dimensions:
     - **Solution Rarity** ($\text{rar}(G)$): Uniqueness of connecting path topologies.
     - **Topical Density** ($\text{topd}$): Local conceptual cohesion around bridge $C$.
     - **Epistemic Relevance** ($\text{topr}$): Degree of mutual argumentative support along the chain.
     - **Topical Novelty** ($\text{topn}$): Semantic distance between endpoint embedding clusters $A$ and $B$.
3. **LBD Discovery Workbench**:
   - Dedicated Studio view listing candidate discovered bridges, ranked by composite discovery score, with full provenance path visualization ($A \to C \to B$).

---

## 3. Acceptance Criteria
- [ ] Post-processing pass identifies high-scoring indirect pathways between disconnected communities.
- [ ] Discovery scores ($\text{rar}, \text{topd}, \text{topr}, \text{topn}$) are computed deterministically.
- [ ] GLP Studio surfaces candidate discoveries in a dedicated Discovery drawer.

---

## 4. Key Target Files
- `packages/episteme-pipeline/episteme_pipeline/post_processing/discovery/`
- `packages/episteme-studio/frontend/src/panels/`
