---
status: in_progress
tags:
  - Algorithms
  - Metrics
---

# The LPG-ECHO Algorithm

## Overview & Inspiration

The **LPG-ECHO Algorithm** (_echo for large property graphs_) is the central computational engine for resolving belief
propagation, conflict resolution, and global coherence within our theory graph. It is heavily inspired by Paul Thagard's
original ECHO connectionist architecture (Thagard, 1989), which modeled explanatory coherence as a parallel constraint
satisfaction problem.

While Thagard's original ECHO was designed for small-scale cognitive modeling of scientific revolutions, our *LPG-ECHO*
is scaled for large, heterogeneous property graphs (like Neo4j) and incorporates multi-relational weights (e.g.,
analogical, hierarchical, and varying claim strengths like MAJOR/MINOR).

By running a synchronous or asynchronous relaxation loop over the entire graph, the algorithm assigns a continuous
epistemic status (activation) to every single node. This means that instead of manually computing dozens of local
metrics, the LPG-ECHO algorithm organically and implicitly captures the complex interplay of numerous epistemic
virtues simultaneously.

---

## The Core Mechanism

In the LPG-ECHO model, the graph is treated as a neural network:

* **Nodes (Units)**: Represent propositions, hypotheses, axioms, and empirical evidence. Evidence nodes are clamped to
  positive activation.
* **Edges (Weights)**: Excitatory weights ($w > 0$) for explanatory, deductive, or supportive relationships. Inhibitory
  weights ($w < 0$) for contradictions, mutually exclusive hypotheses, or falsifications.
* **Activation Loop**: At each discrete time step $t$, a node updates its activation $a_j (t) \in [-1, 1]$ based on the
  weighted sum of activations from its neighbors, minus a decay factor.
* **Convergence**: The system relaxes into a state of maximum "Harmony" (global energy minimum).

---

## System Skepticism & Decay Dynamics

The resistance of the network to ungrounded or speculative hypotheses is governed by the **System Skepticism / Decay Parameter** ($\theta \in (0, 1)$), originally formalized by Thagard (1989, p. 443).

### Intrinsic Decay Dynamics

In the absence of net positive input from evidentiary nodes ($\text{net}_j (t) \le 0$), a hypothesis node's activation decays exponentially back toward neutrality:

$$a_j (t) = a_j (0) \cdot (1 - \theta)^t$$

### Half-Life of Unsupported Beliefs ($t_{1/2}$)

The half-life of an unsupported proposition (the number of relaxation cycles before initial confidence is halved) is:

$$t_{1/2} = \frac{\ln (0.5)}{\ln (1 - \theta)}$$

For the canonical standard setting $\theta = 0.05$:
$$t_{1/2} \approx \frac{-0.693}{-0.0513} \approx 13.5 \text{ iterations}$$

### Epistemic Diagnostic Profile

| Skepticism Parameter $\theta$ | Epistemic Stance            | Solver Behavior                                                                      |
|:------------------------------|:----------------------------|:-------------------------------------------------------------------------------------|
| $\theta < 0.02$               | Credulous / Gullible        | Speculative auxiliary hypotheses survive without solid data support.                 |
| $\theta \approx 0.05$         | Normative Epistemic Balance | Standard scientific skepticism; requires continuous evidentiary backing.             |
| $\theta > 0.15$               | Hyper-Skeptical             | Even well-grounded theories struggle to propagate activation to higher-level axioms. |

Propositions whose activation collapses to $< 0.01$ under normative decay are formally diagnosed as **unsupported speculation ("ghost nodes")**.

---

## Implicitly Collected Metrics

The true power of the LPG-ECHO algorithm is that its convergence state mathematically synthesizes multiple distinct
metrics. By running this single algorithm, we implicitly collect or account for the following theoretical properties:

### A. Epistemic Coherence Metrics

1. **Node Activation (Acceptability)**: Directly calculated. The final equilibrium state $a_j^*$ determines if a
   hypothesis is accepted, rejected, or neutral.
2. **System Coherence (Harmony, $H$)**: The global energy state of the network at convergence directly measures the
   overall consistency and lack of contradictions across the paradigm.
3. **Simplicity / Elegance**: Implicitly captured. Complex explanations (those requiring many auxiliary co-hypotheses)
   suffer from excitation dilution. Simpler explanations automatically channel higher, undistiluted excitation to their
   conclusions, naturally favoring Occam's Razor.
4. **Conservatism / Tenability**: Implicitly captured by the temporal persistence of node activations. Established
   paradigm nodes resist deactivation from minor anomalies unless overwhelmed by a highly coherent alternative theory.

### B. Empirical Power Metrics

5. **Explanatory Breadth**: Implicitly captured. A theory node that explains many distinct empirical evidence nodes
   receives excitatory feedback from all of them, naturally driving its activation toward $+1.0$.
6. **Construct Validity / Empirical Adequacy**: Evidence nodes are hard-clamped to $+1.0$. The flow of this empirical
   certainty upward into the theoretical layers intrinsically measures how well grounded the theory is in observation.
7. **Ratio of Axioms vs. Observations (Unification)**: While we explicitly measure this via the Schurz Unification
   Ratio, ECHO implicitly models it. A theory with too few observations and too many ungrounded axioms will suffer from
   baseline decay, as the clamped empirical activation is insufficient to keep the vast theoretical network "alive."

### C. Metatheoretical Metrics

8. **Higher-Level Warrant**: Implicitly captured by adding vertical excitatory channels from higher-level paradigm nodes
   down to specific theory nodes.
9. **Analogical Support**: Modeled by excitatory horizontal links between distinct but structurally similar domains,
   allowing them to mutually boost each other's activation.

---

## Grounding References

* **[Thagard, 1989]** Thagard, P. (1989). Explanatory Coherence. *Behavioral and Brain Sciences*, 12 (3), 435–467.
* **[Schurz, 2024]** Schurz, G. (2024). *Philosophy of Science: A Unified Approach*. Routledge.
