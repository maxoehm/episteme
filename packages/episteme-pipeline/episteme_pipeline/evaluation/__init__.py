"""Evaluation scaffolding for the theory-graph construction pipeline.

This package is the minimum viable evaluation setup as described in:
- docs/research/evaluation_methodology.md
- docs/research/evaluation_harness.md
- docs/architecture/remediation_status.md (Phase 3)

It provides:
- EvaluationResult: phase-level evaluation results with metrics and error buckets
- EvaluationReport: a report tied to concrete runs, schemas, corpora, and artifacts
- EvaluationDataset: reference to gold/silver/review/stress-test evaluation datasets
- EvaluationRubric: structured human-review rubrics tied to pipeline runs
- EvaluationComparison: side-by-side comparison of runs for method/tuning comparison
"""

from episteme_pipeline.evaluation.comparison import (
    ComparisonAxis,
    EvaluationComparison,
    RunComparison,
)
from episteme_pipeline.evaluation.datasets import DatasetReference, EvaluationDataset
from episteme_pipeline.evaluation.extrinsic import (
    calculate_hits_at_k,
    calculate_mrr,
    calculate_ndcg,
)
from episteme_pipeline.evaluation.intrinsic import (
    calculate_graph_bertscore,
    calculate_oep_rates,
)
from episteme_pipeline.evaluation.models import (
    DatasetType,
    EvaluationErrorBucket,
    EvaluationLevel,
    EvaluationMetric,
    EvaluationOutcome,
    EvaluationReport,
    EvaluationResult,
)
from episteme_pipeline.evaluation.rubrics import (
    EvaluationJudgment,
    EvaluationRubric,
    RatingLevel,
    RubricCriterion,
)

__all__ = [
    # comparison
    "ComparisonAxis",
    "EvaluationComparison",
    "RunComparison",
    # datasets
    "DatasetReference",
    "EvaluationDataset",
    # extrinsic
    "calculate_hits_at_k",
    "calculate_mrr",
    "calculate_ndcg",
    # intrinsic
    "calculate_graph_bertscore",
    "calculate_oep_rates",
    # models
    "DatasetType",
    "EvaluationErrorBucket",
    "EvaluationLevel",
    "EvaluationMetric",
    "EvaluationOutcome",
    "EvaluationReport",
    "EvaluationResult",
    # rubrics
    "EvaluationJudgment",
    "EvaluationRubric",
    "RatingLevel",
    "RubricCriterion",
]
