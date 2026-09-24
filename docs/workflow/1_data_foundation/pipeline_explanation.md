# Phase 1: Data Foundation

## Overview

Phase 1 ingests raw source documents (TeX, Markdown, plain text), converts them to normalised Markdown, splits the text
into semantically coherent chunks, embeds each chunk, and commits the full document structure — Document, Chapter, and
Chunk nodes with CONTAINS and NEXT edges — to the graph store.

This phase establishes the Layer 1 backbone. Every extraction in later phases traces back to a Chunk node via
`EXTRACTED_FROM` edges.

## Goals

- Convert heterogeneous document formats to a canonical internal representation
- Produce semantically coherent chunks that fit within an LLM context window
- Embed chunks for later vector search (Phase 3 TAG envelope retrieval)
- Commit an auditable provenance trail (stable deterministic IDs, ingestion timestamps)
- Be idempotent: re-running Phase 1 on already-committed documents is safe (MERGE)

## Steps

1. **Format conversion** (`DataSourceAdapter`) — each supported format has an adapter. The default `TexAdapter` calls
   Pandoc (`--wrap=none --strip-comments`) to convert TeX to Markdown, optionally injecting bibliography files. Adapter
   selection is by `can_handle(path)`.
2. **Section parsing** (`parse_sections`) — splits Markdown at H1/H2 boundaries into `RawSection` objects. Content
   before the first header becomes a "Preamble" section.
3. **Chunk splitting** (`chunk_section`) — splits each section at paragraph boundaries, falling back to sentence-level
   splitting (using NLTK sentence tokenization) if a paragraph is larger than the max token limit. Token counts are
   computed exactly using `tiktoken` (cl100k_base encoder). Overlap carry-forward guarantees that sentences are never
   split in half across chunk boundaries.

   *Architectural Note (Adaptive Rhetorical Chunking):* By strictly adhering to structural boundaries (H1/H2) and only
   splitting by paragraph or sentence when a section exceeds the efficient context limit, we actively mitigate the
   "evidence fragmentation" and cross-chunk context loss commonly seen in naive fixed-window chunking approaches (such
   as those observed in the *SciGraph-LLM (2026)* study).
4. **Embedding** — `embed_model.aget_text_embedding(chunk.text)` for each chunk; sync fallback if the model does not
   support async.
5. **Graph commit** — Document, Chapter, Chunk nodes upserted via MERGE. CONTAINS edges (Document→Chapter,
   Chapter→Chunk) and NEXT edges (Chunk[i]→Chunk[i+1]) committed.

## Phase Data Flow

- **Input:** `PipelineInput(source_paths: list[str])` — file paths to source documents.
- **Output:** Phase 1 document/chunk artifact collection.
- **Graph updates:**
    - `Document` node: `id`, `title`, `source_path`, `ingested_at`
    - `Chapter` node: `id`, `title`, `sequence_index`
    - `Chunk` node: `id`, `text`, `embedding`, `source_doc_id`, `chapter_id`, `sequence_index`, `token_count`
    - `CONTAINS` edges: Document→Chapter, Chapter→Chunk
    - `NEXT` edges: Chunk[i]→Chunk[i+1] (`distance: 1`)

## Pluggability

- **Custom document format:** implement `DataSourceAdapter(ABC)` and pass via `Phase1Runner(adapters=[MyAdapter()])`.
- **Embedding model:** any LlamaIndex `BaseEmbedding`; inject via `Pipeline.from_config(embed_model=...)`.
- **Chunk size / overlap:** `Phase1Config(chunk_size=768, chunk_overlap=100)`.

## Provenance and IDs

All IDs are deterministic SHA-256 hashes of content:

- `doc_id(path)` = `"doc_" + sha256(path.stem)[:14]`
- `chapter_id(doc_id, title)` = `"{doc_id}_chap_{sha256(title)[:10]}"`
- `chunk_id(chap_id, sequence_index, text)` = `"{chap_id}_chunk_{seq:04d}_{sha256(text[:200])[:8]}"`

Re-ingesting the same document produces the same IDs, so MERGE leaves existing nodes unchanged.

## Implementation

`pipeline/phases/phase1_foundation/__init__.py` — `Phase1Runner`  
`pipeline/phases/phase1_foundation/chunker.py` — `parse_sections`, `chunk_section`, `chunk_document`  
`pipeline/phases/phase1_foundation/provenance.py` — `doc_id`, `chapter_id`, `chunk_id`  
`pipeline/phases/phase1_foundation/adapters/tex_adapter.py` — `TexAdapter`
