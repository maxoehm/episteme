from abc import ABC, abstractmethod

from episteme_pipeline.artifacts.models import ArtifactEnvelope, ArtifactPayload


class GraphProjectionProtocol(ABC):
    """Projects durable artifacts into the graph representation."""

    @abstractmethod
    async def project(self, artifact: ArtifactEnvelope[ArtifactPayload]) -> None: ...
