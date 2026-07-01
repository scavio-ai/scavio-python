from __future__ import annotations

from typing import Any, Optional

from ._exceptions import ScavioError
from ._http import BASE_URL, DEFAULT_TIMEOUT, _resolve_api_key, sync_request
from ._namespaces_sync import (
    _AmazonNamespace,
    _GoogleNamespace,
    _InstagramNamespace,
    _RedditNamespace,
    _TikTokNamespace,
    _WalmartNamespace,
    _YouTubeNamespace,
)
from ._params import build_body
from ._ratelimit import SyncRateLimiter
from ._retry import RetryConfig
from ._spec import ENDPOINTS
from ._types import UsageResponse


class ScavioClient:
    """Synchronous client for the Scavio Search API.

    A unified API over Google, YouTube, Amazon, Walmart, Reddit, TikTok, and
    Instagram. Every provider is exposed as a namespace (``client.google``,
    ``client.amazon``, ...) whose methods return the raw JSON response as a
    ``dict``.

    Args:
        api_key: Your Scavio API key. Falls back to the ``SCAVIO_API_KEY``
            environment variable when omitted.
        base_url: API base URL (default ``https://api.scavio.dev``).
        timeout: Per-request timeout in seconds.
        max_requests_per_second: Client-side rate limit; must be 1-10.
        max_retries: Automatic retries for 429/5xx and network errors
            (exponential backoff with jitter). ``0`` disables retries.

    Example:
        >>> from scavio import ScavioClient
        >>> with ScavioClient(api_key="sk_...") as client:
        ...     results = client.google.search("openai", gl="us", hl="en")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_requests_per_second: int = 1,
        max_retries: int = 2,
    ) -> None:
        if not 1 <= max_requests_per_second <= 10:
            raise ScavioError("max_requests_per_second must be between 1 and 10")
        self._api_key = _resolve_api_key(api_key)
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._rate_limiter = SyncRateLimiter(max_requests_per_second)
        self._retry = RetryConfig(max_retries=max_retries)

        self.google = _GoogleNamespace(self)
        self.amazon = _AmazonNamespace(self)
        self.walmart = _WalmartNamespace(self)
        self.youtube = _YouTubeNamespace(self)
        self.reddit = _RedditNamespace(self)
        self.tiktok = _TikTokNamespace(self)
        self.instagram = _InstagramNamespace(self)

    # -- transport ---------------------------------------------------------

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return sync_request(
            "POST",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            rate_limiter=self._rate_limiter,
            retry=self._retry,
            json=body,
        )

    def _get(self, path: str) -> dict[str, Any]:
        return sync_request(
            "GET",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            rate_limiter=self._rate_limiter,
            retry=self._retry,
        )

    def _call(
        self,
        key: str,
        values: dict[str, Any],
        extra: dict[str, Any],
    ) -> dict[str, Any]:
        endpoint = ENDPOINTS[key]
        if endpoint.http == "GET":
            return self._get(endpoint.path)
        return self._post(endpoint.path, build_body(endpoint, values, extra))

    # -- convenience -------------------------------------------------------

    def search(self, query: str, **extra: Any) -> dict[str, Any]:
        """Shortcut for :meth:`google.search` (Google SERP via /api/v2/google)."""
        return self.google.search(query, **extra)

    def get_usage(self) -> UsageResponse:
        """Return the account's plan, credit balance, and usage for the period."""
        return self._get("/api/v1/usage")  # type: ignore[return-value]

    def __enter__(self) -> ScavioClient:
        return self

    def __exit__(self, *args: Any) -> None:
        return None
