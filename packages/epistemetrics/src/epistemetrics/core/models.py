"""
Domain models and DTOs for graph algorithms and evaluation.

Provides validated boundary data transfer objects and normalized result
containers for topological graph algorithms (centralities, community detection,
and connectivity components).
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Iterator, Mapping
import numpy as np
from pydantic import BaseModel, ConfigDict, Field


class AlgorithmExecutionMode(str, Enum):
    """Execution mode for graph data science algorithms.

    Attributes
    ----------
    STREAM : str
        Stream computation results directly back as rows.
    MUTATE : str
        Write computation results back into an in-memory graph projection.
    WRITE : str
        Write computation results back into database node/relationship properties.
    STATS : str
        Return statistical summary without mutating or returning all rows.
    """

    STREAM = "stream"
    MUTATE = "mutate"
    WRITE = "write"
    STATS = "stats"


class CentralityResult(BaseModel, Mapping[str, float]):
    """Standardized result container for node centrality calculations.

    Provides a dictionary-like interface mapping node identifiers to their
    continuous centrality scores, alongside metadata regarding algorithm provenance.

    Parameters
    ----------
    scores : dict[str, float]
        Mapping from canonical node IDs to computed centrality scores.
    algorithm : str
        Name of the centrality algorithm (e.g. 'pagerank', 'betweenness').
    backend : str
        Execution backend responsible for computation (e.g. 'neo4j_gds', 'networkx').
    """

    model_config = ConfigDict(frozen=True)

    scores: dict[str, float] = Field(
        default_factory=dict,
        description="Mapping from node domain ID to centrality score.",
    )
    algorithm: str = Field(
        ...,
        description="Name of the computed algorithm.",
    )
    backend: str = Field(
        ...,
        description="Underlying execution backend ('neo4j_gds' or 'networkx').",
    )

    def __getitem__(self, node_id: str) -> float:
        """Retrieve centrality score for a specific node ID."""
        return self.scores[node_id]

    def __iter__(self) -> Iterator[str]:
        """Iterate over all node IDs in the result."""
        return iter(self.scores)

    def __len__(self) -> int:
        """Return total number of scored nodes."""
        return len(self.scores)

    def top_k(self, k: int = 5) -> list[tuple[str, float]]:
        """Return the top-k highest scored nodes in descending order.

        Parameters
        ----------
        k : int, optional
            Number of top nodes to return (default: 5).

        Returns
        -------
        list[tuple[str, float]]
            List of (node_id, score) pairs sorted from highest to lowest.
        """
        sorted_items = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        return sorted_items[:k]

    @property
    def max_score(self) -> float:
        """Return maximum centrality score, or 0.0 if empty."""
        return max(self.scores.values()) if self.scores else 0.0

    @property
    def min_score(self) -> float:
        """Return minimum centrality score, or 0.0 if empty."""
        return min(self.scores.values()) if self.scores else 0.0

    @property
    def mean_score(self) -> float:
        """Return arithmetic mean of centrality scores, or 0.0 if empty."""
        if not self.scores:
            return 0.0
        return float(np.mean(list(self.scores.values())))


class PartitionResult(BaseModel):
    """Standardized result container for graph partition and community algorithms.

    Parameters
    ----------
    partitions : list[set[str]]
        List of disjoint node ID sets representing detected communities or components.
    node_to_partition : dict[str, int]
        Mapping from individual node ID to its assigned partition/community index.
    algorithm : str
        Name of the partition algorithm (e.g. 'louvain', 'wcc').
    backend : str
        Execution backend responsible for computation ('neo4j_gds' or 'networkx').
    """

    model_config = ConfigDict(frozen=True)

    partitions: list[set[str]] = Field(
        default_factory=list,
        description="List of component/community node sets.",
    )
    node_to_partition: dict[str, int] = Field(
        default_factory=dict,
        description="Mapping from node domain ID to partition index.",
    )
    algorithm: str = Field(
        ...,
        description="Name of the computed algorithm.",
    )
    backend: str = Field(
        ...,
        description="Underlying execution backend ('neo4j_gds' or 'networkx').",
    )

    @property
    def num_partitions(self) -> int:
        """Return total number of detected partitions."""
        return len(self.partitions)

    def partition_of(self, node_id: str) -> int:
        """Retrieve the partition ID assigned to a node.

        Parameters
        ----------
        node_id : str
            Domain identifier of the node.

        Returns
        -------
        int
            Partition index.

        Raises
        ------
        KeyError
            If node_id is not found in the partition result.
        """
        return self.node_to_partition[node_id]

    def get_partition(self, partition_id: int) -> set[str]:
        """Retrieve the set of nodes belonging to a partition.

        Parameters
        ----------
        partition_id : int
            Index of the partition.

        Returns
        -------
        set[str]
            Set of node IDs.
        """
        return self.partitions[partition_id]

    @property
    def partition_sizes(self) -> list[int]:
        """Return the size of each partition in order."""
        return [len(part) for part in self.partitions]
