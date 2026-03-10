class ThorixError(Exception):
    """Base exception for all Thorix errors"""


# --------------------------------------
# HTTP Errors
# -------------------------------------


class ThorixHttpError(ThorixError):
    """Base exception for all Thorix http errors"""


class ThorixHTTPStatusError(ThorixHttpError):
    """HTTP response had non retriable status code"""


class ThorixHTTPRetryError(ThorixHttpError):
    """HTTP Retry attempts were exhausted"""


class ThorixHTTPInvalidResponseError(ThorixHttpError):
    """HTTP response was invalid"""


# ---------------------------------------
# Config Errors
# ---------------------------------------


class ThorixConfigError(ThorixError):
    """Invalid configuration"""
