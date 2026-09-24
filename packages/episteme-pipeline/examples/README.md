# Examples

This directory contains example scripts for running the Grund GLP pipeline.

## Available Examples

### `pipeline_full_run.py` (Recommended)
An example running the complete 7-runner pipeline pass across all 5 conceptual phases as defined in `docs/concepts/pipeline_architecture.md`. Uses `LiteLLM` for OpenAILike generation and embeddings, `SentenceTransformerCrossEncoderReranker` for HuggingFace cross-encoder relation reranking, and Neo4j graph stores via `Pipeline.for_task()`.

### `kg_construction.py`
An example script demonstrating knowledge graph construction with customized extractor pipelines and Langfuse observability integration.

### `main_fixed.py`
A minimal working example that shows basic pipeline setup.

### `main.py` (Deprecated)
An outdated example that contains references to non-existent methods. This example should not be used.

## Running Examples

To run any example:

```bash
uv run python examples/[script_name].py
```

Make sure to set the required environment variables:
- `OPENAI_API_KEY` (or appropriate key for your LLM provider)
- `NEO4J_URL`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`

You can also create a `.env` file in the project root with these variables.
