from abc import ABC, abstractmethod
from typing import Any, Mapping

Json = dict[str, Any] | list[Any] | None


class AsyncTransport(ABC):
    @abstractmethod
    async def get_json(
        self, path: str, *, params: Mapping[str, Any] | None = None
    ) -> Json: ...

    @abstractmethod
    async def post_json(self, path: str, *, body: Mapping[str, Any]) -> Json: ...

    @abstractmethod
    async def aclose(self) -> None: ...


class SyncTransport(ABC):
    @abstractmethod
    def get_json(
        self, path: str, *, params: Mapping[str, Any] | None = None
    ) -> Json: ...

    @abstractmethod
    def post_json(self, path: str, *, body: Mapping[str, Any]) -> Json: ...

    @abstractmethod
    def close(self) -> None: ...
