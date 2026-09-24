"""
Neo4j adapter subpackage for epistemetrics.

Provides connection handling, session management, and server-side Graph Data Science (GDS)
algorithm execution.
"""

from __future__ import annotations

from epistemetrics.adapters.neo4j.client import Neo4jClient
from epistemetrics.adapters.neo4j.gds_engine import Neo4jGDSAlgorithmsEngine

__all__ = [
    "Neo4jClient",
    "Neo4jGDSAlgorithmsEngine",
]
