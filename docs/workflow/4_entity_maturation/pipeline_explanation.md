# Phase 4: Entity Maturation (Batch Epistemic Synthesis)

## Overview

Phase 4 executes the **Two-Stage Entity Maturation Protocol**. While Phase 2 extracts entities with high throughput
using the first encountered mention for initial description, Phase 4 runs as a batch synthesis pass before argument
mining to stabilize entity identities and mitigate **epistemic drift**.

It retrieves all textual envelopes associated with an entity, computes the geometric centroid of these envelopes in
latent embedding space, selects the most representative envelopes closest to that centroid, and uses an LLM to
synthesize a canonical, stable description.

Processing is crash-resilient and incremental: only entities where `is_mature` is `False` are processed, and batches are
checkpointed to the graph store immediately.

## Goals

- Eliminate the "first-mention-wins" bias in entity descriptions.
- Prevent epistemic drift where continuous description updates destabilize downstream vector alignments.
- Preserve topological invariance in the latent embedding space.
- Produce stabilized, canonical entity nodes with `is_mature = True` before argument mining (Phase 4b) and theory fusion
  (Phase 5).

## Steps

1. **Immature Entity Identification**:
    - Loads all entities from the graph store via `get_entities()`.
    - Filters down to entities where `not getattr(e, "is_mature", False)`.
    - Emits `ProgressStarted` with the count of immature entities.
2. **Textual Envelope Retrieval**:
    - For each entity in a batch, queries `graph_store.get_entity_envelopes(entity.id)` to fetch all mention context
      envelopes linked via `EXTRACTED_FROM` relationships.
    - If an entity has no envelopes (e.g. isolated node), it is marked mature with its existing description to prevent
      redundant reprocessing on future runs.
3. **Geometric Centroid Calculation**:
    - Envelopes are embedded concurrently via `embedding_model.aget_text_embedding_batch(envelopes)` and converted to
      PyTorch tensors (`as_tensor`).
    - The geometric centroid $\mathbf{c} \in \mathbb{R}^d$ is computed:
$$\mathbf{c} = \frac{1}{N} \sum_{i=1}^N \mathbf{e}_i$$
      where $\mathbf{e}_i$ is the dense embedding vector of envelope $T_i$.
4. **Top-K Representative Selection**:
    - If the entity has fewer envelopes than `maturation_top_k` (default: 5), all envelopes are retained.
    - Otherwise, cosine similarities between each envelope embedding and the centroid $\mathbf{c}$ are computed:
$$\text{sim} (\mathbf{e}_i, \mathbf{c}) = \frac{\mathbf{e}_i \cdot \mathbf{c}}{\|\mathbf{e}_i\| \|\mathbf{c}\|}$$
    - Envelopes are sorted in descending order of similarity, and the top-$K$ envelopes closest to the centroid are
      selected.
5. **LLM Generative Description Synthesis**:
    - The selected envelopes and entity name are formatted into `entity_synthesis_prompts`.
    - Structured decoding (`ensure_structured_llm`) parses the output into `EntitySynthesisOutput(description=...)`.
6. **Graph Checkpoint & Telemetry**:
    - The entity is updated: `entity.model_copy(update={"description": output.description, "is_mature": True})`.
    - The runner emits `EntityMaturationSynthesized(entity_id=..., name=..., envelope_count=...)`.
    - Enriched entities are committed in sub-batches to Neo4j via `graph_store.upsert_entities()`.
    - Generates `build_linked_entity_artifact` envelopes for the run manifest.

## Phase Data Flow

- **Input:** `Phase3ArtifactsView` (dependency gate) + entities from graph store.
- **Output:** Phase 4 entity maturation artifact collection.
- **Graph updates:**
    - Entity nodes: `description` updated to synthesized canonical text, `is_mature = True`.

## Pluggability

- **Embedding Model**: Injected via `Pipeline.for_task(embedding_model=...)` or configured in `ModelConfig`.
- **Top-K Window**: Configured via `Phase4EntityMaturationConfig.maturation_top_k` (default 5).
- **Prompt Bundle**: Overridable via `Phase4EntityMaturationConfig.entity_synthesis_prompts`.
- **Batch Size**: Configured via `Phase4EntityMaturationConfig.batch_size` (default 10).

## Implementation

- `pipeline/phases/phase4_entity_maturation/__init__.py` — `Phase4EntityMaturationRunner`
- `pipeline/config.py` — `Phase4EntityMaturationConfig`
- `pipeline/contracts/domain.py` — `L2Entity`
- `pipeline/protocols/extractors.py` — `EmbeddingModel`, `as_tensor`
- `pipeline/protocols/graph_store.py` — `ProcessingGraph.get_entity_envelopes`
