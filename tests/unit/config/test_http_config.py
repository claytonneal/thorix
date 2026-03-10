import pytest

from thorix.config.http_config import HTTPConfig
from thorix.errors import ThorixConfigError


class TestHTTPConfigDefaults:
    def test_default_values(self):
        config = HTTPConfig()
        assert config.max_retries == 3
        assert config.retry_base_delay == 0.5
        assert config.retry_max_delay is None
        assert config.retry_delay_jitter == 0.1

    def test_is_immutable(self):
        config = HTTPConfig()
        with pytest.raises(Exception):
            config.max_retries = 5  # type: ignore[misc]


class TestHTTPConfigValid:
    def test_custom_values(self):
        config = HTTPConfig(max_retries=5, retry_base_delay=1.0, retry_delay_jitter=0.2)
        assert config.max_retries == 5
        assert config.retry_base_delay == 1.0
        assert config.retry_delay_jitter == 0.2

    def test_zero_max_retries(self):
        config = HTTPConfig(max_retries=0)
        assert config.max_retries == 0

    def test_zero_base_delay(self):
        config = HTTPConfig(retry_base_delay=0)
        assert config.retry_base_delay == 0

    def test_zero_jitter(self):
        config = HTTPConfig(retry_delay_jitter=0)
        assert config.retry_delay_jitter == 0

    def test_max_delay_equal_to_base_delay(self):
        config = HTTPConfig(retry_base_delay=1.0, retry_max_delay=1.0)
        assert config.retry_max_delay == 1.0

    def test_max_delay_greater_than_base_delay(self):
        config = HTTPConfig(retry_base_delay=1.0, retry_max_delay=5.0)
        assert config.retry_max_delay == 5.0

    def test_max_delay_none(self):
        config = HTTPConfig(retry_max_delay=None)
        assert config.retry_max_delay is None


class TestHTTPConfigInvalid:
    def test_negative_max_retries(self):
        with pytest.raises(ThorixConfigError, match="max_retries"):
            HTTPConfig(max_retries=-1)

    def test_negative_base_delay(self):
        with pytest.raises(ThorixConfigError, match="retry_base_delay"):
            HTTPConfig(retry_base_delay=-0.1)

    def test_negative_jitter(self):
        with pytest.raises(ThorixConfigError, match="retry_delay_jitter"):
            HTTPConfig(retry_delay_jitter=-0.1)

    def test_max_delay_less_than_base_delay(self):
        with pytest.raises(ThorixConfigError, match="retry_max_delay"):
            HTTPConfig(retry_base_delay=2.0, retry_max_delay=1.0)
