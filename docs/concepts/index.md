# Theory & Concepts

This section contains the theoretical foundations, formal mathematical models, and epistemological justifications for **Episteme**.

## Purpose

These documents answer **why** architectural choices were made and **what** mathematical and metatheoretical models govern theory graph construction. They are written for researchers, reviewers, and scientific data scientists who need to understand the formal underpinnings of the system.

For software implementation and engineering details, refer to the [System Architecture](../architecture/overview.md) and [Pipeline Architecture](../architecture/pipeline_architecture.md).

---

## Epistemic & Theoretical Foundations

### [From Knowledge Graphs to Theory Graphs](kg_vs_tg.md)

Conceptual distinction between traditional factual knowledge graphs and dialectical theory graphs, explaining why standard entity-relation extraction fails for contested scientific claims.
*Key topics: Epistemic attribution, truth pluralism, dialectical edges, non-factual contestation.*

### [Epistemology & Wissenschaftstheorie](epistemology.md)

Metatheoretical and philosophical criteria governing scientific progress, empirical creativity, and dialectical evaluation. Synthesizes Gerhard Schurz’s theory statics, Imre Lakatos’ research programmes, and Paul Thagard’s explanatory coherence.
*Key topics: Duhem-Quine holism, non-factorizable homogeneity, Degeneration Index, TEC/ECHO, anti-presentism.*

### [Assumptions & Limitations](assumptions_limitations.md)

Rigorous documentation of foundational epistemic assumptions, technical scalability constraints, model biases, and methodological boundaries of the pipeline.
*Key topics: Textual theory representation, LLM competence bounds, compositional hierarchy, scalability constraints.*

---

## Formal Models & Mathematical Foundations

### [Formal Graph Schema (TheoryNet)](formal_graph_model.md)

Canonical mathematical specification of the Theory Graph multigraph isomorphic to logical TheoryNet representations. Establishes the three-layer ontology, gradual argumentation semantics, and Sneedian structuralist model triads.
*Key topics: Multigraph isomorphism, Layer 1–3 ontology, QBAF gradual semantics, DL-LiteR super-roles, mapping laws (Zuordnungsgesetze), uniform spaces, admissible blurs.*

### [Epistemic Grounding & Dense Alignment](dense_alignment.md)

Formal mathematical model for grounding raw textual assertions into unified ontological entities across heterogeneous literature.
*Key topics: Heterogeneous Information Networks (HIN), symmetrical context envelopes, dual-space bi/cross-encoder alignment, two-stage centroid entity maturation.*

### [Theory-Nets, Posets & Topologies](theory_nets_and_topologies.md)

Structural and topological analysis of intra-theory and inter-theory knowledge networks. Formulates theory evolution as partially ordered sets (posets) and provides multi-scale community detection.
*Key topics: Bourbaki structure species, Theory-Trees, horizontal constraints, Theory-Holons, Hierarchical Leiden clustering, topological centrality.*

### [Theory Metrics Subsystem](theory/metrics/index.md)

Formal specification of the 5-pillar mathematical evaluation suite for measuring the structural, coherence, empirical, dynamic, and metatheoretical quality of constructed theory graphs.
*Key topics: Structural topology, epistemic coherence, empirical power, theory dynamics, metatheoretical framework.*

---

## Cognitive Context & Stateful Memory

### [Episodic Working Memory](episodic_working_memory.md)

Theoretical architecture for preserving conversational and epistemic context across sequential document chunks during extraction without quadratic token overhead.
*Key topics: Dual-memory architecture, chapter outline coordinates, decoupled state machine, boundary-based episodic eviction.*

---

## Reference & Terminology

### [Glossary](glossary.md)

Authoritative bilingual reference defining core technical, graph-theoretic, and epistemological terms with complete academic citations and anchors.
*Key topics: Epistemic terminology, structuralist taxonomy, graph metrics, formal concepts.*

---

## Navigation Matrix

| Document | Category | Primary Focus | Key Frameworks & Concepts |
| :--- | :--- | :--- | :--- |
| **[KG vs Theory Graphs](kg_vs_tg.md)** | Epistemic Foundations | Factual vs. dialectical representation | Epistemic attribution, truth pluralism |
| **[Epistemology](epistemology.md)** | Epistemic Foundations | Criteria for scientific progress | Schurz, Lakatos, Thagard |
| **[Assumptions & Limitations](assumptions_limitations.md)** | Epistemic Foundations | Boundary conditions & constraints | Methodological & model bounds |
| **[Formal Graph Schema](formal_graph_model.md)** | Formal Models | Complete TheoryNet specification | Multigraph isomorphism, $L1\text{--}L3$, QBAF, Sneed |
| **[Dense Alignment](dense_alignment.md)** | Formal Models | Coordinate grounding & entity linking | HIN, Bi/Cross-Encoders, Centroid maturation |
| **[Theory-Nets & Topologies](theory_nets_and_topologies.md)** | Formal Models | Posets, trees, and community detection | Bourbaki species, Theory-Holons, Leiden |
| **[Theory Metrics Subsystem](theory/metrics/index.md)** | Formal Models | Quantitative theory evaluation | 5-pillar epistemic metrics |
| **[Episodic Working Memory](episodic_working_memory.md)** | Cognitive Context | Chunk-to-chunk context tracking | Dual-memory, outline coordinates, eviction |
| **[Glossary](glossary.md)** | Reference | Bilingual terminology & citations | Canonical philosophical & formal terms |

---

## Related Documentation

- **System Architecture**: [System Architecture Overview](../architecture/overview.md) and [Pipeline Architecture](../architecture/pipeline_architecture.md)
- **Execution Workflow**: [Workflow Overview](../workflow/index.md)
- **Decisions**: [Architectural Decision Records](../adr/index.md)
- **Research Paper**: [Paper Overview](/paper/index.md)
