from thorix.http.transport import SyncTransport
from thorix.thorest.accounts import AccountsAPI


class ThorClient:
    """
    Synchronous client for the VeChain Thor blockchain
    """

    def __init__(self, transport: SyncTransport):
        self.accounts = AccountsAPI(transport)
