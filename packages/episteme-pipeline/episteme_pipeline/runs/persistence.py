"""Minimal run manifest persistence helpers."""

from __future__ import annotations

import json
from pathlib import Path

from episteme_pipeline.runs.models import RunManifest, RunStatus


class JsonRunManifestStore:
    """One JSON file per run under ``root_dir``.

    Reads are memoised on (path, mtime_ns, size) because ``latest_manifest`` is
    called several times per run and each call otherwise re-reads and
    re-validates every manifest on disk (O-16). A manifest rewritten in place
    invalidates its own entry.
    """

    def __init__(self, root_dir: str | Path) -> None:
        self.root_dir = Path(root_dir)
        # Create runs directory eagerly so code that expects its presence
        # (and tests that assert it) behaves deterministically.
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[Path, tuple[tuple[int, int], RunManifest]] = {}

    def _load(self, path: Path) -> RunManifest | None:
        try:
            stat = path.stat()
        except OSError:
            self._cache.pop(path, None)
            return None
        stamp = (stat.st_mtime_ns, stat.st_size)
        cached = self._cache.get(path)
        if cached is not None and cached[0] == stamp:
            return cached[1]
        manifest = RunManifest.model_validate_json(path.read_text(encoding="utf-8"))
        self._cache[path] = (stamp, manifest)
        return manifest

    def write_manifest(self, manifest: RunManifest) -> Path:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        path = self.root_dir / f"{manifest.run_id}.json"
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(
            json.dumps(manifest.model_dump(mode="json"), indent=2),
            encoding="utf-8",
        )
        tmp.replace(path)
        self._cache.pop(path, None)
        return path

    def read_manifest(self, run_id: str) -> RunManifest | None:
        return self._load(self.root_dir / f"{run_id}.json")

    def list_manifests(self) -> list[RunManifest]:
        manifests: list[RunManifest] = []
        for path in sorted(self.root_dir.glob("*.json")):
            manifest = self._load(path)
            if manifest is not None:
                manifests.append(manifest)
        return manifests

    def latest_manifest(self, *, only_completed: bool = True) -> RunManifest | None:
        """The most recent run, by default the most recent **completed** one.

        A crashed run leaves a ``RUNNING`` manifest on disk that is newer than
        the last good one. Returning it made it the next run's reuse parent, so
        the next run copied phase records from a run that never finished and
        hydrated from its partial artifacts (O-04). Pass
        ``only_completed=False`` to inspect the true latest, crashes included.
        """
        manifests = self.list_manifests()
        if only_completed:
            manifests = [m for m in manifests if m.status == RunStatus.COMPLETED]
        if not manifests:
            return None
        manifests.sort(key=lambda manifest: manifest.created_at)
        return manifests[-1]
