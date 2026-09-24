# Ontology Reference

What the Studio may assume about node and relation types — and, more importantly,
what it may **not**.

The governing rule is **D-13: the schema is served, never compiled in.** This document
explains the shape of the schema and the resolution rules. It is a reference for
implementers, not a list of constants to transcribe into TypeScript.

Sources: `../../../pipeline/schema/default_schema.py`, `../../../pipeline/contracts/domain.py`,
`../../../docs/concepts/theorynet_concept.md`, `../../../docs/concepts/formal_model.md`.

---

## 1. The rule that matters

> The frontend contains **zero** hardcoded node-type or relation-type names.

Everything renderable derives from `SchemaConfig`, fetched at runtime:

- `GET /api/schema` — the active schema, for live views
- `GET /api/runs/{run_id}` — returns `config_snapshot.graph_schema`, the schema **that
  run was produced under**

Reading a run under its own schema is what makes evolution free. A run from March
renders correctly after the ontology changes in September, because the manifest carries
its own copy. Never render a historical run against the current schema.

`SchemaConfig` (in `../../../pipeline/schema/default_schema.py`) carries everything needed:

| Field | Purpose |
|---|---|
| `version` | Schema version string, surfaced in the UI |
| `node_types` | L2 entity types |
| `relation_types` | L2 relation types |
| `component_types` | L3 component types |
| `argument_relation_types` | L3 relation types |
| `component_definitions` | Human-readable text → inspector and tooltips |
| `argument_relation_definitions` | Same, for relations |
| `relation_polarities` | `{type: -1 \| 0 \| 1}` → edge styling |
| `component_partitions` | `{type: "B" \| "A"}` → the Δ = (B, A) partition |

The last two are the important ones: **the formalism is already encoded in the schema.**
Nothing needs to be re-derived in the Studio.

---

## 2. Layers

| Layer | Contents | Contract types | Cardinality |
|---|---|---|---|
| **L1** | Documents, chunks, embeddings | `L1Document`, `L1Chunk` | Largest — thousands |
| **L2** | Entities and semantic relations | `L2Entity`, `L2Triple` | Hundreds |
| **L3** | Theory atoms and argumentative relations | `TheoryAtom`, `TheoryRelation` | Smallest |

L1 is renderable but **off by default** (D-20); each layer toggles independently in
explore mode.

**Strip embeddings at the adapter boundary.** `L1Chunk.embedding` is an inline
`list[float]`. It must never reach the wire.

### The provenance chain

Complete, and the Studio's core value:

```
TheoryAtom.source_chunk_id ─────────────────────────► L1Chunk
TheoryAtom.entity_ids ──► L2Entity.source_chunk_ids ─► L1Chunk
                                                        └─► L1Document
```

Span granularity differs by layer (D-19): `EntityMentionArtifact` carries
`start_char`/`end_char`; `TheoryAtomArtifact` carries only `chunk_id` and `text`.

---

## 3. Declared types (defaults — read from the schema, do not transcribe)

### L2

`node_types`: `Concept` · `Person` · `Work` · `Theory` · `Institution`

`relation_types`: `RELATED_TO` · `INSTANCE_OF` · `PART_OF` · `SUBCLASS_OF` ·
`SUPPORTS` · `REFUTES` · `IMPLIES` · `CONTRADICTS`

### L3

`component_types`, with their Δ partition:

| Type | Partition | Meaning |
|---|---|---|
| `ObservationUnit` | **B** | Localized statements in purely observational terms; raw data nodes |
| `EmpiricalStatement` | **B** | Statements over logical and empirical concepts only |
| `TheoreticalHypothesis` | **A** | Statements with theoretical concepts or theoretical quantifier scope; core laws |
| `CoreExpansion` | **A** | Auxiliary laws forming the shifting superstructure around the core |

`argument_relation_types`, with polarity:

| Type | Polarity | Class | Meaning |
|---|---|---|---|
| `SUPPORTS_ARG` | +1 | $\mathcal{R}_{sup}$ | Provides support for another component |
| `COHERES_WITH` | +1 | $\mathcal{R}_{sup}$ | Excitatory link between co-explaining hypotheses |
| `ENTAILS` | +1 | $\mathcal{R}_{sup}$ | Intertheoretical entailment |
| `REDUCES_TO` | +1 | $\mathcal{R}_{sup}$ | Strict intertheoretical reduction |
| `DEDUCES` | +1 | $\mathcal{R}_{sup}$ | Logical entailment (explanation / falsification schema) |
| `ATTACKS` | −1 | $\mathcal{R}_{att}$ | Critical relation against another component |
| `INHIBITS` | −1 | $\mathcal{R}_{att}$ | Inhibitory link between competing hypotheses |
| `UNDERCUTS` | −1 | $\mathcal{R}_{att}$ | Undermines another's **inference** — see §5 |
| `SPECIALIZES` | 0 | neutral | Vertical hierarchy; inherits and restricts |
| `CONSTRAINS` | 0 | neutral | Lateral constraint across overlapping applications |

