# GLP Studio: Feature Specification & Functional Requirements Report

## Executive Summary

**GLP Studio** is the dedicated interface and analytical workstation for the Grund GLP pipeline. Unlike standard
knowledge graph platforms (e.g., Neo4j Bloom, Gephi) that treat graphs as flat collections of empirical facts, GLP
Studio is designed as an **epistemic analytics workstation**. It operationalizes **structuralist philosophy of science**
(Sneed, Stegmüller, Balzer, Moulines), **computational epistemology**, and **quantitative argumentation theory (QBAF)**.

The platform must bridge the gap between raw textual corpora in Layer 1 (Source Embedding), empirical relational
networks in Layer 2 (Knowledge Graph), and formal theoretical constructs in Layer 3 (Theory Framework).

```
+-------------------------------------------------------------------------------+
|                                  GLP STUDIO                                   |
|   +-----------------------+-------------------------+---------------------+   |
|   | 1. Multi-Layer Canvas | 2. Structuralist Engine | 3. Metrics Suite    |   |
|   | (L1/L2/L3, Leiden,    | (M_p, M_pp, Tenability, | (Newman Centrality, |   |
|   | Posets, Spectral)     | Ramseyification)        | Nováček Virtues)    |   |
|   +-----------------------+-------------------------+---------------------+   |
|   +-----------------------+-------------------------+---------------------+   |
|   | 4. Diachronic Tracker | 5. Pipeline & HITL Hub  | 6. Discovery & LBD  |   |
|   | (Echelon, Reduction,  | (Provenance, Langfuse,  | (Swanson Linking,   |   |
|   | Kuhn-Loss, Versioning)| Artifact Replay, Audit) | Genetic Refinement) |   |
|   +-----------------------+-------------------------+---------------------+   |
+-------------------------------------------------------------------------------+

```

---

## 1. Multi-Layer Graph Visualization & Structural Navigation

The visualization core must manage multi-scale hierarchical complexity, moving between textual tokens and
macro-theoretical holons without visual clutter.

### 1.1 Layer-Specific Rendering & Composability

* **Three-Layer Projection**:
* **Layer 1 (Substrate & Provenance)**: Document nodes, chunk nodes, character-offset boundaries, and citation anchors.
* **Layer 2 (Domain Knowledge Graph)**: Extracted empirical entities, co-occurrences, basic semantic triples, and
  relation classifications.
* **Layer 3 (Theory Framework)**: Argumentative premises/conclusions, model-theoretic structures, theoretical laws, and
  intertheoretical bridges.


* **Composability Modes**: Provide a persistent toggle between:
* *Isolated View*: Renders only elements of a selected layer.
* *Composite / Projection View*: Renders L3 theoretical nodes while drawing translucent projection cones down to
  supporting L2 entities and L1 textual chunks.

### 1.2 Topology-Aware Layout Engines

* **Tree / Poset Layouts for Theory-Nets**: Enforces hierarchical, partially ordered sets (posets) for specialization
  nets where a basic theory-element ($T_b$) sits at the root, branching downwards into specialized elements ($T_i$).
* **DAG & Cyclic Coherentist Visualizer**: Force-directed layouts configured for directed acyclic graphs (DAGs),
  equipped with visual callouts for feedback loops or mutual coherence cycles (e.g., Thagardian coherence loops).
* **Graph Laplacian & Spectral Layouts**: Partitioning via algebraic connectivity (the Fiedler vector / second-smallest
  eigenvalue of the Laplacian) to expose natural structural communities and bridge bottlenecks with minimized edge
  crossings.
* **Stable Epistemic Anchors**: Fixed visual pinning for high-betweenness bridging concepts, preventing layout jumping
  when filtering subgraphs or applying threshold sliders.

### 1.3 Hierarchical Community Navigation

* **Leiden Multi-Scale Zooming**: Zoom synchronization across **Macro** (holons / paradigms), **Meso** (specialized
  theory-elements), and **Micro** (individual claim paths and model predicates).
* **Multigraph Edge Encoding**: Distinguish concurrent edges between identical node pairs (e.g., an empirical
  co-occurrence edge alongside a deductive entailment edge) using typed parallel arcs, varied line patterns (dashed for
  theoretical links, solid for empirical constraints), and dynamic width/opacity scaled to epistemic confidence.

---

## 2. Structuralist Model Validation & Tenability Engine

GLP Studio must translate structuralist metatheory into an executable computational engine, operationalizing theoretical
structures beyond binary first-order logic.

