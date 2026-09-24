---
status: needs_verification
tags:
  - Metrics
---

# T-Theoreticity

## Definition & Conceptual Goal

The **T-Theoreticity** metric formally determines whether a scientific term, relation, or function $\tau$ can be
measured independently of the specific theory ($T$) in which it occurs, or whether its measurement presupposes the
actual validity of $T$
([Balzer et al., 1987, pp. 49–78, 391–393]; [Stegmüller, 1976, pp. 40–56]; [Schurz, 2024, pp. 251–252]).

Originally formulated by Joseph D. Sneed, this functional criterion solves the classical problem of theoretical terms by
relativizing "theoreticity" to a specific theory $T$, thereby preventing the vicious epistemic circle in empirical
testing (where testing $T$ would presuppose the truth of $T$).

---

## Theoretical Grounding & Model Formulation

Two primary formal criteria exist in structuralist philosophy of science to establish $T$-theoreticity:

### Sneed's Functional Criterion (Primary Baseline)

A function or relation $\tau$ is **$T$-theoretical** iff every known, admissible measurement method for determining
values of $\tau$ in an intended application presupposes the actual validity of the fundamental laws of $T$.

* **Example of $T$-Theoretical terms**: In Classical Particle Mechanics (CPM), mass ($m$) and force ($f$) are $T$
  -theoretical because their value determination relies on Newton's laws or momentum conservation.
* **Example of $T$-Non-Theoretical terms**: If there exists at least one measurement method for $\tau$ that is
  independent of $T$, $\tau$ is **$T$-non-theoretical** ($T$-empirical/pre-theoretical). Position/distance ($s$) in CPM
  is $T$-non-theoretical because it can be determined via optical or geometric pre-theories without presupposing
  Newton's second law.

### Balzer–Gähde Invariance Criterion & Metascientific Limitations

A term $\tau$ is formally $T$-theoretical if there exists a $T$-admissible measurement method invariant under $T$
-compatible transformations ([Balzer et al., 1987, DII-9]).

* **Metascientific Critique**: As Gerhard Schurz ([2024, p. 252]) explicitly notes, this purely theory-internal
  invariance criterion turned out to be **too broad**—it can classify simple empirical concepts as $T$-theoretical and
  allow circular value determinations in empirically empty theories. Consequently, Sneed's functional criterion remains
  the preferred baseline for empirical grounding.

---

## Mathematical Specification & Graph Formulation

In a multi-relational theory graph or theory-holon $H$, let $M (\tau)$ be the set of measurement pathways (represented
as incoming `:MEASURED_BY` or `:DETERMINED_BY` dependency chains) for term $\tau$:

$$M (\tau) = \{p_1, p_2, \dots, p_k\}$$

Each pathway $p_i$ depends on a set of theory laws $\text{Presupposes} (p_i) \subseteq \text{Laws} (G)$.

### Theoreticity Index ($TI$)

$$TI (\tau, T) = \begin{cases} 1 & \text{if } \forall p \in M (\tau), \, \text{Laws} (T) \cap \text{Presupposes} (p) \neq \emptyset \\ 0 & \text{if } \exists p \in M (\tau) \text{ s.t. } \text{Laws} (T) \cap \text{Presupposes} (p) = \emptyset \end{cases}$$

* $TI (\tau, T) = 1 \implies \tau \in M_p \setminus M_{pp}$ ($T$-theoretical construct).
* $TI (\tau, T) = 0 \implies \tau \in M_{pp}$ ($T$-non-theoretical / observational and pre-theoretical basis for $T$).

### Global vs. Local Graph Scope

* **Local Scope ($T$)**: Evaluates dependency pathways strictly within the axioms of theory core $T$.
* **Global Scope / Holon ($H$)**: Evaluates intertheoretical links (`:LINKED_TO`), checking if incoming measurement
  chains originate from pre-theories $T^*$ connected via entailment links outside $T$.

---

## Measurement & Graph Implementation

1. **Traverse Dependency Chains**: Trace all `:DETERMINED_BY` or `:MEASURED_VIA` incoming edges to the term node $\tau$.
2. **Law Dependency Check**: Verify whether all measurement paths route through axioms belonging to `:TheoryCore` $T$ or
   whether an independent path exists via an intertheoretical link to a pre-theory $T^*$.
3. **Partition Verification**: Assign $\tau$ to either the theoretical vocabulary ($M_p \setminus M_{pp}$) or partial
   potential model vocabulary ($M_{pp}$).

---

## Diagnostic & Metascientific Value

| $TI(\tau, T)$ | Classification      | Metascientific Role                                                                                       |
|:--------------|:--------------------|:----------------------------------------------------------------------------------------------------------|
| $TI = 1$      | $T$-Theoretical     | Internal theoretical construct; must be constrained across applications via constraints ($C$).            |
| $TI = 0$      | $T$-Non-Theoretical | Independent empirical anchor point; provides the observational/pre-theoretical testing ground ($M_{pp}$). |

---

## Grounding References

* **[Balzer et al., 1987]** Balzer, W., Moulines, C. U., & Sneed, J. D. (1987). *An Architectonic for Science*. Reidel
  Publishing, pp. 49–78, 391–393.
* **[Schurz, 2024]** Schurz, G. (2024). *Philosophy of Science: A Unified Approach*. Routledge, Def. 5.3-1, pp. 251–252.
* **[Stegmüller, 1976]** Stegmüller, W. (1976). *The Structure and Dynamics of Theories*. Springer-Verlag, pp. 40–56.
