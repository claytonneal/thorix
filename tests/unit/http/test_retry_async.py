from unittest.mock import MagicMock, patch

import httpx
import pytest

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPRetryError, ThorixHTTPStatusError
from thorix.http.retry import retry_async

NO_RETRY = HTTPConfig(max_retries=0, retry_base_delay=0, retry_delay_jitter=0)
ONE_RETRY = HTTPConfig(max_retries=1, retry_base_delay=0, retry_delay_jitter=0)
TWO_RETRIES = HTTPConfig(max_retries=2, retry_base_delay=0, retry_delay_jitter=0)


def make_status_error(status_code: int) -> httpx.HTTPStatusError:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    return httpx.HTTPStatusError("error", request=MagicMock(), response=response)


# ---------------------------------------------------------------------------
# retry_async
# ---------------------------------------------------------------------------


class TestRetryAsyncSuccess:
    @pytest.mark.asyncio
    async def test_returns_result_on_first_attempt(self):
        async def fn():
            return {"ok": True}

        result = await retry_async(fn, NO_RETRY)
        assert result == {"ok": True}

    @pytest.mark.asyncio
    async def test_returns_result_after_retry(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise httpx.ConnectError("fail")
            return {"ok": True}

        result = await retry_async(fn, ONE_RETRY)
        assert result == {"ok": True}
        assert call_count == 2


class TestRetryAsyncRequestError:
    @pytest.mark.asyncio
    async def test_raises_retry_error_when_exhausted(self):
        async def fn():
            raise httpx.ConnectError("fail")

        with pytest.raises(ThorixHTTPRetryError):
            await retry_async(fn, ONE_RETRY)

    @pytest.mark.asyncio
    async def test_attempts_correct_number_of_times(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            raise httpx.ConnectError("fail")

        with pytest.raises(ThorixHTTPRetryError):
            await retry_async(fn, TWO_RETRIES)
        assert call_count == 3


class TestRetryAsyncStatusError:
    @pytest.mark.asyncio
    async def test_raises_status_error_on_4xx(self):
        async def fn():
            raise make_status_error(404)

        with pytest.raises(ThorixHTTPStatusError):
            await retry_async(fn, TWO_RETRIES)

    @pytest.mark.asyncio
    async def test_retries_on_500(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            raise make_status_error(500)

        with pytest.raises(ThorixHTTPRetryError):
            await retry_async(fn, ONE_RETRY)
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_recovers_after_500(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise make_status_error(500)
            return {"ok": True}

        result = await retry_async(fn, ONE_RETRY)
        assert result == {"ok": True}


class TestRetryAsyncSleep:
    @pytest.mark.asyncio
    async def test_sleeps_between_retries(self):
        config = HTTPConfig(max_retries=1, retry_base_delay=1.0, retry_delay_jitter=0)
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise httpx.ConnectError("fail")
            return {"ok": True}

        with patch("thorix.http.retry.asyncio.sleep") as mock_sleep:
            mock_sleep.return_value = None
            await retry_async(fn, config)
        mock_sleep.assert_called_once()
        assert mock_sleep.call_args[0][0] == pytest.approx(1.0, abs=0.01)
