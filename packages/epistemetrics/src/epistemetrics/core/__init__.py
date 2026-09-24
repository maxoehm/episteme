"""
Core domain contracts, models, and exceptions for epistemetrics.
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

__all__ = [
    "AdapterError",
    "AlgorithmConvergenceError",
    "AlgorithmError",
    "AlgorithmExecutionMode",
    "CentralityResult",
    "DomainValidationError",
    "EpistemetricsError",
    "GDSNotAvailableError",
    "GDSProjectionError",
    "GraphNotFoundError",
    "PartitionResult",
    "RepositoryConnectionError",
]
