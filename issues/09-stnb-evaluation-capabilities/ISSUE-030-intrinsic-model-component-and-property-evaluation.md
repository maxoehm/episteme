# [ISSUE-030] Comprehensive Intrinsic Evaluation: Model Component Decomposition & Full Property Subsumption

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-030` |
| **Component(s)** | `packages/epistemetrics` (`epistemic/model_evaluation.py`), `packages/episteme-pipeline` (`episteme_pipeline/evaluation/`) |
| **Roadmap Horizon** | **Horizon 1** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | Critical / Blocker |
| **Status** | Open |
| **Source Ref** | [`docs/research/structuralist_theory_benchmark.md §Target Graph Schema`](../../docs/research/structuralist_theory_benchmark.md#L52-L122), [`docs/concepts/formal_graph_model.md`](../../docs/concepts/formal_graph_model.md), [Balzer, Moulines, & Sneed (1987)](../../docs/research/structuralist_theory_benchmark.md#L317-L318) |

---

## 1. Problem Statement & Motivation

In the formal structuralist philosophy of science ([Balzer, Moulines, & Sneed, 1987]; [Stegmüller, 1976]; [Schurz, 2014, 2024]), a scientific theory is **not** a flat unipartite graph of lexical entities. A Theory Element $T = \langle K, I \rangle$ is a Bourbaki species of structure consisting of a formal core:
$$K = \langle \mathcal{M}_p, \mathcal{M}, \mathcal{M}_{pp}, GC, GL \rangle$$
and an empirical application domain $I \subseteq \mathcal{M}_{pp}$.

Existing evaluation scorers (such as `gm_gbs.py` and `oep.py`):
1. **Treat graphs as flat collections of relation strings:** They measure only whether edge labels (e.g. `"USED_FOR"`, `"specializes"`) match text embeddings, discarding node identities, mathematical axioms, and structural roles.
2. **Completely ignore model-class decomposition:** They do not verify whether a theory element contains the actual mathematical components that define its model classes.
3. **Ignore node and edge attributes:** Properties such as `formalAxiom`, `epistemic_status`, primitive base sets, function domains, polarities, and character-level `textAnchor` offsets are completely unverified.

To rigorously determine whether a predicted graph **has at least the capabilities of the reference graph**, intrinsic evaluation must evaluate against **all properties within the reference graph** and verify that the predicted graph **contains the constituent components that make up each Model**.

---

## 2. Model Component Decomposition Specification

Every scientific Theory Element in the reference graph decomposes into five formal model classes. Intrinsic evaluation must decompose and evaluate each of these constituent components:

```mermaid
classDiagram
    class TheoryElement {
        +str id
        +str label
        +str epistemic_status
    }
    class PotentialModel {
        +list[str] base_sets
        +list[str] primitive_functions
        +dict signatures
        +TextAnchor textAnchor
    }
    class ActualModel {
        +str formalAxiom
        +list[str] governing_equations
        +str verbatimQuote
        +TextAnchor textAnchor
    }
    class PartialPotentialModel {
        +list[str] non_theoretical_terms
        +list[str] observational_base
        +TextAnchor textAnchor
    }
    class GlobalConstraint {
        +str invariant_property
        +str cross_model_rule
        +TextAnchor textAnchor
    }
    class Paradigm {
        +str exemplar_system
        +TextAnchor textAnchor
    }

    TheoryElement --> PotentialModel : str:hasPotentialModel
    TheoryElement --> ActualModel : str:hasActualModel
    TheoryElement --> PartialPotentialModel : str:hasPartialPotentialModel
    TheoryElement --> GlobalConstraint : str:hasConstraint
    TheoryElement --> Paradigm : str:hasParadigm
