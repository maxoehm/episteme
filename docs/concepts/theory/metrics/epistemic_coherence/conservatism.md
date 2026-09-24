---
status: needs_verification
tags:
  - Metrics
---

# Conservatism & Epistemic Safety

## Definition & Conceptual Goal

The following metric will discuss two core metrics from epistemology and scientific theory.

* **Conservatism** evaluates the *conceptual detour* of a claim. A conservative theory introduces incremental semantic
  steps that stay closely anchored to known paradigms, whereas radical hypotheses make large conceptual leaps across
  disparate topics (Novacek, 2015).
* **Epistemic Safety** evaluates the *evidential decay* of a claim. It measures how much confidence is retained when
  traversing the chain of reasoning from empirical axioms to a final conclusion.

---

## Topological Preconditions

To calculate both metrics, the underlying theory graph (as defined in Layer 3 of the Formal Model) must explicitly
support a directed argumentative structure. The metrics require identifiable paths representing the flow of inference,
specifically originating from an empirical core and terminating at a theoretical claim.

A standard required path structure takes the form:

```mermaid
flowchart LR
    Source([Empirical Sentences]) --> H[Hypothesis]
    H --> P[Premises]
    P --> AL[Assignment Laws]
    AL --> Target([Conclusion])
    style Source fill: #e1f5fe, stroke: #01579b, stroke-width: 2px
    style Target fill: #fce4ec, stroke: #880e4f, stroke-width: 2px
```

By defining explicit **Source** nodes (empirical grounding/axioms) and **Target** nodes (conclusions), we can
meaningfully measure both the semantic distance and the confidence drop-off between them.

---

## Theoretical Grounding & Model Formulation

### Conservatism (Conceptual Detour)

Following Novacek (2015), conservatism is a topological and semantic distance metric. It assesses whether the semantic
"distance" between the premises and the conclusions is minimized. Novacek describes the node's conceptual position with
the term 'characteristic context vector'; in order to avoid confusion with eigenvectors, we will consistently use *"
weighted adjacency vector"* instead. A hypothesis path is conservative if the direct distance between its start and end
is highly correlated with the sum of the individual step distances along the path.

### Epistemic Safety (Confidence Propagation)

Safety operates strictly on the explicit confidence weights of the relationships (edges). It assumes that every logical
step introduces some uncertainty. Therefore, safety models how confidence propagates and decays through the graph.

---

## Mathematical Specification & Graph Formulation

Let $H = (V_H, E_H)$ be a directed hypothesis graph containing a path $p = (v_1, v_2, \dots, v_{|p|})$ from an empirical
source $v_1$ to a conclusion $v_{|p|}$.

### Conservatism Formula (Novacek, 2015)

To measure the overall conservatism of a hypothesis graph $H$, we compute the arithmetic mean of the conservatism for
all shortest paths $p \in \pi_s (H, \delta)$ within that graph. The formula exactly follows Novacek (2015):

$$
C (H) = \frac{1}{|\pi_s (H, \delta)|} \sum_{p \in \pi_s (H, \delta)} \frac{\delta (v_1, v_{|p|})}{\sum_{i=1}^{|p|-1} \delta (v_i, v_{i+1})}
$$

*(Note: $\delta$ is the Euclidean distance between the weighted adjacency vectors of the vertices. A value closer to 1
implies a highly conservative, straight-line conceptual graph, while a value approaching 0 indicates a radical
conceptual detour).*

### Epistemic Safety Formula

Safety operates strictly on explicit confidence weights $w (e) \in [0, 1]$ assigned to edges. For a target
node $v_{target}$ supported by a source node $v_{source}$ with initial confidence $c (v_{source})$, safety seeks the
**Maximum Reliability Path**:

$$
\text{Safety} (v_{target}) = \max_{p \in \text{paths}} \left (\prod_{e \in p} w (e) \right) \times c (v_{source})
$$

!!! note "Connection to LPG-ECHO"
     Epistemic Safety is fundamentally related to our [LPG-ECHO Algorithm](../adapted_echo_algorithm.md). While Safety calculates confidence propagation along a *single, optimal discrete path*, the ECHO algorithm performs continuous, global belief propagation across the *entire network* (where evidence nodes are clamped to $+1.0$). Therefore, this
     path-based Safety metric can be viewed as the localized, deterministic foundation of the broader, connectionist "Empirical Adequacy" that ECHO dynamically resolves.

---

## Measurement & Graph Implementation

1. **Path Identification**: Query the graph for paths matching the required topology (e.g., Empirical
   Source $\to \dots \to$ Conclusion).
2. **Measuring Conservatism**: Extract the weighted adjacency vectors for nodes along the path. Calculate the pairwise
   distances and compute the conservatism ratio.
3. **Measuring Safety (Implementation Trick)**: While Safety uses the product of weights, it is typically implemented
   using standard shortest-path algorithms (like Dijkstra's) by transforming the edge
   weights: $\text{cost} (e) = -\log (w (e))$. The shortest path in the transformed graph corresponds exactly to the
   Maximum Reliability Path.

---

## Diagnostic & Metascientific Value

| Metric               | High Value Interpretation                                                                   | Low Value Interpretation                                                                  |
|:---------------------|:--------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------|
| **Conservatism**     | **Incremental:** Stays strictly within established conceptual boundaries; linear reasoning. | **Radical:** Revolutionary or highly speculative; bridges distant, disconnected concepts. |
| **Epistemic Safety** | **Secure:** Closely tied to empirical evidence with few, highly reliable assumptions.       | **Tenuous:** Relies on long chains of reasoning with compounding uncertainties.           |

---

## Grounding References

* **[Novacek, 2015]** Novacek, V. (2015). Formalising Hypothesis Virtues in Knowledge Graphs.
