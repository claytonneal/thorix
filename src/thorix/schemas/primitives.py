import re
from functools import partial
from typing import Annotated, TypeAlias

from pydantic import BeforeValidator

_HEX_RE = re.compile(r"^0x[0-9a-fA-F]*$")


def _parse_hex_str(v: object) -> str:
    if not isinstance(v, str):
        raise ValueError(f"Expected a string, got {type(v).__name__!r}")
    if not _HEX_RE.match(v):
        raise ValueError(f"Invalid hex string: {v!r}")
    return v.lower()


def _parse_hex_int(v: object) -> int:
    if isinstance(v, str):
        if not _HEX_RE.match(v):
            raise ValueError(f"Invalid hex string: {v!r}")
        return int(v, 16)
    if isinstance(v, int):
        return v
    raise ValueError(f"Expected a hex string or int, got {type(v).__name__!r}")


def _validate_hex_str_len(n: int, v: object) -> str:
    s = _parse_hex_str(v)
    if len(s) != 2 + n:
        raise ValueError(f"expected {n} hex chars after 0x")
    return s


# --- generic types ----

HexStr: TypeAlias = Annotated[str, BeforeValidator(_parse_hex_str)]
HexInt: TypeAlias = Annotated[int, BeforeValidator(_parse_hex_int)]

# --- fixed size hex strings ----

HexStr16: TypeAlias = Annotated[
    str, BeforeValidator(partial(_validate_hex_str_len, 16))
]
HexStr40: TypeAlias = Annotated[
    str, BeforeValidator(partial(_validate_hex_str_len, 40))
]
HexStr64: TypeAlias = Annotated[
    str, BeforeValidator(partial(_validate_hex_str_len, 64))
]

# --- thorest specific ---

Address: TypeAlias = HexStr40
BlockRef: TypeAlias = HexStr16
TransactionId: TypeAlias = HexStr64
BlockId: TypeAlias = HexStr64
