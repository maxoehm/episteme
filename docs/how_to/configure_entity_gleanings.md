# How to Configure Entity Gleanings for Dense Text

This guide explains how to configure and use the **Entity Gleanings** loop in Phase 2 for multi-pass entity extraction.

---

## Overview

When extracting concepts, arguments, and relations from complex academic texts (such as dense philosophy or scientific
literature), single-pass Named Entity Recognition (NER) prompts can miss critical entities or subtle arguments.

The **Entity Gleanings** loop implements a multi-pass approach (similar to GraphRAG). After the first extraction, if
configured, the pipeline will re-prompt the LLM with the text and the list of already extracted items to ask: *"Are
there any other entities or arguments that were not extracted yet?"*. This loop repeats up to a configurable number of
iterations or until the LLM yields no new entities.

---

## Configuration

To enable entity gleanings, update the `Phase2Config` in your pipeline configuration:

```python
from pipeline.config import PipelineConfig, Phase2Config

config = PipelineConfig(
    phase2=Phase2Config(
        max_gleanings=2,  # Repeat up to 2 extra times to extract missed entities
    )
)
```

### Parameters

- `max_gleanings` (int, default `0`): The maximum number of extra gleaning passes. Set to `0` to disable (default
  behavior).
- `ner_prompt_template` (str): You can also supply a custom extraction prompt, though the pipeline provides a default
  query structure for the gleanings loop.

---

## How It Works

1. **Initial Pass**: The `LLMNERExtractor` queries the LLM with the default extraction prompt and schema.
2. **Gleaning Checks**: If `max_gleanings > 0`, the extractor formats a new prompt:
    - Includes the original chunk text.
    - Lists the names of the entities already extracted in prior passes.
    - Requests any new entities/relations in the same structured format.
3. **Early Exit**: If the LLM returns empty entity and relation lists, the loop immediately terminates early.
4. **Union & De-duplication**: The results of all passes are combined, normalized, and linked to their canonical IDs.
