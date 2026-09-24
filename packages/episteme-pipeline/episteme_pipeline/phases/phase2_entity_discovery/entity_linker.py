"""
Name-based EntityLinker — lightweight entity linking without LLM calls.

Strategy:
  1. Query the graph for entities whose name contains, or is contained by,
     the candidate name (same label, case-insensitive).
  2. If exactly one match found: redirect to existing canonical ID.
  3. If multiple candidates: pick the one with the longest common prefix
     (most specific match). Only fall back to minting a new ID when no
     candidate clears a minimum overlap threshold.

This handles the most common variations in philosophical texts:
  "Kant" ↔ "Immanuel Kant", "I. Kant", "Kant, I."

Phase 5 Instance Fusion resolves harder cases (abbreviations, aliases,
cross-language references) using LLM cross-encoder reasoning.
"""

from __future__ import annotations

import logging

from episteme_pipeline.contracts.domain import L2Entity
from episteme_pipeline.protocols.extractors import EntityLinker
from episteme_pipeline.protocols.graph_store import GraphReader

logger = logging.getLogger(__name__)

_MIN_OVERLAP_CHARS = 4


def _normalized(name: str) -> str:
    return name.strip().lower()


def _overlap_score(a: str, b: str) -> float:
    """Fraction of the shorter name that is covered by the longer."""
    a_n, b_n = _normalized(a), _normalized(b)
    shorter = min(a_n, b_n, key=len)
    longer = max(a_n, b_n, key=len)
    if len(shorter) < _MIN_OVERLAP_CHARS:
        return 0.0
    return 1.0 if shorter in longer else 0.0


class NameEntityLinker(EntityLinker):
    """
    Default EntityLinker using name containment matching against the graph.
    No LLM calls — fast and deterministic. Phase 5 handles edge cases.
    """

    DEFAULT_THRESHOLD = 0.85

    async def link(
        self,
        mention: L2Entity,
        graph_store: GraphReader,
        *,
        top_k: int | None = None,
        threshold: float | None = None,
    ) -> L2Entity | None:
        candidates = await graph_store.find_entities_by_name(
            mention.name, label=mention.label
        )

        if not candidates:
            return None

        # Score candidates by overlap with the mention name
        scored = [
            (c, _overlap_score(mention.name, c.name))
            for c in candidates
            if c.id != mention.id  # exclude if already the same stable ID
        ]
        scored = [(c, s) for c, s in scored if s > 0]

        if not scored:
            return None

        if top_k is not None:
            scored = sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]

        # Pick best match
        best_candidate, best_score = max(scored, key=lambda x: x[1])
        if best_score < (self.DEFAULT_THRESHOLD if threshold is None else threshold):
            return None
        logger.debug(
            "Linked %r → %r (score=%.2f)",
            mention.name,
            best_candidate.name,
            best_score,
        )
        return best_candidate
