from episteme_pipeline.artifacts.models import (
    ArtifactEnvelope,
    ArtifactKind,
    ArtifactProvenance,
    ChunkArtifact,
)
from episteme_pipeline.runs.models import RunManifest, RunPhaseRecord, RunStatus


def test_artifact_envelope_captures_run_scope_and_payload() -> None:
    payload = ChunkArtifact(
        chunk_id="chunk-1",
        document_id="doc-1",
        text="Example text.",
        sequence_index=0,
        token_count=3,
    )

    artifact = ArtifactEnvelope(
        artifact_id="artifact-1",
        identity_key="chunk::chunk-1",
        kind=ArtifactKind.CHUNK,
        run_id="run-1",
        phase_name="phase1_foundation",
        method="chunker.default",
        provenance=ArtifactProvenance(source_path="docs/example.md"),
        payload=payload,
    )

    assert artifact.run_id == "run-1"
    assert artifact.kind == ArtifactKind.CHUNK
    assert artifact.payload.chunk_id == "chunk-1"
    assert artifact.provenance.source_path == "docs/example.md"


def test_run_manifest_tracks_phase_records() -> None:
    manifest = RunManifest(
        run_id="run-1",
        status=RunStatus.RUNNING,
        input_sources=["docs/example.md"],
        phase_records=[
            RunPhaseRecord(
                phase_name="phase1_foundation",
                ordinal=1,
                status=RunStatus.COMPLETED,
                output_artifact_ids=["artifact-1"],
            )
        ],
    )

    assert manifest.run_id == "run-1"
    assert manifest.phase_records[0].status == RunStatus.COMPLETED
    assert manifest.phase_records[0].output_artifact_ids == ["artifact-1"]
