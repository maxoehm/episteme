# Phase 2 — Prompting Strategy

## NER and Local Relation Extraction

### Chain-of-Thought Approach

The NER prompt uses a two-step chain-of-thought (CoT) strategy before classification:

1. **Structural reasoning first** — the model identifies logical connectives and argument structure (e.g., "X implies
   Y", "A contradicts B", "because", "therefore"). This primes the model to treat philosophical sentences as relational
   structures rather than isolated facts.
2. **Entity and relation classification** — only after the structural pass does the model assign labels and extract
   triples.

This order matters for philosophical texts: a sentence like *"Hegel's dialectic presupposes Kant's transcendental
idealism"* contains a SETZT_VORAUS relation between two KONZEPT nodes, but a model that does not first identify "
presupposes" as a logical connective will miss it.

### Alias Resolution within a Chunk

The prompt includes an explicit instruction to resolve within-chunk aliases: *"Resolve pronouns or aliases that are
clearly identifiable within this chunk."* The LLM normalises the entity name it writes — so "he", "the philosopher", "I.
Kant" all become "Kant" (or the canonical form it infers from context). This eliminates a whole class of phantom
duplicate entities.

Cross-chunk aliases are not resolved here. They are handled downstream by Phase 3b Latent Graph Consolidation. See
`docs/workflow/3b_consolidation/index.md` and `docs/adr/0003-coreference-absorbed-into-fusion.md`.

### Default Prompt Template

The following is the prompt used in `pipeline/prompts/default_prompts.py` (`NER_EXTRACTION_PROMPT`). It is injected with
`{entity_types}` and `{relation_types}` at runtime from `SchemaConfig`.

```
You are an expert in formal logic and the history of philosophy.
Extract all entities and their local relations from the following text chunk.

### Entity Types (use exactly these labels)
{entity_types}

### Relation Types (use exactly these labels)
{relation_types}

### Instructions
1. First identify logical connectives and argument structure (chain-of-thought step).
2. Then classify each entity span and extract local triples.
3. Resolve pronouns or aliases that are clearly identifiable within this chunk.
4. Output strictly valid JSON matching the schema below. No text outside the JSON.

### Output Schema
{
  "entities": [{"id": "<str>", "label": "<entity_type>", "name": "<canonical name>", "text": "<span>"}],
  "triples":  [{"subject_id": "<str>", "predicate": "<relation_type>", "object_id": "<str>", "confidence": <float 0-1>}]
}

### Input Text
{chunk_text}
```

This prompt is overridable per-run via `Phase2Config.ner_prompt_template`.

### Key prompt design choices

| Choice                                | Rationale                                                                                                                      |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Canonical `name` separate from `text` | Allows normalisation (e.g., "the Königsberg philosopher" → "Kant") while preserving the original span in `text` for provenance |
| LLM-local `id` (`e1`, `e2`, …)        | Decouples triple references from stable graph IDs; remapping happens in `LLMNERExtractor` after parsing                        |
| `confidence` on triples               | Enables noise filtering in later phases; LLMs often assign lower confidence to inferred vs explicit relations                  |
| Strict JSON output instruction        | Required for `astructured_predict` to parse reliably; hallucinated prose before/after JSON breaks structured output            |

---

## Entity Linking (Disambiguation)

Entity linking during Phase 2 matches extracted entities against canonical graph nodes using string containment
(`NameEntityLinker`). Downstream cross-chunk deduplication and consolidation is handled non-generatively by Phase 3b
Latent Graph Consolidation. See [`docs/workflow/3b_consolidation/index.md`](../3b_consolidation/index.md).

---

## Tuning guidance

- **Dense philosophical texts** — consider raising `Phase2Config.batch_size` to 100+ chunks if per-chunk extraction is
  fast; LLM latency dominates over I/O at small batch sizes.
- **German-language sources** — entity types `KONZEPT`, `SCHULE_STROEMUNG`, etc. are German-labelled by design. If the
  LLM struggles with German labels, consider using English aliases in `SchemaConfig` and mapping back at output time.
- **Long chunks** — chunks exceeding ~800 tokens have higher NER miss rates because the model attends less to entity
  spans at the end. The default `Phase1Config.chunk_size = 1024` tokens is a reasonable upper bound; consider reducing
  to 768 for dense texts.
