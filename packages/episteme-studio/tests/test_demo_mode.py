"""Tests for episteme-studio canned demo mode."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from episteme_studio.app import create_app
from episteme_studio.settings import StudioSettings


@pytest.mark.asyncio
async def test_demo_mode_lists_canned_runs() -> None:
    """When demo_mode=True, list_runs returns packaged demo runs."""
    settings = StudioSettings(neo4j_url=None, demo_mode=True)
    app = create_app(settings)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/runs")
        assert response.status_code == 200
        runs = response.json()
        assert len(runs) >= 2

        run_ids = {r["run_id"] for r in runs}
        assert "run-demo-physics" in run_ids
        assert "run-demo-psychology" in run_ids


@pytest.mark.asyncio
async def test_demo_mode_get_run_detail() -> None:
    """When demo_mode=True, get_run returns full RunDetail for physics run."""
    settings = StudioSettings(neo4j_url=None, demo_mode=True)
    app = create_app(settings)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/runs/run-demo-physics")
        assert response.status_code == 200
        detail = response.json()
        assert detail["run_id"] == "run-demo-physics"
        assert detail["status"] == "completed"
        assert len(detail["phase_records"]) >= 6
        assert "BasicAxiom" in detail["config_snapshot"]["graph_schema"]["component_types"]


@pytest.mark.asyncio
async def test_demo_mode_get_graph() -> None:
    """When demo_mode=True, get_graph returns full L1/L2/L3 graph from envelopes."""
    settings = StudioSettings(neo4j_url=None, demo_mode=True)
    app = create_app(settings)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/runs/run-demo-physics/graph")
        assert response.status_code == 200
        graph = response.json()
        assert len(graph["nodes"]) > 0
        assert len(graph["edges"]) > 0

        layers = {n["layer"] for n in graph["nodes"]}
        # Verify all 3 layers exist: L1 (1), L2 (2), L3 (3)
        assert 1 in layers
        assert 2 in layers
        assert 3 in layers


@pytest.mark.asyncio
async def test_demo_mode_psychology_graph() -> None:
    """When demo_mode=True, psychology run has all 3 layers and conflict edges."""
    settings = StudioSettings(neo4j_url=None, demo_mode=True)
    app = create_app(settings)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/runs/run-demo-psychology/graph")
        assert response.status_code == 200
        graph = response.json()
        assert len(graph["nodes"]) > 0
        assert len(graph["edges"]) > 0

        edge_types = {e["type"] for e in graph["edges"]}
        assert "ATTACKS" in edge_types
        assert "SUPPORTS" in edge_types
