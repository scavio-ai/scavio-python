from __future__ import annotations

from typing import Any, Optional

from ._exceptions import ScavioError
from ._extract import ExtractNamespace
from ._http import BASE_URL, DEFAULT_TIMEOUT, _resolve_api_key, sync_request
from ._namespaces_sync import (
    _AirbnbNamespace,
    _AmazonNamespace,
    _AppStoreNamespace,
    _BookingNamespace,
    _CapterraNamespace,
    _ChatGPTNamespace,
    _CompaniesHouseNamespace,
    _CostcoNamespace,
    _DecathlonNamespace,
    _EbayNamespace,
    _G2Namespace,
    _GeminiNamespace,
    _GlassdoorNamespace,
    _GoogleAdsNamespace,
    _GoogleNamespace,
    _GooglePlayNamespace,
    _HebNamespace,
    _HomeDepotNamespace,
    _IndeedNamespace,
    _InstagramNamespace,
    _KrogerNamespace,
    _KuaishouNamespace,
    _LinkedInNamespace,
    _MercadoLibreNamespace,
    _MetaAdsNamespace,
    _RealtorNamespace,
    _RedditNamespace,
    _RedfinNamespace,
    _RightmoveNamespace,
    _SECNamespace,
    _SpecsNamespace,
    _TargetNamespace,
    _ThreadsNamespace,
    _TikTokNamespace,
    _TikTokShopNamespace,
    _TotalWineNamespace,
    _TripadvisorNamespace,
    _TrustpilotNamespace,
    _WalmartNamespace,
    _XNamespace,
    _YelpNamespace,
    _YouTubeNamespace,
    _ZillowNamespace,
)
from ._params import build_body
from ._ratelimit import MAX_REQUESTS_PER_SECOND, SyncRateLimiter
from ._retry import RetryConfig
from ._spec import ENDPOINTS
from ._types import UsageResponse


class ScavioClient:
    """Synchronous client for the Scavio Search API.

    A unified API over 31 providers: search and SERP (Google), retail (Amazon,
    Walmart, eBay, Target, Home Depot), social and video (YouTube, Reddit, X,
    TikTok, TikTok Shop, Instagram, LinkedIn, Threads, Kuaishou), travel and
    local (Booking.com, Tripadvisor, Airbnb, Yelp), real estate (Zillow,
    Redfin), jobs and employers (Indeed, Glassdoor), app stores (Apple App
    Store, Google Play), business registries (SEC EDGAR, Companies House),
    software reviews (G2, Capterra), and ad transparency (Google Ads, Meta Ad
    Library). Every provider is exposed as a namespace (``client.google``,
    ``client.amazon``, ...) whose methods return the raw JSON response as a
    ``dict``.

    ``client.extract`` is the one exception: reading arbitrary URLs is a core
    capability rather than a platform. Call it for one page
    (``client.extract(url)``) or use ``client.extract.map`` / ``.crawl`` /
    ``.batch`` (and their status and cancel calls) for whole sites and URL lists.

    Args:
        api_key: Your Scavio API key. Falls back to the ``SCAVIO_API_KEY``
            environment variable when omitted.
        base_url: API base URL (default ``https://api.scavio.dev``).
        timeout: Per-request timeout in seconds.
        max_requests_per_second: Client-side rate limit; must be 1-50.
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
        if not 1 <= max_requests_per_second <= MAX_REQUESTS_PER_SECOND:
            raise ScavioError(
                f"max_requests_per_second must be between 1 and {MAX_REQUESTS_PER_SECOND}"
            )
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
        self.x = _XNamespace(self)
        self.tiktok = _TikTokNamespace(self)
        self.instagram = _InstagramNamespace(self)
        self.linkedin = _LinkedInNamespace(self)
        self.tiktok_shop = _TikTokShopNamespace(self)
        self.threads = _ThreadsNamespace(self)
        self.kuaishou = _KuaishouNamespace(self)
        self.ebay = _EbayNamespace(self)
        self.target = _TargetNamespace(self)
        self.home_depot = _HomeDepotNamespace(self)
        self.zillow = _ZillowNamespace(self)
        self.booking = _BookingNamespace(self)
        self.tripadvisor = _TripadvisorNamespace(self)
        self.indeed = _IndeedNamespace(self)
        self.airbnb = _AirbnbNamespace(self)
        self.glassdoor = _GlassdoorNamespace(self)
        self.yelp = _YelpNamespace(self)
        self.app_store = _AppStoreNamespace(self)
        self.google_play = _GooglePlayNamespace(self)
        self.sec = _SECNamespace(self)
        self.redfin = _RedfinNamespace(self)
        self.companies_house = _CompaniesHouseNamespace(self)
        self.g2 = _G2Namespace(self)
        self.capterra = _CapterraNamespace(self)
        self.google_ads = _GoogleAdsNamespace(self)
        self.meta_ads = _MetaAdsNamespace(self)
        self.costco = _CostcoNamespace(self)
        self.decathlon = _DecathlonNamespace(self)
        self.totalwine = _TotalWineNamespace(self)
        self.specs = _SpecsNamespace(self)
        self.trustpilot = _TrustpilotNamespace(self)
        self.realtor = _RealtorNamespace(self)
        self.rightmove = _RightmoveNamespace(self)
        self.mercadolibre = _MercadoLibreNamespace(self)
        self.chatgpt = _ChatGPTNamespace(self)
        self.gemini = _GeminiNamespace(self)
        self.heb = _HebNamespace(self)
        self.kroger = _KrogerNamespace(self)
        self._extract = ExtractNamespace(self)

    # -- transport ---------------------------------------------------------

    def _post(
        self, path: str, body: dict[str, Any], timeout: Optional[float] = None
    ) -> dict[str, Any]:
        return sync_request(
            "POST",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=timeout if timeout is not None else self._timeout,
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

    def _send(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Any method, with an optional query string and extra headers (extract jobs)."""
        return sync_request(
            method,
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            rate_limiter=self._rate_limiter,
            retry=self._retry,
            json=json,
            params=params,
            extra_headers=headers,
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
        timeout = None
        if endpoint.min_timeout is not None and endpoint.min_timeout > self._timeout:
            timeout = endpoint.min_timeout
        return self._post(endpoint.path, build_body(endpoint, values, extra), timeout)

    # -- convenience -------------------------------------------------------

    def search(self, query: str, **extra: Any) -> dict[str, Any]:
        """Shortcut for :meth:`google.search` (Google SERP via /api/v2/google)."""
        return self.google.search(query, **extra)

    @property
    def extract(self) -> ExtractNamespace:
        """Read any URL and return it as raw HTML, readability Markdown, or plain text.

        ``client.extract(url, format=..., mode=...)`` is the single-page call it
        has always been. The same object carries the Extract family's multi-page
        operations: ``map``, ``crawl``, ``crawl_status``, ``cancel_crawl``,
        ``batch``, ``batch_status`` and ``cancel_batch``.

        Tier-priced by ``mode`` - 'normal' and 'advanced' cost 1 credit,
        'ultra' costs 2 - and only a successful extraction is billed, so a dead
        link, bot wall, or timeout costs nothing. Crawl and batch bill the same
        price per successful page; map costs 1 credit on the normal tier.
        """
        return self._extract

    def get_usage(self) -> UsageResponse:
        """Return the account's plan, credit balance, and usage for the period."""
        return self._get("/api/v1/usage")  # type: ignore[return-value]

    def __enter__(self) -> ScavioClient:
        return self

    def __exit__(self, *args: Any) -> None:
        return None
