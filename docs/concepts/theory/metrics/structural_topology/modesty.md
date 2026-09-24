---
status: needs_verification
tags:
  - Metrics
---

# Modesty

## Definition & Conceptual Goal

The **Modesty** metric evaluates how constrained or "bold" a theory-net is by comparing the number of claims it actually
makes to the total number of claims it *could* possibly make (Novacek, 2015). A modest hypothesis minimizes the risk of
wrong or redundant claims by making fewer structural assertions relative to the total entities it spans.

Epistemologically, the probability and the content of hypotheses are often inversely proportional (Schurz, 2026). 
A modest hypothesis maximizes truth chances by avoiding the over-assertion of risky, unproven relationships, whereas 
content-rich, bold claims carry higher risk. Within the structuralist program in philosophy of science, this metric 
reflects how tightly constrained a hierarchical "theory-net" is (Balzer et al., 1987; Stegmüller, 1976).

!!! note "Composite Index Context"
	This is a foundational metric. In our taxonomy, Modesty (Inverse Density) is balanced against Global Cohesion 
	($\lambda_2$) to form the **[Structural Elegance Index](structural_elegance.md)**, which penalizes highly connected
	theories if they are overly dense and immodest.

---

## Theoretical Grounding & Model Formulation

Ideally, modesty is defined as the ratio between all possible simple paths (claims) in a complete graph $H_\omega$ and 
the actual number of simple paths in the hypothesis graph $H$: $\frac{|\Pi(H_\omega)|}{|\Pi(H)|}$ (Novacek, 2015).

Since calculating all possible simple paths in a graph is computationally intractable, Novacek introduces a structural 
approximation that is monotonic to the ideal measure: the **inverse edge density of the graph**.

A completely immodest hypothesis would assert a relationship between every single entity in its domain (a complete
graph). A highly modest hypothesis (a sparse graph) only asserts the exact relationships necessary to hold its structure 
together. This formulation connects directly to the graph-theoretic concepts of network density and sparsity (Newman, 2018).

---

## Mathematical Specification & Graph Formulation

Let $H = (V_H, E_H)$ be the hypothesis or theory subgraph.

Following Newman (2018), the density (or connectance) $\rho$ of a simple network is the fraction of possible edges 
that are actually present: $\rho = \frac{2|E_H|}{|V_H|(|V_H|-1)}$. The Modesty $M (H)$ is mathematically equivalent 
to the inverse of the graph's edge density ($1/\rho$):

$$
M (H) = \frac{|V_H| (|V_H| - 1)}{2|E_H|}
$$

Where:

* $|V_H|$ is the number of vertices.
* $|E_H|$ is the number of edges (claims).

---

## Measurement & Graph Implementation

1. **Count Nodes and Edges**: Query the number of nodes and edges within the target subgraph.
2. **Calculate Ratio**: Compute the inverse density mathematically.

---

## Diagnostic & Metascientific Value

| Measurement Result        | Metascientific Interpretation                                                                              |
|:--------------------------|:-----------------------------------------------------------------------------------------------------------|
| **High Modesty (Sparse)** | The theory makes a minimal number of bold, precise claims.                                                 |
| **Low Modesty (Dense)**   | The theory is structurally "immodest", asserting high interconnectivity that may be redundant or unproven. |

---

## Grounding References

* **[Balzer et al., 1987]** Balzer, W., Moulines, C. U., & Sneed, J. D. (1987). An Architectonic for Science: The Structuralist Program.
* **[Newman, 2018]** Newman, M. (2018). Networks (2nd ed.). Oxford University Press.
* **[Novacek, 2015]** Novacek, V. (2015). Formalising Hypothesis Virtues in Knowledge Graphs: A General Theoretical
  Framework and its Validation in Literature-Based Discovery Experiments.
* **[Schurz, 2026]** Schurz, G. (2026). Philosophy of Science: A Unified Approach.
* **[Stegmüller, 1976]** Stegmüller, W. (1976). The Structure and Dynamics of Theories.
