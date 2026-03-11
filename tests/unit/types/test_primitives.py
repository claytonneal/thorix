import pytest

from thorix.types.primitives import Address

# ---------------------------------------------------------------------------
# Address
# ---------------------------------------------------------------------------


class TestAddress:
    VALID = "0xd3ae78222beadb038203be21ed5ce7c9b1bff602"

    def test_valid_address(self):
        assert Address(self.VALID) == self.VALID

    def test_normalises_to_lowercase(self):
        upper = "0xD3AE78222BEADB038203BE21ED5CE7C9B1BFF602"
        assert Address(upper) == self.VALID

    def test_is_str(self):
        assert isinstance(Address(self.VALID), str)

    def test_invalid_too_short(self):
        with pytest.raises(ValueError, match="Invalid address"):
            Address("0x1234")

    def test_invalid_too_long(self):
        with pytest.raises(ValueError, match="Invalid address"):
            Address(self.VALID + "00")

    def test_invalid_no_prefix(self):
        with pytest.raises(ValueError, match="Invalid address"):
            Address("d3ae78222beadb038203be21ed5ce7c9b1bff602")

    def test_invalid_non_hex_chars(self):
        with pytest.raises(ValueError, match="Invalid address"):
            Address("0xGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")

    def test_invalid_empty_string(self):
        with pytest.raises(ValueError, match="Invalid address"):
            Address("")
