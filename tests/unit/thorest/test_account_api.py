from unittest.mock import AsyncMock, MagicMock

import pytest

from thorix.errors import ThorixHTTPInvalidJSON
from thorix.thorest.accounts import AccountsAPI, AsyncAccountsAPI
from thorix.types.account import Account
from thorix.types.primitives import Address, BlockLabel

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

ADDRESS = Address("0xd3ae78222beadb038203be21ed5ce7c9b1bff602")

VALID_RESPONSE = {
    "balance": "0x47ff1f90327aa0f8e",
    "energy": "0x1d9b457ad0e7e",
    "hasCode": False,
}

INVALID_RESPONSE = {
    "balance": "not-hex",
    "energy": "0x0",
    "hasCode": False,
}


def make_sync_transport(return_value: object) -> MagicMock:
    transport = MagicMock()
    transport.get_json.return_value = return_value
    return transport


def make_async_transport(return_value: object) -> MagicMock:
    transport = MagicMock()
    transport.get_json = AsyncMock(return_value=return_value)
    return transport


# ---------------------------------------------------------------------------
# AccountsAPI (sync)
# ---------------------------------------------------------------------------


class TestAccountsAPI:
    def test_get_account_returns_account(self):
        transport = make_sync_transport(VALID_RESPONSE)
        api = AccountsAPI(transport)
        account = api.get_account(ADDRESS)
        assert isinstance(account, Account)
        assert account.balance == 0x47FF1F90327AA0F8E
        assert account.energy == 0x1D9B457AD0E7E
        assert account.has_code is False

    def test_get_account_calls_correct_path(self):
        transport = make_sync_transport(VALID_RESPONSE)
        api = AccountsAPI(transport)
        api.get_account(ADDRESS)
        transport.get_json.assert_called_once_with(
            f"/accounts/{ADDRESS}", params={"revision": BlockLabel("best")}
        )

    def test_get_account_passes_revision(self):
        transport = make_sync_transport(VALID_RESPONSE)
        api = AccountsAPI(transport)
        api.get_account(ADDRESS, revision=BlockLabel("finalized"))
        transport.get_json.assert_called_once_with(
            f"/accounts/{ADDRESS}", params={"revision": BlockLabel("finalized")}
        )

    def test_get_account_raises_on_invalid_response(self):
        transport = make_sync_transport(INVALID_RESPONSE)
        api = AccountsAPI(transport)
        with pytest.raises(ThorixHTTPInvalidJSON):
            api.get_account(ADDRESS)


# ---------------------------------------------------------------------------
# AsyncAccountsAPI
# ---------------------------------------------------------------------------


class TestAsyncAccountsAPI:
    @pytest.mark.asyncio
    async def test_get_account_returns_account(self):
        transport = make_async_transport(VALID_RESPONSE)
        api = AsyncAccountsAPI(transport)
        account = await api.get_account(ADDRESS)
        assert isinstance(account, Account)
        assert account.balance == 0x47FF1F90327AA0F8E
        assert account.energy == 0x1D9B457AD0E7E
        assert account.has_code is False

    @pytest.mark.asyncio
    async def test_get_account_calls_correct_path(self):
        transport = make_async_transport(VALID_RESPONSE)
        api = AsyncAccountsAPI(transport)
        await api.get_account(ADDRESS)
        transport.get_json.assert_called_once_with(
            f"/accounts/{ADDRESS}", params={"revision": BlockLabel("best")}
        )

    @pytest.mark.asyncio
    async def test_get_account_passes_revision(self):
        transport = make_async_transport(VALID_RESPONSE)
        api = AsyncAccountsAPI(transport)
        await api.get_account(ADDRESS, revision=BlockLabel("finalized"))
        transport.get_json.assert_called_once_with(
            f"/accounts/{ADDRESS}", params={"revision": BlockLabel("finalized")}
        )

    @pytest.mark.asyncio
    async def test_get_account_raises_on_invalid_response(self):
        transport = make_async_transport(INVALID_RESPONSE)
        api = AsyncAccountsAPI(transport)
        with pytest.raises(ThorixHTTPInvalidJSON):
            await api.get_account(ADDRESS)
