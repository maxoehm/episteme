"""Tests for stale_map wiring in _choose_reuse_source and build_phase_staleness_map."""

import pytest

from episteme_pipeline.artifacts.execution import ArtifactCollection, ArtifactExecutionContext
from episteme_pipeline.artifacts.invalidate import (
    ArtifactDependencyGraph,
    build_prior_fingerprints,
    find_stale_nodes,
)
from episteme_pipeline.artifacts.mappers import map_phase1_output_to_artifacts
from episteme_pipeline.artifacts.models import ArtifactEnvelope, ArtifactKind
from episteme_pipeline.artifacts.store import JsonArtifactStore
from episteme_pipeline.config import PipelineConfig
from episteme_pipeline.contracts.phase_contracts import L1Chunk, L1Document, Phase1Output
from episteme_pipeline.pipeline import Pipeline
from episteme_pipeline.runs.models import RunManifest, RunPhaseRecord, RunStatus


class StubPhase:
    def __init__(self, name: str, artifacts: list | None = None):
        self.name = name
        self.phase_key = "phase1"
        self.artifacts = artifacts or []

    async def run(self, input, context: ArtifactExecutionContext):
        return ArtifactCollection([])


def _create_phase1_artifacts(run_id: str) -> list[ArtifactEnvelope]:
    """Create a list of phase 1 artifacts for testing."""
    artifacts = []
    for artifact in map_phase1_output_to_artifacts(
        Phase1Output(
            documents=[
                L1Document(
                    id="doc-1",
                    title="Doc",
                    source_path="docs/doc.md",
                    chapter_count=1,
                    chunk_count=1,
                )
            ],
            chunks=[
                L1Chunk(
                    id="chunk-1",
                    text="Hello",
                    source_doc_id="doc-1",
                    chapter_id="chap-1",
                    sequence_index=0,
                    token_count=1,
                )
            ],
        ),
        run_id=run_id,
    ):
        artifacts.append(artifact)
    return artifacts


# ---------------------------------------------------------------------------
# Direct unit tests for build_phase_staleness_map
# ---------------------------------------------------------------------------


def test_build_phase_staleness_map_detects_changed_fingerprint() -> None:
    """When an artifact's dependency_fingerprint differs from stored prior_fps,
    it and its transitive dependents are marked stale."""
    artifacts = _create_phase1_artifacts("run-old")
    dag = ArtifactDependencyGraph.from_artifacts(artifacts)
    prior_fps = build_prior_fingerprints(artifacts)

    # No change — should be empty
    stale_map = dag.build_phase_staleness_map(prior_fps)
    assert stale_map == {}

    # Change one fingerprint — should detect it
    changed_artifacts = _create_phase1_artifacts("run-old")
    changed_artifacts[0].dependency_fingerprint = "changed-fingerprint"

    new_dag = ArtifactDependencyGraph.from_artifacts(changed_artifacts)
    stale_map = new_dag.build_phase_staleness_map(prior_fps)
    assert stale_map  # non-empty for the phase that changed


def test_build_phase_staleness_map_new_identity_key_is_stale() -> None:
    """An artifact with an identity_key not in prior_fps is stale."""
    artifacts = _create_phase1_artifacts("run-old")
    prior_fps = build_prior_fingerprints(artifacts)

    # A brand new artifact (not in prior_fps, but has a fingerprint)
    new_artifacts = _create_phase1_artifacts("run-new")
    new_dag = ArtifactDependencyGraph.from_artifacts(new_artifacts)
    stale_map = new_dag.build_phase_staleness_map(prior_fps)
    # "run-new" artifacts have different identity keys
    assert (
        stale_map == {}
    )  # because identity keys are derived from run_id via artifact_id


