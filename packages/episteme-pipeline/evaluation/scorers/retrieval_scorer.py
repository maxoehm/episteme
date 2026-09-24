import math
from typing import Any

from episteme_pipeline.protocols.graph_store import GraphReader


class ExtrinsicRetrievalEvaluator:
    """
    Evaluates downstream knowledge graph utility via Information Retrieval metrics.
    """

    def __init__(self, graph_reader: GraphReader, embed_fn: Any):
        """
        Initialize the extrinsic retrieval evaluator.

        Parameters
        ----------
        graph_reader : GraphReader
            The protocol interface for executing queries against the graph store.
        embed_fn : Any
            A function that takes a query string and returns its vector embedding.
        """
        self.graph_reader = graph_reader
        self.embed_fn = embed_fn

    async def evaluate_query(
        self, query: str, gold_node_ids: set[str], top_k: int = 10
    ) -> dict[str, float]:
        """
        Execute a query and calculate ranking metrics against gold standard IDs.

        Parameters
        ----------
        query : str
            The benchmark question or search query.
        gold_node_ids : set[str]
            A set of node identifiers representing the ground-truth relevant
            documents or entities.
        top_k : int, optional
            The maximum number of results to retrieve. Default is 10.

        Returns
        -------
        dict[str, float]
            A dictionary containing MRR, Hits@k, nDCG, and Average Precision.
        """
        if not gold_node_ids:
            return {"MRR": 0.0, f"Hits@{top_k}": 0.0, "nDCG": 0.0, "AP": 0.0}

        # Embed query and search
        query_embedding = self.embed_fn([query])[0]
        results = await self.graph_reader.vector_search(
            embedding=query_embedding, top_k=top_k
        )

        retrieved_ids = [res.id for res in results]

        # Calculate metrics
        mrr = self._calculate_mrr(retrieved_ids, gold_node_ids)
        hits_k = self._calculate_hits_at_k(retrieved_ids, gold_node_ids)
        ndcg = self._calculate_ndcg(retrieved_ids, gold_node_ids)
        ap = self._calculate_average_precision(retrieved_ids, gold_node_ids)

        return {"MRR": mrr, f"Hits@{top_k}": hits_k, "nDCG": ndcg, "AP": ap}

    def _calculate_mrr(self, retrieved: list[str], gold: set[str]) -> float:
        for i, doc_id in enumerate(retrieved):
            if doc_id in gold:
                return 1.0 / (i + 1)
        return 0.0

    def _calculate_hits_at_k(self, retrieved: list[str], gold: set[str]) -> float:
        return 1.0 if any(doc_id in gold for doc_id in retrieved) else 0.0

    def _calculate_ndcg(self, retrieved: list[str], gold: set[str]) -> float:
        dcg = 0.0
        for i, doc_id in enumerate(retrieved):
            if doc_id in gold:
                dcg += 1.0 / math.log2(i + 2)

        # Ideal DCG (if all gold documents were at the top)
        idcg = sum(1.0 / math.log2(i + 2) for i in range(min(len(gold), len(retrieved))))
        return dcg / idcg if idcg > 0 else 0.0

    def _calculate_average_precision(self, retrieved: list[str], gold: set[str]) -> float:
        num_relevant_found = 0
        sum_precisions = 0.0

        for i, doc_id in enumerate(retrieved):
            if doc_id in gold:
                num_relevant_found += 1
                precision_at_i = num_relevant_found / (i + 1)
                sum_precisions += precision_at_i

        return sum_precisions / len(gold) if len(gold) > 0 else 0.0
