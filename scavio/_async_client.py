from __future__ import annotations

from typing import Any, Optional

import httpx

from ._exceptions import ScavioError
from ._http import BASE_URL, DEFAULT_TIMEOUT, _resolve_api_key, async_request
from ._namespaces_async import (
    _AsyncAmazonNamespace,
    _AsyncGoogleNamespace,
    _AsyncInstagramNamespace,
    _AsyncRedditNamespace,
    _AsyncTikTokNamespace,
    _AsyncWalmartNamespace,
    _AsyncYouTubeNamespace,
)
from ._params import build_body
from ._ratelimit import AsyncRateLimiter
from ._retry import RetryConfig
from ._spec import ENDPOINTS
from ._types import UsageResponse


class AsyncScavioClient:
    """Asynchronous client for the Scavio Search API.

    Mirrors :class:`~scavio.ScavioClient` method-for-method. A single pooled
    ``httpx.AsyncClient`` is created lazily on first request and reused for the
    client's lifetime; close it with ``await client.aclose()`` or use the async
    context manager.

    Args:
        api_key: Your Scavio API key. Falls back to the ``SCAVIO_API_KEY``
            environment variable when omitted.
        base_url: API base URL (default ``https://api.scavio.dev``).
        timeout: Per-request timeout in seconds.
        max_requests_per_second: Client-side rate limit; must be 1-10.
        max_retries: Automatic retries for 429/5xx and network errors
            (exponential backoff with jitter). ``0`` disables retries.

    Example:
        >>> import asyncio
        >>> from scavio import AsyncScavioClient
        >>> async def main():
        ...     async with AsyncScavioClient(api_key="sk_...") as client:
        ...         return await client.google.search("openai")
        >>> asyncio.run(main())
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
        self._rate_limiter = AsyncRateLimiter(max_requests_per_second)
        self._retry = RetryConfig(max_retries=max_retries)
        self._http_client: Optional[httpx.AsyncClient] = None

        self.google = _AsyncGoogleNamespace(self)
        self.amazon = _AsyncAmazonNamespace(self)
        self.walmart = _AsyncWalmartNamespace(self)
        self.youtube = _AsyncYouTubeNamespace(self)
        self.reddit = _AsyncRedditNamespace(self)
        self.tiktok = _AsyncTikTokNamespace(self)
        self.instagram = _AsyncInstagramNamespace(self)

    # -- transport ---------------------------------------------------------

    def _ensure_client(self) -> httpx.AsyncClient:
        # Safe without a lock: there is no ``await`` between the check and the
        # assignment, so concurrent coroutines cannot interleave here.
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client

    async def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return await async_request(
            "POST",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            http_client=self._ensure_client(),
            rate_limiter=self._rate_limiter,
            retry=self._retry,
            json=body,
        )

    async def _get(self, path: str) -> dict[str, Any]:
        return await async_request(
            "GET",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            http_client=self._ensure_client(),
            rate_limiter=self._rate_limiter,
            retry=self._retry,
        )

    async def _call(
        self,
        key: str,
        values: dict[str, Any],
        extra: dict[str, Any],
    ) -> dict[str, Any]:
        endpoint = ENDPOINTS[key]
        if endpoint.http == "GET":
            return await self._get(endpoint.path)
        return await self._post(endpoint.path, build_body(endpoint, values, extra))

    # -- convenience -------------------------------------------------------

    async def search(self, query: str, **extra: Any) -> dict[str, Any]:
        """Shortcut for :meth:`google.search` (Google SERP via /api/v2/google)."""
        return await self.google.search(query, **extra)

    async def get_usage(self) -> UsageResponse:
        """Return the account's plan, credit balance, and usage for the period."""
        return await self._get("/api/v1/usage")  # type: ignore[return-value]

    async def aclose(self) -> None:
        """Close the underlying HTTP client and release its connection pool."""
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    # Backwards-compatible alias for aclose().
    close = aclose

    async def __aenter__(self) -> AsyncScavioClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
