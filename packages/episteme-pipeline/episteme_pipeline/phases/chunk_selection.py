"""Shared work-list selection for the chunk-processing phases (F-07).

Phase 2 (entity discovery) and Phase 4 (argument mining) answer the same
question — *which chunks does this phase still owe work on?* — and both had
their own copy of the answer. The copies diverged: Phase 4's treated **every**
chunk in the graph as already processed, so once Phase 1 had written anything
the fallback always produced an empty work list and the phase returned
immediately. One implementation, used by both.
"""

from __future__ import annotations

from collections.abc import Sequence

from episteme_pipeline.contracts.domain import L1Chunk
from episteme_pipeline.protocols.graph_store import ProcessingGraph


async def select_pending_chunks(
    graph_store: ProcessingGraph,
    phase_tag: str,
    view_chunks: Sequence[L1Chunk],
) -> list[L1Chunk]:
    """Return the chunks ``phase_tag`` still has to process.

    The graph is the authority: ``get_unprocessed_chunks`` returns chunks whose
    ``{phase_tag}_processed`` flag is unset. When it comes back empty that is
    ambiguous — either the phase is genuinely done, or the chunks live only in
    the artifact stream because nothing projected them into the graph. So the
    fallback subtracts the chunks the graph *does* record as processed from the
    incoming artifact view; whatever remains is real, unprocessed work.

    Subtracting all graph chunks instead of just the processed ones (Phase 4's
    old behaviour) is the bug this helper exists to prevent: it makes the
    fallback unconditionally empty.

    Parameters
    ----------
    graph_store
        Read + checkpoint surface for the current run.
    phase_tag
        The phase's checkpoint tag, e.g. ``"phase2"``. The graph property is
        ``{phase_tag}_processed``.
    view_chunks
        Chunks carried by the incoming artifact view.
    """
    pending = await graph_store.get_unprocessed_chunks(phase_tag)
    if pending:
        return pending

    processed = await graph_store.get_chunks(
        filters={f"{phase_tag}_processed": True}
    )
    processed_ids = {chunk.id for chunk in processed}
    return [chunk for chunk in view_chunks if chunk.id not in processed_ids]


__all__ = ["select_pending_chunks"]