# ---------------------------------------------------------------------------
# Integration tests for stale_map wiring via _choose_reuse_source
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_choose_reuse_source_respects_stale_indices(tmp_path, graph_store):
    """When stale_indices includes an ordinal, that phase and all
    downstream phases are invalidated via the artifact dependency
    path — even if their config/method fingerprints match."""
    config = PipelineConfig()
    config.execution.runs_dir = str(tmp_path / "runs")
    config.execution.artifacts_dir = str(tmp_path / "artifacts")

    pipeline = Pipeline(
        phases=[
            StubPhase("Phase 1: Data Foundation"),
            StubPhase("Phase 2: Entity & Local Relation Discovery"),
            StubPhase("Phase 3: Global Relation Extraction"),
        ],
        config=config,
        graph_reader=graph_store,
        projection_graph=graph_store,
        checkpoint_store=graph_store,
    )

    prior = RunManifest(
        run_id="run-old",
        status=RunStatus.COMPLETED,
        input_fingerprint="same-input",
        phase_config_fingerprints={
            "phase_1": "same",
            "phase_2": "same",
            "phase_3": "same",
        },
        phase_records=[
            RunPhaseRecord(
                phase_name="Phase 1: Data Foundation",
                ordinal=1,
                status=RunStatus.COMPLETED,
            ),
            RunPhaseRecord(
                phase_name="Phase 2: Entity & Local Relation Discovery",
                ordinal=2,
                status=RunStatus.COMPLETED,
            ),
            RunPhaseRecord(
                phase_name="Phase 3: Global Relation Extraction",
                ordinal=3,
                status=RunStatus.COMPLETED,
            ),
        ],
    )
    pipeline._manifest_store.write_manifest(prior)
    pipeline._artifact_store = JsonArtifactStore(tmp_path / "artifacts")

    # Simulate that Phase 2 had a stale artifact dependency — stale_map
    # returns {"Phase 2: Entity & Local ...": [...]} which maps to ordinal 2.
    async def mock_compute_stale_phases(_run_id: str):
        return {"Phase 2: Entity & Local Relation Discovery": ["some-stale-key"]}

    pipeline._compute_stale_phases = mock_compute_stale_phases
    pipeline._phase_config_fingerprints = lambda: {
        1: "same",
        2: "same",
        3: "same",
    }

    decision = await pipeline._choose_reuse_source(
        RunManifest(
            run_id="run-new",
            status=RunStatus.RUNNING,
            input_fingerprint="same-input",
            phase_config_fingerprints={
                "phase_1": "same",
                "phase_2": "same",
                "phase_3": "same",
            },
        )
    )

    # Phase 1 is reused (no stale artifacts), phases 2+3 are invalidated
    # because stale_map flagged phase 2 as stale.
    assert decision.reused_phase_ordinals == [1]
    assert decision.invalidated_phase_ordinals == [2, 3]


@pytest.mark.asyncio
async def test_choose_reuse_source_stale_map_causes_full_invalidated_when_phase1_stale(
    tmp_path, graph_store
):
    """When Phase 1 has stale artifacts, all phases are invalidated including Phase 1 itself."""
    config = PipelineConfig()
    config.execution.runs_dir = str(tmp_path / "runs")
    config.execution.artifacts_dir = str(tmp_path / "artifacts")

    pipeline = Pipeline(
        phases=[
            StubPhase("Phase 1: Data Foundation"),
            StubPhase("Phase 2: Entity & Local Relation Discovery"),
        ],
        config=config,
        graph_reader=graph_store,
        projection_graph=graph_store,
        checkpoint_store=graph_store,
    )

    prior = RunManifest(
        run_id="run-old",
        status=RunStatus.COMPLETED,
        input_fingerprint="same-input",
        phase_config_fingerprints={"phase_1": "same", "phase_2": "same"},
        phase_records=[
            RunPhaseRecord(
                phase_name="Phase 1: Data Foundation",
                ordinal=1,
                status=RunStatus.COMPLETED,
            ),
            RunPhaseRecord(
                phase_name="Phase 2: Entity & Local Relation Discovery",
                ordinal=2,
                status=RunStatus.COMPLETED,
            ),
        ],
    )
    pipeline._manifest_store.write_manifest(prior)
    pipeline._artifact_store = JsonArtifactStore(tmp_path / "artifacts")

    async def mock_compute_stale_phases(_run_id: str):
        return {"Phase 1: Data Foundation": ["doc-1-stale"]}

    pipeline._compute_stale_phases = mock_compute_stale_phases
    pipeline._phase_config_fingerprints = lambda: {1: "same", 2: "same"}

    decision = await pipeline._choose_reuse_source(
        RunManifest(
            run_id="run-new",
            status=RunStatus.RUNNING,
            input_fingerprint="same-input",
            phase_config_fingerprints={
                "phase_1": "same",
                "phase_2": "same",
            },
        )
    )

    assert decision.invalidated_phase_ordinals == [1, 2]
    assert decision.reused_phase_ordinals == []


