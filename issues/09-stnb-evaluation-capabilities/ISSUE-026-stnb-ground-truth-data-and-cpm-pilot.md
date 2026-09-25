# [ISSUE-026] STNB Ground-Truth Data Absence & Missing CPM Pilot Corpus

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-026` |
| **Component(s)** | `packages/episteme-pipeline` (`evaluation/data/`, `evaluation/manifests/eval_stnb.yaml`) |
| **Roadmap Horizon** | **Horizon 1** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | Critical / Blocker |
| **Status** | Open |
| **Source Ref** | [`docs/research/structuralist_theory_benchmark.md §Benchmark Profile & Data Card`](../../docs/research/structuralist_theory_benchmark.md#L18-L50), [`eval_stnb.yaml`](../../packages/episteme-pipeline/evaluation/manifests/eval_stnb.yaml) |

---

## 1. Problem Statement & Motivation

According to [`docs/research/structuralist_theory_benchmark.md`](../../docs/research/structuralist_theory_benchmark.md#L120-L122):
> "The complete machine-readable specification and sample graph for Classical Particle Mechanics is maintained in `packages/episteme-pipeline/evaluation/data/stnb_cpm_pilot.jsonld`."

Furthermore, [`evaluation/manifests/eval_stnb.yaml`](../../packages/episteme-pipeline/evaluation/manifests/eval_stnb.yaml#L3-L6) declares:
```yaml
corpus:
  dataset_type: "structuralist"
  gold_standard_path: "packages/episteme-pipeline/evaluation/data/stnb_cpm_pilot.jsonld"
  texts_dir: "packages/episteme-pipeline/evaluation/data"
  limit: 10
```

However, in the actual repository:
1. **The directory `packages/episteme-pipeline/evaluation/data/` does not exist.**
2. **`stnb_cpm_pilot.jsonld` does not exist.**
3. **No primary text files (e.g. Newton's 1687 *Principia* Book 1 Axioms) exist.**
4. None of the five benchmark corpora from the STNB portfolio (Classical Particle Mechanics, Theory of the Unconscious, Cognitive Dissonance Theory, Structural Psychology, Equilibrium Thermodynamics) have machine-readable gold standards.

Attempting to run an evaluation using `eval_stnb.yaml` immediately fails with `FileNotFoundError` or silently skips intrinsic evaluation entirely. The benchmark cannot evaluate anything without ground truth.

---

## 2. Functional Requirements

### 2.1 Classical Particle Mechanics (CPM) Gold-Standard Construction
Curate and serialize the canonical Bourbaki structuralist reconstruction of Classical Particle Mechanics (Balzer, Moulines, & Sneed, 1987, Chapter 2) into `packages/episteme-pipeline/evaluation/data/stnb_cpm_pilot.jsonld`.

The dataset must contain:
1. **Theory Elements ($T = \langle K, I \rangle$):**
   - Fundamental Base Element: $T_{\text{CPM\_Base}}$ (Newton's Core Mechanics).
   - Specialization Elements:
     - $T_{\text{CPM\_Grav}}$ (Newtonian Gravitational Systems).
     - $T_{\text{CPM\_Harmonic}}$ (Hookean Harmonic Oscillators).
     - $T_{\text{CPM\_Free}}$ (Free Particle Systems).
2. **Model Classes:**
   - **Potential Models ($\mathcal{M}_p$):** Primitive sets (Particles $P$, Time intervals $T \subseteq \mathbb{R}$), kinematic position function $s: P \times T \to \mathbb{R}^3$, mass function $m: P \to \mathbb{R}^+$, force function $f: P \times T \times \mathbb{N} \to \mathbb{R}^3$.
   - **Actual Models ($\mathcal{M}$):**
     - Newton's Second Law ($\sum_i f(p, t, i) = m(p) \cdot \frac{d^2 s(p,t)}{dt^2}$).
     - Newton's Third Law (Action-Reaction: $f(p, p', t) = -f(p', p, t)$).
     - Law of Universal Gravitation ($f_G(p_1, p_2) = -G \frac{m_1 m_2}{r^2} \hat{\mathbf{r}}$).
     - Hooke's Law ($f_H(p) = -k \cdot s(p)$).
   - **Partial Potential Models ($\mathcal{M}_{pp}$):** Kinematic observational framework $\langle P, T, s \rangle$ where theoretical terms (mass $m$, force $f$) are cut off.
   - **Global Invariance Constraints ($GC$):** Mass invariance constraint asserting identical scalar mass values across distinct physical applications ($m(p)$ is application-independent).
   - **Paradigmatic Applications ($I_0$):** Keplerian planetary orbits, terrestrial projectile trajectories, harmonic springs.

### 2.2 Text Corpus & Character-Offset Anchors
1. Ingest clean, unabridged historical primary text for Newton's *Principia* (1687, Motte-Cajori translation Book 1, *Axiomata sive Leges Motus* and *De Motu Corporum*) into `packages/episteme-pipeline/evaluation/data/newton_principia_1687.txt`.
2. Every empirical node in `stnb_cpm_pilot.jsonld` must carry an `Episteme:textAnchor` (and backwards-compatible `textAnchor`) with exact character offsets (`charStart`, `charEnd`), chunk ID, source doc ID, and verbatim quote matching the primary text.

### 2.3 JSON-LD Envelope Schema
Enforce valid JSON-LD graph envelope with standard context:
```json
{
  "@context": {
    "str": "https://structuralism.org/ontology#",
    "Episteme": "https://grund.ai/schema#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "specializes": {"@id": "str:specializes", "@type": "@id"},
    "reducesTo": {"@id": "str:reducesTo", "@type": "@id"},
    "hasActualModel": {"@id": "str:hasActualModel", "@type": "@id"},
    "hasPotentialModel": {"@id": "str:hasPotentialModel", "@type": "@id"},
    "hasPartialPotentialModel": {"@id": "str:hasPartialPotentialModel", "@type": "@id"},
    "hasConstraint": {"@id": "str:hasConstraint", "@type": "@id"},
    "textAnchor": "Episteme:textAnchor"
  },
  "@graph": [ ... ]
}
```

---

## 3. Acceptance Criteria

- [ ] Directory `packages/episteme-pipeline/evaluation/data/` is created and committed to the repository.
- [ ] `packages/episteme-pipeline/evaluation/data/newton_principia_1687.txt` contains clean primary source text.
- [ ] `packages/episteme-pipeline/evaluation/data/stnb_cpm_pilot.jsonld` contains valid JSON-LD with:
  - At least 4 `TheoryElement` nodes.
  - At least 8 `ActualModel` / `PotentialModel` nodes.
  - At least 2 `Constraint` nodes.
  - Character offsets matching `newton_principia_1687.txt` verbatim.
- [ ] `packages/episteme-pipeline/evaluation/manifests/eval_stnb.yaml` points to existing paths and parses cleanly without `FileNotFoundError`.

---

## 4. Key Target Files

- `packages/episteme-pipeline/evaluation/data/stnb_cpm_pilot.jsonld`
- `packages/episteme-pipeline/evaluation/data/newton_principia_1687.txt`
- `packages/episteme-pipeline/evaluation/manifests/eval_stnb.yaml`
