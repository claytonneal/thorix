from dataclasses import dataclass


@dataclass
class Account:
    """
    On-chain account state as returned by the Thor node.

    balance: VET balance in wei, hex-encoded.
    energy: VTHO balance in wei, hex-encoded.
    has_code: True if the account is a smart contract.
    """

    balance: int
    energy: int
    has_code: bool
