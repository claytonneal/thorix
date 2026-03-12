import pytest
from pydantic import BaseModel, ValidationError

from thorix.schemas.primitives import HexInt, HexStr

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
