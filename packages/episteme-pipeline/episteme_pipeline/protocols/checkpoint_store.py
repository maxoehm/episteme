from abc import ABC, abstractmethod


class CheckpointStoreProtocol(ABC):
    """Execution checkpoint tracking, separate from graph persistence."""

    @abstractmethod
    async def mark_processed(self, item_id: str, stage: str) -> None: ...

    @abstractmethod
    async def is_processed(self, item_id: str, stage: str) -> bool: ...

    @abstractmethod
    async def get_unprocessed_ids(self, stage: str) -> list[str]: ...
