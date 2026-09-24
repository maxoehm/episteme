# Phase 6: TheoryNet Projection

## Overview

Phase 6 executes the **TheoryNet Projection** pass (`Phase6Runner`). Operating on the mined theory atoms and argument relations produced through Phase 4b and clustered in Phase 5, Phase 6 formalizes the graph into a structuralist theory network $T = \langle \mathcal{A}, \mathcal{R}, \rho, \alpha \rangle$.

It assigns plausibility functions ($\rho$) to nodes, weights ($\alpha$) to dialectical relations, and performs structural verification of empirical content via $Z_1$ path reachability.

## Goals

- Project raw argument components into formal theoretical atoms categorized by epistemic partition ($A$ vs. $B$).
- Assign normalized plausibility values to all theory atoms.
- Assign normalized weights to all dialectical relations.
- Evaluate $Z_1$ empirical connectivity: verifying which theoretical hypotheses connect directly or transitively to empirical observations.
- Commit formalized attributes back to the Neo4j graph store.

## Steps

1. **Projection from Artifact View**:
   - Ingests `Phase4ArtifactsView` containing all cumulative `TheoryAtom` and `TheoryRelation` domain objects.
   - Invokes `TheoryNetProjector.project(input)` to generate a strongly-typed `TheoryNet` structure.
2. **Plausibility Scoring ($\rho$)**:
   - For each atom in `theory_net.atoms`:
$$\rho(a) = \begin{cases} \text{confidence}(a) & \text{if confidence is defined} \\ 1.0 & \text{otherwise} \end{cases}$$
   - Prepares atoms for batch upsert.
3. **Relation Weighting ($\alpha$)**:
   - For each relation in `theory_net.relations`:
$$\alpha(r) = \begin{cases} \text{confidence}(r) & \text{if confidence is defined} \\ 1.0 & \text{otherwise} \end{cases}$$
   - Preserves relation properties: `scope` (`"local"` vs. `"global"`), `relation_type`, and `weight`.
4. **Graph Persistence**:
   - Upserts updated `TheoryAtom` nodes in batches of 500 via `graph_store.upsert_argument_components()`.
   - Upserts updated `TheoryRelation` edges in batches of 500 via `graph_store.upsert_relations()`.
5. **Empirical Content ($Z_1$) Verification**:
   - Partitions atoms using `SchemaConfig.component_partitions`:
     - **Partition A**: Theoretical Hypotheses (`component_partitions[type] == "A"`)
     - **Partition B**: Empirical Observations (`component_partitions[type] == "B"`)
   - Constructs the theoretical adjacency graph $\mathcal{G}_A = (V_A, E_{A \times A})$.
   - Identates the direct empirical boundary $Z_1^{\text{direct}} \subseteq V_A$: theoretical atoms that share an edge with at least one $B$-atom.
   - Executes breadth-first search (BFS) starting from $Z_1^{\text{direct}}$ across $\mathcal{G}_A$ to identify all reachable $A$-atoms.
   - Computes empirical content metrics and logs ungrounded theoretical components.

## Phase Data Flow

- **Input:** `Phase4ArtifactsView` (cumulative theory atoms and relations).
- **Output:** Phase 6 `ArtifactCollection` containing formal TheoryNet envelopes.
- **Graph updates:**
  - `ArgumentComponent` / `TheoryAtom` nodes: `plausibility: float`
  - `TheoryRelation` edges: `weight: float`

## Pluggability

- **Projector**: Custom projector implementations can be injected via `Phase6Runner(projector=MyProjector())`.
- **Schema**: Partition definitions and component types are governed by `SchemaConfig`.

## Implementation

- `pipeline/phases/phase6_theorynet/__init__.py` — `Phase6Runner`
- `pipeline/projection/theorynet_projector.py` — `TheoryNetProjector`
- `pipeline/contracts/domain.py` — `TheoryNet`, `TheoryAtom`, `TheoryRelation`
- `pipeline/config.py` — `Phase6Config`
