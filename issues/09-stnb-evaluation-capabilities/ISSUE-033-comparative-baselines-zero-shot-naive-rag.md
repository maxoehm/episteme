# [ISSUE-033] Comparative Baseline Harness for STNB (Zero-Shot LLM, Naive KG, Text RAG)

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-033` |
| **Component(s)** | `packages/episteme-pipeline` (`evaluation/baselines/`, `evaluation/run_eval.py`, `evaluation/comparison.py`) |
| **Roadmap Horizon** | **Horizon 2** (Dialectical Modeling & Benchmarks) |
| **Priority** | High |
| **Status** | Open |
| **Source Ref** | [`docs/research/structuralist_theory_benchmark.md §Native Evaluation Scaffolding`](../../docs/research/structuralist_theory_benchmark.md#L267-L300), [`docs/research/evaluation_methodology.md §11`](../../docs/research/evaluation_methodology.md) |

---

## 1. Problem Statement & Motivation

To establish scientific credibility in peer-reviewed venues and prove that **Episteme** represents a genuine advance in automated scientific theory extraction, pipeline performance on STNB must be benchmarked against recognized baseline architectures.

Currently:
1. **Zero Baselines Exist in the Repository:** There are no reference implementations or comparison models in `evaluation/`.
2. **Unsupported SOTA Claims:** It is impossible to prove whether the 6-phase pipeline produces superior theory graphs compared to prompting an LLM directly in a single pass.
3. **No Comparative Reporting:** Although [`episteme_pipeline/evaluation/comparison.py`](../../packages/episteme-pipeline/episteme_pipeline/evaluation/comparison.py) defines data models (`RunComparison`, `EvaluationComparison`), no automated orchestrator executes or tabulates comparisons between baseline runs and pipeline runs.

---

## 2. Functional Requirements

### 2.1 Implement Standard Baseline Runners (`evaluation/baselines/`)
Implement three standard baselines in `packages/episteme-pipeline/evaluation/baselines/`:

1. **`BaselineZeroShotLLM` (`baselines/zero_shot_llm.py`):**
   - Ingests the full text (or sequential chunks) with a single comprehensive prompt instructing the LLM to directly output `TheoryElement` nodes, governing axioms, and specialization edges.
   - Evaluates pipeline lift over naive prompt engineering.

2. **`BaselineNaiveKG` (`baselines/naive_kg.py`):**
   - Standard unipartite entity-relation extraction (e.g. LangChain `LLMGraphTransformer` pattern) without epistemic layer typing (Partition $A$ vs $B$), argument mining, or formal TheoryNet projection.
   - Evaluates whether the structuralist formal metamodel provides superior structural accuracy over flat open-IE knowledge graphs.

3. **`BaselineTextRAG` (`baselines/text_rag.py`):**
   - Standard dense vector retrieval over raw `L1Chunk` embeddings without graph structuring.
   - Evaluates whether the graph-structured TheoryNet outperforms flat vector search on downstream competency questions.

### 2.2 Baseline Manifests & CLI Flag
1. Support `--baseline [zero_shot | naive_kg | text_rag]` in `run_eval.py`:
   ```bash
   rtk python packages/episteme-pipeline/evaluation/run_eval.py \
     --manifest packages/episteme-pipeline/evaluation/manifests/eval_stnb.yaml \
     --baseline zero_shot
   ```
2. Generate side-by-side comparative Markdown/JSON tables using `RunComparison` in `episteme_pipeline/evaluation/comparison.py`:
   - Metric delta ($\Delta F_1$, $\Delta \text{GM-GBS}$, $\Delta \text{MRR}$).
   - Token cost and latency overhead comparisons.

---

## 3. Acceptance Criteria

- [ ] Directory `packages/episteme-pipeline/evaluation/baselines/` contains executable baseline runners for Zero-Shot LLM, Naive KG, and Text RAG.
- [ ] `run_eval.py` can execute baseline pipelines against `eval_stnb.yaml`.
- [ ] Evaluation reports include comparative tables displaying relative performance lift over baselines.
- [ ] Deterministic tests in `packages/episteme-pipeline/tests/` verify baseline output structure against mock text.

---

## 4. Key Target Files

- `packages/episteme-pipeline/evaluation/baselines/zero_shot_llm.py`
- `packages/episteme-pipeline/evaluation/baselines/naive_kg.py`
- `packages/episteme-pipeline/evaluation/baselines/text_rag.py`
- `packages/episteme-pipeline/evaluation/run_eval.py`
- `packages/episteme-pipeline/episteme_pipeline/evaluation/comparison.py`
