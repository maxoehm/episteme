"""
Pydantic output models for LLM-structured prediction in Phase 3.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class GlobalRelationOutput(BaseModel):
    """Structured LLM output for a single entity-pair relation decision."""

    relation: str | None = Field(
        default=None,
        description="Relation type label, or null if no meaningful relation exists.",
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    direction: Literal["A_to_B", "B_to_A"] = Field(
        default="A_to_B",
        description="Which entity is subject (A→B) vs object (B→A).",
    )
    reasoning: str = Field(default="", description="One-sentence justification.")

    @field_validator("confidence", mode="before")
    @classmethod
    def clamp_confidence(cls, v) -> float:
        try:
            return max(0.0, min(1.0, float(v)))
        except (TypeError, ValueError):
            return 0.5
