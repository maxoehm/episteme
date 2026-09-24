from __future__ import annotations

import logging
from episteme_pipeline.artifacts.execution import ArtifactCollection, ArtifactExecutionContext, Phase4ArtifactsView
from episteme_pipeline.projection.theorynet_projector import TheoryNetProjector
from episteme_pipeline.schema.default_schema import SchemaConfig
from episteme_pipeline.protocols.graph_store import ProjectionGraph

logger = logging.getLogger(__name__)

from episteme_pipeline.protocols.phase_runner import PhaseRunner

class Phase6Runner(PhaseRunner[Phase4ArtifactsView]):
    """Executes the Phase 6 TheoryNet materialization.

    Constructs the formalized argument graph ($\rho$, $\alpha$) from
    the Phase 4 mined theories.
    """

    name = "Phase 6: TheoryNet Projection"
    phase_key = "phase6"
    input_view = Phase4ArtifactsView

    def __init__(
        self,
        config: dict | None = None,
        schema: SchemaConfig | None = None,
        graph_store: ProjectionGraph | None = None,
        projector: TheoryNetProjector | None = None,
    ) -> None:
        self.config = config
        self.schema = schema or SchemaConfig()
        self.graph_store = graph_store
        self.projector = projector or TheoryNetProjector(schema=self.schema)

    @property
    def event_emitter(self):
        from episteme_pipeline.events.context import get_event_emitter
        return get_event_emitter()

    async def run(
        self, input: Phase4ArtifactsView, context: ArtifactExecutionContext
    ) -> ArtifactCollection:
        logger.info("Phase 6: Projecting formal TheoryNet")
        theory_net = self.projector.project(input)

        if not self.graph_store:
            return ArtifactCollection([])

        atoms_updated = 0
        relations_updated = 0

        atoms_to_upsert = []
        for atom in theory_net.atoms:
            if atom.plausibility is None:
                atom.plausibility = atom.confidence if atom.confidence is not None else 1.0
            atoms_to_upsert.append(atom)
            atoms_updated += 1

        relations_to_upsert = []
        for rel in theory_net.relations:
            if rel.weight is None:
                rel.weight = rel.confidence
            relations_to_upsert.append({
                "from_id": rel.source_id,
                "relation_type": rel.relation_type,
                "to_id": rel.target_id,
                "properties": {"confidence": rel.confidence, "scope": rel.scope, "weight": rel.weight}
            })
            relations_updated += 1

        from itertools import batched
        for atom_batch in batched(atoms_to_upsert, 500):
            await self.graph_store.upsert_argument_components(list(atom_batch))
            
        for rel_batch in batched(relations_to_upsert, 500):
            await self.graph_store.upsert_relations(list(rel_batch))

        logger.info("Phase 6: Updated %d TheoryAtoms and %d TheoryRelations with weights/plausibility", atoms_updated, relations_updated)

        a_atoms = {a.id for a in theory_net.atoms if self.schema.component_partitions.get(a.component_type) == "A"}
        b_atoms = {a.id for a in theory_net.atoms if self.schema.component_partitions.get(a.component_type) == "B"}
        
        adj = {a_id: set() for a_id in a_atoms}
        z1_connected = set()
        
        for rel in theory_net.relations:
            if rel.source_id in a_atoms and rel.target_id in b_atoms:
                z1_connected.add(rel.source_id)
            elif rel.target_id in a_atoms and rel.source_id in b_atoms:
                z1_connected.add(rel.target_id)
            elif rel.source_id in a_atoms and rel.target_id in a_atoms:
                adj[rel.source_id].add(rel.target_id)
                adj[rel.target_id].add(rel.source_id)
                
        visited = set(z1_connected)
        queue = list(z1_connected)
        while queue:
            curr = queue.pop(0)
            for neighbor in adj.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        empirical_content = len(visited) / len(a_atoms) if a_atoms else 0.0
        logger.info("Phase 6: Empirical Content metric = %.3f (%d/%d A-atoms with a Z1 path to B)", empirical_content, len(visited), len(a_atoms))

        return ArtifactCollection([])
