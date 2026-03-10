from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPConfig:
    max_retries: int = 3
    retry_base_delay: float = 0.5
    retry_max_delay: float | None = None
    retry_delay_jitter: float = 0.1
