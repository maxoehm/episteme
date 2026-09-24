# [ISSUE-023] SemanticChunker Tokenization Documentation & Configurable Encodings

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-023` |
| **Component(s)** | `packages/episteme-pipeline` (`pipeline/phases/phase1_foundation/chunker.py`, `pipeline/config.py`) |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Hygiene) |
| **Priority** | Low |
| **Status** | Open |
| **Source Ref** | [`review/07/02_indexing_and_chunking.md`](review/07/02_indexing_and_chunking.md), [`chunker.py`](packages/episteme-pipeline/episteme_pipeline/phases/phase1_foundation/chunker.py) |

---

## 1. Problem Statement & Motivation
During earlier development, `SemanticChunker` relied on an approximate word count heuristic (`word_count * 1.35`). This was subsequently upgraded in [`chunker.py`](packages/episteme-pipeline/episteme_pipeline/phases/phase1_foundation/chunker.py#L32-L36) to use exact token counting via `tiktoken` (`cl100k_base`) alongside `nltk.sent_tokenize` for linguistic boundary splitting.

However, several inconsistencies and hygiene gaps remain:
1. **Stale Documentation & Docstrings:** The module docstring in `chunker.py` still states:
   ```python
   Token count is approximated as word count × 1.35 (empirically close to
   BPE counts for dense philosophical prose in German/English).
   ```
   This contradicts the actual implementation and confuses external contributors.
2. **Hardcoded Tiktoken Encoding:** The tokenizer is hardcoded to `cl100k_base`. If local models (e.g., Llama-3, Mistral, Gemma) or alternative embeddings with different tokenizers are configured, token lengths and context window boundaries will diverge.

---

## 2. Functional Requirements
1. **Clean Up Docstrings & Architectural Docs**:
   - Update `chunker.py` docstrings to accurately document the dual tiktoken + NLTK sentence boundary chunking algorithm.
   - Synchronize Diátaxis documentation in `docs/workflow/1_data_foundation.md` and related pages.
2. **Configurable Tokenizer Encoding in `Phase1Config`**:
   - Expose `tokenizer_encoding: str = "cl100k_base"` on `Phase1Config`.
   - Pass the configured encoding into `_count_tokens` or allow providing a custom tokenizer callable, matching the flexible encoder design recommended in GraphRAG comparison review §02.

---

## 3. Acceptance Criteria
- [ ] Module and function docstrings in `chunker.py` accurately describe exact tokenization and sentence boundaries.
- [ ] `Phase1Config` includes `tokenizer_encoding` and passes it to `chunker.py`.
- [ ] Unit tests in `packages/episteme-pipeline/tests/` verify token counting with custom encodings.

---

## 4. Key Target Files
- [`packages/episteme-pipeline/episteme_pipeline/phases/phase1_foundation/chunker.py`](packages/episteme-pipeline/episteme_pipeline/phases/phase1_foundation/chunker.py)
- [`packages/episteme-pipeline/episteme_pipeline/config.py`](packages/episteme-pipeline/episteme_pipeline/config.py)
