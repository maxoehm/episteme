# Inspecting Outputs

Guide to examining and analyzing the results produced by the Episteme pipeline.

## Run Reports

Each pipeline execution generates a comprehensive report with execution details.

### Accessing Reports

Retrieve reports programmatically:

```python
# Get report for a specific run
report = await pipeline.get_run_report("run-abc123")

# View summary information
print(report.summary)

# Access detailed phase information
for phase_record in report.phase_records:
    print(f"Phase {phase_record.phase_ordinal}: {phase_record.status}")
```

### Report Contents

Reports contain valuable information:

1. **Execution Metadata**: Start time, duration, configuration
2. **Phase Statistics**: Success/failure counts, timing data
3. **Performance Metrics**: Token usage, API calls, costs
4. **Error Summary**: Failed operations and exception details
5. **Artifact Inventory**: Generated artifacts and their locations

## Artifact Inspection

Artifacts provide detailed insight into intermediate pipeline results.

### Retrieving Artifacts

Access artifacts by run ID and phase:

```python
# Get all artifacts from a run
all_artifacts = await pipeline.get_run_artifacts("run-abc123")

# Filter by phase
phase2_artifacts = await pipeline.get_run_artifacts(
    "run-abc123", 
    phase_name="phase2"
)

# Filter by artifact type
entity_artifacts = await pipeline.get_run_artifacts(
    "run-abc123",
    kind="entity_mention"
)
```

### Examining Artifact Content

Inspect individual artifacts:

```python
for artifact in entity_artifacts:
    print(f"Document: {artifact.provenance.source_document}")
    print(f"Confidence: {artifact.payload.confidence}")
    print(f"Entity: {artifact.payload.text}")
    print(f"Type: {artifact.payload.entity_type}")
    print("---")
```

## Graph Database Inspection

The Neo4j database contains the final theory graph representation.

### Connecting to Neo4j

Connect using standard Neo4j tools:

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)
```

### Querying Graph Structure

Explore the constructed graph:

```cypher
// Count nodes by type
MATCH (n)
WHERE NOT n:Chunk
RETURN labels(n)[0] as type, count(*) as count
ORDER BY count DESC

// Find high-confidence relationships
MATCH (a)-[r]->(b)
WHERE r.confidence > 0.8
RETURN a.name, type(r), b.name, r.confidence
LIMIT 20

// Examine argument structures
MATCH (claim:ArgumentComponent {component_type: "CLAIM"})-[r:SUPPORTS]->(premise:ArgumentComponent)
RETURN claim.text, premise.text
LIMIT 10
```

### Analyzing Entity Networks

Investigate entity relationships:

```cypher
// Find entities with many relationships
MATCH (n)
WHERE NOT n:Chunk AND NOT n:ArgumentComponent
WITH n, size([(n)-->() | 1]) + size([()-->(n) | 1]) as degree
WHERE degree > 5
RETURN n.name, labels(n)[0] as type, degree
ORDER BY degree DESC

// Explore entity neighborhoods
MATCH (center:Concept {name: "Situation Calculus"})
MATCH (center)-[r]-(neighbor)
RETURN center.name, type(r), neighbor.name
```

## File System Artifacts

Artifacts are also persisted to the file system for offline analysis.

### Artifact Directory Structure

```
.pipeline_artifacts/
├── run-abc123/
│   ├── phase1/
│   │   ├── chunks/
│   │   └── documents/
│   ├── phase2/
│   │   ├── entity_mentions/
│   │   └── linked_entities/
│   └── phase3/
│       ├── local_relations/
│       └── global_relations/
```

### Reading Artifact Files

Examine JSON artifact files directly:

```python
import json

with open(".pipeline_artifacts/run-abc123/phase2/entity_mentions/artifact-xyz.json", "r") as f:
    artifact = json.load(f)
    print(artifact["payload"]["text"])
    print(artifact["payload"]["confidence"])
```

## Visualization Tools

Several approaches exist for visualizing theory graphs.

### Neo4j Browser

The built-in Neo4j Browser provides graph visualization:

1. Open `http://localhost:7474` in your browser
2. Connect to your database
3. Run Cypher queries to retrieve graph data
4. Use the visualization panel to explore results

### Export for External Tools

Export graph data for analysis in external tools:

