import pytest
from pydantic import ValidationError

from thorix.schemas.transactions import TransactionSchema

VALID_ADDRESS = "0x" + "ab" * 20  # 40 hex chars
VALID_TX_ID = "0x" + "cd" * 32  # 64 hex chars
VALID_BLOCK_ID = "0x" + "ef" * 32  # 64 hex chars
VALID_BLOCK_REF = "0x" + "12" * 8  # 16 hex chars

VALID_CLAUSE = {
    "to": VALID_ADDRESS,
    "value": "0x0",
    "data": "0x",
}

VALID_META = {
    "blockID": VALID_BLOCK_ID,
    "blockNumber": 1000,
    "blockTimestamp": 1700000000,
}

VALID_PAYLOAD = {
    "id": VALID_TX_ID,
    "type": 0,
    "origin": VALID_ADDRESS,
    "delegator": None,
    "size": 128,
    "chainTag": 39,
    "blockRef": VALID_BLOCK_REF,
    "expiration": 720,
    "clauses": [VALID_CLAUSE],
    "gasPriceCoef": None,
    "maxFeePerGas": None,
    "maxPriorityFeePerGas": None,
    "gas": 21000,
    "dependsOn": None,
    "nonce": "0xaabbccdd",
    "meta": VALID_META,
}


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------


class TestTransactionSchemaValid:
    def test_valid_full_payload(self):
        m = TransactionSchema.model_validate(VALID_PAYLOAD)
        assert m.id == VALID_TX_ID
        assert m.type == 0
        assert m.origin == VALID_ADDRESS
        assert m.size == 128
        assert m.chain_tag == 39
        assert m.block_ref == VALID_BLOCK_REF
        assert m.expiration == 720
        assert m.gas == 21000
        assert m.nonce == "0xaabbccdd"

    def test_clauses_parsed(self):
        m = TransactionSchema.model_validate(VALID_PAYLOAD)
        assert len(m.clauses) == 1
        assert m.clauses[0].to == VALID_ADDRESS
        assert m.clauses[0].value == 0
        assert m.clauses[0].data == "0x"

    def test_meta_parsed(self):
        m = TransactionSchema.model_validate(VALID_PAYLOAD)
        assert m.meta.block_id == VALID_BLOCK_ID
        assert m.meta.block_number == 1000
        assert m.meta.block_timestamp == 1700000000

    def test_multiple_clauses(self):
        payload = {**VALID_PAYLOAD, "clauses": [VALID_CLAUSE, VALID_CLAUSE]}
        m = TransactionSchema.model_validate(payload)
        assert len(m.clauses) == 2

    def test_empty_clauses_list(self):
        m = TransactionSchema.model_validate({**VALID_PAYLOAD, "clauses": []})
        assert m.clauses == []

    def test_hex_fields_normalised_to_lowercase(self):
        payload = {
            **VALID_PAYLOAD,
            "id": "0x" + "CD" * 32,
            "origin": "0x" + "AB" * 20,
            "blockRef": "0x" + "12" * 8,
            "nonce": "0xAABBCCDD",
        }
        m = TransactionSchema.model_validate(payload)
        assert m.id == VALID_TX_ID
        assert m.origin == VALID_ADDRESS
        assert m.block_ref == VALID_BLOCK_REF
        assert m.nonce == "0xaabbccdd"

    def test_extra_fields_ignored(self):
        m = TransactionSchema.model_validate({**VALID_PAYLOAD, "unexpected": "value"})
        assert not hasattr(m, "unexpected")

    def test_serialises_with_aliases(self):
        m = TransactionSchema.model_validate(VALID_PAYLOAD)
        d = m.model_dump()
        assert "chainTag" in d
        assert "blockRef" in d
        assert "dependsOn" in d

    # --- optional fields present ---

    def test_delegator_set(self):
        m = TransactionSchema.model_validate(
            {**VALID_PAYLOAD, "delegator": VALID_ADDRESS}
        )
        assert m.delegator == VALID_ADDRESS

    def test_gas_price_coef_set(self):
        m = TransactionSchema.model_validate({**VALID_PAYLOAD, "gasPriceCoef": 128})
        assert m.gas_price_coef == 128

    def test_max_fee_per_gas_set(self):
        m = TransactionSchema.model_validate({**VALID_PAYLOAD, "maxFeePerGas": "0x64"})
        assert m.max_fee_per_gas == 100

    def test_max_priority_fee_per_gas_set(self):
        m = TransactionSchema.model_validate(
            {**VALID_PAYLOAD, "maxPriorityFeePerGas": "0x0a"}
        )
        assert m.max_priority_fee_per_gas == 10

    def test_depends_on_set(self):
        depends = "0x" + "ff" * 32
        m = TransactionSchema.model_validate({**VALID_PAYLOAD, "dependsOn": depends})
        assert m.depends_on == depends

    # --- optional fields omitted (default to None) ---

    def test_delegator_defaults_to_none(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "delegator"}
        m = TransactionSchema.model_validate(payload)
        assert m.delegator is None

    def test_gas_price_coef_defaults_to_none(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "gasPriceCoef"}
        m = TransactionSchema.model_validate(payload)
        assert m.gas_price_coef is None

    def test_max_fee_per_gas_defaults_to_none(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "maxFeePerGas"}
        m = TransactionSchema.model_validate(payload)
        assert m.max_fee_per_gas is None

    def test_max_priority_fee_per_gas_defaults_to_none(self):
        payload = {
            k: v for k, v in VALID_PAYLOAD.items() if k != "maxPriorityFeePerGas"
        }
        m = TransactionSchema.model_validate(payload)
        assert m.max_priority_fee_per_gas is None

    def test_depends_on_defaults_to_none(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "dependsOn"}
        m = TransactionSchema.model_validate(payload)
        assert m.depends_on is None


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------


class TestTransactionSchemaInvalid:
    @pytest.mark.parametrize(
        "field",
        [
            "id",
            "type",
            "origin",
            "size",
            "chainTag",
            "blockRef",
            "expiration",
            "clauses",
            "gas",
            "nonce",
            "meta",
        ],
    )
    def test_missing_required_field(self, field: str):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != field}
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate(payload)

    def test_id_wrong_length(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "id": "0x1234"})

    def test_id_no_prefix(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "id": "cd" * 32})

    def test_origin_wrong_length(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "origin": "0x1234"})

    def test_delegator_wrong_length(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "delegator": "0x1234"})

    def test_block_ref_wrong_length(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "blockRef": "0x1234"})

    def test_depends_on_wrong_length(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "dependsOn": "0x1234"})

    def test_nonce_no_prefix(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "nonce": "aabbccdd"})

    def test_type_negative(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "type": -1})

    def test_size_negative(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "size": -1})

    def test_gas_negative(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "gas": -1})

    def test_clauses_not_a_list(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({**VALID_PAYLOAD, "clauses": "not-a-list"})

    def test_meta_invalid(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate(
                {**VALID_PAYLOAD, "meta": {"blockID": "bad"}}
            )

    def test_empty_payload(self):
        with pytest.raises(ValidationError):
            TransactionSchema.model_validate({})
