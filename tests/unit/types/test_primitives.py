import pytest

from thorix.types.primitives import Address, BlockId, BlockLabel, BlockRef, Revision

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


# ---------------------------------------------------------------------------
# BlockRef
# ---------------------------------------------------------------------------


class TestBlockRef:
    VALID = "0x00000000aabbccdd"

    def test_valid_block_ref(self):
        assert BlockRef(self.VALID) == self.VALID

    def test_normalises_to_lowercase(self):
        upper = "0x00000000AABBCCDD"
        assert BlockRef(upper) == self.VALID

    def test_is_str(self):
        assert isinstance(BlockRef(self.VALID), str)

    def test_invalid_too_short(self):
        with pytest.raises(ValueError, match="Invalid block ref"):
            BlockRef("0x00000000aabb")

    def test_invalid_too_long(self):
        with pytest.raises(ValueError, match="Invalid block ref"):
            BlockRef(self.VALID + "00")

    def test_invalid_no_prefix(self):
        with pytest.raises(ValueError, match="Invalid block ref"):
            BlockRef("00000000aabbccdd")

    def test_invalid_non_hex_chars(self):
        with pytest.raises(ValueError, match="Invalid block ref"):
            BlockRef("0x00000000GGGGGGGG")

    def test_invalid_empty_string(self):
        with pytest.raises(ValueError, match="Invalid block ref"):
            BlockRef("")


# ---------------------------------------------------------------------------
# BlockId
# ---------------------------------------------------------------------------


class TestBlockId:
    VALID = "0x" + "ab" * 32  # 64 hex chars

    def test_valid_block_id(self):
        assert BlockId(self.VALID) == self.VALID

    def test_normalises_to_lowercase(self):
        upper = "0x" + "AB" * 32
        assert BlockId(upper) == self.VALID

    def test_is_str(self):
        assert isinstance(BlockId(self.VALID), str)

    def test_invalid_too_short(self):
        with pytest.raises(ValueError, match="Invalid block ID"):
            BlockId("0x" + "ab" * 31)

    def test_invalid_too_long(self):
        with pytest.raises(ValueError, match="Invalid block ID"):
            BlockId(self.VALID + "00")

    def test_invalid_no_prefix(self):
        with pytest.raises(ValueError, match="Invalid block ID"):
            BlockId("ab" * 32)

    def test_invalid_non_hex_chars(self):
        with pytest.raises(ValueError, match="Invalid block ID"):
            BlockId("0x" + "GG" * 32)

    def test_invalid_empty_string(self):
        with pytest.raises(ValueError, match="Invalid block ID"):
            BlockId("")


# ---------------------------------------------------------------------------
# BlockLabel
# ---------------------------------------------------------------------------


class TestBlockLabel:
    def test_best(self):
        assert BlockLabel("best") == "best"

    def test_justified(self):
        assert BlockLabel("justified") == "justified"

    def test_finalized(self):
        assert BlockLabel("finalized") == "finalized"

    def test_is_str(self):
        assert isinstance(BlockLabel("best"), str)

    def test_invalid_label(self):
        with pytest.raises(ValueError, match="Invalid block label"):
            BlockLabel("latest")

    def test_invalid_empty_string(self):
        with pytest.raises(ValueError, match="Invalid block label"):
            BlockLabel("")

    def test_invalid_uppercase(self):
        with pytest.raises(ValueError, match="Invalid block label"):
            BlockLabel("Best")


# ---------------------------------------------------------------------------
# Revision
# ---------------------------------------------------------------------------


class TestRevision:
    def test_block_id_is_revision(self):
        rev = BlockId("0x" + "ab" * 32)
        assert isinstance(rev, BlockId)

    def test_block_label_is_revision(self):
        rev = BlockLabel("best")
        assert isinstance(rev, BlockLabel)

    def test_revision_is_str(self):
        assert isinstance(BlockId("0x" + "ab" * 32), str)
        assert isinstance(BlockLabel("finalized"), str)

    def test_plain_string_is_not_revision(self):
        assert not isinstance("best", BlockId)
        assert not isinstance("best", BlockLabel)
