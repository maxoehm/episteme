---
status: needs_verification
tags:
  - Metrics
---

# Tenability (Haltbarkeit)

!!! info ""
    **Implementation:** Implemented as a post-processing pass in [Theoretical Enrichment & Tenability Evaluation](../../../../reference/theoretical_enrichment.md) and governed by [ADR 0015: Theoretical Enrichment and Tenability Evaluation](../../../../adr/0015-theoretical-enrichment-and-tenability-evaluation.md).

## Definition & Conceptual Goal

The **Tenability (Haltbarkeit)** metric evaluates whether a theory's empirical claim can be considered approximately
true or highly plausible given a set of empirical observations
([Stegmüller, 1976, pp. 120, 270](zotero://select/library/items/2WXH9HSL); [Schurz, 2024, sec. 2.3](zotero://select/library/items/24SNSW2B)).
In the non-statement view of scientific theories, a theory is reconstructed not as a system of linguistic statements,
but as a system of set-theoretical models ([Stegmüller, 1976, pp. 7, 75](zotero://select/library/items/2WXH9HSL)).

While **[Empirical Adequacy](../empirical_power/empirical_adequacy.md)** measures numerical agreement and residual blur tolerances, *tenability* represents the non-trivial truth of the
theory's empirical claim ([Stegmüller, 1976, pp. 78, 101](zotero://select/library/items/2WXH9HSL)): it ensures that the
set of intended applications ($I$)—which have the structure of partial potential models ($M_{pp}$) consisting only of
non-theoretical, theory-independent concepts
([Stegmüller, 1976, pp. 86, 107](zotero://select/library/items/2WXH9HSL); [Schurz, 2024, sec. 2.3](zotero://select/library/items/24SNSW2B))
—can be theoretically enriched by postulating theoretical terms (such as mass or force)
([Stegmüller, 1976, pp. 77, 121](zotero://select/library/items/2WXH9HSL)) in a way that simultaneously satisfies the
core physical laws ($M$), the global inter-application constraints ($GC$), and the intertheoretical links ($GL$) of the
theory-core ([Stegmüller, 1976, pp. 78, 94](zotero://select/library/items/2WXH9HSL)).

---

## Theoretical Grounding & Model Formulation

In structuralist metatheory, a theory-element is represented as $T = \langle K, I \rangle$, where the core is
$K = \langle M_p, M, M_{pp}, GC, GL \rangle$ ([Stegmüller, 1976, p. 94](zotero://select/library/items/2WXH9HSL)). The
set of intended applications $I$ is a subset of the partial potential models ($I \subseteq M_{pp}$)
([Stegmüller, 1976, pp. 86, 94](zotero://select/library/items/2WXH9HSL)). Within the context of our Theory Graph, the
set of intended applications $I$ corresponds to subsets of the empirical base $B$ (Empirical Observation Sentences). An
intended application is thus formed by empirical observations $b \in I \subseteq B$.

The idealized empirical claim of the theory asserts that the intended applications can be enriched to full models
satisfying all constraints and links ([Stegmüller, 1976, pp. 78, 94](zotero://select/library/items/2WXH9HSL)):
$$I \in \mathrm{Cn} (K)$$
Where the content $\mathrm{Cn} (K)$ is the class of sets of partial potential models that are the non-theoretical
restrictions of sets of models satisfying the constraints $GC$ and links $GL$
([Stegmüller, 1976, pp. 78, 94](zotero://select/library/items/2WXH9HSL)).

### The Need for Continuous Approximation over Binary Thresholds

In real-world scientific texts, NLP-extracted graphs, and empirical data, absolute exactness is an idealization.
Therefore, tenability must be modeled utilizing the formal structuralist apparatus of **uniformities ($U$)** and
**admissible blurs ($\mathcal{A}$)**
([Stegmüller, 1976, pp. 75, 110](zotero://select/library/items/2WXH9HSL); [Balzer et al., 1987, pp. 209–217](zotero://select/library/items/24SNSW2B)).

A classical binary threshold (such as defining $\text{Score} = 1 \text{ if error } < \epsilon \text{ else } 0$)
introduces a sharp, non-differentiable step-function. In graph-based extraction and empirical scientific domains, this
binary discontinuity is deeply problematic:

* A theory that misses a hard threshold by an infinitesimal margin (e.g., error is $0.1001$ instead of $0.1000$) would
  abruptly be classified as completely untenable ($\text{Score} = 0$).
* Conversely, all theories meeting the threshold would be treated as equally "perfect" ($\text{Score} = 1$), obscuring
  meaningful gradations in empirical fit.

Rather than a binary truth value, Tenability is operationalized as a robust, continuous structural compatibility score
in the interval $[0, 1]$ ([Stegmüller, 1976, p. 101](zotero://select/library/items/2WXH9HSL)), assessing the degree of
approximation required to satisfy both local laws and global constraints
([Stegmüller, 1976, pp. 76, 116](zotero://select/library/items/2WXH9HSL)). This gradualism is philosophically aligned
with the concept of **truthlikeness (verisimilitude)** and approximate truth
([Schurz, 2024, sec. 2.3](zotero://select/library/items/24SNSW2B); [Stegmüller, 1976, pp. 56, 106](zotero://select/library/items/2WXH9HSL)):
a theory is not simply "true" or "false," but possesses a measurable degree of empirical success and tolerance
([Stegmüller, 1976, pp. 76, 101](zotero://select/library/items/2WXH9HSL)).

### The Topology of Uniform Spaces vs. Metric Spaces

In Sneed's and Stegmüller's metatheory, approximation is formalized using Bourbaki's **uniform spaces** rather than
metric spaces ([Bourbaki, 1966]; [Stegmüller, 1976, pp. 110, 115](zotero://select/library/items/2WXH9HSL)). This
topological approach is crucial because scientific theories routinely deal with heterogeneous physical quantities (e.g.,
measuring positions in meters, times in seconds, and masses in kilograms)
([Stegmüller, 1976, pp. 113, 137](zotero://select/library/items/2WXH9HSL)). There is no single, natural, universal
metric distance function $d (x, y)$ that can combine these different dimensions without introducing arbitrary scaling
factors ([Stegmüller, 1976, p. 113](zotero://select/library/items/2WXH9HSL)).

Instead of a single metric distance, a **uniformity $U$** specifies a family of nested relational "blurs"
$\{u_\delta\}$ ([Stegmüller, 1976, pp. 111, 112](zotero://select/library/items/2WXH9HSL)). Because one cannot simply
write "$\text{distance} < x$," the framework utilizes this family of blurs. Topological neighborhood inclusion is
thereby translated into a rigorous basis for continuous approximation.

---

## Mathematical Specification & Graph Formulation

Let $y \in I \subseteq M_{pp}$ be an empirical data node (representing a partial potential model containing only
non-theoretical variables)
([Stegmüller, 1976, pp. 86, 107](zotero://select/library/items/2WXH9HSL)).

### The Dual-Enrichment Architecture ($\Phi$)

To computationally implement theoretical enrichment in a graph pipeline without assuming a mathematically untenable
universal parametric space, the enrichment function $\Phi (y)$ is constructed as a composite function:

$$\Phi (y) = \Phi_{\text{spec}} (\Phi_{\text{gen}} (y))$$

1. **General Enrichment ($\Phi_{\text{gen}}$):** A domain-agnostic parser that maps raw data (or text) into an abstract
   structural space. Rather than physical metrics, its dimensions consist of structural and relational properties:
	* **Topology:** Set-theoretic relations (e.g., is node $A$ a subset of $B$?)
	* **Causality:** Directed acyclic graphs (e.g., does an edge go from $A \to B$?)
	* **Covariance:** Monotonicity and logical correlation (e.g., if $A$ increases, does $B$ increase?)

    It yields an abstract graph where baseline structural tenability (e.g., checking for logical contradictions
   like $A \to B$ and $B \to A$ where strict acyclicity is required) can be evaluated, but lacks empirical metric
   dimensions.

2. **Specific Enrichment ($\Phi_{\text{spec}}$):** An ontological projector that receives the abstract graph and
   projects it into the bespoke parametric space of the specific theory ($M_p$). By assigning precise dimensions (e.g.,
   "mass" in $\mathbb{R}^+$), it establishes the local metric rules where the blur $\delta$ is actually evaluated.

This composite $\Phi (y)$ maps the partial potential model $y$ to a full potential model $x = \Phi (y) \in M_p$ by
adding theory-specific theoretical terms.

Let $M \subseteq M_p$ be the set of actual models satisfying the fundamental laws
([Stegmüller, 1976, p. 78](zotero://select/library/items/2WXH9HSL)). Let $U$ be an empirical uniformity on $M_p$, and
let $u_{\delta} \in \mathcal{A}$ denote a scaled admissible blur (inaccuracy neighborhood) associated with the theory
([Stegmüller, 1976, pp. 76, 115](zotero://select/library/items/2WXH9HSL)).

### Local Tenability Score ($TS_{\text{local}}$) and Parameter Estimation

The local tenability of an empirical application node $y \in I$ measures how closely its theoretical enrichment
satisfies the fundamental law $M$, utilizing the supremum over acceptable approximations:

$$TS_{\text{local}} (y, M) = \sup \{ 1 - \delta \mid \exists x^* \in M : (\Phi (y), x^*) \in u_{\delta} \}$$

#### Rationale for the Supremum ($\sup$) over Blurs

In scientific practice, theoretical parameters (e.g., the mass of a planet, a gravitational constant, or the coupling
strength of a node) are not directly observed; they are estimated post-factum from raw empirical observations
([Stegmüller, 1976, pp. 57, 61](zotero://select/library/items/2WXH9HSL)). This corresponds to the enrichment function
$\Phi (y)$ which postulates values for these theoretical terms
([Stegmüller, 1976, p. 121](zotero://select/library/items/2WXH9HSL)).

We do not merely ask whether *some* parameter set meets an arbitrary threshold; we actively search for the **best
possible fit** ([Stegmüller, 1976, p. 61](zotero://select/library/items/2WXH9HSL)). Mathematically, finding the
best-fitting model is an optimization problem (analogous to the method of least squares
([Stegmüller, 1976, p. 61](zotero://select/library/items/2WXH9HSL))):
$$\text{Minimize } \delta \quad \text{subject to } \Phi (y) \in u_\delta \text{ of some } x^* \in M$$

Minimizing the error $\delta$ is mathematically equivalent to **maximizing the structural compatibility score**
$1 - \delta$ ([Stegmüller, 1976, p. 26](zotero://select/library/items/2WXH9HSL)). The supremum ($\sup$) represents this
exact optimization process: it finds the **finest, most precise neighborhood $u_\delta$ in our family of blurs** that
can still successfully reconcile our empirical data with the laws of the theory
([Stegmüller, 1976, pp. 115, 119, 147, 148](zotero://select/library/items/2WXH9HSL)). This elegantly translates pure
topological neighborhood inclusion into a continuous, normalized numerical confidence score for graph processing.

* **Boundary Conditions**: If the system satisfies the law exactly, $\delta = 0 \implies TS_{\text{local}} = 1.0$. If no
  admissible approximation exists within the boundaries of $\mathcal{A}$, the score drops to $0.0$
  ([Stegmüller, 1976, p. 142](zotero://select/library/items/2WXH9HSL)).

### Edge Tenability Score ($TS_{\text{edge}}$) via Global Constraints

Constraints ($GC$) prevent triviality by linking theoretical parameters (e.g., mass, coupling constants) across
different applications ([Stegmüller, 1976, p. 108](zotero://select/library/items/2WXH9HSL)).
Let $e = (y_a, y_b) \in I \times I$
be a constraint edge representing an inter-application relation. Under a constraint blur $v_{\delta_C} \in \mathcal{A}$,
the consistency of theoretical values across the edge is operationalized as:

$$TS_{\text{edge}} (e) = \sup \{ 1 - \delta_C \mid (\Phi (y_a), \Phi (y_b)) \in v_{\delta_C} \}$$

### Propagated Tenability

If a theoretical value is calculated at node $y_a$ (where $TS_{\text{local}} (y_a)$ is known) and projected onto a new
node $y_b$ via a constraint edge $e = (y_a, y_b)$, the predicted tenability at $y_b$ is the product of the node's local
tenability and the edge consistency:

$$\text{Tenability}_{\text{pred}} (y_b) = TS_{\text{local}} (y_a, M) \cdot TS_{\text{edge}} (e)$$

### Aggregated Tenability of a Theory-Element $T$

To evaluate the global tenability of the theory-element $T = \langle K, \mathcal{A}, I \rangle$ over the graph of its
applications $I$ and constraint edges $E_{GC}$, we define the weighted average:

$$\text{Tenability} (T) = w_{\text{local}} \cdot \left (\frac{1}{|I|} \sum_{y \in I} TS_{\text{local}} (y, M) \right) + w_{\text{edge}} \cdot \left (\frac{1}{|E_{GC}|} \sum_{e \in E_{GC}} TS_{\text{edge}} (e) \right)$$

Where $w_{\text{local}}, w_{\text{edge}} \in [0,1]$ are weights such that $w_{\text{local}} + w_{\text{edge}} = 1$,
representing the balance between local law-adherence and global cross-application consistency.

---

## Measurement & Graph Implementation

1. **Schema Typing & Model Verification**: Compare extracted empirical entity attributes and observation spans against
   the formal predicate signatures in the theory's `:PotentialModelClass` ($M_p$) and non-theoretical base ($M_{pp}$).
2. **Theoretical Enrichment ($\Phi$)**: Apply $\Phi_{\text{gen}}$ to extract the domain-agnostic relational graph, then
   apply $\Phi_{\text{spec}}$ to instantiate domain-specific theoretical edges and parameters connecting empirical
   observation nodes $y \in I$ to candidate model structures $x \in M_p$.
3. **Local Inaccuracy Minimization**: Determine the tightest admissible blur $u_\delta \in \mathcal{A}$ reconciling
   enriched empirical instances with theoretical laws $M$, computing $TS_{\text{local}} (y, M) = 1 - \delta^*$.
4. **Constraint Consistency Evaluation**: Evaluate inter-application constraint edges $e = (y_a, y_b) \in E_{GC}$,
   scoring theoretical parameter consistency across applications under constraint blurs $v_{\delta_C}$.
5. **Graph Inspection & Anomaly Flagging**: Application nodes or constraint edges with $TS < 0.5$ are flagged as
   category errors, severe law deviations, or cross-application parameter incompatibilities.

---

## Diagnostic & Metascientific Value

| Tenability Score                  | Conceptual Fit             | Metascientific Interpretation                                                                                           |
|:----------------------------------|:---------------------------|:------------------------------------------------------------------------------------------------------------------------|
| $\text{Tenability} \ge 0.8$       | High Tenability            | Applications naturally instantiate the theory; theoretical terms reconcile empirical data within tight blurs.           |
| $0.5 \le \text{Tenability} < 0.8$ | Approximative Fit          | Acceptable empirical fit; minor deviations or tolerable constraint tensions present across applications.                |
| $\text{Tenability} < 0.5$         | Category Error / Untenable | Attempt to apply framework to an ontologically mismatched domain or failure to satisfy laws within blurs $\mathcal{A}$. |

---

## Grounding References

* **[Stegmüller, 1976]** Stegmüller, W. (1976). *The Structure and Dynamics of Theories*. Springer-Verlag, pp. 7, 26,
  56–61, 75–121, 137–148, 270.
* **[Schurz, 2024]** Schurz, G. (2024). *Philosophy of Science: A Unified Approach*. Routledge, sec. 2.3.
* **[Balzer et al., 1987]** Balzer, W., Moulines, C. U., & Sneed, J. D. (1987). *An Architectonic for Science*. Reidel
  Publishing Company, pp. 209–217.
* **[Bourbaki, 1966]** Bourbaki, N. (1966). *General Topology: Part 1*. Hermann / Addison-Wesley, Chapter II: Uniform
  Structures.
* **[Sneed, 1971]** Sneed, J. D. (1971). *The Logical Structure of Mathematical Physics*. Reidel Publishing Company.