```
                  [ Theoretical Level (M_p) ]
                   ^                       |
                   | Theoretical           | Model Validation:
                   | Enrichment (Φ)        | Law Application
                   |                       v
[ Empirical Core (I ⊆ M_pp) ] ===> [ Actual Models (M) ]
                   \                       /
                    \-- Admissible Blur --/
                       (TS_local ≥ 0.5)

```

### 2.1 Model-Theoretic Decomposition

* **Theory-Element Inspector ($T = \langle K, I \rangle$)**:
* Visual separation of the theoretical core $K = \langle M_p, M, M_{pp}, GC, GL \rangle$ and the intended
  applications $I$.
* **Potential Models ($M_p$)**: Displays the conceptual framework (types, predicates, functions).
* **Partial Potential Models ($M_{pp}$)**: Visualizes the non-theoretical empirical basis ($T$-non-theoretical data).
* **Actual Models ($M$)**: Subsets of $M_p$ that satisfy the fundamental laws of the theory.
* **Global Constraints ($GC$)**: Inter-application constraints cross-linking identical objects across distinct domains.
* **Global Intertheoretical Links ($GL$)**: Directed pathways tying parameters from one theory to foundational
  constructs in another.

### 2.2 Continuous Tenability & Admissible Blurs

* **Continuous Tenability Engine**: Evaluates empirical compatibility without rigid binary satisfiability:
* **Local Tenability Score ($TS_{\text{local}}$)**: Evaluates empirical observations ($y \in I \subseteq M_{pp}$)
  against theoretical laws using topological uniformities ($U$) and tolerance neighborhoods (admissible
  blurs $\mathcal{A}$).
* **Edge Tenability ($TS_{\text{edge}}$)**: Propagates parameter consistency checks along constraint paths ($GC$)
  connecting distinct empirical domains.


* **Enrichment Inspector ($\Phi = \Phi_{\text{spec}} \circ \Phi_{\text{gen}}$)**: Visualizes the step-by-step
  mathematical projection of empirical data into full theoretical models via the introduction of theoretical terms.
* **Anomaly & Untenability Detection**:
* Automated visual alerts for untenable nodes or edges where $TS < 0.5$.
* Explanatory path traces highlighting the precise constraint equations or law violations driving down the tenability
  score.


* **Interactive Domain Lensing**: Real-time slider adjustments over blur radius $\delta^*$ to observe boundary
  conditions where theoretical models transition from tenable to falsified.

### 2.3 Sneedian $T$-Theoreticity & Ramseyification

* **Automated Sneedian Classification**: Categorizes terms and predicates as **$T$-theoretical** or **$T$
  -non-theoretical** based on whether measurement requires operational dependence on an application of theory $T$.
* **Ramsey-Sentence Evaluator**: Strips theoretical functions ($r (K)$) to extract the non-theoretical empirical claim
  ($\text{Cn} (K)$), verifying that the empirical assertion carries non-vacuous empirical content.

---

## 3. Epistemic Metrics & Quantitative Argumentation

A dual metrics suite balancing standard network topology with formal philosophical criteria for hypothesis evaluation.

### 3.1 Network Topology & Centrality Suite (Newman)

* **Centrality Profiles**: Computes in/out-degree, betweenness centrality (identifying inferential bottlenecks),
  closeness, eigenvector/Katz centrality, PageRank, and HITS (hub/authority scoring).
* **Clustering & Structure**: Local clustering coefficients ($C_i$), global transitivity, modularity ($Q$) via
  Leiden/Louvain, and power-law distribution tests for scale-free characteristics.

### 3.2 Formalized Hypothesis Virtues (Nováček Suite)

* **Metrics from Epistemetrics**
* **Pareto Ranking Multigraphs**: Aggregates multi-virtue metrics into directed multigraphs, identifying Pareto-optimal
  theories along efficiency frontiers (e.g., highest refutability at lowest structural entropy).

### 3.3 Argumentation & Coherence Dynamics

* **Extended QBAF Engine**: Supports Quantitative Bipolar Argumentation Frameworks:
* Node activation values represent belief strength; edges express graded support or attack.
* Interactive gradual semantics recomputation with user-defined damping and belief decay ($\theta$).


* **Thagardian ECHO / Harmony Calculation**:
* Constraint satisfaction relaxation calculating **System Harmony ($H$)**.
* Dynamic tracking of node activation settling under mutual coherence and incoherence constraints.

---

## 4. Diachronic Evolution & Intertheoretical Dynamics

The platform must explicitly capture how scientific theories evolve, merge, specialize, and undergo paradigm shifts
across historical time.

