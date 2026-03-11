import re

_ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
_BLOCK_REF_RE = re.compile(r"^0x[0-9a-fA-F]{16}$")
_BLOCK_ID_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")
_BLOCK_LABELS = {"best", "justified", "finalized"}


class Address(str):
    """
    A VeChain address: 0x-prefixed 40-character hex string (20 bytes).
    Normalised to lowercase on construction.
    """

    def __new__(cls, value: str) -> "Address":
        if not _ADDRESS_RE.match(value):
            raise ValueError(f"Invalid address: {value!r}")
        return str.__new__(cls, value.lower())


class BlockRef(str):
    """
    A VeChain block reference: 0x-prefixed 16-character hex string (8 bytes).
    Normalised to lowercase on construction.
    """

    def __new__(cls, value: str) -> "BlockRef":
        if not _BLOCK_REF_RE.match(value):
            raise ValueError(f"Invalid block ref: {value!r}")
        return str.__new__(cls, value.lower())


class BlockId(str):
    """
    A VeChain block ID: 0x-prefixed 64-character hex string (32 bytes).
    Normalised to lowercase on construction.
    """

    def __new__(cls, value: str) -> "BlockId":
        if not _BLOCK_ID_RE.match(value):
            raise ValueError(f"Invalid block ID: {value!r}")
        return str.__new__(cls, value.lower())


class BlockLabel(str):
    """
    A VeChain block label: one of 'best', 'justified', or 'finalized'.
    """

    def __new__(cls, value: str) -> "BlockLabel":
        if value not in _BLOCK_LABELS:
            raise ValueError(
                f"Invalid block label: {value!r}. Must be one of {sorted(_BLOCK_LABELS)}"
            )
        return str.__new__(cls, value)


# Revision type is either a BlockId or a BlockLabel
Revision = BlockId | BlockLabel
