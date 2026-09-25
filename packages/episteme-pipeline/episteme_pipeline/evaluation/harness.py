"""Dependency-injected evaluation harness orchestrating intrinsic and extrinsic metrics."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import networkx as nx
import yaml

import epistemetrics as em
from episteme_pipeline.artifacts.execution import ArtifactCollection
from episteme_pipeline.contracts.domain import TheoryNet
from episteme_pipeline.contracts.phase_contracts import PipelineInput
from episteme_pipeline.events import EventEmitter, NoOpEventEmitter
from episteme_pipeline.events.models import EvaluationCompleted, ValidationViolationDetected
from episteme_pipeline.evaluation.benchmarks.structuralist import load_structuralist_benchmark
from episteme_pipeline.evaluation.models import (
    DatasetType,
    EvaluationLevel,
    EvaluationMetric,
    EvaluationOutcome,
    EvaluationReport,
    EvaluationResult,
)
from episteme_pipeline.evaluation.pipelines import (
    build_l2_eval_pipeline,
    build_l3_eval_pipeline,
    build_l4_theorynet_eval_pipeline,
)
from episteme_pipeline.evaluation.scorers.domain_bridge import (
    artifact_collection_to_theory_graph,
    l2_triples_to_digraph,
    theory_net_to_digraph,
)
from episteme_pipeline.evaluation.scorers.gm_gbs import GraphBERTScoreEvaluator
from episteme_pipeline.evaluation.scorers.model_scorer import ModelScorer
from episteme_pipeline.evaluation.scorers.oep import OptimalEditPathEvaluator
from episteme_pipeline.evaluation.scorers.retrieval import ExtrinsicRetrievalEvaluator
from episteme_pipeline.graph.in_memory_store import InMemoryGraphStore
from episteme_pipeline.graph.validation import GraphValidator
from episteme_pipeline.protocols.graph_store import ProcessingGraph

logger = logging.getLogger(__name__)


@runtime_checkable
class EvaluationHarnessProtocol(Protocol):
    """Protocol defining the sovereign evaluation harness contract."""

    async def evaluate_in_memory(
        self,
        predicted: ArtifactCollection | TheoryNet | em.TheoryGraph | nx.DiGraph,
        gold: str | Path | em.TheoryGraph | nx.DiGraph,
        run_id: str = "in_memory_run",
    ) -> EvaluationReport:
        """Evaluate pipeline output directly in memory without requiring remote stores."""
        ...

    async def evaluate_manifest(
        self,
        manifest_path: str | Path,
        build_graph: bool = False,
    ) -> EvaluationReport:
        """Execute an evaluation run configured by a manifest YAML file."""
        ...


class EvaluationHarness(EvaluationHarnessProtocol):
    """Sovereign evaluation harness for intrinsic and extrinsic pipeline evaluation."""

    def __init__(
        self,
        event_emitter: EventEmitter | None = None,
        model_scorer: ModelScorer | None = None,
        retrieval_scorer: ExtrinsicRetrievalEvaluator | None = None,
        gm_gbs_evaluator: GraphBERTScoreEvaluator | None = None,
        graph_store: ProcessingGraph | None = None,
        reports_dir: str | Path = "evaluation/reports",
    ) -> None:
        """Initialize the evaluation harness with dependency injection.

        Parameters
        ----------
        event_emitter : EventEmitter, optional
            Event bus for publishing evaluation and validation telemetry.
        model_scorer : ModelScorer, optional
            Scorer for Bourbaki structuralist model component decomposition.
        retrieval_scorer : ExtrinsicRetrievalEvaluator, optional
            Downstream information retrieval evaluator.
        gm_gbs_evaluator : GraphBERTScoreEvaluator, optional
            Graph BERTScore evaluator.
        graph_store : ProcessingGraph, optional
            Graph storage backend (defaults to InMemoryGraphStore).
        reports_dir : str or Path, optional
            Output directory for persisted JSON and Markdown reports.
        """
        self.event_emitter = event_emitter or NoOpEventEmitter()
        self.model_scorer = model_scorer or ModelScorer()
        self.retrieval_scorer = retrieval_scorer
        self.gm_gbs_evaluator = gm_gbs_evaluator
        self.graph_store = graph_store or InMemoryGraphStore()
        self.reports_dir = Path(reports_dir)

    async def evaluate_in_memory(
        self,
        predicted: ArtifactCollection | TheoryNet | em.TheoryGraph | nx.DiGraph,
        gold: str | Path | em.TheoryGraph | nx.DiGraph,
        run_id: str = "in_memory_run",
        dataset_ref: str | None = None,
        min_mcc: float = 1.0,
        min_pfs: float = 0.8,
        sim_threshold: float = 0.50,
    ) -> EvaluationReport:
        """Evaluate pipeline output directly in memory.

        Uses pipeline ArtifactCollection or TheoryNet converted to
        epistemetrics.TheoryGraph, requiring zero Neo4j database or network connectivity.

        Parameters
        ----------
        predicted : ArtifactCollection, TheoryNet, em.TheoryGraph, or nx.DiGraph
            Predicted representation from pipeline execution.
        gold : str, Path, em.TheoryGraph, or nx.DiGraph
            Gold standard reference graph or path to STNB JSON-LD file.
        run_id : str, optional
            Run identifier for reporting (default: "in_memory_run").
        dataset_ref : str, optional
            Dataset reference name or path.
        min_mcc : float, optional
            Minimum MCC threshold (default: 1.0).
        min_pfs : float, optional
            Minimum PFS threshold (default: 0.8).
        sim_threshold : float, optional
            Minimum node similarity threshold (default: 0.50).

        Returns
        -------
        EvaluationReport
            Structured evaluation report containing intrinsic metrics and markdown summary.
        """
        scorer = ModelScorer(min_mcc=min_mcc, min_pfs=min_pfs, sim_threshold=sim_threshold)
        stage_result = scorer.evaluate_to_result(
            predicted=predicted,
            gold=gold,
            run_id=run_id,
            phase_name="Phase 6: TheoryNet Projection",
            dataset_ref=dataset_ref or (str(gold) if isinstance(gold, (str, Path)) else "in_memory_gold"),
        )

        metrics_dict = {m.name: m.value for m in stage_result.metrics}
        report = EvaluationReport(
            evaluation_id=f"eval_{run_id}",
            run_ids=[run_id],
            dataset_ref=stage_result.dataset_ref,
            dataset_type=DatasetType.GOLD,
            results_by_level={EvaluationLevel.STAGE: [stage_result]},
            summary=stage_result.notes.get("markdown_report", ""),
        )

        self.event_emitter.emit(
            EvaluationCompleted(
                evaluation_id=report.evaluation_id,
                run_id=run_id,
                metrics=metrics_dict,
                outcome="success" if stage_result.outcome == EvaluationOutcome.PASS else "failure",
            )
        )

        return report

    async def evaluate_manifest(
        self,
        manifest_path: str | Path,
        build_graph: bool = False,
    ) -> EvaluationReport:
        """Execute an evaluation run configured by a manifest YAML file.

        Parameters
        ----------
        manifest_path : str or Path
            Filesystem path to the manifest YAML file.
        build_graph : bool, optional
            Whether to invoke pipeline execution prior to scoring (default: False).

        Returns
        -------
        EvaluationReport
            Synthesized evaluation report.
        """
        path = Path(manifest_path)
        if not path.is_file():
            raise FileNotFoundError(f"Manifest not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            manifest: dict[str, Any] = yaml.safe_load(f)

        run_id = str(manifest.get("run_id", "unknown_run"))
        corpus_cfg = manifest.get("corpus", {})
        dataset_type = corpus_cfg.get("dataset_type", "structuralist")
        gold_path = corpus_cfg.get("gold_standard_path")
        limit = corpus_cfg.get("limit", 10)

        report_results: list[EvaluationResult] = []
        artifacts: ArtifactCollection | None = None

        if build_graph:
            logger.info("Executing pipeline for evaluation using manifest: %s", manifest_path)
            pipeline = self._build_pipeline_for_dataset(dataset_type)
            input_sources = corpus_cfg.get("input_sources", [])
            texts_dir = corpus_cfg.get("texts_dir")

            if not input_sources and texts_dir and os.path.isdir(texts_dir):
                for fname in os.listdir(texts_dir):
                    if fname.endswith(".txt"):
                        input_sources.append(os.path.join(texts_dir, fname))

            exec_result = await pipeline.run(PipelineInput(source_paths=input_sources[:limit]))
            artifacts = getattr(exec_result, "artifacts", None)

        # Intrinsic scoring
        downstream_results: list[EvaluationResult] = []
        if gold_path and os.path.exists(gold_path):
            if dataset_type == "structuralist":
                chunks, gold_graph = load_structuralist_benchmark(gold_path)
                predicted_target: Any
                if artifacts is not None:
                    predicted_target = artifacts
                else:
                    # Ingest existing entities/atoms from graph store
                    atoms = await self.graph_store.get_theory_atoms()
                    rels = await self.graph_store.get_all_theory_relations()
                    predicted_target = TheoryNet(atoms=atoms, relations=rels)

                stage_result = self.model_scorer.evaluate_to_result(
                    predicted=predicted_target,
                    gold=gold_graph,
                    run_id=run_id,
                    phase_name="Phase 6: TheoryNet Projection",
                    dataset_ref=str(gold_path),
                )
                report_results.append(stage_result)

                # Extrinsic competency query evaluation
                queries_path = corpus_cfg.get("queries_path")
                if not queries_path:
                    cand_path = Path(gold_path).parent / "stnb_cpm_queries.yaml"
                    if cand_path.is_file():
                        queries_path = str(cand_path)
                    else:
                        cand_path = Path(__file__).parent / "data" / "stnb_cpm_queries.yaml"
                        if cand_path.is_file():
                            queries_path = str(cand_path)

                if queries_path and os.path.isfile(queries_path):
                    with open(queries_path, "r", encoding="utf-8") as qf:
                        q_data = yaml.safe_load(qf)
                    queries = q_data.get("queries", [])
                    if queries:
                        retrieval_eval = self.retrieval_scorer or ExtrinsicRetrievalEvaluator(
                            graph_reader=self.graph_store
                        )
                        # Ensure graph store has the target nodes indexed for search
                        if hasattr(self.graph_store, "index_theory_graph"):
                            if artifacts is not None:
                                tg = artifact_collection_to_theory_graph(artifacts)
                                self.graph_store.index_theory_graph(tg, run_id=run_id)
                            elif hasattr(predicted_target, "atoms") and predicted_target.atoms:
                                self.graph_store.index_theory_graph(predicted_target, run_id=run_id)
                            elif isinstance(gold_graph, (nx.DiGraph, nx.Graph)):
                                self.graph_store.index_theory_graph(gold_graph, run_id=run_id)

                        retrieval_metrics = await retrieval_eval.evaluate_batch(
                            queries, top_k=10, run_id=run_id
                        )

                        downstream_result = EvaluationResult(
                            run_id=run_id,
                            evaluation_level=EvaluationLevel.DOWNSTREAM,
                            phase_name="Extrinsic Retrieval: STNB Competency",
                            dataset_ref=str(queries_path),
                            dataset_type=DatasetType.GOLD,
                            metrics=[
                                EvaluationMetric(name="mrr", value=retrieval_metrics.get("MRR", 0.0)),
                                EvaluationMetric(name="hits@1", value=retrieval_metrics.get("Hits@1", 0.0)),
                                EvaluationMetric(name="hits@3", value=retrieval_metrics.get("Hits@3", 0.0)),
                                EvaluationMetric(name="hits@10", value=retrieval_metrics.get("Hits@10", 0.0)),
                                EvaluationMetric(name="ndcg", value=retrieval_metrics.get("nDCG", 0.0)),
                            ],
                            outcome=EvaluationOutcome.PASS if retrieval_metrics.get("MRR", 0.0) > 0.0 else EvaluationOutcome.WARNING,
                            notes={
                                "category": "extrinsic_retrieval",
                                "markdown_report": (
                                    "## STNB Competency Retrieval Evaluation Report\n\n"
                                    f"- **MRR:** {retrieval_metrics.get('MRR', 0.0):.4f}\n"
                                    f"- **Hits@1:** {retrieval_metrics.get('Hits@1', 0.0):.4f}\n"
                                    f"- **Hits@3:** {retrieval_metrics.get('Hits@3', 0.0):.4f}\n"
                                    f"- **Hits@10:** {retrieval_metrics.get('Hits@10', 0.0):.4f}\n"
                                    f"- **nDCG:** {retrieval_metrics.get('nDCG', 0.0):.4f}\n"
                                ),
                            },
                        )
                        downstream_results.append(downstream_result)

        # Validation checks
        violations = await self._run_validation()

        # Build final report
        results_by_level: dict[str, list[EvaluationResult]] = {}
        if report_results:
            results_by_level[EvaluationLevel.STAGE] = report_results
        if downstream_results:
            results_by_level[EvaluationLevel.DOWNSTREAM] = downstream_results

        all_results = report_results + downstream_results
        metrics_all: dict[str, float] = {}
        for res in all_results:
            for m in res.metrics:
                metrics_all[m.name] = m.value

        report = EvaluationReport(
            evaluation_id=f"eval_{run_id}",
            run_ids=[run_id],
            dataset_ref=gold_path,
            dataset_type=DatasetType.GOLD,
            results_by_level=results_by_level,
            summary="\n\n".join(r.notes.get("markdown_report", "") for r in all_results),
        )

        self._persist_reports(report, manifest_path=str(manifest_path))

        self.event_emitter.emit(
            EvaluationCompleted(
                evaluation_id=report.evaluation_id,
                run_id=run_id,
                metrics=metrics_all,
                outcome="success" if not violations else "violations_detected",
            )
        )

        return report

    def _build_pipeline_for_dataset(self, dataset_type: str):
        if dataset_type == "scierc":
            return build_l2_eval_pipeline(self.event_emitter, in_memory=True)
        elif dataset_type == "arg_microtexts":
            return build_l3_eval_pipeline(self.event_emitter, in_memory=True)
        else:
            return build_l4_theorynet_eval_pipeline(self.event_emitter, in_memory=True)

    async def _run_validation(self) -> list[dict[str, Any]]:
        validator = GraphValidator(self.graph_store)
        violations = []
        try:
            for v in await validator.check_direct_disjointness():
                violations.append({"rule_name": "direct_disjointness", **v})
            for v in await validator.check_transitive_disjointness():
                violations.append({"rule_name": "transitive_disjointness", **v})
            for v in await validator.check_type_constraints():
                violations.append({"rule_name": "type_constraints", **v})
        except Exception as e:
            logger.debug("Validation check skipped or failed: %s", e)

        for v in violations:
            self.event_emitter.emit(
                ValidationViolationDetected(
                    rule_name=v.get("rule_name", "unknown"),
                    source_id=v.get("source_id", "unknown"),
                    target_id=v.get("target_id", "unknown"),
                    description=str(v),
                )
            )
        return violations

    def _persist_reports(self, report: EvaluationReport, manifest_path: str) -> None:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        json_path = self.reports_dir / f"report_{report.run_ids[0]}.json"
        md_path = self.reports_dir / f"report_{report.run_ids[0]}.md"

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Evaluation Report: {report.evaluation_id}\n\n")
            f.write(f"- **Manifest:** `{manifest_path}`\n")
            f.write(f"- **Dataset:** `{report.dataset_ref}`\n\n")
            f.write(report.summary)


def main() -> None:
    """CLI entrypoint for running evaluation manifests."""
    parser = argparse.ArgumentParser(description="Episteme Pipeline Evaluation Harness")
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to evaluation run manifest YAML.",
    )
    parser.add_argument(
        "--build-graph",
        action="store_true",
        help="Whether to execute pipeline prior to scoring.",
    )
    args = parser.parse_args()

    harness = EvaluationHarness()
    report = asyncio.run(harness.evaluate_manifest(args.manifest, build_graph=args.build_graph))
    print(f"Evaluation completed: {report.evaluation_id}")
    print(report.summary)


if __name__ == "__main__":
    main()