```
[ Classical Paradigm (T_old) ]
          |
          | Formal Reduction Matrix (ρ)
          | Kuhn-Loss Tracking: L_{lost}
          v
[ Successor Framework (T_new) ]
          +-- Specialization Lattice (Echelon Substructures)
          +-- Intertheoretical Bridge (GL) ---> [ External Foundational Theory ]

```

### 4.1 Structuralist Theory Dynamics

* **Crystallization**: Visualizes the formal phase transition from unstructured, proto-theoretical narrative clusters
  into formalized theory-nets utilizing **echelon partial substructures**.
* **Normal Scientific Evolution**: Models expansion across specialization lattices where the core basic element ($T_b$)
  remains invariant while specialized terminal nodes proliferate.
* **Embedding & Intertheoretical Subsumption**: Maps exact structural embedding (e.g., Classical Mechanics into
  Relativistic Mechanics), verifying subset preservation across empirical ranges.
* **Incommensurability & Kuhn-Loss Tracking**:
* Computes formal reduction functions ($\rho$) between competing theories.
* Flags **Kuhn-Loss**: Empirical applications successfully explained by a prior theory $T$ that are unaccounted for or
  conceptually displaced by successor theory $T'$.


* **Bed-Rock & Intertheoretical Dependency Chains**: Visualizes global link paths ($GL$), tracing how higher-level
  sciences rely on operational parameters provided by foundational disciplines (e.g., chemistry providing stoichiometric
  mole inputs to thermodynamic frameworks).

### 4.2 Temporal Versioning & Non-Destructive Diffing

* **Timeline Scrubber**: Temporal slider to scrub through historic states, tracking the temporal birth, mutation, and
  retirement of theoretical concepts.
* **Side-by-Side Version Diffing**:
* Node/edge diff highlighting: additions (green), deletions (red), semantic type shifts (blue), and confidence shifts.
* Terminology Drift Inspector: Tracks linguistic label shifts for stable theoretical roles over time without overwriting
  historic descriptions.

---

## 5. Pipeline Orchestration, Observability & Human-in-the-Loop (HITL)

GLP Studio serves as the control room for executing the Grund GLP pipeline against Neo4j, inspecting intermediate
artifacts, and debugging extraction logic.

### 5.1 Pipeline Run Observability

* **Phase-Based Execution Timeline**: Visual tracking of extraction phases:
* *Phase 1*: Document Chunking & Ingestion.
* *Phase 2*: Entity/Relation Extraction & LLM Parsing.
* *Phase 3*: Graph Linking, Resolution, and Cross-Encoder Reranking.
* *Phase 4*: Layer 3 Synthesis (QBAF construction, Model-Theoretic typing).


* **LLM Trace & Telemetry Linking**: Direct integration with telemetry providers (e.g., Langfuse):
* Link individual graph nodes and relations directly to LLM prompts, completions, token counts, latency, and model
  versions.


* **Retrieval Decision Auditing**: Exposes bi-encoder Maximum Inner Product Search (MIPS) candidate sets, cross-encoder
  rerank scores, and acceptance threshold cutoffs ($\tau$) to trace why specific edges were asserted or dropped.
* **Artifact Caching & Replay**: Inspect intermediate JSON artifacts generated per phase; capability to re-run pipeline
  segments downstream from cached checkpoints without re-extracting from raw text.

### 5.2 Deep Provenance & Jump-to-Source

* **1-Click Textual Envelope Inspection**: Selecting any node or relation opens a provenance drawer displaying:
* The raw source sentence and paragraph context.
* Extracted entity character offsets highlighted within the original document.
* Full bibliographic metadata (author, journal, year, DOI, section headers).

### 5.3 Human-in-the-Loop (HITL) Curation

* **Curator Actions**:
* In-line edge and node editing: Merge duplicates, split conflated theoretical concepts, adjust edge polarities (e.g.,
  change `SUPPORTS` to `ATTACKS`), or invalidate spurious extractions.


* **Schema Validation Feedback**: Live feedback flagging constraint violations (e.g., invalid edge types between
  incompatible layers or missing mandatory functional dependencies).
* **Non-Destructive Epistemic Audit Trail**: User annotations and modifications are versioned as distinct curation
  commits; original machine extractions remain preserved for auditability.

---

## 6. Querying, Discovery Informatics & Schema Administration

### 6.1 Hybrid Search & Retrieval

