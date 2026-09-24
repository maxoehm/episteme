# Glossary

Definitions of key computational, graph-theoretic, and epistemological terms used throughout the Episteme documentation and codebase.

---

## A

### <span id="adu-argumentative-discourse-unit"></span>ADU (Argumentative Discourse Unit)
A segment of text that functions as an atomic argumentative component, such as an empirical premise, theoretical claim, or deductive conclusion.

### <span id="approximative-empirische-adaquatheit-approximative-empirical-adequacy"></span>Approximative Empirical Adequacy (Approximative empirische Adäquatheit)
The degree of empirical agreement between observed data $I$ and theoretical models $M$ under real-world measurement tolerances. It is fulfilled if the deviation remains strictly within the boundaries of admissible blurs ($\exists X \in \text{Cn}(K) \text{ s.t. } I \approx_A X$) ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="apoc-awesome-procedures-on-cypher"></span>APOC (Awesome Procedures On Cypher)
Neo4j plugin providing additional graph algorithms, data integration utilities, and procedural cypher extensions.

### <span id="argumentative-diskrepanz"></span>Argumentative Discrepancy (Argumentative Diskrepanz)
A tension between normative rational reconstruction and historical description where structurally foundational, high-centrality axioms (implicit core hypotheses) are barely mentioned in surface text. Reflects the gap between the context of discovery and the context of justification ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3)).

### <span id="artifact"></span>Artifact
Persistent, content-addressed output from a pipeline phase (stored under `.pipeline_artifacts/`) for execution caching, resume workflows, and auditability.

---

## B

### <span id="balzer-gahde-invarianz-kriterium"></span>Balzer-Gähde Invariance Criterion (Balzer-Gähde Invarianz-Kriterium)
A formal structuralist criterion stating that a concept $t$ is non-theoretical with respect to a theory $T$ if it remains invariant under arbitrary theoretical modifications as long as the fundamental laws are preserved ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

---

## C

