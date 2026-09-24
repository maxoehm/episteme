---
status: needs_verification
tags:
  - Metrics
---

# Structural Refutability

## Definition & Conceptual Goal

The **Structural Refutability** metric quantifies the topological fragility of a hypothesis or theory graph. Unlike
semantic refutability (which measures logical predictions), structural refutability measures how easily the overarching
claim volume of the graph collapses if its most structurally vital concepts are invalidated or removed (Novacek, 2015).

It answers the question: *What is the weakest link in the network, and how many claims must be falsified until the
theory splits into heterogeneous, non-connected parts?* This serves as a structural proxy for "Hard Falsifiability."

!!! note "Composite Index Context"
   This is a foundational metric. In our taxonomy, the mathematical impact of breaking central hubs (Top-$k$ Refutability)
   is unified with the presence of those hubs (Homogeneity) to form the overall
   **[Bottleneck Fragility Profile](bottleneck_fragility.md)**.

---

## Theoretical Grounding & Model Formulation

A highly structurally refutable hypothesis relies heavily on a few critical conceptual bottlenecks. If one of these
bottlenecks is falsified, the entire structure shatters, losing its explanatory power. Conversely, a theory with low
structural refutability is highly redundant and robust; falsifying one concept does not significantly disrupt the
overall network of claims.

This concept is strictly bounded by **$k$-connectivity**: a theory with a vertex connectivity of $k$ requires the
falsification of at least $k$ distinct core concepts to shatter.

---

## Mathematical Specification & Graph Formulation

Let $H$ be the theory subgraph.

### Hard Falsifiability Bound ($k$-connectivity)

The absolute minimum threshold for shattering the graph is its vertex connectivity $\kappa (H)$, defining the fewest
number of nodes required to disconnect the graph.

### Top-$k$ Refutability Score (Centrality-based)

To measure the real-world impact of targeted falsification, we rank the vertices $v \in V_H$ by their **Betweenness
Centrality**. Let $R (i)$ be the $i$-th ranked vertex.

The top-$k$ refutability is defined as:

$$
\text{Refutability}_k (H) = \frac{|\Pi (H)|}{|\Pi (H)| + \sum_{i=1}^k |\Pi (H/R (i))|}
$$

Where:

* $|\Pi (H)|$ is the number of shortest paths (claims) in the original graph.
* $H/R (i)$ is the graph after removing the $i$-th most central vertex.
* Removing highly central nodes that cause a massive drop in shortest paths results in a higher refutability score.

---

## Measurement & Graph Implementation

1. **Calculate Connectivity Bounds**: Find $\kappa (H)$ to determine the absolute minimum falsification threshold
   required for structural collapse.
2. **Calculate Centrality**: Compute the betweenness centrality for all nodes in the theory subgraph.
3. **Node Removal Simulation**: Iteratively "remove" the top $k$ nodes (often $k=1$ is sufficient).
4. **Path Re-computation**: Calculate the drop in the total number of shortest paths across the remaining subgraph to
   score the theory's fragility.

---

## Diagnostic & Metascientific Value

| Measurement Result                                    | Metascientific Interpretation                                                                              |
|:------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------|
| **High Refutability (Low $\kappa$, huge path drop)**  | The theory relies on highly critical assumptions. Falsifying one shatters the theory (highly falsifiable). |
| **Low Refutability (High $\kappa$, redundant paths)** | The theory is structurally redundant and robust. It can easily absorb anomalies (Quinean web).             |

---

## Grounding References

* **[Novacek, 2015]** Novacek, V. (2015). Formalising Hypothesis Virtues in Knowledge Graphs.
