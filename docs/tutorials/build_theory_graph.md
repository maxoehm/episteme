# Building a Theory Graph

This tutorial walks through creating a comprehensive theory graph from a collection of philosophical texts.

## Scenario Overview

We'll process a set of related philosophical works to construct a theory graph that captures:

- Core theoretical concepts
- Relationships between ideas
- Argumentative structures
- Cross-work references

## Preparation

### Source Document Selection

Choose documents that form a coherent theoretical discourse:

```python
SOURCE_PATHS = [
    "texts/kant_critique_pure_reason.pdf",
    "texts/kant_prolegomena.pdf",
    "texts/hermann_helmholtz_fact_science.tex",
    "texts/ernst_mach_physical_principles.tex"
]
```

### Domain Configuration

Set up configuration optimized for philosophical content:

```python
from pipeline.config import (
    PipelineConfig, ExecutionConfig, Phase1Config, 
    Phase2Config, Phase3Config, GraphSchemaConfig
)

config = PipelineConfig(
    execution=ExecutionConfig(
        project_artifacts_to_graph=True,
        allow_phase_reuse=True
    ),
    phase1=Phase1Config(
        chunk_size=1200,      # Balance detail with context
        chunk_overlap=200
    ),
    phase2=Phase2Config(
        ner_confidence_threshold=0.85,  # High precision for concepts
        allowed_entity_types=[
            "CONCEPT", "PERSON", "WORK", "THEORY", "SCHOOL"
        ]
    ),
    phase3=Phase3Config(
        global_relation_sample_size=100,  # Rich context for relationships
        reranker_top_k=40,
        global_relation_confidence_threshold=0.8
    ),
    graph_schema=GraphSchemaConfig(
        allowed_entity_types=[
            "Concept", "Person", "Work", "Theory", "School", "Argument"
        ],
        allowed_relation_types=[
            "SUPPORTS", "REFUTES", "RELATED_TO", "INSTANCE_OF", 
            "PART_OF", "INFLUENCES", "PRECEDES"
        ]
    )
)
```

## Execution Strategy

### Initial Run

Process all documents in a single execution:

```python
# Set up pipeline components
pipeline = create_pipeline(config, llm, embed_model)

# Execute full pipeline
result = await pipeline.run(
    PipelineInput(source_paths=SOURCE_PATHS)
)

print(f"Run completed: {result.manifest.run_id}")
```

### Quality Assessment

Evaluate initial results:

```python
# Check entity extraction quality
artifacts = await pipeline.get_run_artifacts(
    result.manifest.run_id, 
    kind="linked_entity"
)

concepts = [a for a in artifacts if a.payload.label == "Concept"]
print(f"Extracted {len(concepts)} concepts")

# Review high-confidence relationships
relations = await pipeline.get_run_artifacts(
    result.manifest.run_id,
    kind="global_relation"
)

high_confidence = [r for r in relations if r.payload.confidence > 0.9]
print(f"High-confidence relations: {len(high_confidence)}")
```

## Iterative Improvement

### Refining Configuration

Based on initial results, adjust configuration:

```python
# If too many false positives, increase thresholds
refined_config = PipelineConfig(
    phase2=Phase2Config(
        ner_confidence_threshold=0.9,  # Increased from 0.85
    ),
    phase3=Phase3Config(
        global_relation_confidence_threshold=0.85  # Increased from 0.8
    )
)
```

### Targeted Re-execution

Re-run specific phases with refined settings:

```python
# Resume from Phase 3 with new configuration
refined_result = await pipeline.resume_from_run(
    run_id=result.manifest.run_id,
    input=PipelineInput(source_paths=SOURCE_PATHS),
    from_phase=3  # Re-execute phases 3-5
)
```

## Analysis and Exploration

### Concept Network Analysis

Explore relationships between key concepts:

```cypher
// Find central concepts in the theory graph
MATCH (c:Concept)
WITH c, size([(c)-->() | 1]) + size([()-->(c) | 1]) as degree
WHERE degree > 10
RETURN c.name, degree
ORDER BY degree DESC
```

### Argument Structure Investigation

Examine argumentative relationships:

