"""Run-scoped artifact models for the target research-library architecture.

These models intentionally do not replace the current domain models yet.
They provide a first architecture-facing scaffold for the artifact/run model
described in `docs/architecture/artifact_run_model.md` and `docs/architecture/overview.md`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field, model_validator

from episteme_pipeline.contracts.domain import GlobalStructuralAnchor


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ArtifactKind(StrEnum):
    DOCUMENT = "document"
    CHUNK = "chunk"
    ENTITY_MENTION = "entity_mention"
    LINKED_ENTITY = "linked_entity"
    LOCAL_RELATION = "local_relation"
    GLOBAL_RELATION = "global_relation"
    THEORY_ATOM = "theory_atom"
    THEORY_RELATION = "theory_relation"
    FUSION_DECISION = "fusion_decision"
    CANONICALIZATION = "canonicalization"
    THEORETICAL_ENRICHMENT = "theoretical_enrichment"


class ArtifactRef(BaseModel):
    artifact_id: str
    kind: ArtifactKind
    run_id: str
    phase_name: str


class ArtifactProvenance(BaseModel):
    source_path: str | None = None
    source_document_id: str | None = None
    source_chunk_id: str | None = None
    upstream_artifact_ids: list[str] = Field(default_factory=list)
    notes: dict[str, str] = Field(default_factory=dict)


class DocumentArtifact(BaseModel):
    document_id: str
    title: str
    source_path: str
    structural_anchor: GlobalStructuralAnchor | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    ingested_at: datetime = Field(default_factory=utc_now)


class ChunkArtifact(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    sequence_index: int
    chapter_id: str | None = None
    token_count: int


class EntityMentionArtifact(BaseModel):
    mention_id: str
    chunk_id: str
    surface_form: str
    entity_type: str
    start_char: int | None = None
    end_char: int | None = None
    confidence: float | None = None


class LinkedEntityArtifact(BaseModel):
    entity_id: str
    canonical_name: str
    entity_type: str
    mention_ids: list[str] = Field(default_factory=list)
    description: str | None = None
    textual_envelope: str | None = None
    is_mature: bool = False
    confidence: float | None = None


class LocalRelationArtifact(BaseModel):
    relation_id: str
    subject_entity_id: str
    predicate: str
    object_entity_id: str
    source_chunk_id: str
    confidence: float
    scope: Literal["local"] = "local"


class GlobalRelationArtifact(BaseModel):
    relation_id: str
    subject_entity_id: str
    predicate: str
    object_entity_id: str
    supporting_chunk_ids: list[str] = Field(default_factory=list)
    confidence: float
    rerank_score: float | None = None
    scope: Literal["global"] = "global"


class FusionDecisionArtifact(BaseModel):
    decision_id: str
    artifact_ids: list[str] = Field(default_factory=list)
    decision_type: Literal["merge", "keep_separate", "cluster"]
    rationale: str | None = None
    confidence: float | None = None


class CanonicalizationArtifact(BaseModel):
    canonical_id: str
    original_artifact_ids: list[str] = Field(default_factory=list)
    canonical_label: str
    canonical_type: str


class TheoryAtomArtifact(BaseModel):
    component_id: str
    chunk_id: str
    text: str
    component_type: str
    confidence: float | None = None
    plausibility: float | None = None
    epistemic_status: str | None = None
    scope_type: str | None = None


class TheoryRelationArtifact(BaseModel):
    relation_id: str
    source_component_id: str
    target_component_id: str
    relation_type: str
    scope: str
    confidence: float
    weight: float | None = None


class TheoreticalEnrichmentArtifact(BaseModel):
    enrichment_id: str
    cluster_id: str
    theory_id: str
    projected_parameters: dict[str, Any] = Field(default_factory=dict)
    local_tenability: float
    edge_tenabilities: dict[str, float] = Field(default_factory=dict)
    aggregated_tenability: float
    admissible_blur_delta: float
    is_tenable: bool
    anomalies: list[str] = Field(default_factory=list)


ArtifactPayload = (
    DocumentArtifact
    | ChunkArtifact
    | EntityMentionArtifact
    | LinkedEntityArtifact
    | LocalRelationArtifact
    | GlobalRelationArtifact
    | TheoryAtomArtifact
    | TheoryRelationArtifact
    | FusionDecisionArtifact
    | CanonicalizationArtifact
    | TheoreticalEnrichmentArtifact
)

ArtifactPayloadT = TypeVar("ArtifactPayloadT", bound=ArtifactPayload)


class ArtifactEnvelope(BaseModel, Generic[ArtifactPayloadT]):
    artifact_id: str
    identity_key: str | None = None
    kind: ArtifactKind
    run_id: str
    phase_name: str
    method: str
    method_version: str = "v1"
    config_fingerprint: str | None = None
    dependency_fingerprint: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    provenance: ArtifactProvenance = Field(default_factory=ArtifactProvenance)
    payload: ArtifactPayloadT
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def populate_identity_key(self):
        if self.identity_key is None:
            self.identity_key = self.artifact_id
        return self

    def ref(self) -> ArtifactRef:
        return ArtifactRef(
            artifact_id=self.artifact_id,
            kind=self.kind,
            run_id=self.run_id,
            phase_name=self.phase_name,
        )
