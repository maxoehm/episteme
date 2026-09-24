# Algorithmic Transparency & Model Provenance

To ensure the reproducibility of the Episteme pipeline and to adhere to academic standards for Natural Language
Processing (NLP), this document specifies the provenance of models, prompts, and the handling of non-determinism during
the theory graph construction.

## Model Provenance

The pipeline utilizes state-of-the-art Large Language Models (LLMs) via the LiteLLM interface.

* **Primary Extraction Model:** (Specify model here, e.g., `gpt-4o`, `claude-3-opus-20240229`)
* **Embeddings / Retrieval Model:** (Specify model here, e.g., `text-embedding-3-large`)
* **Temperature:** Set to `0.0` across all extraction phases to minimize stochasticity and maximize determinism.

## Prompt Engineering & Methodology

In an LLM-driven pipeline, prompts serve as the methodological instructions for the system. Our prompts are maintained
as version-controlled code artifacts rather than isolated text files, ensuring they evolve synchronously with the phase
logic.

* **Entity Extraction (Phase 2):** Defined within `LLMNERExtractor`. Utilizes Chain-of-Thought (CoT) structural
  reasoning to identify logical connectives before assigning entity types.
* **Global Relation Reranking (Phase 3):** Defined by `GLOBAL_RELATION_PROMPT`. Utilizes cross-encoder joint attention
  to evaluate context envelopes.
* **Argument Mining (Phase 4):** Prompts for ADU segmentation, component classification, and relation classification are
  maintained within their respective `TAG*` classifier components.

## Handling Non-Determinism

Because LLMs introduce inherent stochasticity, Episteme employs multiple strategies to enforce theoretical rigor and
graph stability:

1. **Entity Gleanings (Multi-Pass Validation):** Allows for multiple extraction passes over the same context window to
   catch missed entities, mitigating the "lost in the middle" phenomenon.
2. **Epistemic Centroid Calculation:** Instead of relying on a single generative description for a concept, Phase 4
   computes the geometric centroid of all empirical envelopes attached to an entity, synthesizing a canonical
   description (`ENTITY_SYNTHESIS_PROMPT`) that resists epistemic drift.
3. **Confidence Thresholds:** All local and global relations (`L2Triple`, `L3ArgumentRelation`) are assigned confidence
   scores. Edges failing to meet the `structural_correspondence` threshold are pruned.
