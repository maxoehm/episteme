"""Artifact domain models for durable, run-scoped pipeline outputs."""

from episteme_pipeline.artifacts.models import (
    ArtifactEnvelope,
    ArtifactKind,
    ArtifactProvenance,
    ArtifactRef,
    TheoryAtomArtifact,
    TheoryRelationArtifact,
    CanonicalizationArtifact,
    ChunkArtifact,
    DocumentArtifact,
    EntityMentionArtifact,
    FusionDecisionArtifact,
    GlobalRelationArtifact,
    LinkedEntityArtifact,
    LocalRelationArtifact,
)

__all__ = [
    "ArtifactEnvelope",
    "ArtifactKind",
    "ArtifactProvenance",
    "ArtifactRef",
    "TheoryAtomArtifact",
    "TheoryRelationArtifact",
    "CanonicalizationArtifact",
    "ChunkArtifact",
    "DocumentArtifact",
    "EntityMentionArtifact",
    "FusionDecisionArtifact",
    "GlobalRelationArtifact",
    "LinkedEntityArtifact",
    "LocalRelationArtifact",
]
from episteme_pipeline.artifacts.mappers import (
    map_phase1_output_to_artifacts,
    map_phase2_output_to_artifacts,
    map_phase3_output_to_artifacts,
    map_phase4_output_to_artifacts,
)

__all__ = [
    "map_phase1_output_to_artifacts",
    "map_phase2_output_to_artifacts",
    "map_phase3_output_to_artifacts",
    "map_phase4_output_to_artifacts",
]
