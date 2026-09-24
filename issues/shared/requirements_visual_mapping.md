### 1. Requirements Already Fulfilled

The current implementation of GLP Studio directly satisfies core visualization, pipeline orchestration, structuralist partitioning, and run-comparison requirements:

* **Three-Layer Graph Projection & Semantic Canvas (Req 1.1, 1.2)**:
* The canvas renders a force-directed multi-layer graph explicitly distinguishing Layer 1 Ground-Truth Sources (blue), Layer 2 Empirical Entities (green), and Layer 3 Theoretical Constructs (purple).
* Dialectical relations (`SUPPORT` in green, `ATTACK` in red) and unscoped drift entities (orange) are visually encoded.


* **Structuralist Ontological Partitions (Req 2.1)**:
* The **Views & Overlays** panel includes structuralist filters: the **Empirical Base ($M_{pp}$)** for non-theoretical data, **Theoretical Postulates ($M$)**, the **Dialectical Argument Web**, and **Intertheoretical Bridges**.


* **Formal Metatheoretical Tenability & Basic Topology (Req 2.2, 3.1)**:
* The inspection drawer tracks local node confidence alongside formal **Tenability** scores and theoretical evaluation constraints (e.g., structural and discourse constraints).
* The **Graph Metrics** panel includes Stegmüller (1976) / Balzer (1987) metatheory tenability algorithms.
* Centrality and clustering algorithms are active: Global PageRank (with Neo4j GDS execution, Python fallback, damping factor, and tolerance parameters), Global Degree Centrality, Weakly Connected Components (WCC), and Global Louvain Community Detection.


* **Side-by-Side Version Diffing & Set-Theoretic Deltas (Req 4.2)**:
* The **Comparison Engine** executes differential graph analysis, providing a Visual Canvas Diff, side-by-side YAML/JSON configuration diffs across all pipeline phases, and overlapping Kernel Density Estimates (KDE) for confidence score shifts.
* Explicit set-theoretic deltas calculate Intersection ($A \cap B$), Run A Complement ($A \setminus B$, pruned/omitted), and Run B Complement ($B \setminus A$, novel entities) across entity and edge cardinalities.


* **Modular Pipeline Orchestration & Caching (Req 5.1)**:
* The **Execution** view provides a 10-phase extraction DAG (Defaults, Schema, Chunking, NER & Triples, Global Relations, Consolidation, Maturation, Mining, Dialectical Web, Epistemic Synthesis).
* Supports configurable inference stacks: generative LLMs with discrete "Thinking Levels" (`Off`, `Low`, `Medium`, `High`, `Custom`), dense embedding model selectors (`text-embedding-3-large`), and cross-encoder rerankers (`gte-multilingual-reranker-base`).
* Features phase-level cache management (Cache BUST modes), pre-flight inspection with compute/cost estimation, Langfuse telemetry integration, immutable decision manifests, and reproducible CLI command generation.


* **Native Cypher Querying (Req 6.1)**:
* The **Cypher Console** provides a direct read-only query editor with syntax highlighting and sample query templates connected directly to Neo4j.



---

### 2. Unfulfilled Requirements Easily & Intelligently Integrated

These capabilities do not require new top-level architecture; they fit into existing interface panels, layout hooks, or algorithmic execution loops:

* **Topological Poset / Tree & Spectral Layouts (Req 1.2)**:
* *Integration Spot*: The Explorer toolbar's layout selector (currently defaulting to `Force-Directed`).
* *Implementation*: Add **Poset / Hierarchical DAG** (for theory specialization trees) and **Spectral / Laplacian** (using the Fiedler vector for community isolation) directly to this dropdown alongside existing physics controls.


* **Additional Newman Centrality & Clustering Metrics (Req 3.1)**:
* *Integration Spot*: The right-hand **Graph Metrics** panel in the Explorer view.
* *Implementation*: Betweenness centrality, Closeness, Katz/Eigenvector centrality, HITS, local clustering coefficients ($C_i$), and transitivity can be added as selectable algorithms alongside PageRank and Degree Centrality.


* **Interactive Tenability Blur Radius ($\delta^*$) & Anomaly Alerts (Req 2.2)**:
* *Integration Spot*: The **Theoretical Tenability Evaluation** configuration panel (Metrics) and the **Node Inspector**.
* *Implementation*: The algorithm configuration panel already supports numeric slider controls (as shown in PageRank damping/iterations). A slider for blur radius $\delta^*$ fits there, dynamically updating the canvas to highlight nodes dropping below $TS_{\text{local}} < 0.5$. The exact law violations can be surfaced within the node inspector's existing *Theoretical Evaluation* list.


* **Full Structuralist Core Projections: $M_p$, $GC$, and $GL$ (Req 2.1)**:
* *Integration Spot*: The **Ontological Partitions** section inside **Views & Overlays**.
* *Implementation*: This section already toggles $M_{pp}$ and $M$. Adding explicit filter toggles for Potential Models ($M_p$), Global Constraints ($GC$), and Global Links ($GL$) completes the structuralist quintuple $K = \langle M_p, M, M_{pp}, GC, GL \rangle$ without modifying the underlying UI layout.


