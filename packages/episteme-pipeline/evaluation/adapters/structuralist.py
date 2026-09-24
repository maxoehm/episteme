"""Adapter for the Structuralist Theory-Net Benchmark (STNB).

This module ingests benchmark JSON-LD graph serializations and maps them into
canonical Grund GLP pipeline domain objects and structural NetworkX digraphs
for intrinsic graph evaluation (GM-GBS, OEP, and Epistemetrics).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import networkx as nx

from episteme_pipeline.contracts.domain import L1Chunk


def load_structuralist_benchmark(
    benchmark_path: str | Path,
) -> tuple[list[L1Chunk], nx.DiGraph]:
    """Load an STNB JSON-LD benchmark file into pipeline chunks and a gold DiGraph.

    Parameters
    ----------
    benchmark_path : str or Path
        Filesystem path to the STNB JSON-LD file.

    Returns
    -------
    tuple of (list of L1Chunk, nx.DiGraph)
        A 2-tuple containing:
        - chunks : list of L1Chunk
            Source text chunks extracted from `glp:textAnchor` annotations in the
            benchmark graph, ordered by sequential appearance.
        - gold_graph : nx.DiGraph
            Directed graph containing formal structuralist nodes (TheoryElement,
            PotentialModel, ActualModel, PartialPotentialModel, Constraint) and
            relational edges (specializes, reducesTo, hasConstraint).

    Raises
    ------
    FileNotFoundError
        If the specified `benchmark_path` does not exist.
    ValueError
        If the file content is not valid JSON or lacks an `@graph` array.
    """
    path = Path(benchmark_path)
    if not path.is_file():
        raise FileNotFoundError(f"Benchmark file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    graph_nodes = data.get("@graph")
    if not isinstance(graph_nodes, list):
        raise ValueError(f"STNB benchmark file {path} missing '@graph' list.")

    gold_graph = nx.DiGraph()
    chunks: list[L1Chunk] = []
    seen_chunk_ids: set[str] = set()

    for item in graph_nodes:
        node_id = item.get("@id")
        if not node_id:
            continue

        node_type = item.get("@type", "TheoryElement")
        label = item.get("rdfs:label", node_id)
        formal_axiom = item.get("str:formalAxiom", "")
        anchor = item.get("glp:textAnchor")

        if anchor and isinstance(anchor, dict):
            chunk_id = anchor.get("chunkId", f"chunk_{node_id}")
            quote = anchor.get("verbatimQuote", "")
            source_doc_id = anchor.get("sourceDocId", "unknown_doc")

            if chunk_id not in seen_chunk_ids and quote:
                seen_chunk_ids.add(chunk_id)
                chunks.append(
                    L1Chunk(
                        id=chunk_id,
                        text=quote,
                        source_doc_id=source_doc_id,
                        sequence_index=len(chunks),
                        token_count=len(quote.split()),
                        metadata={
                            "char_start": anchor.get("charStart"),
                            "char_end": anchor.get("charEnd"),
                            "anchored_node_id": node_id,
                        },
                    )
                )

        gold_graph.add_node(
            node_id,
            label=label,
            node_type=node_type,
            formal_axiom=formal_axiom,
            anchor=anchor,
        )

        # Map relational edges
        if "str:specializes" in item:
            gold_graph.add_edge(node_id, item["str:specializes"], relation="specializes")
        if "str:reducesTo" in item:
            gold_graph.add_edge(node_id, item["str:reducesTo"], relation="reducesTo")
        if "str:hasConstraint" in item:
            gold_graph.add_edge(node_id, item["str:hasConstraint"], relation="hasConstraint")
        if "str:hasActualModel" in item:
            gold_graph.add_edge(node_id, item["str:hasActualModel"], relation="hasActualModel")
        if "str:hasPotentialModel" in item:
            gold_graph.add_edge(node_id, item["str:hasPotentialModel"], relation="hasPotentialModel")
        if "str:hasPartialPotentialModel" in item:
            gold_graph.add_edge(node_id, item["str:hasPartialPotentialModel"], relation="hasPartialPotentialModel")

    return chunks, gold_graph
