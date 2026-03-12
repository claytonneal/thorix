from pydantic import Field, NonNegativeInt

from .clause import ClauseSchema
from .primitives import Address, BlockId, BlockRef, HexInt, HexStr, TransactionId
from .thorest_model import ThorestModel


class TransactionMetaSchema(ThorestModel):
    """
    Transaction meta schema from /transactions/{id} endpoint.
    """

    block_id: BlockId = Field(alias="blockID")
    block_number: NonNegativeInt = Field(alias="blockNumber")
    block_timestamp: NonNegativeInt = Field(alias="blockTimestamp")


class TransactionSchema(ThorestModel):
    """
    Transaction schema from /transactions/{id} endpoint.
    """

    id: TransactionId
    type: NonNegativeInt
    origin: Address
    delegator: Address | None = None
    size: NonNegativeInt
    chain_tag: NonNegativeInt = Field(alias="chainTag")
    block_ref: BlockRef = Field(alias="blockRef")
    expiration: NonNegativeInt
    clauses: list[ClauseSchema]
    gas_price_coef: NonNegativeInt | None = Field(alias="gasPriceCoef", default=None)
    max_fee_per_gas: HexInt | None = Field(alias="maxFeePerGas", default=None)
    max_priority_fee_per_gas: HexInt | None = Field(
        alias="maxPriorityFeePerGas", default=None
    )
    gas: NonNegativeInt
    depends_on: TransactionId | None = Field(alias="dependsOn", default=None)
    nonce: HexStr
    meta: TransactionMetaSchema
