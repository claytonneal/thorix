from unittest.mock import MagicMock

import httpx
import pytest

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPInvalidResponseError, ThorixHTTPStatusError
from thorix.http.http_sync import HttpTransport

NO_RETRY = HTTPConfig(max_retries=0, retry_base_delay=0, retry_delay_jitter=0)


def make_client(json_data=None, status_code: int = 200, raise_for_status=None, json_side_effect=None):
    """Build a mock httpx.Client with a pre-configured response."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.raise_for_status.side_effect = raise_for_status
    if json_side_effect is not None:
        mock_response.json.side_effect = json_side_effect
    else:
        mock_response.json.return_value = json_data

    mock_client = MagicMock(spec=httpx.Client)
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    return mock_client


def make_status_error(status_code: int) -> httpx.HTTPStatusError:
    return httpx.HTTPStatusError(
        str(status_code),
        request=MagicMock(),
        response=MagicMock(status_code=status_code),
    )


def make_transport(client) -> HttpTransport:
    return HttpTransport("http://localhost", NO_RETRY, client=client)


# ---------------------------------------------------------------------------
# get_json
# ---------------------------------------------------------------------------


class TestGetJson:
    def test_returns_parsed_json(self):
        client = make_client(json_data={"block": 1})
        result = make_transport(client).get_json("/blocks/1")
        assert result == {"block": 1}

    def test_passes_query_params(self):
        client = make_client(json_data={"ok": True})
        make_transport(client).get_json("/blocks", params={"expanded": "true"})
        client.get.assert_called_once_with("/blocks", params={"expanded": "true"})

    def test_sends_get_request_to_correct_path(self):
        client = make_client(json_data={"ok": True})
        make_transport(client).get_json("/blocks/100")
        client.get.assert_called_once_with("/blocks/100", params=None)

    def test_raises_status_error_on_4xx(self):
        client = make_client(raise_for_status=make_status_error(404))
        with pytest.raises(ThorixHTTPStatusError):
            make_transport(client).get_json("/blocks/missing")

    def test_raises_invalid_response_on_bad_json(self):
        client = make_client(json_side_effect=ValueError("bad json"))
        with pytest.raises(ThorixHTTPInvalidResponseError):
            make_transport(client).get_json("/blocks/1")


# ---------------------------------------------------------------------------
# post_json
# ---------------------------------------------------------------------------


class TestPostJson:
    def test_returns_parsed_json(self):
        client = make_client(json_data={"txid": "abc"})
        result = make_transport(client).post_json("/transactions", body={"raw": "0x..."})
        assert result == {"txid": "abc"}

    def test_sends_body_as_json(self):
        client = make_client(json_data={"ok": True})
        make_transport(client).post_json("/transactions", body={"raw": "0xdeadbeef"})
        client.post.assert_called_once_with("/transactions", json={"raw": "0xdeadbeef"})

    def test_sends_post_request_to_correct_path(self):
        client = make_client(json_data={"ok": True})
        make_transport(client).post_json("/transactions", body={})
        client.post.assert_called_once_with("/transactions", json={})

    def test_raises_status_error_on_4xx(self):
        client = make_client(raise_for_status=make_status_error(400))
        with pytest.raises(ThorixHTTPStatusError):
            make_transport(client).post_json("/transactions", body={"raw": "0x..."})

    def test_raises_invalid_response_on_bad_json(self):
        client = make_client(json_side_effect=ValueError("bad json"))
        with pytest.raises(ThorixHTTPInvalidResponseError):
            make_transport(client).post_json("/transactions", body={"raw": "0x..."})


# ---------------------------------------------------------------------------
# close
# ---------------------------------------------------------------------------


class TestClose:
    def test_close_closes_client(self):
        mock_client = MagicMock(spec=httpx.Client)
        make_transport(mock_client).close()
        mock_client.close.assert_called_once()
