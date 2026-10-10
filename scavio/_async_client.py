from __future__ import annotations

from typing import Any, Literal, Optional

import httpx

from ._exceptions import ScavioError
from ._http import BASE_URL, DEFAULT_TIMEOUT, _resolve_api_key, async_request
from ._namespaces_async import (
    _AsyncAirbnbNamespace,
    _AsyncAmazonNamespace,
    _AsyncAppStoreNamespace,
    _AsyncBookingNamespace,
    _AsyncCapterraNamespace,
    _AsyncCompaniesHouseNamespace,
    _AsyncCostcoNamespace,
    _AsyncEbayNamespace,
    _AsyncG2Namespace,
    _AsyncGlassdoorNamespace,
    _AsyncGoogleAdsNamespace,
    _AsyncGoogleNamespace,
    _AsyncGooglePlayNamespace,
    _AsyncHomeDepotNamespace,
    _AsyncIndeedNamespace,
    _AsyncInstagramNamespace,
    _AsyncKuaishouNamespace,
    _AsyncLinkedInNamespace,
    _AsyncMetaAdsNamespace,
    _AsyncRedditNamespace,
    _AsyncRedfinNamespace,
    _AsyncSECNamespace,
    _AsyncTargetNamespace,
    _AsyncThreadsNamespace,
    _AsyncTikTokNamespace,
    _AsyncTikTokShopNamespace,
    _AsyncTripadvisorNamespace,
    _AsyncTrustpilotNamespace,
    _AsyncWalmartNamespace,
    _AsyncXNamespace,
    _AsyncYelpNamespace,
    _AsyncYouTubeNamespace,
    _AsyncZillowNamespace,
)
from ._params import build_body
from ._ratelimit import MAX_REQUESTS_PER_SECOND, AsyncRateLimiter
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
        max_requests_per_second: Client-side rate limit; must be 1-50.
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
        if not 1 <= max_requests_per_second <= MAX_REQUESTS_PER_SECOND:
            raise ScavioError(
                f"max_requests_per_second must be between 1 and {MAX_REQUESTS_PER_SECOND}"
            )
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
        self.x = _AsyncXNamespace(self)
        self.tiktok = _AsyncTikTokNamespace(self)
        self.instagram = _AsyncInstagramNamespace(self)
        self.linkedin = _AsyncLinkedInNamespace(self)
        self.tiktok_shop = _AsyncTikTokShopNamespace(self)
        self.threads = _AsyncThreadsNamespace(self)
        self.kuaishou = _AsyncKuaishouNamespace(self)
        self.ebay = _AsyncEbayNamespace(self)
        self.target = _AsyncTargetNamespace(self)
        self.home_depot = _AsyncHomeDepotNamespace(self)
        self.zillow = _AsyncZillowNamespace(self)
        self.booking = _AsyncBookingNamespace(self)
        self.tripadvisor = _AsyncTripadvisorNamespace(self)
        self.indeed = _AsyncIndeedNamespace(self)
        self.airbnb = _AsyncAirbnbNamespace(self)
        self.glassdoor = _AsyncGlassdoorNamespace(self)
        self.yelp = _AsyncYelpNamespace(self)
        self.app_store = _AsyncAppStoreNamespace(self)
        self.google_play = _AsyncGooglePlayNamespace(self)
        self.sec = _AsyncSECNamespace(self)
        self.redfin = _AsyncRedfinNamespace(self)
        self.companies_house = _AsyncCompaniesHouseNamespace(self)
        self.g2 = _AsyncG2Namespace(self)
        self.capterra = _AsyncCapterraNamespace(self)
        self.google_ads = _AsyncGoogleAdsNamespace(self)
        self.meta_ads = _AsyncMetaAdsNamespace(self)
        self.costco = _AsyncCostcoNamespace(self)
        self.trustpilot = _AsyncTrustpilotNamespace(self)

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

    async def extract(
        self,
        url: str,
        *,
        format: Optional[Literal["html", "markdown", "text"]] = None,
        mode: Optional[Literal["normal", "advanced", "ultra"]] = None,
    ) -> dict[str, Any]:
        """Read any URL and return it as raw HTML, readability Markdown, or plain text.

        A CORE endpoint, not a platform: it is a top-level method, never a
        namespace. Tier-priced by ``mode`` - 'normal' and 'advanced' cost 1
        credit, 'ultra' costs 2 - and only a successful extraction is billed, so
        a dead link, bot wall, or timeout costs nothing.

        Args:
            url: Page to read (1-2048 characters). http(s) only; a bare host is
                upgraded to https, and loopback, private, link-local, and
                metadata hosts are rejected with a 400.
            format: 'html' is the raw page, 'markdown' a readability extraction,
                'text' that markdown flattened to plain text. Server default
                'markdown'.
            mode: Fetch tier, and the price-bearing parameter: 'normal' plain
                datacenter fetch (1 credit), 'advanced' full browser render
                (1 credit), 'ultra' the hardest-target tier (2 credits). Server
                default 'normal'.

        Returns:
            ``{"url", "format", "mode", "content", "content_length"}``.
        """
        return await self._call("extract", {"url": url, "format": format, "mode": mode}, {})

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
