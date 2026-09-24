# Customizing Configuration

Guide to tailoring pipeline behavior through configuration options.

## Configuration Overview

Pipeline behavior is controlled through a hierarchical configuration system.

### Configuration Structure

The main configuration object:

```python
from pipeline.config import PipelineConfig

config = PipelineConfig(
    execution=ExecutionConfig(...),
    phase1=Phase1Config(...),
    phase2=Phase2Config(...),
    phase3=Phase3Config(...),
    phase4=Phase4Config(...),
    phase5=Phase5Config(...),
    graph_schema=GraphSchemaConfig(...)
)
```

### Configuration Sources

Settings can be specified through:

1. **Direct Code Configuration**: Explicit values in Python code
2. **Environment Variables**: System environment overrides
3. **Configuration Files**: YAML or JSON files
4. **Command-Line Arguments**: Runtime parameters

## Core Configuration Areas

### Execution Configuration

Control overall pipeline execution behavior:

```python
from pipeline.config import ExecutionConfig

execution_cfg = ExecutionConfig(
    project_artifacts_to_graph=True,    # Enable Neo4j projection
    allow_phase_reuse=True,             # Reuse cached artifacts
    allow_artifact_hydration=True,      # Load previous artifacts
    continue_on_error=False,            # Stop on failures
    max_retry_attempts=3,               # Retry failed operations
    runs_dir="./runs",                  # Run manifest storage
    artifacts_dir="./artifacts"         # Artifact storage
)
```

### Graph Schema Configuration

Define the structure of the resulting theory graph:

```python
from pipeline.config import GraphSchemaConfig

schema_cfg = GraphSchemaConfig(
    allowed_entity_types=[
        "Concept", "Person", "Work", "Theory", "Institution"
    ],
    allowed_relation_types=[
        "SUPPORTS", "REFUTES", "RELATED_TO", "INSTANCE_OF", "PART_OF"
    ],
    entity_uniqueness_constraints=[
        # Define uniqueness requirements
    ],
    relation_cardinality_constraints=[
        # Define relationship limits
    ]
)
```

## Phase-Specific Customization

### Phase 1: Data Foundation

Document parsing and chunking parameters:

```python
from pipeline.config import Phase1Config

phase1_cfg = Phase1Config(
    chunk_size=1000,           # Target characters per chunk
    chunk_overlap=150,         # Overlap between chunks
    min_chunk_size=200,        # Minimum chunk size
    max_workers=4,             # Concurrent document processors
    bib_paths=[],              # Bibliography file paths
    include_metadata=True      # Extract document metadata
)
```

### Phase 2: Entity Discovery

Entity extraction and linking settings:

```python
from pipeline.config import Phase2Config

phase2_cfg = Phase2Config(
    # Entity Recognition
    ner_confidence_threshold=0.8,     # Minimum confidence for entities
    max_entity_length=100,            # Maximum entity text length
    allowed_entity_types=[            # Restrict entity categories
        "CONCEPT", "PERSON", "WORK"
    ],
    
    # Entity Linking
    entity_linking_enabled=True,      # Enable entity disambiguation
    linking_confidence_threshold=0.7, # Minimum linking confidence
    max_candidate_entities=10,        # Candidates per mention
    
    # Prompt Templates
    ner_prompt_template="...",        # Custom NER instruction
    entity_linking_prompt_template="..." # Custom linking instruction
)
```

### Phase 3: Relation Extraction

Relationship discovery parameters:

```python
from pipeline.config import Phase3Config

phase3_cfg = Phase3Config(
    # Local Relations
    local_relation_confidence_threshold=0.75,
    max_local_relations_per_chunk=20,
    
    # Global Relations
    global_relation_sample_size=50,       # Context window size
    reranker_top_k=30,                    # Candidates to rerank
    reranker_max_length=512,              # Max sequence length
    global_relation_confidence_threshold=0.8,
    
    # Prompt Templates
    local_relation_prompt_template="...",
    global_relation_prompt_template="..."
)
```

### Phase 4: Argument Mining

Argument structure extraction settings:

