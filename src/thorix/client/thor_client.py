from thorix.http.http_async import AsyncHttpTransport
from thorix.http.transport import SyncTransport
from thorix.thorest.accounts import AccountsAPI, AsyncAccountsAPI


class ThorClient:
    """
    Synchronous client for the VeChain Thor blockchain
    """

    def __init__(self, transport: SyncTransport):
        self.accounts = AccountsAPI(transport)


class AsyncThorClient:
    """
    Asynchronous client for the VeChain Thor blockchain
    """

    def __init__(self, transport: AsyncHttpTransport):
        self.accounts = AsyncAccountsAPI(transport)
