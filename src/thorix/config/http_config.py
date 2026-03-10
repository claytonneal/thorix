from dataclasses import dataclass

from thorix.errors import ThorixConfigError


@dataclass(frozen=True)
class HTTPConfig:
    max_retries: int = 3
    retry_base_delay: float = 0.5
    retry_max_delay: float | None = None
    retry_delay_jitter: float = 0.1

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ThorixConfigError("max_retries must be >= 0")
        if self.retry_base_delay < 0:
            raise ThorixConfigError("retry_base_delay must be >= 0")
        if self.retry_delay_jitter < 0:
            raise ThorixConfigError("retry_delay_jitter must be >= 0")
        if (
            self.retry_max_delay is not None
            and self.retry_max_delay < self.retry_base_delay
        ):
            raise ThorixConfigError("retry_max_delay must be >= retry_base_delay")
