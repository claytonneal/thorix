from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixHTTPInvalidResponseError, ThorixHTTPStatusError
from thorix.http.http_async import AsyncHttpTransport

NO_RETRY = HTTPConfig(max_retries=0, retry_base_delay=0, retry_delay_jitter=0)


def make_client(json_data=None, raise_for_status=None, json_side_effect=None):
    """Build a mock httpx.AsyncClient with a pre-configured response."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.raise_for_status.side_effect = raise_for_status
    if json_side_effect is not None:
        mock_response.json.side_effect = json_side_effect
    else:
        mock_response.json.return_value = json_data

    mock_client = MagicMock(spec=httpx.AsyncClient)
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()
    return mock_client


def make_status_error(status_code: int) -> httpx.HTTPStatusError:
    return httpx.HTTPStatusError(
        str(status_code),
        request=MagicMock(),
        response=MagicMock(status_code=status_code),
    )


def make_transport(client) -> AsyncHttpTransport:
    return AsyncHttpTransport("http://localhost", NO_RETRY, client=client)


# ---------------------------------------------------------------------------
# get_json
# ---------------------------------------------------------------------------


class TestGetJson:
    @pytest.mark.asyncio
    async def test_returns_parsed_json(self):
        client = make_client(json_data={"block": 1})
        result = await make_transport(client).get_json("/blocks/1")
        assert result == {"block": 1}

    @pytest.mark.asyncio
    async def test_passes_query_params(self):
        client = make_client(json_data={"ok": True})
        await make_transport(client).get_json("/blocks", params={"expanded": "true"})
        client.get.assert_called_once_with("/blocks", params={"expanded": "true"})

    @pytest.mark.asyncio
    async def test_sends_get_request_to_correct_path(self):
        client = make_client(json_data={"ok": True})
        await make_transport(client).get_json("/blocks/100")
        client.get.assert_called_once_with("/blocks/100", params=None)

    @pytest.mark.asyncio
    async def test_raises_status_error_on_4xx(self):
        client = make_client(raise_for_status=make_status_error(404))
        with pytest.raises(ThorixHTTPStatusError):
            await make_transport(client).get_json("/blocks/missing")

    @pytest.mark.asyncio
    async def test_raises_invalid_response_on_bad_json(self):
        client = make_client(json_side_effect=ValueError("bad json"))
        with pytest.raises(ThorixHTTPInvalidResponseError):
            await make_transport(client).get_json("/blocks/1")


# ---------------------------------------------------------------------------
# post_json
# ---------------------------------------------------------------------------


class TestPostJson:
    @pytest.mark.asyncio
    async def test_returns_parsed_json(self):
        client = make_client(json_data={"txid": "abc"})
        result = await make_transport(client).post_json("/transactions", body={"raw": "0x..."})
        assert result == {"txid": "abc"}

    @pytest.mark.asyncio
    async def test_sends_body_as_json(self):
        client = make_client(json_data={"ok": True})
        await make_transport(client).post_json("/transactions", body={"raw": "0xdeadbeef"})
        client.post.assert_called_once_with("/transactions", json={"raw": "0xdeadbeef"})

    @pytest.mark.asyncio
    async def test_sends_post_request_to_correct_path(self):
        client = make_client(json_data={"ok": True})
        await make_transport(client).post_json("/transactions", body={})
        client.post.assert_called_once_with("/transactions", json={})

    @pytest.mark.asyncio
    async def test_raises_status_error_on_4xx(self):
        client = make_client(raise_for_status=make_status_error(400))
        with pytest.raises(ThorixHTTPStatusError):
            await make_transport(client).post_json("/transactions", body={"raw": "0x..."})

    @pytest.mark.asyncio
    async def test_raises_invalid_response_on_bad_json(self):
        client = make_client(json_side_effect=ValueError("bad json"))
        with pytest.raises(ThorixHTTPInvalidResponseError):
            await make_transport(client).post_json("/transactions", body={"raw": "0x..."})


# ---------------------------------------------------------------------------
# aclose
# ---------------------------------------------------------------------------


class TestAclose:
    @pytest.mark.asyncio
    async def test_aclose_closes_client(self):
        mock_client = MagicMock(spec=httpx.AsyncClient)
        mock_client.aclose = AsyncMock()
        await make_transport(mock_client).aclose()
        mock_client.aclose.assert_called_once()