```python
from pipeline.config import Phase4Config

phase4_cfg = Phase4Config(
    # ADU Segmentation
    adu_confidence_threshold=0.8,
    
    # Component Classification
    acc_confidence_threshold=0.75,
    
    # Relation Classification
    arc_confidence_threshold=0.8,
    
    # Prompt Templates
    adu_segmentation_prompt_template="...",
    acc_prompt_template="...",
    arc_prompt_template="..."
)
```

### Phase 5: Alignment Fusion

Entity canonicalization parameters:

```python
from pipeline.config import Phase5Config

phase5_cfg = Phase5Config(
    # Matching Thresholds
    similarity_threshold=0.85,         # Entity similarity cutoff
    confidence_threshold=0.8,          # Minimum alignment confidence
    
    # Clustering
    clustering_algorithm="hierarchical", # Clustering approach
    max_cluster_size=50,               # Maximum entities per cluster
    
    # Conflict Resolution
    conflict_resolution_strategy="majority_vote"
)
```

## Environment-Based Configuration

Use environment variables for deployment flexibility:

```python
import os

# Override configuration with environment variables
config = PipelineConfig(
    execution=ExecutionConfig(
        project_artifacts_to_graph=os.getenv("PROJECT_TO_GRAPH", "true").lower() == "true",
        runs_dir=os.getenv("RUNS_DIR", "./runs"),
        artifacts_dir=os.getenv("ARTIFACTS_DIR", "./artifacts")
    ),
    phase1=Phase1Config(
        chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
        max_workers=int(os.getenv("MAX_WORKERS", "4"))
    )
)
```

## Configuration Files

Manage complex configurations with external files:

### YAML Configuration

Create a `config.yaml` file:

```yaml
execution:
  project_artifacts_to_graph: true
  allow_phase_reuse: true
  runs_dir: "./pipeline_runs"
  artifacts_dir: "./pipeline_artifacts"

phase1:
  chunk_size: 1200
  chunk_overlap: 200
  max_workers: 4

phase2:
  ner_confidence_threshold: 0.85
  entity_linking_enabled: true
  linking_confidence_threshold: 0.8

phase3:
  global_relation_sample_size: 75
  reranker_top_k: 25
  global_relation_confidence_threshold: 0.85

graph_schema:
  allowed_entity_types:
    - Concept
    - Person
    - Work
    - Theory
    - Institution
  allowed_relation_types:
    - SUPPORTS
    - REFUTES
    - RELATED_TO
    - INSTANCE_OF
    - PART_OF
```

Load configuration from file:

```python
import yaml
from pipeline.config import PipelineConfig

with open("config.yaml", "r") as f:
    config_dict = yaml.safe_load(f)
    
config = PipelineConfig(**config_dict)
```

## Dynamic Configuration

Modify configuration at runtime:

### Conditional Settings

Adjust configuration based on input characteristics:

```python
def create_adaptive_config(document_types):
    if "philosophy" in document_types:
        # Use settings optimized for philosophical texts
        return PipelineConfig(
            phase2=Phase2Config(
                ner_confidence_threshold=0.9,  # Higher precision
                allowed_entity_types=["CONCEPT", "PERSON", "WORK"]
            )
        )
    else:
        # Use general settings
        return PipelineConfig()
```

### Performance-Based Adjustment

Tune settings based on resource constraints:

```python
def create_resource_aware_config(available_memory_gb):
    max_workers = min(4, max(1, int(available_memory_gb / 2)))
    
    return PipelineConfig(
        phase1=Phase1Config(max_workers=max_workers),
        execution=ExecutionConfig(
            max_concurrent_phases=min(3, max_workers)
        )
    )
```

## Prompt Template Customization

Tailor LLM instructions for domain-specific requirements:

### Custom NER Prompt

```python
custom_ner_prompt = """
Extract named entities from the following text. Focus on theoretical concepts, 
philosophers, philosophical works, and schools of thought.

Text: {text}

Respond in JSON format with an array of entities:
[{"text": "...", "type": "...", "start": ..., "end": ..., "confidence": ...}]

Entity Types:
- CONCEPT: Theoretical ideas or abstract notions
- PERSON: Philosophers, scientists, or other individuals
- WORK: Books, papers, or other scholarly works
- THEORY: Formal theoretical frameworks or schools of thought
"""

phase2_cfg = Phase2Config(
    ner_prompt_template=custom_ner_prompt
)
```

