"""
LLMADUSegmenter — default ADUSegmenter implementation.

Uses LlamaIndex astructured_predict to identify Argumentative Discourse Units
and wrap them in <ACn>...</ACn> markup tags. On parsing failure the segmenter
returns (chunk_text, []) — no ADUs found — and logs a warning.
The chunk is still marked as processed to avoid infinite retry of non-argumentative
chunks (e.g. bibliography sections, tables of contents).
"""

from __future__ import annotations

import logging

from llama_index.core import PromptTemplate

from episteme_pipeline.llm import ensure_structured_llm
from episteme_pipeline.phases.phase4_argument_mining.models import ADUSegmentationOutput
from episteme_pipeline.protocols.argument_mining import ADUSegmenter

logger = logging.getLogger(__name__)


class LLMADUSegmenter(ADUSegmenter):
    """
    Default ADUSegmenter using LlamaIndex LLM structured prediction.
    Accepts any LlamaIndex BaseLLM.
    """

    def __init__(self, llm, prompt_template: str) -> None:
        self.llm = ensure_structured_llm(llm)
        self.prompt_template = prompt_template

    async def segment(
        self,
        chunk_id: str,
        chunk_text: str,
    ) -> tuple[str, list[str]]:
        prompt = PromptTemplate(self.prompt_template)

        try:
            raw: ADUSegmentationOutput = await self.llm.predict_structured(
                ADUSegmentationOutput,
                prompt,
                chunk_text=chunk_text,
            )
        except Exception as exc:
            logger.warning(
                "ADU segmentation failed for chunk %s: %s", chunk_id, exc
            )
            return chunk_text, []

        if not raw.adu_ids:
            logger.debug("No ADUs found in chunk %s", chunk_id)
            return chunk_text, []

        return raw.tagged_text, raw.adu_ids
