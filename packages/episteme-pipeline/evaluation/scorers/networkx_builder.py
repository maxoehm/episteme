import networkx as nx

def build_digraph(triples: list[dict]) -> nx.DiGraph:
    """
    Construct a NetworkX directed graph from a list of triple dictionaries.

    Parameters
    ----------
    triples : list[dict]
        A list of dictionaries representing graph edges. Expected to contain
        'head', 'relation', and 'tail' keys. Example:
        [{'head': 'Entity A', 'relation': 'CAUSES', 'tail': 'Entity B'}]

    Returns
    -------
    nx.DiGraph
        A NetworkX directed graph where entities are nodes and relationships
        are directed edges with a 'label' attribute.
    """
    graph = nx.DiGraph()
    for triple in triples:
        u = triple.get("head")
        v = triple.get("tail")
        relation = triple.get("relation")

        if u and v and relation:
            # Add edge automatically creates nodes if they don't exist
            graph.add_edge(u, v, label=relation)

    return graph
