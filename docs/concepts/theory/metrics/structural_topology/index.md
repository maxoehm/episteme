# Structural Topology Metrics

The topological metrics in Episteme evaluate the structural integrity, theoretical cohesion, and vulnerabilities of a generated theory graph. 

Because many network properties (like density, connectivity, and centrality) are mathematically intertwined, evaluating them in isolation can lead to redundant or conflicting epistemological diagnoses. Therefore, we organize our structural metrics into a **Dimensional Taxonomy**.

We provide high-level **Composite Indices** for summarizing a theory's performance along these dimensions, while preserving the foundational mathematical metrics for rigorous analysis.

---

## The Three Dimensions of Structural Topology

### Dimension 1: Macro-Topology (Global Cohesion & Economy)
*Answers the question: Is the theory unified, and does it achieve this efficiently without making unnecessary claims?*

* **[Structural Elegance Index](structural_elegance.md)**: The primary composite metric. It evaluates whether a theory achieves robust unification while remaining economically formulated.
  * *Foundational*: [Connectedness & Cohesion](connectedness.md) ($\lambda_2$ / Algebraic Connectivity)
  * *Foundational*: [Modesty](modesty.md) (Inverse Graph Density)

### Dimension 2: Micro-Topology (Vulnerability & Bottlenecks)
*Answers the question: Does the theory rely on a few central dogmas that, if falsified, cause catastrophic structural collapse?*

* **[Bottleneck Fragility Profile](bottleneck_fragility.md)**: The primary composite report. It unifies the detection of central hubs with the mathematical impact of their removal.
  * *Foundational*: [Structural Homogeneity](structural_homogeneity.md) (Node Degree Entropy & Gini)
  * *Foundational*: [Structural Refutability](structural_refutability.md) (Centrality-based shortest path drop)
  * *Foundational*: [Connectedness & Cohesion](connectedness.md) ($k$-connectivity threshold)

### Dimension 3: Meso-Topology (Inter-Theoretical Translation)
*Answers the question: How rigorously do different sub-disciplines or modules connect?*

* **[Community Bridges](community_bridges.md)**: Evaluates whether cross-community links represent genuine theoretical translations (formal constraints) or superficial, ad-hoc lexical associations.

## Logical Integrity Constraints
*Prerequisite Checks: A theory must pass these before structural virtues (like Elegance or Fragility) can be meaningfully evaluated.*

* **[Non-Cyclic Form (DAG Property)](dag_property.md)**: Asserts that intra-theory specialization and derivation relations strictly form a Directed Acyclic Graph. Circular specializations represent logical fallacies.
* **[Tree / Hierarchical Conformity](hierarchical_conformity.md)**: Evaluates whether the specialization DAG strictly conforms to a single-rooted arborescence (Theory-Tree) anchored in a unique fundamental root element $T_0$.

---

## Dimension 4: Socio-Epistemic Alignment
*Answers the question: Does the textual prominence of a hypothesis in the scientific discourse match its actual logical necessity in the theory?*

* **[Centrality & Argumentative Discrepancy](centrality.md)**: Compares structural centrality (Non-Statement-View) against textual discourse prominence (Statement-View) to identify tacit paradigm cores vs. fringe controversies.

---

## Foundational & Utility Metrics

The following metrics support the broader calculation of the dimensions above and are available for deep-dive analysis:

* **[Connectedness & Cohesion](connectedness.md)**: Foundational metric for Elegance and Fragility.
* **[Modesty](modesty.md)**: Foundational metric for Elegance.
* **[Structural Homogeneity](structural_homogeneity.md)**: Foundational metric for Fragility.
* **[Structural Refutability](structural_refutability.md)**: Foundational metric for Fragility.
* **[Modularity Clustering](modularity_clustering.md)**: Base calculations for Louvain/Leiden community detection used in Community Bridges.