* **QBAF Gradual Semantics Recomputation & Thagardian ECHO (Req 3.3)**:
* *Integration Spot*: The **Graph Metrics** list and execution engine.
* *Implementation*: Since `SUPPORT` and `ATTACK` polarities and confidence weights already exist, a QBAF relaxation pass or Thagardian ECHO solver can be invoked as an algorithm from this panel, projecting converged belief/harmony scores directly onto node sizes or color saturation.


* **Retrieval & Rerank Decision Auditing (Req 5.1)**:
* *Integration Spot*: The **Corpus & Runs -> Stage Output & Analytics** view.
* *Implementation*: This tab already breaks down generated artifacts, distribution plots, and causal provenance for Phases 2 and 3. Surfacing MIPS candidate cutoff distances and cross-encoder scores ($\tau$) here is the natural design placement.


* **Deep Provenance & Jump-to-Source Text Highlighting (Req 5.2)**:
* *Integration Spot*: The **Evidence** tab in the Node/Edge Inspector.
* *Implementation*: The inspector already lists the `source_chunk_id` and document cluster. Populating the currently empty `Evidence (0)` tab with an inline passage viewer highlighting character offsets operationalizes this requirement.


* **HITL Inline Curation & Polarity Modification (Req 5.3)**:
* *Integration Spot*: The inspector ledger and the existing **Staging Editor** interface hook.
* *Implementation*: Clicking on relations in the inspector can allow in-place polarity toggles (e.g., flipping `SUPPORT` to `ATTACK`), staging modifications as a provisional local diff.


* **Hybrid Vector & Graph Search (Req 6.1)**:
* *Integration Spot*: The global command bar (`⌘K Search nodes, runs, commands...`).
* *Implementation*: Expand the omnibox parser to accept natural-language semantic prompts (dispatched to the embedding model defined in Execution) alongside Cypher tokens and node ID lookups.



---

### 3. Requirements Requiring New Features, Views, or Dedicated Engines

These requirements demand new computational backends, specialized formalisms, or distinct top-level interfaces:

* **Diachronic Theory Dynamics, Reduction Matrices ($\rho$), & Kuhn-Loss Tracking (Req 4.1)**:
* *Why*: The current Comparison Engine evaluates set-theoretic differences ($A \cap B$, $A \setminus B$) between two execution runs. Evaluating incommensurability and Kuhn-Loss ($L_{\text{lost}}$) requires formalizing structuralist reduction relations ($\rho: T' \to T$) to track which intended applications $I$ of an older theory are structurally displaced or abandoned by a successor.
* *What is needed*: A dedicated **Theory Dynamics / Reduction Studio** view that models the asymmetric specialization lattices ($T_b \to T_i$) and outputs an empirical Kuhn-Loss matrix.


* **Ramsey-Sentence Evaluator & Automated Sneedian $T$-Theoreticity Engine (Req 2.3)**:
* *Why*: Sneedian criterion checking requires assessing whether a function or predicate can be measured independently of an application of theory $T$. Stripping theoretical terms to compute Ramsey sentences ($\text{Cn}(K)$) requires formal second-order symbolic logic elimination.
* *What is needed*: A specialized symbolic post-processing engine (hooked into the pipeline DAG) and a dedicated **Ramsey Verification Modal** that checks empirical claims for non-vacuous content.


* **Literature-Based Discovery (LBD) & Swanson Bridge Mining (Req 6.2)**:
* *Why*: Currently, graph discovery is restricted to LLM extraction phases and local edge inference. Detecting indirect, cross-domain inferential pathways ($A \to C \to B$) requires multi-hop path traversal algorithms outside standard pipeline extraction.
* *What is needed*: An **LBD Discovery Workbench** that executes Swanson linking, computes the multi-dimensional Discovery Scores (Solution Rarity, Topical Density, Epistemic Relevance, Topical Novelty), and exports candidate hypothetical bridges.


* **Nováček Hypothesis Virtues & Pareto Ranking Multigraphs (Req 3.2)**:
* *Why*: The studio evaluates single-node metrics and standard graph topology, but lacks multi-objective epistemic evaluation across structural modesty, refutability, and simplicity.
* *What is needed*: A **Pareto Frontier Analytics View** plotting competing sub-theories across efficiency frontiers to identify structurally optimal theoretical networks.


* **Neutral Contradiction Management Workspace (Req 6.3)**:
* *Why*: While `ATTACK` edges visualize dialectical conflict, the system lacks formal epistemic neutral contradiction resolution.
* *What is needed*: A **Contradiction Workspace** implementing the 3-state belief vector (`<Belief, Disbelief, Uncertainty>`), allowing researchers to manage conflicting paradigm-relative claims without forcing artificial convergence.


* **Visual Metamodel & Ontology Schema Designer (Req 6.3)**:
* *Why*: The pipeline features a `P0 Schema` phase, but there is no interface to design or alter schemas.
* *What is needed*: A **Schema / Ontology Administration Studio** providing a graphical interface to define entity classes, permissible relational predicates, typed functional dependencies, and corpus-specific epistemological constraints prior to ingestion.