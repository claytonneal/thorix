import logging
from typing import Any, Mapping

import httpx

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPInvalidResponseError

from .retry import retry_sync
from .transport import Json, SyncTransport

logger = logging.getLogger(__name__)


class HttpTransport(SyncTransport):
    """
    Synchronous HTTP transport
    """

    def __init__(
        self, base_url: str, config: HTTPConfig, client: httpx.Client | None = None
    ) -> None:
        self._client = client or httpx.Client(base_url=base_url)
        self._config = config

    def get_json(self, path: str, *, params: Mapping[str, Any] | None = None) -> Json:
        """
        Perform a GET request with retry, returning parsed JSON
        """
        logger.debug("GET %s params=%s", path, params)

        def _do() -> Json:
            r = self._client.get(path, params=params)
            r.raise_for_status()
            try:
                return r.json()
            except ValueError as exc:
                raise ThorixHTTPInvalidResponseError(
                    "Invalid JSON response from Thor node"
                ) from exc

        return retry_sync(_do, self._config)

    def post_json(self, path: str, *, body: Mapping[str, Any]) -> Json:
        """
        Perform a POST request with retry, returning parsed JSON
        """
        logger.debug("POST %s payload=%s", path, body)

        def _do() -> Json:
            r = self._client.post(path, json=body)
            r.raise_for_status()
            try:
                return r.json()
            except ValueError as exc:
                raise ThorixHTTPInvalidResponseError(
                    "Invalid JSON response from Thor node"
                ) from exc

        return retry_sync(_do, self._config)

    def close(self) -> None:
        """
        Closes the httpx client
        """
        self._client.close()
