# Troubleshooting Guide

Solutions and diagnostic steps for common installation, runtime, database, and inference issues in Episteme.

---

## Environment & Installation Issues

### Python Version Incompatibility
* **Symptom**: `uv sync` fails with `requires-python = ">=3.13"` or syntax errors.
* **Solution**: Ensure your active interpreter is Python 3.13 or newer:
  ```bash
  # Install and pin Python 3.13 via uv
  uv python install 3.13
  uv python pin 3.13
  uv sync
  ```

### Virtual Environment or Dependency Conflicts
* **Symptom**: Stale packages or import errors after git pull.
* **Solution**: Clear local cache and re-sync:
  ```bash
  uv cache clean
  rm -rf .venv
  uv sync
  ```

### Pandoc Not Found
* **Symptom**: Ingestion fails with `FileNotFoundError: pandoc not found`.
* **Solution**: Install Pandoc and ensure it is available in your `$PATH`:
  ```bash
  # macOS
  brew install pandoc

  # Ubuntu / Debian
  sudo apt-get install -y pandoc
  ```

---

## Model & Endpoint Issues

### Endpoint Connectivity & Authentication Failure
* **Symptom**: `LiteLLM` raises `APIConnectionError`, `AuthenticationError`, or `404 Not Found`.
* **Solution**:
  1. Test your endpoint outside the pipeline with `curl`:
     ```bash
     curl -s -X POST "$LITELLM_API_BASE/chat/completions" \
       -H "Authorization: Bearer $LITELLM_API_KEY" \
       -H "Content-Type: application/json" \
       -d '{
         "model": "'"$LLM_MODEL"'",
         "messages": [{"role": "user", "content": "ping"}]
       }'
     ```
  2. Verify URL formatting: Some gateways expect `/v1` appended to `LITELLM_API_BASE` (e.g., `http://localhost:4000/v1`).

### Vector Index Dimension Mismatch in Neo4j
* **Symptom**: Cypher exception during Phase 1: `Vector index dimension (1536) does not match embedding dimension (768)`.
* **Solution**:
  1. Verify the vector dimension of your chosen embedding model.
  2. Set `EMBED_DIM` in `.env` to match the exact dimension (e.g. `1536` for standard small embeddings, `768` for Nomic/BERT embeddings).
  3. If switching models on an existing database, drop the outdated vector index in Neo4j Browser:
     ```cypher
     SHOW INDEXES;
     DROP INDEX chunk_vector_index; // Replace with actual index name
     ```

### HuggingFace Cross-Encoder Download or Device Out of Memory
* **Symptom**: Process hangs or fails when loading `Qwen/Qwen3-Reranker-0.6B`.
* **Solution**:
  1. **Network Firewalls**: If operating in an air-gapped environment, pre-download the model and set `HF_HUB_OFFLINE=1`.
  2. **GPU Memory**: For low-memory GPUs, set `torch_dtype="auto"` (default in `SentenceTransformerCrossEncoderReranker`) or use CPU fallback.

---

## Database Issues (Neo4j 5.x)

### Connection Refused (`neo4j://127.0.0.1:7687`)
* **Symptom**: `ServiceUnavailable: Defunct connection`.
* **Solution**:
  1. Verify container or service status:
     ```bash
     docker ps | grep neo4j
     ```
  2. Check port binding on `7687` (Bolt protocol) and `7474` (HTTP Browser).
  3. Confirm `NEO4J_URL` uses the `neo4j://` scheme (recommended for clustered/local instances) or `bolt://`.

### APOC Security & Permission Errors
* **Symptom**: Cypher query fails with `Unknown procedure: apoc.meta.data` or procedure restriction errors.
* **Solution**: Add the following to your `neo4j.conf` (or docker environment variables):
  ```properties
  dbms.security.procedures.unrestricted=apoc.*
  dbms.security.procedures.allowlist=apoc.*
  ```

---

## Episteme Studio Issues

### Port 8000 Already in Use
* **Symptom**: `[Errno 48] Address already in use`.
* **Solution**: Bind to an alternative port using `--port`:
  ```bash
  uv run episteme-studio serve --demo --port 8080
  ```

### Non-Loopback Host Binding Security Policy
* **Symptom**: `Security Error: Host 0.0.0.0 is not loopback; a security token (--token) is required.`
* **Solution**: To prevent unauthorized access when binding to external interfaces, supply an authentication token:
  ```bash
  uv run episteme-studio serve --host 0.0.0.0 --port 8000 --token "your-secret-token"
  ```

---

## Diagnostic Reporting

When reporting issues to project maintainers, include output from this diagnostic script:

```bash
echo "=== System Info ==="
uname -a
python3 --version
uv --version

echo "=== Monorepo Packages ==="
uv pip list | grep -E "(Episteme|epistemetrics|neo4j|llama-index)"

echo "=== Neo4j Connectivity ==="
uv run python -c "
import os
from pipeline.graph import Neo4jProcessingGraph
g = Neo4jProcessingGraph(
    url=os.getenv('NEO4J_URL', 'neo4j://127.0.0.1:7687'),
    username=os.getenv('NEO4J_USERNAME', 'neo4j'),
    password=os.getenv('NEO4J_PASSWORD', 'neo4jdbpass'),
    database=os.getenv('NEO4J_DATABASE', 'neo4j'),
)
print('Neo4j reachable')
"
```
