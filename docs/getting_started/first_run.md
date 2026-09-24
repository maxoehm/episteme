# First Run Tutorial

This tutorial guides you through executing a complete theory graph construction pass on an authentic scientific paper using Episteme's verified runtime entry point.

---

## Scenario & Corpus

We process the classic educational psychology study by Robert Rosenthal and Lenore Jacobson (1966):
> **Rosenthal, R., & Jacobson, L. (1966).** *Teacher expectancies: Determinants of pupils' IQ gains.*
> Source file: `packages/episteme-pipeline/examples/text/teachers_expectancies.md`

This empirical study demonstrates how teacher biases induce self-fulfilling intellectual performance gains in children. It contains empirical claims, experimental methodologies, and dialectical counterarguments—ideal for theory graph construction.

---

## Executing the Pipeline

The primary runnable example is located at `packages/episteme-pipeline/examples/pipeline_langfuse_full_run.py`. It orchestrates all 5 conceptual phases (7 runners) with live Rich progress bars and optional Langfuse tracing.

Run the pipeline from the repository root:

```bash
uv run python packages/episteme-pipeline/examples/pipeline_langfuse_full_run.py
```

```text
⠋ Running Episteme Pipeline...
  Phase 1: Data Foundation       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Phase 2: Entity Discovery      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Phase 3: Global Relations      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Phase 3b: Consolidation        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Phase 4: Entity Maturation     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Phase 4: Argument Mining       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
  Phase 5: Theory Fusion         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
```

---

## What Happens During Execution

The script executes the complete 7-runner pipeline lifecycle:

1. **Index Verification**: Ensures the Neo4j vector index matches the configured `EMBED_DIM` (e.g. 1536) before writing chunks.
2. **Phase 1 (Data Foundation)**: Ingests markdown, extracts bibliographic metadata, generates semantic chunks, and creates Layer 1 nodes in Neo4j.
3. **Phase 2 (Entity Discovery)**: Performs Named Entity Recognition (NER) and entity disambiguation via your OpenAPI endpoint and cross-encoder.
4. **Phase 3 (Global Relations)**: Employs dense vector retrieval and cross-encoder reranking to discover non-local semantic edges across chunks.
5. **Phase 3b (Latent Consolidation)**: Clusters and resolves synonym concepts in the vector latent space.
6. **Phase 4 (Maturation & Argument Mining)**: Synthesizes structured epistemic profiles and segments argument discourse units (ADUs), classifying claims, premises, and objections.
7. **Phase 5 (Theory Fusion & TheoryNet)**: Projects the higher-level dialectical argument web (`SUPPORT` and `ATTACK` edges) and calculates coherence structures.
8. **Observability & Telemetry**: If Langfuse credentials are set in `.env`, a complete distributed trace session is logged with exact prompt token counts and execution latencies.

---

## Understanding the Execution Artifacts

When the pipeline finishes, it outputs a formatted execution report:

```text
================================================================================
                    Episteme PIPELINE EXECUTION REPORT
================================================================================
Run ID:       kg-session-a1b2c3d4
Status:       COMPLETED
Started At:   2026-09-21T11:45:00Z
Duration:     42.8s

Phase Records:
  [✓] Phase 1: Data Foundation           (12 chunks, 0 reused)
  [✓] Phase 2: Entity Discovery          (34 entities, 0 reused)
  [✓] Phase 3: Global Relations          (18 relations, 0 reused)
  [✓] Phase 3b: Latent Consolidation     (6 clusters, 0 reused)
  [✓] Phase 4: Entity Maturation         (34 profiles, 0 reused)
  [✓] Phase 4: Argument Mining           (28 arguments, 0 reused)
  [✓] Phase 5: Theory Fusion             (42 edges, 0 reused)

Artifacts Stored:
  Manifest: .pipeline_runs/kg-session-a1b2c3d4/manifest.json
  Envelopes: .pipeline_artifacts/kg-session-a1b2c3d4/
================================================================================
```

* **`.pipeline_runs/`**: Contains deterministic JSON manifests with parameter fingerprints, enabling cached phase reuse on subsequent runs.
* **`.pipeline_artifacts/`**: Contains typed serialized envelopes for each phase intermediate.

---

## Inspecting Results in Neo4j

Open the Neo4j Browser at `http://localhost:7474` to query the generated graph:

### Count Nodes by Layer
```cypher
MATCH (n)
RETURN labels(n)[0] AS NodeType, count(*) AS Total
ORDER BY Total DESC;
```

### Inspect Extracted Dialectical Relations (Layer 3)
```cypher
MATCH (source:ArgumentComponent)-[r:SUPPORTS|ATTACKS]->(target:ArgumentComponent)
RETURN source.text AS Premise, type(r) AS Relation, target.text AS Claim
LIMIT 10;
```

### Inspect Conceptual Co-Occurrence with Text Grounding
```cypher
MATCH (c:Concept)<-[:MENTIONS]-(chunk:Chunk)-[:MENTIONS]->(c2:Concept)
WHERE c.name < c2.name
RETURN c.name, c2.name, count(chunk) AS SharedChunks
ORDER BY SharedChunks DESC
LIMIT 10;
```

---

## Next Steps

- Explore the generated graph visually with [Episteme Studio Workbench](studio.md)
- Learn how to rerun individual phases or modify prompts in [Running the Pipeline](../how_to/run_pipeline.md)
- Understand the underlying mathematical foundations in [TheoryNet & Formal Models](../concepts/formal_graph_model.md)
