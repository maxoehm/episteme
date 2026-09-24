"""Domain models for engine settings, schema customization, and predicate mapping.

Per D-01, domain models must remain strictly decoupled from episteme_pipeline.* and epistemetrics.*.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, Field


class PredicateMapping(BaseModel):
    """Specification for mapping an open-vocabulary predicate to schema rules.

    Parameters
    ----------
    predicate : str
        The raw predicate label extracted from literature (e.g. 'WIDERSPRICHT').
    polarity : Literal[-1, 0, 1]
        Argumentative charge: +1 (support), 0 (neutral), or -1 (attack/refute).
    canonical : str or None, optional
        Optional canonical schema relation target (e.g. 'ATTACKS' or 'SUPPORTS').
    definition : str or None, optional
        Optional prompt guidance or semantic description for this predicate.
    """

    predicate: str
    polarity: Literal[-1, 0, 1]
    canonical: str | None = None
    definition: str | None = None


class UnmappedPredicateInfo(BaseModel):
    """Telemetry report describing an open-vocabulary predicate discovered in runs.

    Parameters
    ----------
    predicate : str
        The unresolved predicate string.
    occurrences : int
        Number of times this predicate appeared across runs or graphs.
    sample_runs : list of str, default []
        IDs of runs where this predicate was observed.
    """

    predicate: str
    occurrences: int = 1
    sample_runs: list[str] = Field(default_factory=list)


class EngineModelConfig(BaseModel):
    """Domain model representing baseline LLM, embedding, and reranker choices.

    Parameters
    ----------
    llm_model : str, default 'openai/gpt-4o-mini'
        Identifier of the primary reasoning model.
    embedding_model : str, default 'sentence-transformers/all-MiniLM-L6-v2'
        Dense vector embedding model.
    reranker_model : str, default 'Alibaba-NLP/gte-reranker-modernbert-base'
        Cross-encoder reranker model.
    temperature : float, default 0.0
        Generation temperature.
    seed : int or None, optional
        Random seed.
    llm_api_base : str or None, optional
        Custom OpenAI-compatible API base URL.
    thinking_level : str, default 'off'
        Reasoning thinking token budget preset.
    """

    llm_model: str = "openai/gpt-4o-mini"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "Alibaba-NLP/gte-reranker-modernbert-base"
    temperature: float = 0.0
    seed: int | None = None
    llm_api_base: str | None = None
    thinking_level: str = "off"


class EngineSettings(BaseModel):
    """System-level engine settings governing pipeline execution and visualization.

    Parameters
    ----------
    schema_config : dict of str to Any
        The active pipeline ontology serialized dictionary.
    predicate_aliases : dict of str to Any, default {}
        Open-vocabulary predicate mappings (e.g. {'WIDERSPRICHT': {'polarity': -1, 'canonical': 'ATTACKS'}}).
    models : EngineModelConfig
        Default language model, embedding model, and reasoning thinking level presets.
    updated_at : str or None, optional
        ISO 8601 timestamp of last mutation.
    """

    schema_config: dict[str, Any] = Field(default_factory=dict)
    predicate_aliases: dict[str, Any] = Field(default_factory=dict)
    models: EngineModelConfig = Field(default_factory=EngineModelConfig)
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EngineSettingsPatch(BaseModel):
    """Partial update payload for engine settings.

    Parameters
    ----------
    schema_config : dict of str to Any or None, optional
        Updated ontology schema dictionary.
    predicate_aliases : dict of str to Any or None, optional
        Updated predicate alias map.
    models : EngineModelConfig or None, optional
        Updated default model configuration.
    """

    schema_config: dict[str, Any] | None = None
    predicate_aliases: dict[str, Any] | None = None
    models: EngineModelConfig | None = None
