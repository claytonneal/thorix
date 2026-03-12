import pytest
from pydantic import ValidationError

from thorix.schemas.transactions import TransactionMetaSchema

VALID_BLOCK_ID = "0x" + "ab" * 32  # 64 hex chars

VALID_PAYLOAD = {
    "blockID": VALID_BLOCK_ID,
    "blockNumber": 1000,
    "blockTimestamp": 1700000000,
}


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------


class TestTransactionMetaSchemaValid:
    def test_valid_payload(self):
        m = TransactionMetaSchema.model_validate(VALID_PAYLOAD)
        assert m.block_id == VALID_BLOCK_ID
        assert m.block_number == 1000
        assert m.block_timestamp == 1700000000

    def test_block_id_normalised_to_lowercase(self):
        payload = {**VALID_PAYLOAD, "blockID": "0x" + "AB" * 32}
        m = TransactionMetaSchema.model_validate(payload)
        assert m.block_id == VALID_BLOCK_ID

    def test_block_number_zero(self):
        payload = {**VALID_PAYLOAD, "blockNumber": 0}
        m = TransactionMetaSchema.model_validate(payload)
        assert m.block_number == 0

    def test_block_timestamp_zero(self):
        payload = {**VALID_PAYLOAD, "blockTimestamp": 0}
        m = TransactionMetaSchema.model_validate(payload)
        assert m.block_timestamp == 0

    def test_extra_fields_ignored(self):
        payload = {**VALID_PAYLOAD, "unexpected": "value"}
        m = TransactionMetaSchema.model_validate(payload)
        assert not hasattr(m, "unexpected")

    def test_serialises_with_aliases(self):
        m = TransactionMetaSchema.model_validate(VALID_PAYLOAD)
        d = m.model_dump()
        assert "blockID" in d
        assert "blockNumber" in d
        assert "blockTimestamp" in d


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------


class TestTransactionMetaSchemaInvalid:
    def test_missing_block_id(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "blockID"}
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate(payload)

    def test_missing_block_number(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "blockNumber"}
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate(payload)

    def test_missing_block_timestamp(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "blockTimestamp"}
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate(payload)

    def test_block_id_wrong_length(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate({**VALID_PAYLOAD, "blockID": "0x1234"})

    def test_block_id_no_prefix(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate({**VALID_PAYLOAD, "blockID": "ab" * 32})

    def test_block_id_not_a_string(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate({**VALID_PAYLOAD, "blockID": 123})

    def test_block_number_negative(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate({**VALID_PAYLOAD, "blockNumber": -1})

    def test_block_number_not_an_int(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate(
                {**VALID_PAYLOAD, "blockNumber": "not-a-number"}
            )

    def test_block_timestamp_negative(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate({**VALID_PAYLOAD, "blockTimestamp": -1})

    def test_block_timestamp_not_an_int(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate(
                {**VALID_PAYLOAD, "blockTimestamp": "not-a-number"}
            )

    def test_empty_payload(self):
        with pytest.raises(ValidationError):
            TransactionMetaSchema.model_validate({})
