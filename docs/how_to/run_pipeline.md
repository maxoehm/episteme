# Running the Pipeline

Detailed instructions for executing the Episteme pipeline with various configurations.

## Basic Pipeline Execution

The simplest way to run the pipeline is using one of the example scripts:

```bash
uv run python packages/episteme-pipeline/examples/pipeline_langfuse_full_run.py
```

This executes all five phases of the pipeline on the configured input documents.

## Custom Input Documents

To process your own documents:

1. Modify the `SOURCE_PATHS` variable in the example script
2. Ensure documents are in supported formats (PDF, TXT, MD, TEX)
3. Run the pipeline as usual

```python
SOURCE_PATHS = [
    "/path/to/your/document1.pdf",
    "/path/to/your/document2.tex",
]
```

## Phase-Specific Execution

You can run individual phases or start from a specific phase:

### Running from a Specific Phase

To resume execution from a particular phase:

```python
# Assuming you have a pipeline instance
result = await pipeline.run_from_phase(
    phase_number=3,  # Start from Phase 3
    input=PipelineInput(source_paths=["document.tex"])
)
```

### Running Individual Phases

For more granular control, execute phases individually:

```python
# Run Phase 1 only
phase1_result = await phase1_runner.run(phase_input)

# Use result as input for Phase 2
phase2_input = Phase2Input.from_previous(phase1_result)
phase2_result = await phase2_runner.run(phase2_input)
```

## Configuration Options

### Execution Configuration

Control overall pipeline behavior:

```python
cfg = PipelineConfig(
    execution=ExecutionConfig(
        project_artifacts_to_graph=True,  # Enable Neo4j projection
        allow_phase_reuse=True,           # Reuse cached artifacts when possible
        allow_artifact_hydration=True,    # Load previous artifacts to skip work
        runs_dir="./custom_runs",         # Custom location for run manifests
        artifacts_dir="./custom_artifacts" # Custom location for artifacts
    )
)
```

### Phase-Specific Settings

Customize behavior for individual phases:

```python
cfg = PipelineConfig(
    phase1=Phase1Config(
        chunk_size=1500,        # Characters per chunk
        chunk_overlap=200,      # Overlap between chunks
        max_workers=4           # Concurrent document processors
    ),
    phase2=Phase2Config(
        ner_confidence_threshold=0.8,  # Minimum confidence for entities
        max_entity_length=100          # Maximum entity name length
    )
)
```

## Environment Configuration

### OpenAPI / LiteLLM Endpoint Configuration

Configure your OpenAPI-compatible LiteLLM proxy:

```python
llm = LiteLLM(
    model=os.getenv("LLM_MODEL", "custom-model"),
    api_base=os.getenv("LITELLM_API_BASE"),
    api_key=os.getenv("LITELLM_API_KEY"),
)
```

### Neo4j Connection

Configure database connection:

```python
neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
neo4j_user = os.getenv("NEO4J_USERNAME", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
neo4j_database = os.getenv("NEO4J_DATABASE", "neo4j")
```

## Advanced Execution Patterns

### Batch Processing

Process multiple documents efficiently:

```python
# Process documents in batches to manage memory
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

for i in range(0, len(documents), 5):  # Process 5 at a time
    batch = documents[i:i+5]
    input_data = PipelineInput(source_paths=batch)
    result = await pipeline.run(input_data)
    # Handle results
```

### Parallel Execution

Run multiple pipeline instances concurrently:

```python
import asyncio

async def process_document(doc_path):
    input_data = PipelineInput(source_paths=[doc_path])
    return await pipeline.run(input_data)

# Process multiple documents concurrently
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
results = await asyncio.gather(*[process_document(doc) for doc in documents])
```

## Monitoring and Observability

### Progress Tracking

Monitor pipeline execution:

```python
# Register event listeners for progress updates
from pipeline.events import SimpleEventEmitter

emitter = SimpleEventEmitter()

@emitter.on("phase.started")
def on_phase_started(event):
    print(f"Starting phase: {event['phase']}")

@emitter.on("phase.completed")
def on_phase_completed(event):
    print(f"Completed phase: {event['phase']}")
```

### Performance Profiling

Measure execution performance:

```bash
# Enable detailed timing information
export TIMING_LOG_LEVEL=DEBUG
uv run python packages/episteme-pipeline/examples/pipeline_langfuse_full_run.py
```

## Error Handling

### Graceful Failure Management

Configure pipeline to continue despite errors:

```python
cfg = PipelineConfig(
    execution=ExecutionConfig(
        continue_on_error=True,  # Don't abort on individual failures
        max_retry_attempts=3     # Retry failed operations
    )
)
```

### Custom Error Handlers

Implement custom error handling:

```python
try:
    result = await pipeline.run(input_data)
except PipelineError as e:
    # Handle pipeline-specific errors
    logger.error(f"Pipeline failed: {e}")
    # Implement recovery strategy
```

## Resource Management

### Memory Optimization

Control memory usage during execution:

```python
cfg = PipelineConfig(
    execution=ExecutionConfig(
        max_concurrent_phases=2,    # Limit concurrent phases
        artifact_cache_size=1000    # Limit artifact cache size
    ),
    phase1=Phase1Config(
        max_workers=2              # Limit document processing workers
    )
)
```

### Timeout Configuration

Set execution timeouts:

```python
llm = LiteLLM(
    model="openai/gpt-4o-mini",
    api_key=api_key,
    timeout=120.0,      # 2-minute timeout for LLM calls
    max_retries=3       # Retry up to 3 times
)
```

## Output Management

### Artifact Inspection

Access intermediate results:

```python
# Get artifacts from a completed run
artifacts = await pipeline.get_run_artifacts(run_id, phase_name="phase2")

# Filter by artifact kind
entity_artifacts = [a for a in artifacts if a.kind == "entity_mention"]
```

### Report Generation

Generate detailed execution reports:

```python
# Get comprehensive run report
report = await pipeline.get_run_report(run_id)
print(report.summary)
```

## Troubleshooting Execution

### Common Issues

1. **Memory Errors**: Reduce batch sizes or worker counts
2. **Timeout Errors**: Increase timeout values for slow operations
3. **LLM Rate Limits**: Add delays or reduce concurrency
4. **Database Connection Issues**: Verify Neo4j is running and accessible

### Diagnostic Information

Enable verbose logging for troubleshooting:

```bash
export LOG_LEVEL=DEBUG
export PIPELINE_LOG_LEVEL=TRACE
uv run python packages/episteme-pipeline/examples/pipeline_langfuse_full_run.py
```

## Performance Tuning

### Optimizing for Speed

Fast execution configuration:

```python
cfg = PipelineConfig(
    execution=ExecutionConfig(
        allow_phase_reuse=True,           # Reuse cached results
        allow_artifact_hydration=True,    # Load previous artifacts
        max_concurrent_phases=4           # Maximize parallelism
    )
)
```

### Optimizing for Quality

High-quality extraction settings:

```python
cfg = PipelineConfig(
    phase2=Phase2Config(
        ner_confidence_threshold=0.9,     # Higher confidence threshold
        use_entity_disambiguation=True    # Enable sophisticated linking
    ),
    phase3=Phase3Config(
        reranker_top_k=50,                # Consider more candidates
        global_relation_sample_size=100   # Larger context windows
    )
)
```

## Next Steps

- Learn how to [Inspect Outputs](inspect_outputs.md)
- Understand [Resume Capabilities](resume_runs.md)
- Explore [Configuration Customization](customize_config.md)
