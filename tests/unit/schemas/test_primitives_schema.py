import pytest
from pydantic import BaseModel, ValidationError

from thorix.schemas.primitives import (
    Address,
    BlockId,
    BlockRef,
    HexInt,
    HexStr,
    HexStr16,
    HexStr40,
    HexStr64,
    TransactionId,
)

# ---------------------------------------------------------------------------
# Wrapper models
# ---------------------------------------------------------------------------


class HexStrModel(BaseModel):
    value: HexStr


class HexIntModel(BaseModel):
    value: HexInt


# ---------------------------------------------------------------------------
# HexStr
# ---------------------------------------------------------------------------


class TestHexStr:
    def test_valid_hex_string(self):
        m = HexStrModel.model_validate({"value": "0xdeadbeef"})
        assert m.value == "0xdeadbeef"

    def test_normalises_to_lowercase(self):
        m = HexStrModel.model_validate({"value": "0xDEADBEEF"})
        assert m.value == "0xdeadbeef"

    def test_accepts_zero(self):
        m = HexStrModel.model_validate({"value": "0x0"})
        assert m.value == "0x0"

    def test_accepts_empty_hex(self):
        # "0x" with no digits is technically a valid match for ^0x[0-9a-fA-F]*$
        m = HexStrModel.model_validate({"value": "0x"})
        assert m.value == "0x"

    def test_accepts_long_hex(self):
        long_hex = "0x" + "ab" * 32
        m = HexStrModel.model_validate({"value": long_hex})
        assert m.value == long_hex

    def test_invalid_no_prefix(self):
        with pytest.raises(ValidationError):
            HexStrModel.model_validate({"value": "deadbeef"})

    def test_invalid_non_hex_chars(self):
        with pytest.raises(ValidationError):
            HexStrModel.model_validate({"value": "0xGGGG"})

    def test_invalid_not_a_string(self):
        with pytest.raises(ValidationError):
            HexStrModel.model_validate({"value": 123})

    def test_invalid_empty_string(self):
        with pytest.raises(ValidationError):
            HexStrModel.model_validate({"value": ""})

    def test_invalid_plain_string(self):
        with pytest.raises(ValidationError):
            HexStrModel.model_validate({"value": "not-hex"})


# ---------------------------------------------------------------------------
# HexInt
# ---------------------------------------------------------------------------


class TestHexInt:
    def test_valid_hex_string(self):
        m = HexIntModel.model_validate({"value": "0xff"})
        assert m.value == 255

    def test_valid_hex_string_uppercase(self):
        m = HexIntModel.model_validate({"value": "0xFF"})
        assert m.value == 255

    def test_valid_zero(self):
        m = HexIntModel.model_validate({"value": "0x0"})
        assert m.value == 0

    def test_valid_large_hex(self):
        m = HexIntModel.model_validate({"value": "0x47ff1f90327aa0f8e"})
        assert m.value == 0x47FF1F90327AA0F8E

    def test_accepts_int_directly(self):
        m = HexIntModel.model_validate({"value": 255})
        assert m.value == 255

    def test_accepts_int_zero(self):
        m = HexIntModel.model_validate({"value": 0})
        assert m.value == 0

    def test_result_is_int(self):
        m = HexIntModel.model_validate({"value": "0x10"})
        assert isinstance(m.value, int)

    def test_invalid_no_prefix(self):
        with pytest.raises(ValidationError):
            HexIntModel.model_validate({"value": "deadbeef"})

    def test_invalid_non_hex_chars(self):
        with pytest.raises(ValidationError):
            HexIntModel.model_validate({"value": "0xGGGG"})

    def test_invalid_plain_string(self):
        with pytest.raises(ValidationError):
            HexIntModel.model_validate({"value": "not-hex"})

    def test_invalid_empty_string(self):
        with pytest.raises(ValidationError):
            HexIntModel.model_validate({"value": ""})

    def test_invalid_list(self):
        with pytest.raises(ValidationError):
            HexIntModel.model_validate({"value": [1, 2, 3]})

    def test_invalid_dict(self):
        with pytest.raises(ValidationError):
            HexIntModel.model_validate({"value": {"v": 1}})


