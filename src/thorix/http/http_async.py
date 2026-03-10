import logging
from typing import Any, Mapping

import httpx

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPInvalidResponseError

from .retry import retry_async
from .transport import AsyncTransport, Json

logger = logging.getLogger(__name__)


class AsyncHttpTransport(AsyncTransport):
    """
    Asynchronous HTTP transport
    """

    def __init__(
        self, base_url: str, config: HTTPConfig, client: httpx.AsyncClient | None = None
    ) -> None:
        self._client = client or httpx.AsyncClient(base_url=base_url)
        self._config = config

    async def get_json(
        self, path: str, *, params: Mapping[str, Any] | None = None
    ) -> Json:
        """
        Perform a GET request with retry, returning parsed JSON
        """
        logger.debug("GET %s params=%s", path, params)

        async def _do() -> Json:
            r = await self._client.get(path, params=params)
            r.raise_for_status()
            try:
                return r.json()
            except ValueError as exc:
                raise ThorixHTTPInvalidResponseError(
                    "Invalid JSON response from Thor node"
                ) from exc

        return await retry_async(_do, self._config)

    async def post_json(self, path: str, *, body: Mapping[str, Any]) -> Json:
        """
        Perform a POST request with retry, returning parsed JSON
        """
        logger.debug("POST %s payload=%s", path, body)

        async def _do() -> Json:
            r = await self._client.post(path, json=body)
            r.raise_for_status()
            try:
                return r.json()
            except ValueError as exc:
                raise ThorixHTTPInvalidResponseError(
                    "Invalid JSON response from Thor node"
                ) from exc

        return await retry_async(_do, self._config)

    async def aclose(self) -> None:
        """
        Closes the httpx client
        """
        await self._client.aclose()