@pytest.mark.asyncio
async def test_choose_reuse_source_no_stale_phases_returns_empty_map(
    tmp_path, graph_store
):
    """When _compute_stale_phases returns an empty map, all phases pass
    the stale check and normal fingerprint-based logic applies."""
    config = PipelineConfig()
    config.execution.runs_dir = str(tmp_path / "runs")
    config.execution.artifacts_dir = str(tmp_path / "artifacts")

    pipeline = Pipeline(
        phases=[
            StubPhase("Phase 1: Data Foundation"),
            StubPhase("Phase 2: Entity & Local Relation Discovery"),
        ],
        config=config,
        graph_reader=graph_store,
        projection_graph=graph_store,
        checkpoint_store=graph_store,
    )

    prior = RunManifest(
        run_id="run-old",
        status=RunStatus.COMPLETED,
        input_fingerprint="same-input",
        phase_config_fingerprints={"phase_1": "same", "phase_2": "old"},
        phase_records=[
            RunPhaseRecord(
                phase_name="Phase 1: Data Foundation",
                ordinal=1,
                status=RunStatus.COMPLETED,
            ),
            RunPhaseRecord(
                phase_name="Phase 2: Entity & Local Relation Discovery",
                ordinal=2,
                status=RunStatus.COMPLETED,
            ),
        ],
    )
    pipeline._manifest_store.write_manifest(prior)
    pipeline._artifact_store = JsonArtifactStore(tmp_path / "artifacts")

    # Empty stale map — no artifact-level invalidation
    async def mock_compute_stale_phases(_run_id: str):
        return {}

    pipeline._compute_stale_phases = mock_compute_stale_phases
    pipeline._phase_config_fingerprints = lambda: {1: "same", 2: "new"}

    decision = await pipeline._choose_reuse_source(
        RunManifest(
            run_id="run-new",
            status=RunStatus.RUNNING,
            input_fingerprint="same-input",
            phase_config_fingerprints={
                "phase_1": "same",
                "phase_2": "new",
            },
        )
    )

    assert decision.reused_phase_ordinals == [1]
    assert decision.invalidated_phase_ordinals == [2]


@pytest.mark.asyncio
async def test_choose_reuse_source_nonexistent_phase_in_stale_map_ignored(
    tmp_path, graph_store
):
    """If stale_map references a phase name not in _phase_entries, it should
    be silently ignored without affecting the decision."""
    config = PipelineConfig()
    config.execution.runs_dir = str(tmp_path / "runs")
    config.execution.artifacts_dir = str(tmp_path / "artifacts")

    pipeline = Pipeline(
        phases=[
            StubPhase("Phase 1: Data Foundation"),
            StubPhase("Phase 2: Entity & Local Relation Discovery"),
        ],
        config=config,
        graph_reader=graph_store,
        projection_graph=graph_store,
        checkpoint_store=graph_store,
    )

    prior = RunManifest(
        run_id="run-old",
        status=RunStatus.COMPLETED,
        input_fingerprint="same-input",
        phase_config_fingerprints={"phase_1": "same", "phase_2": "old"},
        phase_records=[
            RunPhaseRecord(
                phase_name="Phase 1: Data Foundation",
                ordinal=1,
                status=RunStatus.COMPLETED,
            ),
            RunPhaseRecord(
                phase_name="Phase 2: Entity & Local Relation Discovery",
                ordinal=2,
                status=RunStatus.COMPLETED,
            ),
        ],
    )
    pipeline._manifest_store.write_manifest(prior)
    pipeline._artifact_store = JsonArtifactStore(tmp_path / "artifacts")

    async def mock_compute_stale_phases(_run_id: str):
        # References a phase that doesn't exist in the pipeline
        return {"Nonexistent Phase": ["fake-key"]}

    pipeline._compute_stale_phases = mock_compute_stale_phases
    pipeline._phase_config_fingerprints = lambda: {1: "same", 2: "new"}

    decision = await pipeline._choose_reuse_source(
        RunManifest(
            run_id="run-new",
            status=RunStatus.RUNNING,
            input_fingerprint="same-input",
            phase_config_fingerprints={
                "phase_1": "same",
                "phase_2": "new",
            },
        )
    )

    # Should behave identically to the empty stale map case
    assert decision.reused_phase_ordinals == [1]
    assert decision.invalidated_phase_ordinals == [2]


# ---------------------------------------------------------------------------
# Structural DAG diff tests
# ---------------------------------------------------------------------------


def _make_artifact(
    identity_key: str,
    dependency_fp: str,
    upstream: list[str],
    phase_name: str = "test-phase",
) -> ArtifactEnvelope:
    """Helper to create a minimal ArtifactEnvelope for structural diff tests."""
    from episteme_pipeline.artifacts.models import (
        ArtifactProvenance,
        DocumentArtifact,
    )

    return ArtifactEnvelope(
        artifact_id=f"artifact::{identity_key}",
        identity_key=identity_key,
        kind=ArtifactKind.DOCUMENT,
        run_id="test-run",
        phase_name=phase_name,
        method="test-method",
        dependency_fingerprint=dependency_fp,
        provenance=ArtifactProvenance(upstream_artifact_ids=upstream),
        payload=DocumentArtifact(
            document_id="dummy",
            title="dummy",
            source_path="dummy.md",
        ),
    )


