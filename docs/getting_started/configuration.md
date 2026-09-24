# Configuration & Contracts

Episteme is built on a **contract-driven architecture**: the pipeline engine only interacts with abstract interfaces (`Protocols`). It has zero hard dependencies on specific LLM vendors, API servers, or proxy layers.

You can configure Episteme using either:
1. **Out-of-the-Box Reference Adapters** (configured via `.env` for zero-boilerplate execution).
2. **Custom Contract Implementations** (written in Python for internal clusters, proprietary APIs, or offline research).

---

## Method A: Out-of-the-Box Reference Adapters (`.env`)

For out-of-the-box convenience, the pipeline includes reference adapters built on LiteLLM (for models) and HuggingFace/SentenceTransformers (for cross-encoders).

Create a `.env` file in your workspace root:

```bash
# ==============================================================================
# Model Endpoints (Used by the built-in LiteLLM reference adapters)
# ==============================================================================
# Base URL for any OpenAPI / OpenAI-compatible endpoint (optional if using local proxy)
LITELLM_API_BASE="http://127.0.0.1:4000"

# Endpoint or proxy authentication token
LITELLM_API_KEY="sk-endpoint-token"

# Generation & embedding model identifiers
LLM_MODEL="custom-instruct-model"
EMBED_MODEL="custom-embedding-model"
EMBED_DIM=1536

# Cross-Encoder Reranker (HuggingFace / PyTorch)
RERANKER_MODEL="Qwen/Qwen3-Reranker-0.6B"

# ==============================================================================
# Graph Database (Used by the built-in Neo4j adapters)
# ==============================================================================
NEO4J_URL="neo4j://127.0.0.1:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="neo4jdbpass"
NEO4J_DATABASE="neo4j"

# ==============================================================================
# Observability & Remote Prompt Management (Recommended Reference Adapters)
# ==============================================================================
# Setting these credentials activates both distributed tracing (LangfuseObserver)
# and remote prompt management (LangfusePromptProvider) with automatic fallback.
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_HOST="http://localhost:3000"
```

!!! note "Note on Langfuse Integration"

    Providing Langfuse credentials automatically activates two complementary reference adapters:
    1. **Distributed Tracing (`LangfuseObserver`)**: Captures end-to-end trace graphs, LLM token expenditures, execution latencies, and component errors across all phases.
    2. **Remote Prompt Management (`LangfusePromptProvider`)**: Fetches centralized, versioned prompt templates labeled `production` directly from Langfuse. You can iterate on prompts in the Langfuse UI without touching code. If Langfuse is unreachable or unconfigured, the pipeline gracefully falls back to built-in defaults (`DefaultPromptProvider`).

---

## Method B: Implementing the Contracts Directly

If your team or lab already has a custom model runtime (e.g. local PyTorch inference, an internal HTTP gateway, or in-memory unit testing mocks), you **do not need to set up any proxy or server**. Simply provide any class that implements the pipeline's Python `Protocol` interfaces.

### 1. The Embedding Contract (`EmbeddingModel`)
Defined in `pipeline.protocols.extractors.EmbeddingModel`. Requires only two asynchronous methods returning raw `list[float]`:

```python
class CustomEmbedding:
    """Any class implementing this protocol can be used directly."""

    async def aget_text_embedding(self, text: str) -> list[float]:
        # Return vector for a single text chunk
        return [0.012, -0.045, 0.103, ...]

    async def aget_text_embedding_batch(self, texts: list[str]) -> list[list[float]]:
        # Return batch of vectors
        return [[0.012, -0.045, ...] for _ in texts]
```

### 2. The Cross-Encoder Contract (`CrossEncoder`)
Defined in `pipeline.protocols.extractors.CrossEncoder`. Requires a single synchronous `predict` method returning normalized probability scores in `[0.0, 1.0]`:

```python
from collections.abc import Sequence

class CustomReranker:
    """Scores candidate relationship pairs for Phase 3 and Phase 4."""

    def predict(self, pairs: Sequence[tuple[str, str]]) -> Sequence[float]:
        # Each pair is (source_text, candidate_relation_text)
        # Return a list or array of floats in range [0.0, 1.0]
        return [0.94, 0.12, 0.88]
```

### 3. The LLM Contract (`StructuredLLM` / `BaseLLM`)
Any LlamaIndex-compatible `BaseLLM` instance or any object implementing `predict_structured` can be passed. The pipeline automatically wraps it with structured JSON decoding and local disk caching:

```python
from llama_index.core.llms.custom import CustomLLM

class InstitutionalLLM(CustomLLM):
    ...
```

### 4. Passing Custom Implementations to the Pipeline

Assemble the pipeline with your custom components:

```python
from pipeline import Pipeline, PipelineConfig
from pipeline.graph import Neo4jGraphReader, Neo4jGraphWriter, Neo4jProcessingGraph

pipeline = Pipeline.for_task(
    task="knowledge_graph",
    llm=my_custom_llm,
    embedding_model=CustomEmbedding(),
    cross_encoder=CustomReranker(),
    config=PipelineConfig(),
    graph_reader=graph_reader,
    projection_graph=projection_graph,
    checkpoint_store=checkpoint_store,
)
```

---

## Testing Your Configuration

Verify connectivity using the out-of-the-box adapters:

```bash
uv run python -c "
import asyncio, os
from dotenv import load_dotenv
from llama_index.llms.litellm import LiteLLM
from pipeline.graph import Neo4jProcessingGraph

load_dotenv()

async def test_env():
    # 1. Test Neo4j
    graph = Neo4jProcessingGraph(
        url=os.getenv('NEO4J_URL', 'neo4j://127.0.0.1:7687'),
        username=os.getenv('NEO4J_USERNAME', 'neo4j'),
        password=os.getenv('NEO4J_PASSWORD', 'neo4jdbpass'),
        database=os.getenv('NEO4J_DATABASE', 'neo4j'),
    )
    print('Neo4j connection successful.')
    await graph.close()

    # 2. Test Model Endpoint Adapter
    llm = LiteLLM(
        model=os.getenv('LLM_MODEL', 'default'),
        api_base=os.getenv('LITELLM_API_BASE'),
        api_key=os.getenv('LITELLM_API_KEY'),
    )
    print('Model adapter initialized successfully.')

asyncio.run(test_env())
"
```

---

## Next Steps

With your environment configured or adapters implemented, proceed to the [First Run Tutorial](first_run.md).
