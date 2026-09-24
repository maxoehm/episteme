"""
Epistemetrics: Formal Theory Graph Evaluation and Epistemic Metrics.

A sovereign Python library for structural, argumentation, and epistemic
evaluation of scientific theory graphs.
"""

from __future__ import annotations

from epistemetrics.core.exceptions import (
    AdapterError,
    AlgorithmConvergenceError,
    AlgorithmError,
    DomainValidationError,
    EpistemetricsError,
    GDSNotAvailableError,
    GDSProjectionError,
    GraphNotFoundError,
    RepositoryConnectionError,
)
from epistemetrics.core.models import (
    AlgorithmExecutionMode,
    CentralityResult,
    PartitionResult,
)
from epistemetrics.graph.algorithms import (
    AdaptiveAlgorithmsEngine,
    GraphAlgorithmsEngine,
    NetworkXAlgorithmsEngine,
    betweenness_centrality,
    eigenvector_centrality,
    louvain_communities,
    page_rank,
    weakly_connected_components,
)

__version__ = "0.1.0"

__all__ = [
    # Engines
    "AdaptiveAlgorithmsEngine",
    "GraphAlgorithmsEngine",
    "NetworkXAlgorithmsEngine",
    # Algorithm entry points
    "betweenness_centrality",
    "eigenvector_centrality",
    "louvain_communities",
    "page_rank",
    "weakly_connected_components",
    # Result models
    "AlgorithmExecutionMode",
    "CentralityResult",
    "PartitionResult",
    # Exceptions
    "AdapterError",
    "AlgorithmConvergenceError",
    "AlgorithmError",
    "DomainValidationError",
    "EpistemetricsError",
    "GDSNotAvailableError",
    "GDSProjectionError",
    "GraphNotFoundError",
    "RepositoryConnectionError",
]
