from __future__ import annotations


class ScavioError(Exception):
    pass


class MissingAPIKeyError(ScavioError):
    def __init__(self) -> None:
        super().__init__(
            "No API key provided. Pass api_key or set the SCAVIO_API_KEY "
            "environment variable. Get your free key at https://dashboard.scavio.dev"
        )


class InvalidAPIKeyError(ScavioError):
    def __init__(self, message: str = "Invalid API key") -> None:
        super().__init__(message)


class InsufficientCreditsError(ScavioError):
    def __init__(self, message: str = "Insufficient credits") -> None:
        super().__init__(message)


class RateLimitError(ScavioError):
    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message)


class BadRequestError(ScavioError):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(message)


class ScavioAPIError(ScavioError):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"API error {status_code}: {message}")
