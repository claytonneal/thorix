import pytest

from thorix.client.thor_client import AsyncThorClient, ThorClient
from thorix.config.http_config import HTTPConfig
from thorix.http.http_async import AsyncHttpTransport
from thorix.http.http_sync import HttpTransport
from thorix.networks import Network
from thorix.types.primitives import Address, BlockLabel

FIRST_SOLO_ACCOUNT_ADDRESS = Address("0xf077b491b355E64048cE21E3A6Fc4751eEeA77fa")


class TestThorClient:
    def test_get_first_solo_account_best(self):
        transport = HttpTransport(Network.SOLO, HTTPConfig())
        client = ThorClient(transport)
        account = client.accounts.get_account(
            FIRST_SOLO_ACCOUNT_ADDRESS, revision=BlockLabel.BEST
        )
        assert account.balance > 0
        assert account.energy > 0
        assert account.has_code is False


class TestAsyncThorClient:
    @pytest.mark.asyncio
    async def test_get_first_solo_account_best(self):
        transport = AsyncHttpTransport(Network.SOLO, HTTPConfig())
        client = AsyncThorClient(transport)
        account = await client.accounts.get_account(
            FIRST_SOLO_ACCOUNT_ADDRESS, revision=BlockLabel.BEST
        )
        assert account.balance > 0
        assert account.energy > 0
        assert account.has_code is False
