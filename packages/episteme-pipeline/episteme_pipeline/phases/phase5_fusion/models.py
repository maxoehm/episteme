"""Pydantic output models for Phase 5 LLM-structured predictions."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class EntitySamenessOutput(BaseModel):
    """Structured LLM output for entity identity disambiguation."""

    same_entity: bool = False
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    reasoning: str = Field(default="", description="One-sentence justification.")

    @field_validator("confidence", mode="before")
    @classmethod
    def clamp_confidence(cls, v) -> float:
        try:
            return max(0.0, min(1.0, float(v)))
        except (TypeError, ValueError):
            return 0.5
