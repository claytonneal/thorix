import re
from typing import Annotated

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


HexStr = Annotated[str, BeforeValidator(_parse_hex_str)]
HexInt = Annotated[int, BeforeValidator(_parse_hex_int)]
