from enum import StrEnum


class Network(StrEnum):
    """
    Well-known VeChain Thor network URLs
    """

    SOLO = "http://localhost:8669"
    TESTNET = "https://testnet.vechain.org"
    MAINNET = "https://mainnet.vechain.org"
