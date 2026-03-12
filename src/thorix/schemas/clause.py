from .primitives import Address, HexInt, HexStr
from .thorest_model import ThorestModel


class ClauseSchema(ThorestModel):
    """
    Clause schema as part of a transaction
    """

    to: Address | None = None
    value: HexInt
    data: HexStr