```cypher
// Find key argumentative connections
MATCH (premise:ArgumentComponent {component_type: "PREMISE"})-[s:SUPPORTS]->(claim:ArgumentComponent {component_type: "CLAIM"})
MATCH (claim)<-[a:ATTACKS]-(objection:ArgumentComponent {component_type: "OBJECTION"})
RETURN premise.text, claim.text, objection.text
```

### Cross-Work Analysis

Identify connections between different texts:

```cypher
// Find concepts discussed across multiple works
MATCH (c:Concept)<-[:MENTIONS]-(chunk:Chunk)
WITH c, count(DISTINCT chunk.source_doc_id) as work_count
WHERE work_count > 1
RETURN c.name, work_count
ORDER BY work_count DESC
```

## Advanced Techniques

### Custom Prompt Engineering

Enhance extraction quality with domain-specific prompts:

```python
philosophy_ner_prompt = """
Extract philosophical concepts, theorists, works, and schools from the text.

Focus on:
- Abstract theoretical concepts (e.g., 'categorical imperative', 'phenomenology')
- Philosophers and their schools (e.g., 'Immanuel Kant', 'German Idealism')
- Influential works (e.g., 'Critique of Pure Reason')
- Theoretical frameworks (e.g., 'Utilitarianism', 'Existentialism')

Text: {text}
"""

config = PipelineConfig(
    phase2=Phase2Config(
        ner_prompt_template=philosophy_ner_prompt
    )
)
```

### Schema Extension

Add domain-specific relationship types:

```python
extended_schema = GraphSchemaConfig(
    allowed_entity_types=[
        "Concept", "Person", "Work", "Theory", "School", "Argument"
    ],
    allowed_relation_types=[
        "SUPPORTS", "REFUTES", "RELATED_TO", "INSTANCE_OF", 
        "PART_OF", "INFLUENCES", "PRECEDES", "CONTRADICTS",
        "PARALLEL_TO", "DERIVED_FROM"
    ]
)
```

## Visualization and Presentation

### Graph Visualization

Create visual representations of key theoretical structures:

```python
# Export subgraphs for visualization
def export_concept_subgraph(concept_name, depth=2):
    """Export neighborhood of a concept for visualization."""
    query = """
    MATCH (center:Concept {name: $concept_name})
    CALL apoc.path.subgraphAll(center, {maxLevel: $depth})
    YIELD nodes, relationships
    RETURN nodes, relationships
    """
    # Execute query and export to GraphML or other format
```

### Report Generation

Create analytical reports from the theory graph:

```python
def generate_theory_report():
    """Generate comprehensive report on theory graph structure."""
    # Analyze graph metrics
    # Identify key concepts and relationships
    # Summarize argumentative structures
    # Highlight cross-work connections
```

## Validation and Quality Control

### Expert Review

Sample results for expert validation:

```python
def sample_for_review(run_id, sample_size=50):
    """Select representative artifacts for expert review."""
    # Sample high-confidence entities
    # Sample key relationships
    # Include controversial or complex cases
    # Prepare review package with context
```

### Consistency Checking

Verify theoretical consistency:

```cypher
// Check for contradictory relationships
MATCH (a)-[r1:REFUTES]->(b)-[r2:SUPPORTS]->(a)
RETURN a.name, b.name
```

## Next Steps

### Extending the Corpus

Add related works to enrich the theory graph:

```python
EXTENDED_SOURCES = SOURCE_PATHS + [
    "texts/additional_philosopher_work.pdf",
    "texts/related_theoretical_framework.tex"
]

# Resume with extended source set
extended_result = await pipeline.resume_from_run(
    run_id=refined_result.manifest.run_id,
    input=PipelineInput(source_paths=EXTENDED_SOURCES)
)
```

### Downstream Applications

Use the theory graph for advanced analysis:

1. **Question Answering**: Query theoretical relationships
2. **Gap Analysis**: Identify under-explored areas
3. **Influence Mapping**: Trace theoretical development
4. **Comparison Studies**: Contrast different frameworks

## Conclusion

This tutorial demonstrated a comprehensive approach to building theory graphs from philosophical texts. The iterative
process of execution, analysis, and refinement is key to achieving high-quality results that faithfully represent the
theoretical content of the source materials.
