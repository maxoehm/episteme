"""Domain service orchestrating pipeline engine settings, schema customization, and predicate mapping."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from episteme_studio.adapters.engine_storage import EngineSettingsStorage, FileEngineSettingsStorage
from episteme_studio.adapters.schema_mapper import SchemaMapper
from episteme_studio.domain.engine import (
    EngineSettings,
    EngineSettingsPatch,
    PredicateMapping,
    UnmappedPredicateInfo,
)

if TYPE_CHECKING:
    from episteme_studio.adapters.artifact_reader import ArtifactReader

logger = logging.getLogger(__name__)


class EngineSettingsService:
    """Service managing persistent pipeline engine settings, ontology customization, and predicate mapping.

    Adheres to SOLID principles: Persistence is delegated to an injected EngineSettingsStorage
    data source connection adapter, while domain schema rules and unmapped predicate aggregation
    remain strictly isolated here.

    Parameters
    ----------
    storage : EngineSettingsStorage or None, optional
        Data source connection adapter. Defaults to FileEngineSettingsStorage.
    reader : ArtifactReader or None, optional
        Optional artifact reader used to discover unmapped predicates across historical runs.
    """

    def __init__(
        self,
        storage: EngineSettingsStorage | None = None,
        reader: ArtifactReader | None = None,
    ) -> None:
        self.storage: EngineSettingsStorage = storage or FileEngineSettingsStorage()
        self.reader: ArtifactReader | None = reader
        self._cached_settings: EngineSettings | None = None

    async def get_settings(self) -> EngineSettings:
        """Retrieve the current engine settings, loading from storage if not cached.

        Returns
        -------
        EngineSettings
            Active engine settings instance.
        """
        if self._cached_settings is None:
            self._cached_settings = await self.storage.load()
            if not self._cached_settings.schema_config:
                from episteme_pipeline.schema.default_schema import DEFAULT_SCHEMA

                self._cached_settings.schema_config = DEFAULT_SCHEMA.model_dump()
        return self._cached_settings

    async def update_settings(self, patch: EngineSettingsPatch) -> EngineSettings:
        """Apply partial updates to engine settings and persist to storage.

        Parameters
        ----------
        patch : EngineSettingsPatch
            Fields to update.

        Returns
        -------
        EngineSettings
            Mutated and persisted settings.
        """
        current = await self.get_settings()
        data = current.model_dump()

        if patch.schema_config is not None:
            data["schema_config"] = (
                patch.schema_config
                if isinstance(patch.schema_config, dict)
                else patch.schema_config.model_dump()
            )
        if patch.predicate_aliases is not None:
            data["predicate_aliases"] = patch.predicate_aliases
        if patch.models is not None:
            data["models"] = (
                patch.models
                if isinstance(patch.models, dict)
                else patch.models.model_dump()
            )

        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        updated = EngineSettings.model_validate(data)

        await self.storage.save(updated)
        self._cached_settings = updated
        logger.info("Successfully updated and persisted engine settings.")
        return updated

    async def reset_settings(self) -> EngineSettings:
        """Reset engine settings back to pipeline factory defaults.

        Returns
        -------
        EngineSettings
            Factory settings.
        """
        clean = await self.storage.reset()
        from episteme_pipeline.schema.default_schema import DEFAULT_SCHEMA

        clean.schema_config = DEFAULT_SCHEMA.model_dump()
        self._cached_settings = clean
        logger.info("Reset engine settings to factory defaults.")
        return clean

    async def get_schema_mapper(self) -> SchemaMapper:
        """Create a SchemaMapper bound to the active engine settings.

        Returns
        -------
        SchemaMapper
            Configured schema mapper.
        """
        settings = await self.get_settings()
        schema_dict = settings.schema_config
        schema = None
        if schema_dict:
            try:
                from episteme_pipeline.schema.default_schema import SchemaConfig

                schema = SchemaConfig.model_validate(schema_dict)
            except Exception:
                pass
        return SchemaMapper(
            schema=schema,
            predicate_aliases=settings.predicate_aliases,
        )

    async def map_predicate(self, mapping: PredicateMapping) -> EngineSettings:
        """Map an open-vocabulary predicate to a polarity and optional canonical relation.

        Parameters
        ----------
        mapping : PredicateMapping
            The predicate mapping instruction.

        Returns
        -------
        EngineSettings
            Updated engine settings with new predicate alias recorded.
        """
        settings = await self.get_settings()
        aliases = dict(settings.predicate_aliases)

        aliases[mapping.predicate] = {
            "polarity": mapping.polarity,
            "canonical": mapping.canonical,
            "definition": mapping.definition,
        }

        patch = EngineSettingsPatch(predicate_aliases=aliases)
        return await self.update_settings(patch)

    async def discover_unmapped_predicates(self) -> list[UnmappedPredicateInfo]:
        """Aggregate open-vocabulary predicates found in runs that are unmapped in the current schema.

        Returns
        -------
        list of UnmappedPredicateInfo
            Discovered unmapped predicates sorted by frequency.
        """
        if not self.reader:
            return []

        settings = await self.get_settings()
        mapper = await self.get_schema_mapper()

        schema_dict = settings.schema_config or {}
        rel_types = schema_dict.get("relation_types", [])
        arg_rel_types = schema_dict.get("argument_relation_types", [])

        known_predicates = (
            set(rel_types)
            | set(arg_rel_types)
            | set(settings.predicate_aliases.keys())
        )

        counts: dict[str, int] = {}
        sample_runs: dict[str, set[str]] = {}

        try:
            summaries = self.reader.list_runs()
            # Inspect most recent runs (up to 15) to discover unmapped predicates
            for summary in summaries[:15]:
                run_id = summary.run_id
                try:
                    graph = self.reader.get_graph(run_id, use_run_schema=False)
                    for edge in graph.edges:
                        pred = edge.type
                        if pred and pred not in known_predicates and mapper.resolve_polarity(pred) is None:
                            counts[pred] = counts.get(pred, 0) + 1
                            sample_runs.setdefault(pred, set()).add(run_id)
                except Exception:
                    continue
        except Exception as exc:
            logger.warning("Failed to collect unmapped predicates across runs: %s", exc)

        results: list[UnmappedPredicateInfo] = []
        for pred, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
            results.append(
                UnmappedPredicateInfo(
                    predicate=pred,
                    occurrences=count,
                    sample_runs=sorted(sample_runs.get(pred, set())),
                )
            )
        return results