### <span id="centrality"></span>Centrality
A structural graph-theoretic metric quantifying the relative topological importance, influence, or prominence of a node within a network ([Newman, 2018](https://doi.org/10.1093/oso/9780198805090.001.0001)). See also [Degree Centrality](#degree-centrality), [Eigenvector Centrality](#eigenvector-centrality), and [PageRank](#pagerank).

### <span id="chunk"></span>Chunk
A segment of parsed document text (typically 500–1500 tokens) partitioned along rhetorical section boundaries, serving as the unit of ingestion in Layer 1.

### <span id="concept"></span>Concept
An abstract theoretical entity representing an intellectual notion, paradigm construct, or philosophical category.

### <span id="confidence-score"></span>Confidence Score
A normalized numerical measure ($c \in [0, 1]$) indicating extraction certainty or relationship validity.

### <span id="constraint-c"></span>Constraint ($C, CL$)
A cross-application relational constraint ($C \subseteq \mathcal{P}(M_p)$) demanding that intrinsic theoretical parameters (e.g., mass, charge, or utility preferences) maintain invariant, identical values when an entity appears across overlapping application domains ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3); [Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

---

## D

### <span id="degree-centrality"></span>Degree Centrality
A baseline centrality metric defined as the number of edges incident to a node. Distinguished in directed graphs as in-degree (incoming connections, indexing prestige or evidentiary vulnerability) and out-degree (outgoing connections, indexing deductive generative power) ([Newman, 2018](https://doi.org/10.1093/oso/9780198805090.001.0001)).

### <span id="degenerations-index-lakatosianische-degeneration"></span>Degeneration Index (Lakatosianische Degeneration)
The ratio of ad-hoc resolved anomalies (Type-b failures) to the sum of verified empirical successes and honest direct refutations ($D = |M_b| / (|E| + |M_a|)$). A monotonically rising index indicates a degenerating research programme ([Schurz, 2014](https://doi.org/10.1007/978-3-658-05898-2); [Lakatos, 1978](https://doi.org/10.1017/CBO9780511621123)).

---

## E

### <span id="eigenvector-centrality"></span>Eigenvector Centrality
A spectral centrality metric where a node's score is proportional to the sum of the centralities of its neighbors ($x_i = \kappa^{-1} \sum_j A_{ij} x_j$), weighting connections by the relative prominence of adjacent nodes ([Newman, 2018](https://doi.org/10.1093/oso/9780198805090.001.0001)).

### <span id="empirical-focus-empirischer-fokus"></span><span id="empirischer-fokus-empirical-focus"></span>Empirical Focus (Empirischer Fokus)
The capacity of theoretical terms and their constraints to restrict the volume of admissible observable states, thereby increasing the theory's empirical content and refutability ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3)).

### <span id="entity"></span>Entity
A conceptual or real-world object extracted from text, typed according to an ontology (e.g., *Concept*, *Person*, *Theory*, *Work*).

### <span id="entity-linking"></span>Entity Linking
The algorithmic process of resolving surface text mentions across distinct chunks and documents to a stable canonical node ID using dense vector similarity and cross-encoder reranking.

### <span id="epistemic-cycle-epistemischer-zyklus"></span><span id="epistemischer-zyklus-epistemic-cycle"></span>Epistemic Cycle (Epistemischer Zyklus)
The methodological danger of circular justification arising when the centrality of a node is determined purely through a graph network whose own validity is grounded in that same node ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3); [Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="event-emitter"></span>Event Emitter / Domain Event Bus
An asynchronous publish-subscribe subsystem broadcasting structured domain events during pipeline execution for telemetry, logging, and Langfuse tracing.

---

## F

### <span id="faithfulness"></span>Faithfulness
An intrinsic evaluation metric measuring whether extracted entities and relations are strictly warranted by the source text without hallucination.

### <span id="fusion"></span>Fusion
Phase 5 of the pipeline, which clusters semantically equivalent argument components across documents and computes macroscopic theoretical communities via the Leiden algorithm.

---

## G

### <span id="graph-schema"></span>Graph Schema
The formal specification of allowed vertex labels, relationship edge types, and property constraints within the Neo4j property graph.

### <span id="graph-store"></span>Graph Store
The persistent graph database backend (Neo4j) accessed via an asynchronous Cypher driver.

---

## H

### <span id="homogenitat"></span>Homogeneity (Homogenität)
The overarching requirement of structural, semantic, or methodological unity within a scientific theory.

* <span id="homogenitat-methodologische-konstruktvaliditat"></span>**Methodological Homogeneity (Konstruktvalidität):** Ensures empirical indicators strongly correlate because they measure a common theoretical latent cause.
* <span id="homogenitat-semantisch-axiomatische"></span>**Semantic-Axiomatic Homogeneity:** A formal non-factorizability criterion stating that an axiomatization $Ax$ cannot be partitioned into disjoint subsets whose empirical consequences are mutually independent, preventing the Tacking Paradox ([Schurz, 2014](https://doi.org/10.1007/978-3-658-05898-2)).

---

## I

### <span id="intertheoretische-links-community-bridges"></span>Intertheoretical Links / Community Bridges
Directed relational edges connecting distinct theory-elements across different disciplines or schools of thought. Genuine theoretical translations preserve global homogeneity, whereas ad-hoc bridge edges violate it ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

---

## K

### <span id="katz-centrality"></span>Katz Centrality
An extension of eigenvector centrality assigning a baseline score $\beta$ to all nodes in addition to the weighted sum of neighbor centralities ($x_i = \alpha \sum_j A_{ij} x_j + \beta$), preventing vanishing scores in directed acyclic topologies ([Newman, 2018](https://doi.org/10.1093/oso/9780198805090.001.0001)).

### <span id="knowledge-graph"></span>Knowledge Graph (KG)
A traditional factual graph focusing on concrete real-world entities and deterministic relations, contrasted with dialectical Theory Graphs.

---

## L

### <span id="litellm"></span>LiteLLM
A unified provider-agnostic abstraction layer standardizing API calls to OpenAI, Anthropic, Ollama, and local models.

### <span id="llm-large-language-model"></span>LLM (Large Language Model)
Deep transformer models utilizing billions of parameters for contextual text understanding, extraction, and argument classification.

---

## M

### <span id="misserfolg-typ-a-direkter-widerspruch"></span>Failure Type a / Direct Contradiction (Misserfolg Typ a)
A well-established empirical observation that logically or probabilistically contradicts a theory version directly via *Modus Tollens* ([Schurz, 2014](https://doi.org/10.1007/978-3-658-05898-2)).

### <span id="misserfolg-typ-b-immunisierter-misserfolg-scheinbarer-erfolg"></span>Failure Type b / Immunized Failure (Misserfolg Typ b)
An empirical anomaly that contradicted an earlier theory version, but was neutralized in the current version via an ad-hoc auxiliary clause without generating verified novel predictions. Remains a latent failure in the Degeneration Index ([Schurz, 2014](https://doi.org/10.1007/978-3-658-05898-2)).

---

## N

### <span id="ner-named-entity-recognition"></span>NER (Named Entity Recognition)
The process of identifying and categorizing named entities and abstract concepts within text chunks.

### <span id="non-statement-view-modell-ansatz"></span>Non-Statement View / Model-Theoretic Approach (Modell-Ansatz)
The structuralist philosophy of science perspective that analyzes theories as classes of mathematical model structures ($M_p, M, M_{pp}$) rather than flat sets of linguistic sentences ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3); [Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

---

## P

### <span id="pagerank"></span>PageRank
A variant of Katz centrality that scales a node's contributed centrality inversely by its out-degree, preventing nodes with broad broadcast connectivity from disproportionately inflating target scores ([Newman, 2018](https://doi.org/10.1093/oso/9780198805090.001.0001)).

### <span id="perspektive-historische-adaquatheit"></span>Perspective / Historical Adequacy (Perspektive)
The degree of conceptual congruence between a formal reconstruction of a theory and the measurement apparatus and observational vocabulary historically available at time $t$, avoiding presentism ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3)).

### <span id="phase"></span>Phase
A discrete stage of pipeline execution with strictly defined Pydantic input and output boundaries.

### <span id="prognostische-leistung-prognostic-power"></span>Prognostic Power (Prognostische Leistung)
The capacity of theoretical constraints crossing overlapping application domains to enable strict empirical predictions in previously unmeasured domains ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3)).

### <span id="provenance"></span>Provenance
Deterministic tracking metadata (chunk ID, character offsets, source citation) connecting graph elements directly to source literature.

---

## R

### <span id="ramsey-sneed-behauptung-ramsey-sneed-sentence"></span>Ramsey-Sneed Claim (Ramsey-Sneed-Behauptung)
The structuralist method for eliminating circularity in theoretical terms by asserting that an empirically described situation ($M_{pp}$) can be enriched by theoretical functions such that the resulting structure constitutes a valid model ($M$) satisfying global constraints ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="relationship"></span>Relationship
A directed edge connecting two entities or argument components, annotated with semantic type and confidence.

### <span id="retrospektive-verzerrung-presentism"></span>Retrospective Bias / Presentism (Retrospektive Verzerrung)
The historiographical flaw of analyzing historical scientific theories through modern concepts or measurement standards unavailable to the original authors ([Schurz, 2014](https://doi.org/10.1007/978-3-658-05898-2)).

---

## S

### <span id="same_as"></span>SAME_AS
A structural equivalence relationship indicating that two entity mentions or argument components across different texts denote the identical concept.

### <span id="sneedsches-funktionales-kriterium-fur-t-theoretizitat"></span>Sneed's Functional Criterion for T-Theoreticity (Sneed'sches Kriterium)
A criterion defining a term $\tau$ as $T$-theoretical if every available method for determining its value presupposes the validity of the laws of $T$ ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="starke-idealisierte-empirische-adaquatheit-newmans-problem"></span>Strong Empirical Adequacy (Starke empirische Adäquatheit)
The idealized condition that all intended applications $I$ can be enriched into exact theoretical models without observational noise ($I \in \text{Cn}(K)$). In practice, replaced by Approximative Empirical Adequacy with admissible blurs ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="statement-view-satz-ansatz"></span>Statement View (Satz-Ansatz)
The traditional linguistic view of scientific theories as flat sets of verbal or axiomatic sentences, contrasted with the structuralist model-theoretic approach ([Stegmüller, 1976](https://doi.org/10.1007/978-3-642-66440-3)).

---

## T

### <span id="tacking-paradoxie"></span>Tacking Paradox (Klebeparadoxon)
The logical anomaly where conjoining an arbitrary irrelevant hypothesis $H$ to a confirmed theory $T$ technically increases its empirical content ($E(T \wedge H) \supset E(T)$). Prevented by demanding axiomatic homogeneity ([Schurz, 2014](https://doi.org/10.1007/978-3-658-05898-2)).

### <span id="theorie-baum-theory-tree"></span>Theory-Tree (Theorie-Baum)
A specialization hierarchy $(TN, \alpha)$ characterized by a singleton root element $T_0$ ($B(N) = \{T_0\}$), ensuring that all specialized variants descend from a single fundamental core ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="theorie-holon"></span>Theory-Holon (Theorie-Holon)
The macroscopic global network of all scientific theories, interconnected via directed intertheoretical links and community bridges ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).

### <span id="theory-graph"></span>Theory Graph (TheoryNet)
A layered property graph and argumentation network ($TF = (At, R) \cong G = (V, E, \lambda_v, \lambda_e)$) capturing conceptual abstractions, evidentiary dependencies, and defeasible arguments.

### <span id="triple"></span>Triple
A subject-predicate-object semantic assertion with associated confidence and scope (local vs. global).

---

## V

### <span id="vector-index"></span>Vector Index
Neo4j or in-memory vector index enabling dense Maximum Inner Product Search (MIPS) over contextual embeddings.

---

## W

### <span id="workflow"></span>Workflow
The coordinated execution sequence of pipeline phases transforming raw documents into materialized Theory Graphs.

---

## Z

### <span id="zulassige-unscharfen-admissible-blurs-a"></span>Admissible Blurs (Zulässige Unschärfen, $\mathcal{A}$)
The family of acceptable empirical error tolerances within a uniform space $(M_p, \mathcal{U})$, enabling realistic evaluation of approximative adequacy while preventing vacuous immunization ([Balzer et al., 1987](https://doi.org/10.1007/978-94-009-3759-8)).