* **Dual-Paradigm Querying**: Unified search console accepting:
* **Structured Graph Queries**: Native Cypher queries against Neo4j.
* **Vector Semantic Search**: Dense vector search across node descriptions, textual envelopes, and chunk embeddings.
* **Hybrid Conjunction**: Filter by structural constraints (e.g., paths connecting to specific theoretical terms)
  combined with semantic similarity.


* **Audit & Replay Console**: Library of saved, parameterized query templates for benchmark reproduction.

### 6.2 Literature-Based Discovery (LBD) & Swanson Linking

* **Swanson Bridge Extraction**: Automated detection of indirect inferential pathways:
* Isolates unlinked pairs ($A$ and $B$) connected via intermediate theoretical bridges ($A \rightarrow C \rightarrow B$)
  across disconnected literature silos.


* **Discovery Scorer**: Scores candidate discoveries along four dimensions:
* **Solution Rarity** ($\text{rar} (G)$).
* **Topical Density** ($\text{topd}$).
* **Epistemic Relevance** ($\text{topr}$).
* **Topical Novelty** ($\text{topn}$).


* **Evolutionary Graph Refinement**: Genetic algorithms driven by multi-virtue fitness functions to prune peripheral
  co-occurrence noise and extract high-salience theoretical subgraphs.

### 6.3 Conflict, Uncertainty & Schema Management

* **Neutral Contradiction Management**:
* Explicit 3-state belief indicator: `<Belief, Disbelief, Uncertainty>`.
* Dedicated **Contradiction Workspace** for `WIDERSPRICHT` / `ATTACKS` relationships.
* Strict philosophical policy: System never auto-resolves contradictions; competing theories are presented neutrally as
  framework-relative models.


* **Dynamic Metamodel & Schema Editor**:
* Graphical editor for ontology design: node label definitions, edge typing rules, cardinality restrictions, and inverse
  relationships.
* Corpus-specific schema configurations allowing distinct ontologies across domains without database migrations.

---

## 7. Cross-Cutting Non-Functional Requirements

* **Scalability & Level-of-Detail (LoD) Rendering**:
* Dynamic node aggregation and tiled canvas rendering to sustain responsive interactions on graphs
  containing $> 100{,}000$ active visual elements.
* Server-side job queue handling asynchronous execution of NP-hard graph metrics, Leiden clustering, and QBAF
  convergence algorithms.


* **Epistemic Contextualism**:
* Semantic meaning and tenability scores are explicitly scoped to their governing theoretical framework; nodes must
  reflect context-dependent definitions rather than universal absolute truths.


* **Bilingual Ingestion (DE / EN)**:
* Native cross-lingual alignment linking German and English scholarly discourse, accommodating domain-specific
  philosophical terminology (e.g., *Erkenntniswert*, *Theorie-Element*, *Geltungsbereich*).


* **Reproducibility Manifest**:
* Full export of experiment bundles containing model checkpoints, prompt templates, temperature settings, random seeds,
  and pipeline configurations alongside standard graph formats (GraphML, JSON-LD, Neo4j dumps).

---

## Feature Implementation Roadmap

```
+---------------------------------------------------------------------------------------+
| PHASE 1: CORE WORKBENCH & VISUALIZATION (Months 1-3)                                  |
| * Multi-layer canvas (L1/L2/L3 switchable views)                                      |
| * Provenance drawer (1-click chunk/offset inspection)                                 |
| * Basic Neo4j Cypher querying & vector search                                         |
| * HITL node/edge curation & schema editor                                             |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 2: METRICS & PIPELINE OBSERVABILITY (Months 4-6)                                |
| * Newman Centrality & Leiden community clustering                                     |
| * Pipeline run viewer, Langfuse tracing integration, MIPS candidate audit             |
| * Nováček Virtues (Modesty, Simplicity, Refutability simulation)                      |
| * QBAF gradual semantics & Thagardian ECHO solver                                     |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 3: STRUCTURALIST ENGINE & ADVANCED ANALYTICS (Months 7-9)                       |
| * Model-theoretic decomposition (M_p, M_pp, M, GC, GL)                                |
| * Tenability scoring (TS_local, TS_edge) & Admissible blur sliders                    |
| * Sneedian T-theoreticity classifier & Ramsey sentence verification                   |
| * Diachronic timeline scrubber, version diffing, and Kuhn-loss tracking               |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 4: AUTOMATED DISCOVERY & SYNTHESIS (Months 10-12)                               |
| * Literature-Based Discovery (Swanson A-C-B linking)                                  |
| * Evolutionary graph pruning with multi-virtue fitness functions                      |
| * Automated theoretical survey & epistemological report export                        |
+---------------------------------------------------------------------------------------+

```