`DEDUCES` is deductive rather than argumentative and warrants its own visual channel
even though its polarity is +1.

---

## 4. The declared vocabulary is not the extracted vocabulary

**Read this before implementing edge styling.** See D-15.

The predicates actually present in the largest real run:

```
AQUIVALENT_ZU  BASIERT_AUF   BEEINFLUSST_VON  BEHANDELT_THEMA  BESTAETIGT
FALSIFIZIERT   IMPLIZIERT    KONTRASTIEREND_ZU  SETZT_VORAUS    TEIL_VON
VERFASST_VON   WIDERSPRICHT  ZITIERT
```

**None of these appear in `L2_RELATION_TYPES`.** The intersection with the declared
schema is empty. Extraction produces open-vocabulary German; the schema lists English
placeholders. Several map cleanly onto the formalism by meaning — `WIDERSPRICHT` and
`FALSIFIZIERT` are clearly $\mathcal{R}_{att}$, `BESTAETIGT` and `IMPLIZIERT` clearly
$\mathcal{R}_{sup}$ — but no mapping is recorded, so every lookup misses.

### Polarity resolution

```
1. schema.relation_polarities[type]  →  use it
2. otherwise                         →  polarity = null
```

`null` is **not** `0`. Neutral means "the schema says this relation carries no
argumentative charge"; null means "we do not know". They must render differently —
neutral grey solid, unknown grey dashed — because conflating them would report an
unmapped attack relation as harmless.

### The Unmapped Predicates panel

Ship it in M6 alongside the graph. It lists every predicate in the current view with no
polarity entry, ranked by frequency, with an example edge for each. This is the shortest
path to extending `relation_polarities` correctly, and it makes a real data-quality
problem visible instead of silently flattening the graph.

---

## 5. Two structural cases

### `UNDERCUTS` targets an inference (D-21)

`UNDERCUTS` attacks an *edge*, not a node — G6 cannot draw that. The adapter reifies:
it emits a synthetic `Inference` node at the target edge's midpoint and rewires the
undercut to it. Server-side, so the client stays simple.

`StudioEdge.target_kind` (`"node" | "edge"`) is reserved in the contract now;
reification lands at M6. Not urgent — see below.

### Unresolved components (D-16)

**Across all 117 artifact runs there are zero `theory_atom` artifacts.** The largest run
holds 72 `argument-relation` artifacts whose `upstream_artifact_ids` reference
`artifact::ac_<hash>` components that were never persisted.

L3 relations exist; their endpoints do not. The adapter materialises
`StudioNode{layer: 3, type: "Unresolved", resolved: false}` for each dangling reference
and the renderer draws a dashed outline. Do not drop these edges — surfacing them is
the point (D-17).

---

## 6. QBAF quantities

Per D-12, acceptability is gradual, not extension-based.

| Symbol | Meaning | Field | Status |
|---|---|---|---|
| $\tau$ | Prior plausibility of an argument | `TheoryAtom.plausibility` | `float \| None` |
| $\phi$ | Edge weight | `TheoryRelation.weight` | `float \| None` |
| $\rho$ | Final strength, iteratively propagated | computed | Overlay `gradual_strength` |

$$\alpha(a_i) = \sum_{(a_j,a_i)\in\mathcal{R}_{sup}} \rho(a_j)\,\phi(a_j,a_i) \;-\; \sum_{(a_j,a_i)\in\mathcal{R}_{att}} \rho(a_j)\,\phi(a_j,a_i)$$

**Both τ and φ are nullable, and both are null in practice today.** The Studio renders
"weight unknown" as a distinct visual state. Substituting 0.0 for a null weight would
silently misreport the graph and defeat the diagnostic purpose.

Out of scope (marked *Not Implemented Yet* in `theorynet_concept.md` §6): internal
coherence via maximal B-consistent subsets, and internal correlation. `OverlayKind`
reserves both names and the API returns `501`.

---

## 7. Available metrics — a scope warning

`../../epistemetrics` currently exports exactly two functions:

```python
internal_correlation(graph: ig.Graph, community_attribute: str = "community") -> float
neo4j_result_to_igraph(records: List[Dict[str, Any]]) -> ig.Graph
```

That is all. The earlier plan's "Evaluate Lakatosian Resilience", "Check Schurz Deductive
Excess" and "Check Dung Acceptability" buttons have **no backing implementation**.

The overlay registry must therefore be built to accommodate near-zero available metrics:
a plugin table of `OverlayKind → callable`, with unimplemented kinds returning `501` and
the UI greying them out rather than offering buttons that fail. At first release the
registry realistically holds `internal_correlation`, `gradual_strength` (new, per §6),
plus cheap structural measures (degree, component id) computed directly from the graph.
