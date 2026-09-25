"""Extrinsic Information Retrieval (IR) evaluator."""

from __future__ import annotations

import math
from typing import Any, Callable

from episteme_pipeline.evaluation.extrinsic import calculate_hits_at_k, calculate_mrr, calculate_ndcg
from episteme_pipeline.protocols.graph_store import GraphReader


class ExtrinsicRetrievalEvaluator:
    """Evaluates downstream knowledge graph utility via Information Retrieval metrics."""

    def __init__(
        self,
        graph_reader: GraphReader | None,
        embed_fn: Callable[[list[str]], Any] | None = None,
    ) -> None:
        """Initialize the extrinsic retrieval evaluator.

        Parameters
        ----------
        graph_reader : GraphReader, optional
            The protocol interface for executing queries against the graph store.
        embed_fn : Callable[[list[str]], Any], optional
            Function that takes query strings and returns vector embeddings.
        """
        self.graph_reader = graph_reader
        self.embed_fn = embed_fn

    async def evaluate_query(
        self,
        query: str,
        gold_node_ids: set[str],
        top_k: int = 10,
    ) -> dict[str, float]:
        """Execute a query and calculate ranking metrics against gold standard IDs.

        Parameters
        ----------
        query : str
            Benchmark question or search query.
        gold_node_ids : set of str
            Ground-truth relevant identifiers.
        top_k : int, optional
            Maximum number of results to retrieve (default: 10).

        Returns
        -------
        dict of str to float
            MRR, Hits@k, nDCG, and AP scores.
        """
        if not gold_node_ids:
            return {"MRR": 0.0, f"Hits@{top_k}": 0.0, "nDCG": 0.0, "AP": 0.0}

        if self.graph_reader is None or self.embed_fn is None:
            return {"MRR": 0.0, f"Hits@{top_k}": 0.0, "nDCG": 0.0, "AP": 0.0}

        # Embed query and search
        query_embedding = self.embed_fn([query])[0]
        results = await self.graph_reader.vector_search(
            embedding=query_embedding, top_k=top_k
        )

        retrieved_ids = [res.node_id for res in results]
        mrr = calculate_mrr([retrieved_ids], [gold_node_ids])
        hits_k = calculate_hits_at_k([retrieved_ids], [gold_node_ids], k=top_k)
        ndcg = calculate_ndcg([retrieved_ids], [{gid: 1.0 for gid in gold_node_ids}], k=top_k)
        ap = self._calculate_average_precision(retrieved_ids, gold_node_ids)

        return {"MRR": mrr, f"Hits@{top_k}": hits_k, "nDCG": ndcg, "AP": ap}

    def _calculate_average_precision(self, retrieved: list[str], gold: set[str]) -> float:
        num_relevant_found = 0
        sum_precisions = 0.0

        for i, doc_id in enumerate(retrieved):
            if doc_id in gold:
                num_relevant_found += 1
                precision_at_i = num_relevant_found / (i + 1)
                sum_precisions += precision_at_i

        return sum_precisions / len(gold) if len(gold) > 0 else 0.0
