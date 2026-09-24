"""Comparison scaffolding for evaluating multiple runs against each other.

As described in docs/evaluation/methodology.md section 11, the pipeline
should evaluate not only whether a method works, but whether it works
better than alternatives. This module provides the scaffolding for
comparative evaluation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ComparisonAxis(StrEnum):
    METHOD = "method"
    PROMPT = "prompt"
    SCHEMA = "schema"
    CHUNKING = "chunking"
    THRESHOLD = "threshold"
    CLUSTERING = "clustering"


class RunComparison(BaseModel):
    """Side-by-side metrics for two runs on the same dataset."""

    run_id_a: str
    run_id_b: str
    metric_name: str
    value_a: float
    value_b: float
    axis: ComparisonAxis = ComparisonAxis.METHOD
    delta: float = 0.0
    winner: str | None = None  # "a", "b", or None = tie


class EvaluationComparison(BaseModel):
    """A comparative evaluation across multiple runs and metrics.

    Each comparison references the runs being compared, the dataset
    used, and the set of metrics that were compared.
    """

    comparison_id: str
    run_ids: list[str]
    axis: ComparisonAxis
    dataset_ref: str | None = None
    dataset_type: str | None = None
    schema_version: str | None = None
    pipeline_version: str | None = None
    pairwise_comparisons: list[RunComparison] = Field(default_factory=list)
    summary: str = ""
    created_at: datetime = Field(default_factory=utc_now)
