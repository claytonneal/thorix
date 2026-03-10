import re

_ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
_HEX_RE = re.compile(r"^0x[0-9a-fA-F]*$")


class Hex(str):
    """
    A 0x-prefixed hex string of any length.
    Normalised to lowercase on construction.
    """

    def __new__(cls, value: str) -> "Hex":
        if not _HEX_RE.match(value):
            raise ValueError(f"Invalid hex string: {value!r}")
        return super().__new__(cls, value.lower())


class Address(Hex):
    """
    A VeChain address: 0x-prefixed 40-character hex string (20 bytes).
    Normalised to lowercase on construction.
    """

    def __new__(cls, value: str) -> "Address":
        if not _ADDRESS_RE.match(value):
            raise ValueError(f"Invalid address: {value!r}")
        return str.__new__(cls, value.lower())
