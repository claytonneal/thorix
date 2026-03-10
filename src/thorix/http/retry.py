import asyncio
import logging
import random
import time
from typing import Awaitable, Callable

import httpx

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPRetryError, ThorixHTTPStatusError
from thorix.http.transport import Json

logger = logging.getLogger(__name__)


def _compute_delay(attempt: int, config: HTTPConfig) -> float:
    """
    Compute exponential backoff delay with optional cap and jitter.
    """
    delay = config.retry_base_delay * (2**attempt)
    if config.retry_max_delay is not None:
        delay = min(delay, config.retry_max_delay)
    return delay + random.random() * config.retry_delay_jitter


async def retry_async(fn: Callable[[], Awaitable[Json]], config: HTTPConfig) -> Json:
    """
    Async retry, will retry if it received:
        - RequestError
        - HttpStatusCodeError and status code is >= 500
    It uses an exponential back-off strategy
    Note total attempts is max_retries + 1 (the initial attempt)
    """
    for attempt in range(config.max_retries + 1):
        try:
            return await fn()
        except httpx.RequestError as exc:
            if attempt == config.max_retries:
                logger.error(
                    "Retry attempts exhausted after request error",
                    exc_info=exc,
                )
                raise ThorixHTTPRetryError(
                    "Retry attempts exhausted after request error"
                ) from exc
            delay = _compute_delay(attempt, config)
            logger.warning(
                "HTTP request failed (%s). Retrying attempt %d/%d in %.2fs",
                exc.__class__.__name__,
                attempt + 1,
                config.max_retries,
                delay,
            )
            await asyncio.sleep(delay)
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status < 500:
                logger.error(
                    "HTTP request failed with status %s",
                    status,
                    exc_info=exc,
                )
                raise ThorixHTTPStatusError(
                    f"HTTP request failed with status {status}"
                ) from exc
            if attempt == config.max_retries:
                logger.error(
                    "Retry attempts exhausted after server error %s",
                    status,
                    exc_info=exc,
                )
                raise ThorixHTTPRetryError(
                    f"Retry attempts exhausted after server error {status}"
                ) from exc
            delay = _compute_delay(attempt, config)
            logger.warning(
                "Server error %s. Retrying attempt %d/%d in %.2fs",
                status,
                attempt + 1,
                config.max_retries - 1,
                delay,
            )
            await asyncio.sleep(delay)
    raise ThorixHTTPRetryError("Retry attempts exhausted")


def retry_sync(fn: Callable[[], Json], config: HTTPConfig) -> Json:
    """
    Sync retry, will retry if it receives:
        - RequestError
        - HttpStatusCodeError and status code >= 500
    It uses an exponential back-off strategy
    Note total attempts is max_retries + 1 (the initial attempt)
    """
    for attempt in range(config.max_retries + 1):
        try:
            return fn()
        except httpx.RequestError as exc:
            if attempt == config.max_retries:
                logger.error(
                    "Retry attempts exhausted after request error",
                    exc_info=exc,
                )
                raise ThorixHTTPRetryError(
                    "Retry attempts exhausted after request error"
                ) from exc
            delay = _compute_delay(attempt, config)
            logger.warning(
                "HTTP request failed (%s). Retrying attempt %d/%d in %.2fs",
                exc.__class__.__name__,
                attempt + 1,
                config.max_retries,
                delay,
            )
            time.sleep(delay)
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status < 500:
                logger.error(
                    "HTTP request failed with status %s",
                    status,
                    exc_info=exc,
                )
                raise ThorixHTTPStatusError(
                    f"HTTP request failed with status {status}"
                ) from exc
            if attempt == config.max_retries:
                logger.error(
                    "Retry attempts exhausted after server error %s",
                    status,
                    exc_info=exc,
                )
                raise ThorixHTTPRetryError(
                    f"Retry attempts exhausted after server error {status}"
                ) from exc
            delay = _compute_delay(attempt, config)
            logger.warning(
                "Server error %s. Retrying attempt %d/%d in %.2fs",
                status,
                attempt + 1,
                config.max_retries - 1,
                delay,
            )
            time.sleep(delay)
    raise ThorixHTTPRetryError("Retry attempts exhausted")
