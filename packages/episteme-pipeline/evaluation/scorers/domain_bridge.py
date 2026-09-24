from __future__ import annotations

import networkx as nx

from episteme_pipeline.contracts.domain import L2Entity, L2Triple, TheoryAtom, TheoryRelation
from evaluation.scorers.networkx_builder import build_digraph


def l2_triples_to_digraph(entities: list[L2Entity], triples: list[L2Triple]) -> nx.DiGraph:
    """
    Convert L2 entities and triples to a NetworkX DiGraph.

    Parameters
    ----------
    entities : list[L2Entity]
        A list of L2 entities to add as nodes.
    triples : list[L2Triple]
        A list of L2 triples to add as directed edges.

    Returns
    -------
    nx.DiGraph
        A NetworkX directed graph where entities are nodes (labeled by name)
        and triples are directed edges (labeled by predicate).
    """
    graph = nx.DiGraph()

    # Create mapping from entity id to entity to get names and attributes
    entity_dict = {ent.id: ent for ent in entities}

    for ent in entities:
        graph.add_node(
            ent.name,
            id=ent.id,
            label=ent.label,
            description=ent.description,
            is_mature=ent.is_mature,
        )

    for triple in triples:
        u = entity_dict.get(triple.subject_id)
        v = entity_dict.get(triple.object_id)

        if u and v:
            graph.add_edge(
                u.name,
                v.name,
                label=triple.predicate,
                confidence=triple.confidence,
                scope=triple.scope,
            )

    return graph


def theory_net_to_digraph(atoms: list[TheoryAtom], relations: list[TheoryRelation]) -> nx.DiGraph:
    """
    Convert L3 TheoryAtoms and TheoryRelations to a NetworkX DiGraph.

    Parameters
    ----------
    atoms : list[TheoryAtom]
        A list of TheoryAtoms to add as nodes.
    relations : list[TheoryRelation]
        A list of TheoryRelations to add as directed edges.

    Returns
    -------
    nx.DiGraph
        A NetworkX directed graph where atoms are nodes (labeled by text)
        and relations are directed edges (labeled by relation_type).
    """
    graph = nx.DiGraph()

    atom_dict = {atom.id: atom for atom in atoms}

    for atom in atoms:
        graph.add_node(
            atom.text,
            id=atom.id,
            component_type=atom.component_type,
            confidence=atom.confidence,
        )

    for rel in relations:
        u = atom_dict.get(rel.source_id)
        v = atom_dict.get(rel.target_id)

        if u and v:
            graph.add_edge(
                u.text,
                v.text,
                label=rel.relation_type,
                confidence=rel.confidence,
                scope=rel.scope,
                weight=rel.weight,
            )

    return graph


def gold_standard_to_digraph(triples: list[dict]) -> nx.DiGraph:
    """
    Convert gold standard data to a NetworkX DiGraph.

    This is a thin wrapper around the existing build_digraph function.

    Parameters
    ----------
    triples : list[dict]
        A list of dictionaries representing graph edges. Expected to contain
        'head', 'relation', and 'tail' keys.

    Returns
    -------
    nx.DiGraph
        A NetworkX directed graph where entities are nodes and relationships
        are directed edges with a 'label' attribute.
    """
    return build_digraph(triples)