```

### 2.1 Constituent Components by Model Class

1. **Potential Models ($\mathcal{M}_p$ - Conceptual Framework & Signatures):**
   - **Primitive Base Sets:** The underlying sets specifying the ontology of the theory (e.g., in Classical Particle Mechanics: Particles $P$, Time intervals $T \subseteq \mathbb{R}$, Euclidean Space $\mathbb{R}^3$).
   - **Primitive Function Domains & Typification:** Function signatures establishing mathematical parameters (e.g., position trajectory $s: P \times T \to \mathbb{R}^3$, scalar mass $m: P \to \mathbb{R}^+$, impressed force vector $f: P \times T \times \mathbb{N} \to \mathbb{R}^3$).
   - *Intrinsic Check:* Verifies that $\mathcal{M}_p(G_{\text{pred}})$ contains all base sets and primitive function signatures defined in $\mathcal{M}_p(G_{\text{ref}})$.

2. **Actual Models ($\mathcal{M}$ - Substantive Laws & Axioms):**
   - **Mathematical Governing Equations:** Substantive axioms (e.g. Newton's Second Law: $\sum_i f(p, t, i) = m(p) \cdot \ddot{s}(p, t)$, Newton's Third Law, Hooke's Law: $f = -kx$).
   - *Intrinsic Check:* Evaluates semantic and symbolic equivalence of governing laws between predicted and reference axioms.

3. **Partial Potential Models ($\mathcal{M}_{pp}$ - Empirical Observational Base):**
   - **$T$-Non-Theoretical Basis:** Spatio-temporal observation frames where theoretical terms ($m, f$) are removed.
   - *Intrinsic Check:* Verifies that non-theoretical empirical terms are correctly isolated without theoretical contamination.

4. **Global Constraints ($GC$ - Cross-Model Invariance):**
   - **Invariance Conditions:** Assertions that physical parameters (e.g., mass, charge) maintain identical values across distinct models and independent applications ($m(p)$ invariant).
   - *Intrinsic Check:* Verifies that global equality constraints are linked to participating elements.

5. **Paradigmatic Applications ($I_0$ - Exemplar Setups):**
   - **Physical Exemplars:** Prototypical setups (e.g. harmonic oscillators, planetary systems, free fall).
   - *Intrinsic Check:* Verifies presence and empirical text grounding of reference exemplars.

---

## 3. Full Property-by-Property Verification Requirements

The evaluator must verify all attributes defined on reference nodes and edges:

### 3.1 Node Attribute Matching
For every node $u_{\text{ref}} \in V(G_{\text{ref}})$:
1. **Type & Epistemic Role:** `node_type` (`TheoryElement`, `PotentialModel`, `ActualModel`, `PartialPotentialModel`, `Constraint`, `Paradigm`) and `epistemic_status` (`hard_core`, `protective_belt`, `actual_model`).
2. **Formal Axiom & Proposition:** `formalAxiom` matching using:
   - Safe symbolic formula evaluation (AST comparison) for mathematical expressions.
   - Contextual embedding cosine similarity ($\text{sim} \ge \tau_{\text{axiom}} = 0.88$) for textual expressions.
3. **Text Anchor Grounding:**
   - Source document and chunk resolution (`sourceDocId`, `chunkId`).
   - Character span Intersection over Union ($\text{IoU} = \frac{|S_{\text{pred}} \cap S_{\text{ref}}|}{|S_{\text{pred}} \cup S_{\text{ref}}|}$).
   - Token F1 over normalized `verbatimQuote`.

### 3.2 Edge Attribute Matching
For every edge $(u_{\text{ref}}, v_{\text{ref}}) \in E(G_{\text{ref}})$:
1. **Relation Category:** Canonical relational label (`hasActualModel`, `hasPotentialModel`, `hasPartialPotentialModel`, `hasConstraint`, `specializes`, `reducesTo`, `presupposes`, `empiricallyEquivalent`).
2. **Relational Semantics:** Directionality, polarity ($+1$ for supports/specializes, $-1$ for attacks/reduces), scope (`local` vs `global`), and weight/confidence.

---

## 4. Quantitative Metrics Suite

Implement in `packages/epistemetrics/src/epistemetrics/epistemic/model_evaluation.py`:

1. **Model Component Completeness ($MCC$):**
   $$\text{MCC}(T) = \frac{|\mathcal{M}_{p, \text{matched}}| + |\mathcal{M}_{\text{matched}}| + |\mathcal{M}_{pp, \text{matched}}| + |GC_{\text{matched}}| + |I_{0, \text{matched}}|}{|\text{Total Reference Components}(T)|}$$
2. **Axiomatic Omission Rate ($AOR$):**
   $$AOR = \frac{| \mathcal{M}_{\text{ref}} \setminus \mathcal{M}_{\text{pred, matched}} |}{| \mathcal{M}_{\text{ref}} |}$$
   *Requirement for capability equivalence:* $AOR = 0.0$ (Zero-Omission of core laws).
3. **Property Fidelity Score ($PFS$):**
   Mean macro accuracy across all categorical and scalar attributes (`node_type`, `epistemic_status`, `weight`, `polarity`).
4. **Text Anchor Grounding IoU ($AG_{\text{IoU}}$):**
   Average character span IoU across all matched empirical nodes.

---

## 5. Acceptance Criteria

- [ ] `epistemetrics.epistemic.model_evaluation` implements `evaluate_model_components(pred_graph, ref_graph)`.
- [ ] Evaluates completeness across all 5 model classes ($\mathcal{M}_p, \mathcal{M}, \mathcal{M}_{pp}, GC, I_0$).
- [ ] Evaluates node properties: `formalAxiom`, `label`, `epistemic_status`, and token-level `textAnchor`.
- [ ] Evaluates edge properties: `relation_type`, structural composition links, polarity, and weights.
- [ ] Reports $MCC$, $AOR$, $PFS$, and $AG_{\text{IoU}}$ with zero division errors on empty graphs.
- [ ] Deterministic unit tests in `packages/epistemetrics/tests/` verify scoring on perturbed, omitted, and complete model graphs.

---

## 6. Key Target Files

- `packages/epistemetrics/src/epistemetrics/epistemic/model_evaluation.py`
- `packages/epistemetrics/src/epistemetrics/core/models.py`
- `packages/epistemetrics/src/epistemetrics/__init__.py`
- `packages/episteme-pipeline/episteme_pipeline/evaluation/intrinsic.py`
- `packages/epistemetrics/tests/test_model_evaluation.py`
