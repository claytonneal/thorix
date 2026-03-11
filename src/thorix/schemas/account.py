from pydantic import Field

from .primitives import HexInt
from .thorest_model import ThorestModel


class AccountSchema(ThorestModel):
    """
    Schema representing the raw response from the Thor
    GET /accounts/{address} endpoint.
    """

    balance: HexInt
    energy: HexInt
    has_code: bool = Field(alias="hasCode")