# ---------------------------------------------------------------------------
# bound_hex_str (via HexStr16 / HexStr40 / HexStr64)
# ---------------------------------------------------------------------------


class HexStr16Model(BaseModel):
    value: HexStr16


class HexStr40Model(BaseModel):
    value: HexStr40


class HexStr64Model(BaseModel):
    value: HexStr64


class TestHexStr16:
    VALID = "0x" + "ab" * 8  # 16 hex chars

    def test_valid(self):
        m = HexStr16Model.model_validate({"value": self.VALID})
        assert m.value == self.VALID

    def test_normalises_to_lowercase(self):
        m = HexStr16Model.model_validate({"value": "0x" + "AB" * 8})
        assert m.value == self.VALID

    def test_invalid_too_short(self):
        with pytest.raises(ValidationError, match="expected 16 hex chars after 0x"):
            HexStr16Model.model_validate({"value": "0x" + "ab" * 7})

    def test_invalid_too_long(self):
        with pytest.raises(ValidationError, match="expected 16 hex chars after 0x"):
            HexStr16Model.model_validate({"value": self.VALID + "ab"})

    def test_invalid_non_hex(self):
        with pytest.raises(ValidationError):
            HexStr16Model.model_validate({"value": "0x" + "GG" * 8})


class TestHexStr40:
    VALID = "0x" + "ab" * 20  # 40 hex chars

    def test_valid(self):
        m = HexStr40Model.model_validate({"value": self.VALID})
        assert m.value == self.VALID

    def test_invalid_too_short(self):
        with pytest.raises(ValidationError, match="expected 40 hex chars after 0x"):
            HexStr40Model.model_validate({"value": "0x" + "ab" * 19})

    def test_invalid_too_long(self):
        with pytest.raises(ValidationError, match="expected 40 hex chars after 0x"):
            HexStr40Model.model_validate({"value": self.VALID + "ab"})


class TestHexStr64:
    VALID = "0x" + "ab" * 32  # 64 hex chars

    def test_valid(self):
        m = HexStr64Model.model_validate({"value": self.VALID})
        assert m.value == self.VALID

    def test_invalid_too_short(self):
        with pytest.raises(ValidationError, match="expected 64 hex chars after 0x"):
            HexStr64Model.model_validate({"value": "0x" + "ab" * 31})

    def test_invalid_too_long(self):
        with pytest.raises(ValidationError, match="expected 64 hex chars after 0x"):
            HexStr64Model.model_validate({"value": self.VALID + "ab"})


# ---------------------------------------------------------------------------
# Domain aliases
# ---------------------------------------------------------------------------


class AddressModel(BaseModel):
    value: Address


class BlockRefModel(BaseModel):
    value: BlockRef


class BlockIdModel(BaseModel):
    value: BlockId


class TransactionIdModel(BaseModel):
    value: TransactionId


class TestDomainAliases:
    def test_address_valid(self):
        v = "0x" + "ab" * 20
        assert AddressModel.model_validate({"value": v}).value == v

    def test_address_invalid_length(self):
        with pytest.raises(ValidationError):
            AddressModel.model_validate({"value": "0x1234"})

    def test_block_ref_valid(self):
        v = "0x" + "ab" * 8
        assert BlockRefModel.model_validate({"value": v}).value == v

    def test_block_ref_invalid_length(self):
        with pytest.raises(ValidationError):
            BlockRefModel.model_validate({"value": "0x1234"})

    def test_block_id_valid(self):
        v = "0x" + "ab" * 32
        assert BlockIdModel.model_validate({"value": v}).value == v

    def test_block_id_invalid_length(self):
        with pytest.raises(ValidationError):
            BlockIdModel.model_validate({"value": "0x1234"})

    def test_transaction_id_valid(self):
        v = "0x" + "cd" * 32
        assert TransactionIdModel.model_validate({"value": v}).value == v

    def test_transaction_id_invalid_length(self):
        with pytest.raises(ValidationError):
            TransactionIdModel.model_validate({"value": "0x1234"})
