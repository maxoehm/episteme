"""TheoryNet projection — constructs the core epistemological formalism from artifacts.

Projects Phase 4 artifact outputs into the unified Theory Graph (TheoryNet) formalism.
"""

from __future__ import annotations

from episteme_pipeline.artifacts.execution import Phase4ArtifactsView
from episteme_pipeline.contracts.domain import TheoryNet, TheoryAtom, TheoryRelation

from episteme_pipeline.schema.default_schema import SchemaConfig


class TheoryNetProjector:
    """Project Phase 4 artifacts into a TheoryNet structure."""

    def __init__(self, schema: SchemaConfig | None = None):
        self.schema = schema or SchemaConfig()

    def project(
        self,
        view: Phase4ArtifactsView,
    ) -> TheoryNet:
        """Constructs the full TheoryNet formal model from pipeline artifacts.

        Returns:
            ``TheoryNet`` containing all atoms (B ∪ A) and relations (R).
        """
        # Retrieve all theory relations (including Zuordnungsgesetze and QBAF subsystem logic)
        relations = []
        for r in view.theory_relations:
            rel = r.model_copy()
            rel.weight = self.compute_relation_weight(rel)
            relations.append(rel)

        # Retrieve all theory atoms (empirical base and theoretical antecedents)
        atoms = []
        for c in view.theory_atoms:
            atom = c.model_copy()
            atom.plausibility = self.compute_weight(atom)
            atoms.append(atom)
            
        # QBAF Gradual Semantics Iteration
        atom_by_id = {a.id: a for a in atoms}
        incoming_rels = {a.id: [] for a in atoms}
        for rel in relations:
            if rel.target_id in incoming_rels:
                incoming_rels[rel.target_id].append(rel)
                
        for _ in range(5):
            new_plausibilities = {}
            for atom in atoms:
                base = atom.confidence if atom.confidence is not None else 1.0
                agg = 0.0
                for rel in incoming_rels[atom.id]:
                    source = atom_by_id.get(rel.source_id)
                    if source:
                        src_plausibility = source.plausibility if source.plausibility is not None else 1.0
                        rel_weight = rel.weight if rel.weight is not None else 0.0
                        agg += src_plausibility * rel_weight
                
                new_plausibilities[atom.id] = max(0.0, min(1.0, base + agg))
                
            for atom in atoms:
                atom.plausibility = new_plausibilities[atom.id]

        return TheoryNet(
            atoms=atoms,
            relations=relations,
        )

    def compute_weight(self, atom: TheoryAtom) -> float:
        if atom.plausibility is not None:
            return atom.plausibility
        return atom.confidence if atom.confidence is not None else 1.0

    def compute_relation_weight(self, rel: TheoryRelation) -> float:
        base = rel.weight if rel.weight is not None else (rel.confidence if rel.confidence is not None else 1.0)
        polarity = self.schema.relation_polarities.get(rel.relation_type, 0)
        return float(base * polarity)
