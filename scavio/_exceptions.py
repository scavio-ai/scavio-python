from __future__ import annotations

from typing import Any, Optional


class ScavioError(Exception):
    """Base class for every error raised by the Scavio SDK.

    Catch this to handle any SDK-originated failure (configuration, network,
    or an error response from the API).
    """


class MissingAPIKeyError(ScavioError):
    """Raised at construction time when no API key can be resolved."""

    def __init__(self) -> None:
        super().__init__(
            "No API key provided. Pass api_key or set the SCAVIO_API_KEY "
            "environment variable. Get your free key at https://dashboard.scavio.dev"
        )


class ScavioConnectionError(ScavioError):
    """The request could not reach the API (DNS, connection reset, TLS, ...).

    Raised only after the configured retries are exhausted.
    """


class ScavioTimeoutError(ScavioError):
    """The request did not complete within the configured ``timeout``.

    Raised only after the configured retries are exhausted.
    """


class ScavioAPIStatusError(ScavioError):
    """Base class for any non-2xx HTTP response from the API.

    Attributes:
        status_code: The HTTP status code returned by the API (may be ``None``).
        response_body: The parsed JSON body of the error response, if any.
    """

    default_message = "API error"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        status_code: Optional[int] = None,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message or self.default_message)


class BadRequestError(ScavioAPIStatusError):
    """HTTP 400 - the request was malformed or failed server-side validation."""

    default_message = "Bad request"


class InvalidAPIKeyError(ScavioAPIStatusError):
    """HTTP 401 - the API key is missing, malformed, or revoked."""

    default_message = "Invalid API key"


class InsufficientCreditsError(ScavioAPIStatusError):
    """HTTP 402 - the account is out of credits."""

    default_message = "Insufficient credits"


class NotFoundError(ScavioAPIStatusError):
    """HTTP 404 - the requested resource does not exist."""

    default_message = "Not found"


class RateLimitError(ScavioAPIStatusError):
    """HTTP 429 - too many concurrent or too-frequent requests."""

    default_message = "Rate limit exceeded"


class ScavioAPIError(ScavioAPIStatusError):
    """Any other non-2xx response not covered by a more specific subclass.

    The legacy positional form ``ScavioAPIError(status_code, message)`` is
    preserved for backward compatibility.
    """

    def __init__(
        self,
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        *,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        if status_code is not None:
            rendered = f"API error {status_code}: {message or 'Unknown error'}"
        else:
            rendered = message or self.default_message
        # Skip ScavioAPIStatusError.__init__'s default-message handling so the
        # rendered "API error {code}: ..." string is preserved verbatim.
        self.status_code = status_code
        self.response_body = response_body
        ScavioError.__init__(self, rendered)


class ScavioJobTimeoutError(ScavioTimeoutError):
    """A crawl or batch started with ``wait=True`` did not finish within ``wait_timeout``.

    The job keeps running on the server: poll it with ``client.extract.crawl_status``
    / ``client.extract.batch_status`` using ``job_id``, or stop it with
    ``cancel_crawl`` / ``cancel_batch``.

    Attributes:
        job_id: The id of the job that was still running.
        job_type: ``"crawl"`` or ``"batch"``.
        last_status: The last status response seen while waiting.
    """

    def __init__(self, job_id: str, job_type: str, last_status: Optional[dict[str, Any]]) -> None:
        self.job_id = job_id
        self.job_type = job_type
        self.last_status = last_status
        super().__init__(
            f"{job_type} {job_id} was still running when wait_timeout elapsed; "
            f"poll it with extract.{job_type}_status('{job_id}')"
        )
