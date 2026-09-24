---
status: needs_verification
tags:
  - Metrics
---

## Introduction & Epistemological Purpose

In the philosophy of science and automated theory analysis, **analogical boost** describes the process by which a novel
hypothesis $H_1$ in a specific field (the *target domain* $D_1$) gains credibility and epistemic weight by mirroring the
mathematical or functional structure of an already established, proven hypothesis $H_2$ from another field (the *source
domain* $D_2$). Classic historical examples include the transfer of model structures from hydrodynamics (water waves) to
acoustics (sound waves) or optics (light waves).

The metric of the **Analogical Boost** (*Lateral Analogical Boost*, $LAB_{\text{norm}}$) quantifies this excitatory
(supporting) effect with mathematical rigor. It combines methods from network theory (regular equivalence on bounded
neighborhoods) with principles from cognitive philosophy of science (Thagard's *Explanatory Coherence*).

---

## Graph-Theoretical Foundations

To process theories and hypotheses mathematically, scientific knowledge is modeled as a directed or undirected **theory
graph** $G = (V, E)$:

* **Nodes $V$**: Represent individual hypotheses, law-like statements, or theory elements $H \in V$. Each node is
  assigned to a specific scientific domain $\text{Dom} (H)$.


* **Edges $E$**: Represent relational dependencies, derivations, or structural interactions between the hypotheses.

### The Concept of Regular Equivalence

Genuine scientific analogies are characterized by the fact that two hypotheses from different fields share hardly any
common technical terms or direct connecting edges, but occupy **the same relational roles** in their respective
subnetworks.

In network theory, two types of node similarities are distinguished:

1. **Structural Equivalence**: Two nodes share the same direct neighbor nodes. (Equivalent to synonymy within the same
   domain).


2. **Regular Equivalence**: Two nodes $H_1$ and $H_2$ are similar if they have neighbor nodes that are themselves
   similarly structured – even if $H_1$ and $H_2$ do not share a single common neighbor. It is precisely this measure
   that captures abstract, cross-domain analogies.

### The $k$-Hop Neighborhood

To prevent distant, irrelevant paths in the theory graph from distorting the similarity measure or slowing down the
calculation, the metric locally restricts the structural analysis to a **$k$-hop neighborhood**. This means that only
relationship paths of maximum length $k$ (edge steps) are considered.

---

## Mathematical Formulation of the Metric

The calculation is performed in three consecutive steps: (1) determination of structural-relational similarity, (2)
calculation of the cross-domain weight, and (3) saturation of the total effect.

### Step 1: Bounded Regular Equivalence ($\text{Sim}_{\text{reg}}^{ (k)}$)

Let A $\mathbf{A}$ be the adjacency matrix, and $\mathbf{D}$ the degree diagonal matrix where the $i$-th diagonal
entry $D_{ii} = \sum_{j} A_{ij}$ corresponds to the total number (or sum of weights) of all outgoing edges from
node $i$. By multiplying with the inverse degree matrix $\mathbf{D}^{-1}$, the rows of $\mathbf{A}$ are scaled so that
their entries provide information about the relative connection proportions (transition probabilities on the graph).
Let $(\cdot)^r$ be the matrix power, where he $r$-th power of the normalized adjacency matrix yields the sum of the
weighted paths of exact length $r$ between two nodes.

The relational similarity of two hypotheses $H_1$ and $H_2$ within a $k$-hop environment is calculated via a damped and
degree-normalized path matrix:

$$\text{Sim}_{\text{reg}}^{ (k)} (H_1, H_2) = \sum_{r=1}^{k} \alpha^r \cdot \left ( (\mathbf{D}^{-1}\mathbf{A})^r \right)_{H_1, H_2}$$

#### Explanation of the mathematical terms in this formula

* **$r$ (Path Length)**: The running index of the sum, which incrementally adds up paths from length $1$ to a maximum
  of $k$.

* **$k$ (Search Depth / $k$-Hop Variable)**: A freely selectable integer control variable ($k \in \mathbb{N}^+$) that
  specifies how far the local network environment should be analyzed.

* **Default Value**: $k_{\text{default}} = 3$ (captures direct connections, 2-edge motifs, and 3-edge contextual
  structures).

* **$\alpha$ (Katz Damping Factor)**: A scalar in the range $0 < \alpha < 1$ that exponentially devalues longer paths
  ($\alpha^r$), since distant relational connections possess less epistemic significance.

---

### Step 2: Cross-Domain Weight Function ($w_{\text{analogy}}$)

To ensure that the metric specifically evaluates analogies between different fields, the structural similarity is
combined with a domain filter:

$$w_{\text{analogy}} (H_1, H_2) = w_{\text{base}} \cdot \phi_{\text{domain}} (H_1, H_2) \cdot \text{Sim}_{\text{reg}}^{ (k)} (H_1, H_2)$$

(Where $\phi_{\text{domain}} (H_1, H_2)$ is the Cross-Domain Indicator Function: A binary control function that checks
whether the two hypotheses originate from different domains:

$$\phi_{\text{domain}} (H_1, H_2) = \begin{cases} 1 & \text{if } \text{Dom} (H_1) \neq \text{Dom} (H_2) \\ 0 & \text{if } \text{Dom} (H_1) = \text{Dom} (H_2) \end{cases}$$

This guarantees that pure intra-domain similarities are not falsely evaluated as analogies.

* **Property of Non-Negativity ($w_{\text{analogy}} \ge 0$)**: Since all components of the formula are
  non-negative, $w_{\text{analogy}} \ge 0$ strictly applies. This guarantees that analogies always form excitatory
  (supporting) connections and never falsely generate inhibitory (contradictory) edges).

---

### Step 3: Normalized Lateral Analogical Boost ($LAB_{\text{norm}}$)

The total boost that the target hypothesis $H_1$ receives from all active analogous source hypotheses $H_2$ in the
network is calculated through a saturated summation over all existing nodes, excluding $H_1$ itself. This accumulation
scales the analogical weight by $a_{H_2} (t) \in [-1, 1]$ representing the overall corroboration of the source
hypothesis at time $t$ (where corroborated hypotheses, $a_{H_2} (t) > 0$, primarily drive the boost). Finally, the
hyperbolic tangent ($\tanh$) is applied as a saturation function mapping the input onto the interval $[0, 1)$, which
prevents the target hypothesis from accumulating infinitely high activation values through the aggregation of many weak
analogies and ensures mathematical stability and convergence during network relaxation.

$$LAB_{\text{norm}} (H_1) = \tanh \left (\sum_{H_2 \in V \setminus \{H_1\}} w_{\text{analogy}} (H_1, H_2) \cdot a_{H_2} (t) \right)$$

---

## Parameter and Variable Overview

| Symbol                        | Name / Meaning                       | Mathematical Type / Range                               | Default Value                |
|-------------------------------|--------------------------------------|---------------------------------------------------------|------------------------------| 
| **$k$**                       | $k$-hop search depth                 | Positive integer ($\mathbb{N}^+$)                       | **$3$**<br>                  |
| **$\alpha$**                  | Katz damping factor                  | Real number in $(0, 1)$<br>                             | **$0.1$**<br>                | 
| **$w_{\text{base}}$**         | Base connection weight               | Real number in $(0, 1]$<br>                             | **$0.2$**<br>                | 
| **$\mathbf{A}$**              | Adjacency matrix of the theory graph | $N \times N$ matrix with $A_{ij} \ge 0$<br>             | From graph structure         | 
| **$\mathbf{D}$**              | Degree diagonal matrix               | $N \times N$ diagonal matrix ($D_{ii} = \sum_j A_{ij}$) | From matrix $\mathbf{A}$<br> |
| **$\phi_{\text{domain}}$**    | Domain filter indicator              | Binary value $\{0, 1\}$<br>                             | $1$ for $D_1 \neq D_2$<br>   | 
| **$a_{H_2} (t)$**             | Activation of the source hypothesis  | Real number in $[-1, 1]$<br>                            | Dynamic from network         | 
| **$LAB_{\text{norm}} (H_1)$** | Normalized analogical boost          | Real number in the interval $[0, 1)$<br>                | Calculated output            |

---

## Literature & References

* **Balzer, W., Moulines, C. U., & Sneed, J. D. (1987)**: *An Architectonic for Science: The Structuralist Program*.
  Reidel Publishing Company.
* **Newman, M. (2018)**: *Networks: An Introduction* (2nd ed.). Oxford University Press.
* **Schurz, G. (2014/2024)**: *Philosophy of Science: A Unified Approach*. Routledge.
* **Stegmüller, W. (1976)**: *The Structure and Dynamics of Theories*. Springer-Verlag.
* **Thagard, P. (1989)**: *Explanatory Coherence*. Behavioral and Brain Sciences, 12 (3), 435–502.