```cypher
// Export nodes as CSV
MATCH (n)
WHERE NOT n:Chunk
WITH n, labels(n)[0] as type
RETURN id(n) as id, n.name as name, type
ORDER BY type
```

```cypher
// Export relationships as CSV
MATCH (a)-[r]->(b)
WHERE NOT a:Chunk AND NOT b:Chunk
RETURN id(a) as source_id, id(b) as target_id, type(r) as relationship, r.confidence as confidence
```

## Quality Assessment

Evaluate the quality of pipeline outputs.

### Entity Quality

Assess entity extraction performance:

```cypher
// Distribution of entity confidence scores
MATCH (n)
WHERE NOT n:Chunk AND n.confidence IS NOT NULL
RETURN floor(n.confidence * 10) / 10 as confidence_bin, count(*) as count
ORDER BY confidence_bin

// Entity type distribution
MATCH (n)
WHERE NOT n:Chunk
UNWIND labels(n) as label
RETURN label, count(*) as count
ORDER BY count DESC
```

### Relationship Quality

Analyze relationship extraction results:

```cypher
// Relationship type distribution
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(*) as count
ORDER BY count DESC

// Confidence distribution for relationships
MATCH ()-[r]->()
RETURN floor(r.confidence * 10) / 10 as confidence_bin, count(*) as count
ORDER BY confidence_bin
```

## Debugging Information

Access detailed debugging data when troubleshooting.

### Event Logs

Review event emission during execution:

```python
# Register listener for detailed events
@emitter.on("entity.extracted")
def on_entity_extracted(event):
    print(f"Extracted entity: {event['text']} ({event['confidence']})")
```

### Timing Data

Analyze performance bottlenecks:

```python
# Access timing information from reports
report = await pipeline.get_run_report(run_id)
for phase in report.phase_records:
    print(f"Phase {phase.phase_ordinal} took {phase.duration_seconds}s")
```

## Export and Sharing

Prepare outputs for sharing or further analysis.

### Structured Exports

Export data in standard formats:

```python
# Export entities to CSV
import csv

artifacts = await pipeline.get_run_artifacts(run_id, kind="linked_entity")
with open("entities.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "name", "type", "confidence"])
    for artifact in artifacts:
        payload = artifact.payload
        writer.writerow([
            payload.id,
            payload.name,
            payload.label,
            payload.confidence
        ])
```

### Graph Exports

Export graph structures:

```cypher
// Export as GraphML for external tools
CALL apoc.export.graphml.all("theory_graph.graphml", {})
```

## Comparison Analysis

Compare results across different runs or configurations.

### Run-to-Run Comparison

Analyze differences between pipeline executions:

```python
# Compare entity counts between runs
run1_artifacts = await pipeline.get_run_artifacts("run-1", kind="linked_entity")
run2_artifacts = await pipeline.get_run_artifacts("run-2", kind="linked_entity")

print(f"Run 1 entities: {len(run1_artifacts)}")
print(f"Run 2 entities: {len(run2_artifacts)}")
```

### Configuration Impact

Assess the effect of different settings:

```python
# Compare results with different confidence thresholds
high_confidence_entities = await pipeline.get_run_artifacts(
    "high-threshold-run", 
    kind="linked_entity"
)
low_confidence_entities = await pipeline.get_run_artifacts(
    "low-threshold-run", 
    kind="linked_entity"
)
```

## Archival and Restoration

Preserve results for future reference.

### Backup Strategies

Archive important runs:

```bash
# Archive artifact directory
tar -czf pipeline-artifacts-run-abc123.tar.gz .pipeline_artifacts/run-abc123/

# Backup Neo4j database
neo4j-admin dump --database=neo4j --to=neo4j-backup.dump
```

### Restoration Procedures

Restore previous results:

```bash
# Restore artifacts
tar -xzf pipeline-artifacts-run-abc123.tar.gz

# Restore database
neo4j-admin load --from=neo4j-backup.dump --database=neo4j
```

## Next Steps

- Inspect runs and theory graphs visually in [Episteme Studio](../getting_started/studio.md)
- Learn about [Resume Capabilities](resume_runs.md)
- Explore [Advanced Configuration](customize_config.md)
- Understand [Evaluation Methods](../research/evaluation_methodology.md)