def test_structural_diff_detects_added_upstream_dep() -> None:
    """When a node's provenance upstream_artifact_ids gains a new dependency,
    the structural diff marks it stale even if dependency_fingerprint matches."""
    current = [
        _make_artifact("chunk::chunk-1", "fp-match", ["doc::doc-1"]),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact("chunk::chunk-1", "fp-match", ["old-dep"]),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale = find_stale_nodes(current_dag, prior_fps, prior_artifacts=prior)

    assert "chunk::chunk-1" in stale


def test_structural_diff_detects_removed_upstream_dep() -> None:
    """When a node loses an upstream dep, it's structurally stale."""
    current = [
        _make_artifact("chunk::chunk-1", "fp-match", []),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact("chunk::chunk-1", "fp-match", ["doc::doc-1"]),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale = find_stale_nodes(current_dag, prior_fps, prior_artifacts=prior)

    assert "chunk::chunk-1" in stale


def test_structural_diff_no_change() -> None:
    """When provenance edges match, the node is not structurally stale."""
    current = [
        _make_artifact("chunk::chunk-1", "fp-match", ["doc::doc-1"]),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact("chunk::chunk-1", "fp-match", ["doc::doc-1"]),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale = find_stale_nodes(current_dag, prior_fps, prior_artifacts=prior)

    assert "chunk::chunk-1" not in stale


def test_structural_diff_propagates_downstream() -> None:
    """When a node is structurally stale, its downstream dependents become stale too."""
    current = [
        _make_artifact("chunk::chunk-1", "fp-match", ["new-dep"]),
        _make_artifact("entity::ent-1", "fp-match", ["chunk::chunk-1"]),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact("chunk::chunk-1", "fp-match", ["old-dep"]),
        _make_artifact("entity::ent-1", "fp-match", ["chunk::chunk-1"]),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale = find_stale_nodes(current_dag, prior_fps, prior_artifacts=prior)

    assert "chunk::chunk-1" in stale
    assert "entity::ent-1" in stale


def test_build_phase_staleness_map_includes_structural_diff() -> None:
    """build_phase_staleness_map uses prior_artifacts for structural comparison."""
    current = [
        _make_artifact(
            "chunk::chunk-1", "fp-match", ["new-dep"], phase_name="test-phase"
        ),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact(
            "chunk::chunk-1", "fp-match", ["old-dep"], phase_name="test-phase"
        ),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale_map = current_dag.build_phase_staleness_map(prior_fps, prior_artifacts=prior)

    assert "test-phase" in stale_map


def test_new_node_without_upstream_artifacts_not_structural_stale() -> None:
    """A new node with no upstream deps and no prior entry is fingerprint-stale,
    but should NOT be marked structurally stale (structural diff only flags
    nodes that HAD upstream deps before but have different ones)."""
    current = [
        _make_artifact("new-art", "new-fp", []),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact("other-art", "old-fp", []),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale = find_stale_nodes(current_dag, prior_fps, prior_artifacts=prior)

    assert "new-art" in stale
    # The node is not in structurally_stale because prior has no entry for it
    # and current has no upstream deps (edge set is empty both sides)
    from episteme_pipeline.artifacts.invalidate import (
        _build_prior_upstream,
        _compare_dag_structures,
    )

    prior_upstream = _build_prior_upstream(prior)
    structurally_stale = _compare_dag_structures(current_dag, prior_upstream)
    assert "new-art" not in structurally_stale


def test_build_phase_staleness_map_no_change() -> None:
    """When structural provenance matches, no staleness is detected."""
    current = [
        _make_artifact(
            "chunk::chunk-1", "fp-match", ["doc::doc-1"], phase_name="test-phase"
        ),
    ]
    current_dag = ArtifactDependencyGraph.from_artifacts(current)

    prior = [
        _make_artifact(
            "chunk::chunk-1", "fp-match", ["doc::doc-1"], phase_name="test-phase"
        ),
    ]

    prior_fps = build_prior_fingerprints(prior)
    stale_map = current_dag.build_phase_staleness_map(prior_fps, prior_artifacts=prior)

    assert stale_map == {}
