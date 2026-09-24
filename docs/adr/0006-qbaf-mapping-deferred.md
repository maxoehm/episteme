# [0006] QBAF Weight Computation Deferred — Structural Mapping Only in V1

Status: Accepted

## Context

The research goal is to represent extracted argumentation as a Quantified Bipolar Argumentation Framework (QBAF) Q = ⟨A,
R⁻, R⁺, w⟩ (Baroni et al. 2018), where:

- A = set of argument components (extracted by Phase 4)
- R⁺ = support relations (SUPPORTS edges)
- R⁻ = attack relations (ATTACKS edges)
- w: A → ℝ = a weight function over arguments

The weight function w is what makes QBAF *quantified* — it is the formal bridge to the inner/outer compatibility and
theory stability evaluation notions defined in `/paper.md`. Without w, the QBAF reduces to an unweighted
bipolar AF.

The question of how to assign weights is non-trivial and depends on research decisions not yet taken:

- Should w reflect lexical confidence from the LLM extraction?
- Should w reflect a notion of epistemic strength derived from the text?
- Should w be derived from argumentation semantics (e.g., h-categoriser, DF-QuAD)?
- How does w interact with the philosophical evaluation measures (inner vs outer compatibility)?

## Decision

**QBAF weight computation is deferred from V1.** The structural mapping (A, R⁺, R⁻) is implemented in
`QBAFMapper.map()`. All weight fields are `null` in V1.

The extension point is clean:

- `L3ArgumentComponent.qbaf_weight: float | None = None`
- `L3ArgumentRelation.qbaf_weight: float | None = None`
- `QBAFMapper.compute_weight(component_or_relation) -> float | None` — override point; returns `None` by default

To add weight computation, subclass `QBAFMapper`, override `compute_weight()`, and pass the subclass to
`Phase4Runner(qbaf_mapper=MyWeightedMapper(...))`.

**Before implementing weight computation, write `docs/adr/0007-qbaf-weight-semantics.md`** covering:

1. The chosen weight semantics (confidence-based, strength-based, or semantics-derived)
2. How w maps to the theory evaluation notions in `../../paper/paper.md`
3. How w interacts with Phase 5b argument clustering (should cluster representatives inherit the max or mean weight of
   the cluster?)

## Alternatives considered

- **LLM confidence as w** — `confidence` fields from extraction are already available on every component and relation.
  Simple and reproducible, but conflates extraction quality with argumentative strength — a strong argument with
  uncertain extraction has a low weight, which is semantically wrong.
- **Uniform weights (w = 1 for all)** — makes QBAF equivalent to unweighted BAF; semantically clean but loses the
  quantification benefit entirely.
- **DF-QuAD propagation weights** — well-defined by Baroni et al.; requires choosing a base strength for each argument
  component, which is the unresolved research question.

## Consequences

- The optional QBAF projection over argument artifacts contains a structurally correct QBAF with all
  `qbaf_weight = null` in V1 when materialized.
- Downstream code and query engines must treat `null` weight as "uncomputed" rather than "zero."
- `Phase5Config.theory_fusion_enabled = False` by default — TheoryFusion depends on weight semantics being resolved.
- This ADR is a **blocker** for Phase 5b TheoryFusion implementation.

## Related

- `pipeline/phases/phase4_argument_mining/qbaf_mapper.py` — `QBAFMapper` stub
- `pipeline/contracts/domain.py` — `QBAF`, `L3ArgumentComponent`, `L3ArgumentRelation`
- `../../paper/paper.md` — formal grounding (Baroni et al. QBAF, inner/outer compatibility)
- ADR 0005 — Phase 5b TheoryFusion depends on this decision
