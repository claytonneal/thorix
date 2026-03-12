import pytest
from pydantic import ValidationError

from thorix.schemas.clause import ClauseSchema

VALID_ADDRESS = "0x" + "ab" * 20  # 40 hex chars

VALID_PAYLOAD = {
    "to": VALID_ADDRESS,
    "value": "0xff",
    "data": "0xdeadbeef",
}


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------


class TestClauseSchemaValid:
    def test_valid_payload(self):
        m = ClauseSchema.model_validate(VALID_PAYLOAD)
        assert m.to == VALID_ADDRESS
        assert m.value == 255
        assert m.data == "0xdeadbeef"

    def test_to_is_none_when_omitted(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "to"}
        m = ClauseSchema.model_validate(payload)
        assert m.to is None

    def test_to_explicit_none(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "to": None})
        assert m.to is None

    def test_to_normalised_to_lowercase(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "to": "0x" + "AB" * 20})
        assert m.to == VALID_ADDRESS

    def test_value_zero(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "value": "0x0"})
        assert m.value == 0

    def test_value_as_int(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "value": 100})
        assert m.value == 100

    def test_value_is_int(self):
        m = ClauseSchema.model_validate(VALID_PAYLOAD)
        assert isinstance(m.value, int)

    def test_data_normalised_to_lowercase(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "data": "0xDEADBEEF"})
        assert m.data == "0xdeadbeef"

    def test_data_empty_hex(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "data": "0x"})
        assert m.data == "0x"

    def test_extra_fields_ignored(self):
        m = ClauseSchema.model_validate({**VALID_PAYLOAD, "unexpected": "field"})
        assert not hasattr(m, "unexpected")


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------


class TestClauseSchemaInvalid:
    def test_missing_value(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "value"}
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate(payload)

    def test_missing_data(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "data"}
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate(payload)

    def test_to_wrong_length(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "to": "0x1234"})

    def test_to_no_prefix(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "to": "ab" * 20})

    def test_to_not_a_string(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "to": 123})

    def test_value_not_hex_string(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "value": "not-hex"})

    def test_value_no_prefix(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "value": "ff"})

    def test_value_list(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "value": [1, 2, 3]})

    def test_data_no_prefix(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "data": "deadbeef"})

    def test_data_not_a_string(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({**VALID_PAYLOAD, "data": 0xDEADBEEF})

    def test_empty_payload(self):
        with pytest.raises(ValidationError):
            ClauseSchema.model_validate({})
