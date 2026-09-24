# How to Configure and Use the LLM Caching Layer

This guide explains how to enable, configure, and manage the local LLM-level caching layer in Episteme.

---

## Overview

During development and pipeline execution, LLM API calls can be costly and slow. While Episteme has a phase-level
artifact caching system, modifications to prompts or pipeline components can invalidate entire phases, forcing
re-execution of downstream phases.

The local **LLM Caching Layer** acts as an intra-phase cache. It intercept all structured prediction calls (
`predict_structured`) made via the `StructuredLLM` adapter and caches the raw JSON responses on disk.

### Benefits

- **Resume on Failures**: If the pipeline crashes mid-phase (e.g. rate limit error at chunk 87/100), restarting will
  load the first 86 chunks from the local cache in under 1ms, consuming $0 in API credits.
- **Fast Iteration**: Iterate on prompts, configurations, or downstream phases without paying the time/cost penalty of
  extracting entities from unchanged source documents.

---

## Configuration

By default, the LLM caching layer is enabled and writes cache entries to the `.pipeline_runs/llm_cache/` directory.

### Enabling/Disabling the Cache

The cache is initialized inside the `ensure_structured_llm` adapter helper:

```python
from pipeline.llm import ensure_structured_llm

# Caching enabled (default)
llm = ensure_structured_llm(base_llm, use_cache=True)

# Disable caching for fresh live runs
llm = ensure_structured_llm(base_llm, use_cache=False)
```

---

## How It Works

Cache keys are calculated deterministically using a SHA256 payload fingerprint. The fingerprint payload includes:

1. The **Method Fingerprint** (derived from the class configuration of your LLM provider).
2. The **Output Schema Name** (the name of the target Pydantic class).
3. The **Prompt Template Source**.
4. The exact **Prompt Arguments** (including the chunk content, variables, types).

If any of these change (e.g. you edit the extraction prompt, modify the schema fields, or run a new chunk of text), the
cache key will change, and a cache miss will occur.

---

## Cache Directory Maintenance

Cache files are saved as JSON files in:

```bash
.pipeline_runs/llm_cache/
```

To clear the cache and force fresh API calls, simply delete the contents of this directory:

```bash
rm -rf .pipeline_runs/llm_cache/*
```
