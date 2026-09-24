"""
Exception hierarchy for epistemetrics.

Defines all domain-level exceptions used across the core engine,
epistemic evaluators, and infrastructure adapters.
"""

from __future__ import annotations


class EpistemetricsError(Exception):
    """Base exception for all domain errors raised by epistemetrics."""


class DomainValidationError(EpistemetricsError):
    """Raised when domain constraints or ontology contracts are violated."""


class AlgorithmError(EpistemetricsError):
    """Base exception for graph algorithm failures."""


class AlgorithmConvergenceError(AlgorithmError):
    """Raised when an iterative algorithm (e.g. PageRank, Eigenvector) fails to converge."""


class AdapterError(EpistemetricsError):
    """Base exception for infrastructure adapter errors."""


class RepositoryConnectionError(AdapterError):
    """Raised when connecting to an external graph store (e.g. Neo4j) fails."""


class GraphNotFoundError(AdapterError):
    """Raised when a requested graph or subgraph does not exist in the store."""


class GDSNotAvailableError(AdapterError):
    """Raised when Neo4j Graph Data Science (GDS) plugin is not installed or enabled."""


class GDSProjectionError(AdapterError):
    """Raised when GDS in-memory graph projection fails or does not exist."""
