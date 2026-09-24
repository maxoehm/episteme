---
status: needs_verification
tags:
  - Metrics
---

# Degeneration Index & Immunization Tracking

## Definition & Conceptual Goal

The **Degeneration Index & Immunization Tracking** metric suite measures the Lakatosian degeneration of a scientific research program across historical theory versions and detects ad-hoc immunizing stratagems ([Balzer et al., 1987, pp. 333–338](zotero://select/library/items/24SNSW2B); [Stegmüller, 1976, p. 184](zotero://select/library/items/2WXH9HSL); [Schurz, 2024, pp. 51, 59, 61, 265](zotero://select/library/items/24SNSW2B)).

It diagnoses two interconnected layers of non-progressive theory evolution:

1. **Micro-Level (Node Immunization)**: Detects when a new auxiliary hypothesis or core expansion ($K_{i+1}$) absorbs an empirical anomaly ($a \in I$) but generates zero independent excess empirical content ($\operatorname{Cn}(K_{i+1}) \setminus \{a\} \subseteq \operatorname{Cn}(K_i)$).
2. **Macro-Level (Programme Degeneration Index $D$)**: Quantifies the ratio of ad-hoc resolved anomalies ([Typ-b failures](../../../glossary.md#misserfolg-typ-b-immunisierter-misserfolg-scheinbarer-erfolg)) to the sum of genuine empirical successes and honest direct empirical refutations ([Typ-a failures](../../../glossary.md#misserfolg-typ-a-direkter-widerspruch)).

---
## Theoretical Grounding & Model Formulation

In Schurz's reconstruction of Lakatos's methodology of scientific research programmes:
For each historical version $V_j$ of a theory:

* **$S (V_j)$ (Genuine Successes)**: Phenomena successfully predicted or explained without ad-hoc adjustments.
* **$F_{\text{Typ a}} (V_j)$ (Direct Failures)**: Well-established empirical phenomena that directly contradict $V_j$ logically or probabilistically.
* **$F_{\text{Typ b}} (V_j)$ (Immunized / Ad-Hoc Failures)**: Phenomena that contradicted a prior version $V_{j-1}$, but were absorbed in $V_j$ via auxiliary hypotheses lacking independent empirical confirmation.

An anomaly resolution $E_{i+1} = \langle K_{i+1}, I_{i+1} \rangle$ is an **ad-hoc immunization** if:
$$
\Delta_{\text{anom}} > 0 \quad \text{and} \quad \Delta_{\text{content}} = |\operatorname{Cn} (K_{i+1}) \setminus \operatorname{Cn} (K_i)| = 0
$$

---
## Mathematical Specification & Graph Formulation

### Node-Level Immunization Index ($II$)

For an auxiliary modification introducing new laws resolving anomalies:

$$II (K_i, K_{i+1}) = \begin{cases} 1.0 & \text{if } \Delta_{\text{anom}} > 0 \land \Delta_{\text{content}} = 0 \\ \frac{\Delta_{\text{anom}}}{\Delta_{\text{anom}} + \Delta_{\text{content}}} & \text{otherwise} \end{cases}$$

### Ratio of Progressive to Immunizing Nodes ($RPI$)

Across the entire evolution sequence $\mathcal{E}$:

$$RPI (\mathcal{E}) = \frac{|V_{\text{progressive}}|}{|V_{\text{progressive}}| + |V_{\text{immunizing}}|}$$

### Schurz's Degeneration Index ($D$)

For historical theory version $V_j$:

$$D (V_j) = \frac{|F_{\text{Typ b}} (V_j)|}{|S (V_j)| + |F_{\text{Typ a}} (V_j)|}$$

### Programme Trajectory Trend ($\Delta D$)

Over a sequence of versions $V_1, V_2, \dots, V_m$:

$$\Delta D = \frac{D (V_m) - D (V_1)}{m - 1}$$

* $\Delta D > 0$: **Degenerating Research Programme** (ad-hoc immunizations accumulate faster than real progress).
* $\Delta D \le 0$: **Progressive Research Programme** (genuine successes outpace anomalies).

---
## Measurement & Graph Implementation

1. **Detect Ad-Hoc Nodes**:
   - Trace incoming `:RESOLVES_ANOMALY` edges connected to new auxiliary hypothesis nodes.
   - Query for outgoing `:PREDICTS_NOVEL` edges. Auxiliary nodes with incoming anomaly resolutions but zero novel predictions are labeled `:AdHocImmunization` (Typ-b failure).
2. **Compute Version Degeneration ($D$)**:
   ```cypher
   MATCH (v:TheoryVersion {id: $version_id})
   OPTIONAL MATCH (v)-[:HAS_SUCCESS]->(s:Success)
   OPTIONAL MATCH (v)-[:HAS_FAILURE_A]->(fa:FailureTypA)
   OPTIONAL MATCH (v)-[:HAS_FAILURE_B]->(fb:FailureTypB)
   WITH count(DISTINCT s) AS s_count, count(DISTINCT fa) AS fa_count, count(DISTINCT fb) AS fb_count
   RETURN fb_count * 1.0 / (s_count + fa_count + 1e-6) AS degeneration_index
   ```

---
## Diagnostic & Metascientific Value

| Measurement Indicator        | Programme Dynamic        | Metascientific Interpretation                                         |
|:-----------------------------|:-------------------------|:----------------------------------------------------------------------|
| $\Delta D \le 0, D < 0.3$    | Progressive Programme    | Healthy Lakatosian growth; true empirical successes dominate.         |
| $\Delta D \approx 0, D \sim 0.5$ | Stagnant Programme   | Defensive maintenance; new predictions roughly balance anomaly patches.|
| $\Delta D > 0, D > 1.0$      | Degenerating Programme   | Defensive crisis; majority of modifications are ad-hoc immunizations. |
| $II = 1.0$ (Node Level)      | Pure Immunizing Patch    | Auxiliary node shields theory from falsification without advancing science. |

---
## Grounding References

* **[Schurz, 2024]** Schurz, G. (2024). *Philosophy of Science: A Unified Approach*. Routledge, pp. 51, 59, 61, 265.
* **[Balzer et al., 1987]** Balzer, W., Moulines, C. U., & Sneed, J. D. (1987). *An Architectonic for Science*. Reidel Publishing, pp. 333–338.
* **[Stegmüller, 1976]** Stegmüller, W. (1976). *The Structure and Dynamics of Theories*. Springer-Verlag, p. 184.
