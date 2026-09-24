import argparse
import asyncio
import yaml
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add project root to sys.path so 'pipeline' module can be found
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from episteme_pipeline.events import NoOpEventEmitter
from episteme_pipeline.events.models import EvaluationCompleted, ValidationViolationDetected

from evaluation.scorers.gm_gbs import GraphBERTScoreEvaluator
from evaluation.scorers.oep import OptimalEditPathEvaluator
from evaluation.scorers.retrieval_scorer import ExtrinsicRetrievalEvaluator
from evaluation.adapters.export_baseline import load_gold_standard
from evaluation.scorers.domain_bridge import l2_triples_to_digraph, theory_net_to_digraph

from sentence_transformers import SentenceTransformer

from episteme_pipeline.graph import Neo4jGraphReader
from episteme_pipeline.graph.validation import GraphValidator


class EvaluationReport(BaseModel):
    run_id: str
    manifest_path: str
    timestamp: str
    intrinsic_metrics: dict[str, float] = Field(default_factory=dict)
    extrinsic_metrics: dict[str, float] = Field(default_factory=dict)
    validation_violations: list[dict[str, Any]] = Field(default_factory=list)


class EvaluationRun:
    """
    Orchestrates the evaluation pipeline by running intrinsic and extrinsic scorers.
    """

    def __init__(self, manifest_path: str, event_bus=None, build_graph: bool = False):
        self.manifest_path = manifest_path
        self.manifest = self._parse_manifest(manifest_path)
        self.event_bus = event_bus or NoOpEventEmitter()
        self.build_graph = build_graph
        self.report = EvaluationReport(
            run_id=self.manifest.get("run_id", "unknown"),
            manifest_path=manifest_path,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        self.store = None

    def _parse_manifest(self, path: str) -> dict:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    async def run_pipeline(self) -> None:
        """
        Invoke the core knowledge graph construction pipeline using manifest configurations.
        """
        if self.build_graph:
            print(f"Building pipeline for evaluation using manifest: {self.manifest_path}")
            dataset_type = self.manifest.get("corpus", {}).get("dataset_type", "baseline")
            
            # Determine pipeline depth based on the dataset
            from evaluation.eval_pipelines import build_l2_eval_pipeline, build_l3_eval_pipeline
            from episteme_pipeline.contracts.phase_contracts import PipelineInput
            
            if dataset_type == "scierc":
                pipeline = build_l2_eval_pipeline(self.event_bus)
            elif dataset_type == "arg_microtexts":
                pipeline = build_l3_eval_pipeline(self.event_bus)
            else:
                # Default to L3 for generic cases
                pipeline = build_l3_eval_pipeline(self.event_bus)
                
            input_sources = self.manifest.get("corpus", {}).get("input_sources", [])
            texts_dir = self.manifest.get("corpus", {}).get("texts_dir")
            gold_path = self.manifest.get("corpus", {}).get("gold_standard_path")
            limit = self.manifest.get("corpus", {}).get("limit", 5)
            
            if texts_dir and not input_sources and gold_path and os.path.exists(gold_path):
                import json
                try:
                    with open(gold_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for i, line in enumerate(lines[:limit]):
                        data = json.loads(line)
                        doc_id = data.get("doc_key") or data.get("id") or f"doc_{i}"
                        doc_path = os.path.join(texts_dir, f"{doc_id}.txt")
                        if os.path.exists(doc_path):
                            input_sources.append(doc_path)
                        else:
                            print(f"Warning: Expected text file not found at {doc_path}")
                except Exception as e:
                    print(f"Error resolving texts_dir from gold_standard_path: {e}")

            print(f"Executing pipeline on sources: {input_sources}")
            if input_sources:
                await pipeline.run(PipelineInput(source_paths=input_sources))
            else:
                print("No input_sources defined in manifest. Skipping pipeline execution.")
        else:
            print(f"Evaluating existing graph (skipping pipeline execution) using manifest: {self.manifest_path}")

        # Initialize graph store for retrieving graphs for evaluation
        neo4j_url = os.getenv("NEO4J_URL", "neo4j://127.0.0.1:7687")
        neo4j_user = os.getenv("NEO4J_USERNAME", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4jdbpass")
        neo4j_db = os.getenv("NEO4J_DATABASE", "neo4j")
        self.store = Neo4jGraphReader(url=neo4j_url, username=neo4j_user, password=neo4j_password, database=neo4j_db)

    def _get_embedding_model(self):
        model_name = self.manifest.get("model", {}).get("embedding_model", "all-MiniLM-L6-v2")
        print(f"Loading embedding model: {model_name}")
        model = SentenceTransformer(model_name)
        def embed_fn(texts: list[str]):
            import numpy as np
            return np.array(model.encode(texts))
        return embed_fn

    async def run_scorers(self) -> None:
        """
        Trigger NetworkX Intrinsic modules (GM-GBS, OEP) and Retrieval Extrinsic modules.
        """
        gold_path = self.manifest.get("corpus", {}).get("gold_standard_path")
        dataset_type = self.manifest.get("corpus", {}).get("dataset_type", "baseline")
        limit = self.manifest.get("corpus", {}).get("limit", 5)
        
        if not gold_path or not os.path.exists(gold_path):
            print(f"Gold standard path not found: {gold_path}. Skipping intrinsic metrics.")
        else:
            print(f"Running Phase 1: Intrinsic Evaluation (GM-GBS, OEP) using {dataset_type}...")
            if dataset_type == "scierc":
                from evaluation.adapters.scierc import load_scierc_subset
                gold_data = load_scierc_subset(gold_path, limit=limit)
            elif dataset_type == "arg_microtexts":
                from evaluation.adapters.arg_microtexts import load_arg_microtexts_subset
                gold_data = load_arg_microtexts_subset(gold_path, limit=limit)
            else:
                gold_data = load_gold_standard(gold_path)
            
            # Load predicted graph (from store)
            pred_entities = await self.store.get_entities()
            pred_triples = await self.store.get_all_entity_triples()
            
            pred_graph = l2_triples_to_digraph(pred_entities, pred_triples)
            gold_graph = l2_triples_to_digraph(gold_data["l2_entities"], gold_data["l2_triples"])
            
            embed_fn = self._get_embedding_model()
            gbs_evaluator = GraphBERTScoreEvaluator(embed_fn)
            score, matched_pred, matched_gold = gbs_evaluator.compute_matches(pred_graph, gold_graph)
            hr, or_rate = OptimalEditPathEvaluator.compute_rates(pred_graph, gold_graph, matched_pred, matched_gold)
            
            self.report.intrinsic_metrics = {
                "gm_gbs": score,
                "hallucination_rate": hr,
                "omission_rate": or_rate
            }

        print("Running Phase 2: Extrinsic Evaluation (MRR, Hits@k, nDCG)...")
        if not hasattr(self, '_get_embedding_model_instance'):
            embed_fn = self._get_embedding_model()
        retrieval_evaluator = ExtrinsicRetrievalEvaluator(self.store, embed_fn)
        
        scifact_path = self.manifest.get("corpus", {}).get("scifact_path")
        if scifact_path and os.path.exists(scifact_path):
            from evaluation.adapters.scifact import load_scifact_subset
            queries = load_scifact_subset(scifact_path, limit=limit)
            all_metrics = []
            for q in queries:
                metrics = await retrieval_evaluator.evaluate_query(q["query"], q["gold_ids"])
                all_metrics.append(metrics)
            
            if all_metrics:
                # Average metrics
                avg_metrics = {}
                for key in all_metrics[0].keys():
                    avg_metrics[key] = sum(m[key] for m in all_metrics) / len(all_metrics)
                self.report.extrinsic_metrics = avg_metrics
        else:
            # Dummy evaluation logic (queries should be part of the benchmark)
            dummy_query = "What is the main argument?"
            dummy_gold_ids = {"doc_0"}
            if 'gold_data' in locals() and gold_data.get("l2_entities"):
                dummy_gold_ids = {ent.id for ent in gold_data["l2_entities"][:3]}
            
            metrics = await retrieval_evaluator.evaluate_query(dummy_query, dummy_gold_ids)
            self.report.extrinsic_metrics = metrics
        
    async def run_validation(self) -> None:
        """
        Validate Neo4j schema integrity constraints.
        """
        print("Running GraphValidator constraints...")
        validator = GraphValidator(self.store)
        
        violations = []
        direct_disjointness = await validator.check_direct_disjointness()
        transitive_disjointness = await validator.check_transitive_disjointness()
        type_constraints = await validator.check_type_constraints()
        
        for v in direct_disjointness:
            violations.append({"rule_name": "direct_disjointness", **v})
        for v in transitive_disjointness:
            violations.append({"rule_name": "transitive_disjointness", **v})
        for v in type_constraints:
            violations.append({"rule_name": "type_constraints", **v})
            
        self.report.validation_violations = violations

        for violation in violations:
            event = ValidationViolationDetected(
                rule_name=violation.get("rule_name", "unknown"),
                source_id=violation.get("source_id", "unknown"),
                target_id=violation.get("target_id", "unknown"),
                description=str(violation)
            )
            self.event_bus.emit(event)

    def generate_report(self) -> None:
        """
        Validate Neo4j schema integrity and inject metrics into the final markdown report.
        """
        print("Generating evaluation report...")
        report_data = self.report.model_dump()
        
        # Publish evaluation completed event
        event = EvaluationCompleted(
            evaluation_id=f"eval_{self.report.run_id}",
            run_id=self.report.run_id,
            metrics={**self.report.intrinsic_metrics, **self.report.extrinsic_metrics},
            outcome="success" if not self.report.validation_violations else "violations_detected"
        )
        self.event_bus.emit(event)
        
        report_path_json = f"evaluation/reports/report_{self.report.run_id}.json"
        os.makedirs(os.path.dirname(report_path_json), exist_ok=True)
        with open(report_path_json, "w") as f:
            json.dump(report_data, f, indent=2)
            
        import string
        template_path = "evaluation/templates/report_template.md"
        report_path_md = f"evaluation/reports/report_{self.report.run_id}.md"
        
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                template_str = f.read()
                
            mapping = {
                "RUN_ID": self.report.run_id,
                "DATE": self.report.timestamp,
                "EVAL_MODE": "unknown",
                "CORPUS_NAME": "unknown",
                "VERSION": "unknown",
                "SPLIT": "unknown",
                "MODEL_PROVIDER": "unknown",
                "MODEL_NAME": "unknown",
                "MODEL_VERSION": "unknown",
                "PROMPT_IDS": "unknown",
                "SCHEMA_ID": "unknown",
                "SCHEMA_VERSION": "unknown",
                "CODE_VERSION": "unknown",
                "OBJECTIVE": "Automated evaluation",
                "HIGHLIGHT_1": f"GM-GBS Score: {self.report.intrinsic_metrics.get('gm_gbs', 0):.4f}",
                "HIGHLIGHT_2": f"Hallucination Rate: {self.report.intrinsic_metrics.get('hallucination_rate', 0):.4f}",
                "HIGHLIGHT_3": f"Omission Rate: {self.report.intrinsic_metrics.get('omission_rate', 0):.4f}",
                "TOK_P": "0", "TOK_C": "0", "TIME_S": "0", "MEM_MB": "0",
                "GRAPH_DATASETS_EN": "N/A", "GRAPH_DATASETS_DE": "N/A", "REVIEWSET_INFO": "N/A",
                "CHUNK_PARAMS": "N/A", "RETRIEVAL_PARAMS": "N/A", "LINK_PARAMS": "N/A", "FUSION_PARAMS": "N/A", "SEEDS": "N/A",
                "GM_GBS_SCORE": f"{self.report.intrinsic_metrics.get('gm_gbs', 0):.4f}",
                "GED_SCORE": "N/A", "GM_GBS_ERRORS": "N/A",
                "OEP_HALLUCINATION_RATE": f"{self.report.intrinsic_metrics.get('hallucination_rate', 0):.4f}",
                "OEP_OMISSION_RATE": f"{self.report.intrinsic_metrics.get('omission_rate', 0):.4f}",
                "OEP_ERRORS": "N/A",
                "LLM_FAITHFULNESS": "N/A", "LLM_COMPREHENSIVENESS": "N/A", "LLM_DETECTED_HALLUCINATIONS": "N/A",
                "CONSTRAINT_STATUS": f"{len(self.report.validation_violations)} violations found",
                "PROV_COVERAGE": "N/A", "STORE_CONSISTENCY": "N/A", "STABILITY_STATS": "N/A",
                "HUMAN_REVIEW_SUMMARY": "N/A", "LLM_JUDGE_CORR": "N/A", "CASE_LINKS": "N/A",
                "BASELINES": "N/A", "ABLATIONS": "N/A", "LIFT_SUMMARY": "N/A",
                "INTERPRETATION": "N/A", "LIMITATIONS": "N/A", "NEXT_ACTIONS": "N/A",
                "MANIFEST_PATH": self.manifest_path,
                "ART_CHUNK": "N/A", "ART_EXTRACTED_GRAPHS": "N/A", "ART_OEP_DIAGNOSTICS": "N/A", "ART_LLM_JUDGE_TRANSCRIPTS": "N/A", "ART_FUSION": "N/A"
            }
            
            template = string.Template(template_str)
            md_content = template.safe_substitute(mapping)
            
            with open(report_path_md, "w") as f:
                f.write(md_content)
            print(f"Markdown report saved to {report_path_md}")
        print(f"JSON Report saved to {report_path_json}")

    async def execute(self) -> None:
        """Run the full evaluation workflow."""
        try:
            await self.run_pipeline()
            await self.run_validation()
            await self.run_scorers()
            self.generate_report()
        finally:
            if self.store:
                await self.store.close()


def main() -> None:
    import logging
    from rich.logging import RichHandler
    from episteme_pipeline.events import SimpleEventEmitter, RichProgressObserver, LangfuseObserver
    from episteme_pipeline.runs.observability import run_observability_context

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )

    parser = argparse.ArgumentParser(description="Grund GLP Evaluation Harness")
    parser.add_argument(
        "--manifest",
        type=str,
        required=True,
        help="Path to the evaluation run manifest YAML file.",
    )
    parser.add_argument(
        "--build-graph",
        action="store_true",
        help="If set, executes the pipeline prior to evaluation.",
    )
    args = parser.parse_args()

    emitter = SimpleEventEmitter()
    
    try:
        langfuse_observer = LangfuseObserver()
        emitter.register_observer(langfuse_observer)
    except Exception as e:
        logging.warning(f"Langfuse observability not enabled: {e}")

    with RichProgressObserver() as observer:
        emitter.register_observer(observer)
        
        # Determine a session name based on manifest
        run = EvaluationRun(args.manifest, event_bus=emitter, build_graph=args.build_graph)
        session_name = f"eval_{run.report.run_id}"
        
        with run_observability_context(name=session_name):
            asyncio.run(run.execute())

if __name__ == "__main__":
    main()