### Custom Relation Prompt

```python
custom_relation_prompt = """
Identify relationships between the following entities in the given context.

Entities: {entities}
Context: {context}

Respond in JSON format:
[{{"subject": "...", "predicate": "...", "object": "...", 
   "confidence": ..., "evidence": "..."}}]

Relationship Types:
- SUPPORTS: The subject supports or provides evidence for the object
- REFUTES: The subject contradicts or refutes the object
- RELATED_TO: General associative relationship
- INSTANCE_OF: The subject is an instance of the object
- PART_OF: The subject is part of the object
"""

phase3_cfg = Phase3Config(
    local_relation_prompt_template=custom_relation_prompt
)
```

## Advanced Configuration Patterns

### Profile-Based Configuration

Create configuration profiles for different use cases:

```python
CONFIG_PROFILES = {
    "precise": PipelineConfig(
        phase2=Phase2Config(ner_confidence_threshold=0.9),
        phase3=Phase3Config(global_relation_confidence_threshold=0.9)
    ),
    "comprehensive": PipelineConfig(
        phase2=Phase2Config(ner_confidence_threshold=0.7),
        phase3=Phase3Config(global_relation_confidence_threshold=0.7)
    ),
    "fast": PipelineConfig(
        execution=ExecutionConfig(
            allow_phase_reuse=True,
            allow_artifact_hydration=True
        ),
        phase1=Phase1Config(max_workers=8)
    )
}

# Use profile
config = CONFIG_PROFILES["precise"]
```

### Configuration Validation

Validate configuration settings:

```python
from pydantic import ValidationError

try:
    config = PipelineConfig(**user_provided_config)
except ValidationError as e:
    print(f"Configuration error: {e}")
    # Handle invalid configuration
```

## Best Practices

### Configuration Organization

Structure configurations for maintainability:

```python
# Separate domain-specific settings
PHILOSOPHY_CONFIG = PipelineConfig(
    phase2=Phase2Config(
        allowed_entity_types=["CONCEPT", "PERSON", "WORK", "THEORY"],
        ner_prompt_template=philosophy_ner_prompt
    )
)

SCIENTIFIC_CONFIG = PipelineConfig(
    phase2=Phase2Config(
        allowed_entity_types=["CONCEPT", "PERSON", "WORK", "INSTITUTION"],
        ner_prompt_template=scientific_ner_prompt
    )
)
```

### Version Management

Track configuration versions:

```python
config = PipelineConfig(
    # Include version metadata
    version="1.2.0",
    created_at=datetime.now().isoformat(),
    # ... other settings
)
```

### Testing Configurations

Validate configuration effectiveness:

```python
def test_configuration_effectiveness(config, test_documents):
    """Test that configuration produces expected results."""
    # Run pipeline with test configuration
    # Validate output quality metrics
    # Return assessment results
    pass
```

## Troubleshooting Configuration

### Common Issues

1. **Threshold Settings**: Too high causes missed extractions, too low causes noise
2. **Resource Limits**: Insufficient workers or memory for document volume
3. **Prompt Ambiguity**: Unclear instructions lead to inconsistent outputs
4. **Schema Mismatches**: Configuration doesn't match actual document content

### Debugging Techniques

Enable configuration debugging:

```bash
# Enable detailed configuration logging
export CONFIG_LOG_LEVEL=DEBUG
export PIPELINE_LOG_CONFIG=true

uv run python packages/episteme-pipeline/examples/pipeline_langfuse_full_run.py
```

### Validation Tools

Check configuration validity:

```python
# Validate configuration structure
try:
    validated_config = PipelineConfig.model_validate(config_dict)
    print("Configuration is valid")
except Exception as e:
    print(f"Configuration error: {e}")
```

## Next Steps

- Learn about [Pipeline Execution](run_pipeline.md)
- Understand [Output Inspection](inspect_outputs.md)
- Explore [Run Resumption](resume_runs.md)
