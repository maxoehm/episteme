import networkx as nx


class OptimalEditPathEvaluator:
    """
    Computes Optimal Edit Paths (OEP) to calculate hallucination and omission rates.
    """

    @staticmethod
    def compute_rates(
        pred_graph: nx.DiGraph,
        gold_graph: nx.DiGraph,
        matched_pred_edges: list,
        matched_gold_edges: list,
    ) -> tuple[float, float]:
        """
        Calculate Hallucination Rate and Omission Rate based on edge matches.

        Parameters
        ----------
        pred_graph : nx.DiGraph
            The predicted knowledge graph.
        gold_graph : nx.DiGraph
            The ground-truth knowledge graph.
        matched_pred_edges : list
            List of edges from the predicted graph that found a semantic
            match in the gold graph (from GM-GBS).
        matched_gold_edges : list
            List of edges from the gold graph that were matched.

        Returns
        -------
        tuple[float, float]
            - hallucination_rate: % of predicted edges without a match.
            - omission_rate: % of gold edges that were not matched.
        """
        num_pred_edges = pred_graph.number_of_edges()
        num_gold_edges = gold_graph.number_of_edges()

        if num_pred_edges == 0:
            hallucination_rate = 0.0
        else:
            # Hallucinations = predicted edges that were not matched
            hallucinated_edges = num_pred_edges - len(matched_pred_edges)
            hallucination_rate = hallucinated_edges / num_pred_edges

        if num_gold_edges == 0:
            omission_rate = 0.0
        else:
            # Omissions = gold edges that were not covered by predictions
            # Using set to handle potential multiple predictions mapping to same gold edge
            unique_matched_gold = len(set(matched_gold_edges))
            omitted_edges = num_gold_edges - unique_matched_gold
            omission_rate = omitted_edges / num_gold_edges

        return hallucination_rate, omission_rate
