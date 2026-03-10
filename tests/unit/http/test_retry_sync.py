from unittest.mock import MagicMock, patch

import httpx
import pytest

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPRetryError, ThorixHTTPStatusError
from thorix.http.retry import retry_async, retry_sync

NO_RETRY = HTTPConfig(max_retries=0, retry_base_delay=0, retry_delay_jitter=0)
ONE_RETRY = HTTPConfig(max_retries=1, retry_base_delay=0, retry_delay_jitter=0)
TWO_RETRIES = HTTPConfig(max_retries=2, retry_base_delay=0, retry_delay_jitter=0)


def make_status_error(status_code: int) -> httpx.HTTPStatusError:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    return httpx.HTTPStatusError("error", request=MagicMock(), response=response)


# ---------------------------------------------------------------------------
# retry_sync
# ---------------------------------------------------------------------------


class TestRetrySyncSuccess:
    def test_returns_result_on_first_attempt(self):
        fn = MagicMock(return_value={"ok": True})
        result = retry_sync(fn, NO_RETRY)
        assert result == {"ok": True}
        fn.assert_called_once()

    def test_returns_result_after_retry(self):
        fn = MagicMock(side_effect=[httpx.ConnectError("fail"), {"ok": True}])
        result = retry_sync(fn, ONE_RETRY)
        assert result == {"ok": True}
        assert fn.call_count == 2


class TestRetrySyncRequestError:
    def test_raises_retry_error_when_retries_exhausted(self):
        fn = MagicMock(side_effect=httpx.ConnectError("fail"))
        with pytest.raises(ThorixHTTPRetryError):
            retry_sync(fn, ONE_RETRY)

    def test_attempts_correct_number_of_times(self):
        fn = MagicMock(side_effect=httpx.ConnectError("fail"))
        with pytest.raises(ThorixHTTPRetryError):
            retry_sync(fn, TWO_RETRIES)
        assert fn.call_count == 3  # initial + 2 retries

    def test_no_retry_on_zero_max_retries(self):
        fn = MagicMock(side_effect=httpx.ConnectError("fail"))
        with pytest.raises(ThorixHTTPRetryError):
            retry_sync(fn, NO_RETRY)
        fn.assert_called_once()

    def test_retry_error_chains_original_exception(self):
        original = httpx.ConnectError("fail")
        fn = MagicMock(side_effect=original)
        with pytest.raises(ThorixHTTPRetryError) as exc_info:
            retry_sync(fn, NO_RETRY)
        assert exc_info.value.__cause__ is original


class TestRetrySyncStatusError:
    def test_raises_status_error_on_4xx(self):
        fn = MagicMock(side_effect=make_status_error(404))
        with pytest.raises(ThorixHTTPStatusError):
            retry_sync(fn, TWO_RETRIES)
        fn.assert_called_once()  # no retry on 4xx

    def test_raises_status_error_on_400(self):
        fn = MagicMock(side_effect=make_status_error(400))
        with pytest.raises(ThorixHTTPStatusError):
            retry_sync(fn, TWO_RETRIES)
        fn.assert_called_once()

    def test_retries_on_500(self):
        fn = MagicMock(side_effect=make_status_error(500))
        with pytest.raises(ThorixHTTPRetryError):
            retry_sync(fn, ONE_RETRY)
        assert fn.call_count == 2

    def test_retries_on_503(self):
        fn = MagicMock(side_effect=make_status_error(503))
        with pytest.raises(ThorixHTTPRetryError):
            retry_sync(fn, TWO_RETRIES)
        assert fn.call_count == 3

    def test_recovers_after_500_retry(self):
        fn = MagicMock(side_effect=[make_status_error(500), {"ok": True}])
        result = retry_sync(fn, ONE_RETRY)
        assert result == {"ok": True}

    def test_retry_error_includes_status_code(self):
        fn = MagicMock(side_effect=make_status_error(503))
        with pytest.raises(ThorixHTTPRetryError, match="503"):
            retry_sync(fn, NO_RETRY)


class TestRetrySyncSleep:
    def test_sleeps_between_retries(self):
        config = HTTPConfig(max_retries=1, retry_base_delay=1.0, retry_delay_jitter=0)
        fn = MagicMock(side_effect=[httpx.ConnectError("fail"), {"ok": True}])
        with patch("thorix.http.retry.time.sleep") as mock_sleep:
            retry_sync(fn, config)
        mock_sleep.assert_called_once()
        assert mock_sleep.call_args[0][0] == pytest.approx(1.0, abs=0.01)

    def test_no_sleep_on_final_attempt(self):
        config = HTTPConfig(max_retries=1, retry_base_delay=1.0, retry_delay_jitter=0)
        fn = MagicMock(side_effect=httpx.ConnectError("fail"))
        with patch("thorix.http.retry.time.sleep") as mock_sleep:
            with pytest.raises(ThorixHTTPRetryError):
                retry_sync(fn, config)
        mock_sleep.assert_called_once()  # only between attempts, not after last

    def test_delay_is_capped_by_max_delay(self):
        # base=1.0, so attempt=1 delay = 1.0 * 2^1 = 2.0, capped to 1.5
        config = HTTPConfig(
            max_retries=2,
            retry_base_delay=1.0,
            retry_max_delay=1.5,
            retry_delay_jitter=0,
        )
        fn = MagicMock(side_effect=[httpx.ConnectError("fail"), httpx.ConnectError("fail"), {"ok": True}])
        with patch("thorix.http.retry.time.sleep") as mock_sleep:
            retry_sync(fn, config)
        assert mock_sleep.call_args_list[1][0][0] == pytest.approx(1.5, abs=0.01)
