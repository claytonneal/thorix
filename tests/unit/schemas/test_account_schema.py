import pytest
from pydantic import ValidationError

from thorix.schemas.account import AccountSchema

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_PAYLOAD = {
    "balance": "0x47ff1f90327aa0f8e",
    "energy": "0x1d9b457ad0e7e",
    "hasCode": False,
}


# ---------------------------------------------------------------------------
# AccountSchema
# ---------------------------------------------------------------------------


class TestAccountSchemaValid:
    def test_parses_valid_payload(self):
        account = AccountSchema.model_validate(VALID_PAYLOAD)
        assert account.balance == 0x47FF1F90327AA0F8E
        assert account.energy == 0x1D9B457AD0E7E
        assert account.has_code is False

    def test_has_code_true(self):
        payload = {**VALID_PAYLOAD, "hasCode": True}
        account = AccountSchema.model_validate(payload)
        assert account.has_code is True

    def test_balance_zero(self):
        payload = {**VALID_PAYLOAD, "balance": "0x0"}
        account = AccountSchema.model_validate(payload)
        assert account.balance == 0

    def test_energy_zero(self):
        payload = {**VALID_PAYLOAD, "energy": "0x0"}
        account = AccountSchema.model_validate(payload)
        assert account.energy == 0

    def test_hex_normalised_to_lowercase(self):
        payload = {**VALID_PAYLOAD, "balance": "0xDEADBEEF"}
        account = AccountSchema.model_validate(payload)
        assert account.balance == 0xDEADBEEF

    def test_balance_accepts_int(self):
        payload = {**VALID_PAYLOAD, "balance": 255}
        account = AccountSchema.model_validate(payload)
        assert account.balance == 255

    def test_energy_accepts_int(self):
        payload = {**VALID_PAYLOAD, "energy": 0}
        account = AccountSchema.model_validate(payload)
        assert account.energy == 0

    def test_extra_fields_ignored(self):
        payload = {**VALID_PAYLOAD, "unknown_field": "ignored"}
        account = AccountSchema.model_validate(payload)
        assert not hasattr(account, "unknown_field")

    def test_serialises_with_alias(self):
        account = AccountSchema.model_validate(VALID_PAYLOAD)
        data = account.model_dump(by_alias=True)
        assert "hasCode" in data
        assert "has_code" not in data

    def test_field_name_access(self):
        account = AccountSchema.model_validate(VALID_PAYLOAD)
        assert account.has_code == account.model_dump(by_alias=False)["has_code"]


class TestAccountSchemaInvalid:
    def test_missing_balance(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "balance"}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_missing_energy(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "energy"}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_missing_has_code(self):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "hasCode"}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_balance_invalid_hex(self):
        payload = {**VALID_PAYLOAD, "balance": "0xGGGG"}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_energy_invalid_hex(self):
        payload = {**VALID_PAYLOAD, "energy": "not-hex"}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_balance_not_string_or_int(self):
        payload = {**VALID_PAYLOAD, "balance": [1, 2, 3]}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_energy_not_string_or_int(self):
        payload = {**VALID_PAYLOAD, "energy": {"value": 1}}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_has_code_not_bool(self):
        payload = {**VALID_PAYLOAD, "hasCode": "maybe"}
        with pytest.raises(ValidationError):
            AccountSchema.model_validate(payload)

    def test_empty_payload(self):
        with pytest.raises(ValidationError):
            AccountSchema.model_validate({})
