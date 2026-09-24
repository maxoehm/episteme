# Dataset Adapters — Design Notes

Purpose: Normalize public gold standards to and from our pipeline’s artifacts for comparable scoring without altering core code.

## Inbound (Gold → Normalized)
- Loader produces a normalized JSONL with records for mentions, links, and relations.
- Required fields:
  - Mentions: `{doc_id, span_start, span_end, text, type}`
  - Links: `{doc_id, span_start, span_end, kb_id, kb_source}`
  - Relations: `{doc_id, head_span, tail_span, label, direction}` or document‑level indices.

## Outbound (Syntactic Normalization)
- The adapter only normalizes the format (e.g., converting outputs to standard triples `(head, relation, tail)`).
- **Important Note:** The adapter does *not* handle semantic label mapping or use a strict label mapping table. Semantic alignment (e.g., aligning "supports" to "is_evidence_for") is considered a feature of the knowledge graph pipeline itself (fusion phase). The evaluation scorers will use soft-matching (GM-GBS) to handle any remaining lexical divergence between predictions and the gold standard.
- Handles:
  - Format conversions
  - KB normalization (e.g., Wikipedia ↔︎ Wikidata)
  - Span alignment policy (exact vs. overlap)

## Folder Structure
- `evaluation/adapters/<dataset>/loader.md|py` — notes or code to build normalized gold.
- `evaluation/adapters/<dataset>/mapper.md|py` — notes or code to map predictions to gold labels.
- `evaluation/adapters/<dataset>/README.md` — dataset specifics (license, splits, quirks).

## Scoring Interface
- Scorers consume normalized gold and normalized predictions and emit metrics JSON used by the report template.

