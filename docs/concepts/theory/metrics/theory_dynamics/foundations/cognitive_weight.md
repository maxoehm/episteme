---
status: in_progress
tags:
  - Metrics
  - Foundations
---

# Cognitive Weight $w (P)$

The function $w (P)$ attempts to solve a specific problem: **preventing simple sentence-counting or node-counting from
being mistaken for real scientific progress** (Schurz, 2011, pp. 229–230).

## What is $w (P)$ and What is it Supposed to Do?

We define $w (P)$ as a **cognitive complexity or epistemic weight** assigned to an **irreducible relevant content
element** $P \in E_e (H)$. In a naive graph or set-based metric, every node/proposition has a count of $1$. Under that
naive approach, adding 100 trivial observational statements (e.g., *"Observation #101 of pendulum A swinging in 2.01s"*)
gives 100 times more "progress" than discovering a single grand unifying law (e.g., $\vec{F} = m\vec{a}$) (Schurz, 2011,
pp. 229–230). By using $w (P)$, we effectively scale the value of a content element so that **theoretical depth,
explanatory reach, and cognitive effort** determine progress, rather than raw volume or trivial repetitions.

## What is $w (P)$ Trying to Capture?

Schurz and Lambert identify three main properties that $w (P)$ quantifies:

1. **Cognitive / Epistemic Complexity**: Universal or theoretical claims carry inherently higher weight than localized
   or singular empirical facts.
2. **State-Space Restriction (Information Content)**: A proposition that rules out a huge range of possible physical
   states carries more content (and thus more weight) than a proposition that allows almost anything.
3. **Unificatory / Systematization Value**: A core hypothesis that logically entails or unifies multiple lower-level
   predictions carries higher weight because it performs systemic "work" across the theory-net.

## Operationalizations

We propose four approaches to approximating $w (P)$. Each approach has their own distinct advantages and disadvantages.
While we present them here, they may be found thorought the documentation in different phrasing and contexts, as well as implementation approaches.

### Approach A: Logical & Quantifier Depth (Schurz & Lambert)

In formal philosophy of science, $w (P)$ is operationalized by the **syntactic complexity and scope** of the
formula $P$:

* Singular empirical statements (e.g., $Fa \to Ga$) are assigned a base weight of $w (P) = 1$.
* General laws or universal quantifiers (e.g., $\forall x (Fx \to Gx)$) receive higher weights scaled by quantifier
  depth, domain generality, and predicate complexity.
* This syntactic approach, is highly feasible with our architecture and is implemented. Approach D is more robust and shifts to the structuralist view, is on the other hand, almost non-computable at this point. 

### Approach B: Graph-Theoretic Centrality & Entailment Dependency (Network Science)

In computational theory graphs (e.g., Neo4j or Knowledge Graphs), $w (P)$ can be calculated directly from the **topology
of the graph**:

* **Out-Degree / Downstream Reach**: $w (P)$ is proportional to the number of downstream specializations, empirical
  applications ($M_{pp}$), or observation nodes that logically depend on $P$.
* **Centrality Weighting**: Using algorithms like **Katz Centrality** or **Betweenness Centrality**, a node $P$ that
  sits at the structural root of a theory tree—and whose removal would collapse multiple sub-branches—receives a
  high $w (P)$ score.

### Approach C: Minimum Description Length & Algorithmic Complexity (Information Theory)

Drawing on Chaitin's algorithmic information theory and Bennett's **logical depth**:

* $w (P)$ is measured by the **compressibility / Minimal Description Length (MDL)** of $P$.
* A hypothesis that provides an efficient, non-redundant encoding of complex data has high logical depth.
* We ground $w (P)$ in objective information theory, rewarding hypotheses that maximize information
  compression without redundancy. This alone cannot resolve aspects like the tacking paradox for complex graphs. 

### Approach D: Model-Theoretic State-Space Restriction (Structuralism)

In the model-theoretic triad ($M_p, M, M_{pp}$) of Balzer et al.:

* $w (P) \propto 1 - \frac{|M (P)|}{|M_{pp}|}$, where $M (P)$ is the class of partial potential models that satisfy $P$.
* If $P$ is a tautology, $M (P) = M_{pp}$, so $w (P) = 0$ (no empirical content).
* If $P$ severely restricts the allowed empirical models, $w (P)$ approaches $1.0$.
* It directly reflects Popper's and Sneed's principle that empirical content equals the degree to
  which possible worlds are excluded. An approach to implementing this can be found in our "Tenability Metric"