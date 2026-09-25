# [ISSUE-028] Evaluation Packaging Consolidation & In-Memory TheoryNet Execution

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-028` |
| **Component(s)** | `packages/episteme-pipeline` (`episteme_pipeline/evaluation/`, `evaluation/`) |
| **Roadmap Horizon** | **Horizon 1** (Evaluation Integrity & Benchmark Harness) |
| **Priority** | Critical / Blocker |
| **Status** | Open |
| **Source Ref** | [`run_eval.py`](../../packages/episteme-pipeline/evaluation/run_eval.py#L14-L35), [`eval_pipelines.py`](../../packages/episteme-pipeline/evaluation/eval_pipelines.py#L114-L141) |

---

## 1. Problem Statement & Motivation

The evaluation harness suffers from two major structural design violations that hinder clean testing and SOTA benchmark execution:

### 1.1 Split-Brain Packaging & `sys.path` Hacks (SRP & Packaging Violation)
Currently, evaluation code is split across two disjoint directories:
- `packages/episteme-pipeline/evaluation/`: A loose collection of standalone scripts relying on `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))` to find the pipeline.
- `packages/episteme-pipeline/episteme_pipeline/evaluation/`: A formal package with dummy `0.0` stubs that are completely ignored by `run_eval.py`.

This dual structure violates standard Python package design, cannot be imported cleanly by external tools (e.g. `episteme-studio`), and prevents unified CI test execution.

### 1.2 Mandatory Live Database Coupling for Mathematical Evaluation (DIP & ISP Violation)
`run_eval.py` requires a running Neo4j instance to evaluate graphs. The runner:
1. Executes the pipeline to Neo4j.
2. Queries Neo4j via Cypher for raw triples.
3. Passes these triples to NetworkX.

This creates several fatal defects:
- Offline evaluation and unit testing are impossible.
- Nodes from older test runs contaminate benchmark calculations.
- **Interface Segregation Violation:** Mathematical graph comparison should operate directly on pipeline domain artifacts (`ArtifactCollection`, `TheoryNet`, `TheoryGraph`), not a remote database.

### 1.3 Missing Level 4 TheoryNet Pipeline
`build_l3_eval_pipeline()` halts at Phase 4 argument mining. Phase 6 (`Phase6Runner`) and `TheoryNetProjector` are never invoked, meaning TheoryNet structures are never generated during evaluation runs.

---

## 2. Functional Requirements

### 2.1 Package Consolidation
Consolidate all evaluation machinery into `episteme_pipeline.evaluation`:
```
packages/episteme-pipeline/episteme_pipeline/evaluation/
├── __init__.py
├── harness.py              # Sovereign EvaluationHarness orchestrator
├── pipelines.py            # Level 2, Level 3, and Level 4 TheoryNet pipeline builders
├── datasets.py             # Dataset references and loaders
├── models.py               # EvaluationReport, EvaluationResult, EvaluationMetric
├── comparison.py           # Comparative run metrics
├── rubrics.py              # Review rubrics
├── benchmarks/             # Benchmark adapters
│   ├── structuralist.py    # STNB JSON-LD loader
│   ├── scierc.py
│   └── arg_microtexts.py
├── scorers/                # Intrinsic & extrinsic scorers
│   ├── model_scorer.py     # Invokes epistemetrics model component evaluator
│   └── retrieval.py        # Downstream competency evaluator
└── data/                   # STNB and SciERC benchmark datasets
```
Deprecate and delete the loose `packages/episteme-pipeline/evaluation/` directory.

### 2.2 In-Memory Artifact Evaluation Flow
Allow `EvaluationHarness` to evaluate pipeline output directly in memory:
1. `pipeline.run(PipelineInput(chunks=chunks))` returns an `ExecutionResult` containing `ArtifactCollection`.
2. Extract the in-memory `TheoryNet` artifact (`artifacts.get_artifact(TheoryNet)`).
3. Convert `TheoryNet` directly to an `epistemetrics.TheoryGraph`.
4. Run intrinsic model component and property evaluation against the gold reference graph purely in memory—requiring zero network or database connections.

### 2.3 Level 4 TheoryNet Evaluation Pipeline
Implement `build_l4_theorynet_eval_pipeline(event_emitter)` in `pipelines.py`:
- Configures Phases 1, 2, 3, 3b, 4 (Maturation & Mining).
- Appends `Phase6Runner` (TheoryNet Projection) to materialize formal model structures.

---

## 3. Acceptance Criteria

- [ ] All evaluation modules reside inside `episteme_pipeline.evaluation` without `sys.path` hacks.
- [ ] Evaluation runs end-to-end on STNB purely in memory using pipeline artifacts.
- [ ] CI unit tests run offline without requiring a running Neo4j instance.
- [ ] Phase 6 TheoryNet projection executes cleanly during evaluation.

---

## 4. Key Target Files

- `packages/episteme-pipeline/episteme_pipeline/evaluation/harness.py`
- `packages/episteme-pipeline/episteme_pipeline/evaluation/pipelines.py`
- `packages/episteme-pipeline/episteme_pipeline/evaluation/benchmarks/structuralist.py`
- `packages/episteme-pipeline/episteme_pipeline/evaluation/models.py`
