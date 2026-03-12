import pytest

from thorix.config.http_config import HTTPConfig
from thorix.http.http_async import AsyncHttpTransport
from thorix.http.http_sync import HttpTransport
from thorix.networks import Network
from thorix.thorest.accounts import AccountsAPI, AsyncAccountsAPI
from thorix.types.primitives import Address, BlockLabel

FIRST_SOLO_ACCOUNT_ADDRESS = Address("0xf077b491b355E64048cE21E3A6Fc4751eEeA77fa")


class TestAccountsAPI:
    def test_get_first_solo_account_best(self):
        transport = HttpTransport(Network.SOLO, HTTPConfig())
        api = AccountsAPI(transport)
        account = api.get_account(FIRST_SOLO_ACCOUNT_ADDRESS, revision=BlockLabel.BEST)
        assert account.balance > 0
        assert account.energy > 0
        assert account.has_code is False


class TestAccountsAsyncAPI:
    @pytest.mark.asyncio
    async def test_get_first_solo_account_best(self):
        transport = AsyncHttpTransport(Network.SOLO, HTTPConfig())
        api = AsyncAccountsAPI(transport)
        account = await api.get_account(
            FIRST_SOLO_ACCOUNT_ADDRESS, revision=BlockLabel.BEST
        )
        assert account.balance > 0
        assert account.energy > 0
        assert account.has_code is False
