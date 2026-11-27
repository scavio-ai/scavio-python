from __future__ import annotations

from typing import Any, Optional

from ._exceptions import ScavioError
from ._extract import ExtractNamespace
from ._http import BASE_URL, DEFAULT_TIMEOUT, _resolve_api_key, sync_request
from ._namespaces_sync import (
    _AbercrombieNamespace,
    _AcademyNamespace,
    _AcehardwareNamespace,
    _ActionNamespace,
    _AffordablehousingNamespace,
    _AirbnbNamespace,
    _AldiNamespace,
    _AllegroNamespace,
    _AmazonNamespace,
    _ApartmentlistNamespace,
    _AppStoreNamespace,
    _ArgosNamespace,
    _AshleyNamespace,
    _AsosNamespace,
    _AtacadaoNamespace,
    _AutotraderNamespace,
    _AutozoneNamespace,
    _BarnesandnobleNamespace,
    _BathandbodyworksNamespace,
    _BedbathbeyondNamespace,
    _BelkNamespace,
    _BestBuyNamespace,
    _BjsNamespace,
    _BolcomNamespace,
    _BookingNamespace,
    _BootsNamespace,
    _BoticarioNamespace,
    _BringatrailerNamespace,
    _BuscapeNamespace,
    _CanadianTireNamespace,
    _CapterraNamespace,
    _CargurusNamespace,
    _CarmaxNamespace,
    _CarrefourbrNamespace,
    _CarrefourNamespace,
    _CarscomNamespace,
    _CarvanaNamespace,
    _CasasbahiaNamespace,
    _CentauroNamespace,
    _ChatGPTNamespace,
    _ChewyNamespace,
    _CompaniesHouseNamespace,
    _CompanyNamespace,
    _CompassNamespace,
    _CostcoNamespace,
    _CultbeautyNamespace,
    _CvsNamespace,
    _DecathlonNamespace,
    _DepopNamespace,
    _DermstoreNamespace,
    _DicksNamespace,
    _DiscountTireNamespace,
    _DollarGeneralNamespace,
    _DollarTreeNamespace,
    _DouglasNamespace,
    _EbayNamespace,
    _EdmundsNamespace,
    _EnjoeiNamespace,
    _EstatesalesNamespace,
    _ExpediaNamespace,
    _ExtraspaceNamespace,
    _FanaticsNamespace,
    _FashionnovaNamespace,
    _FootlockerNamespace,
    _G2Namespace,
    _GapNamespace,
    _GeminiNamespace,
    _GlassdoorNamespace,
    _GoodreadsNamespace,
    _GoogleAdsNamespace,
    _GoogleNamespace,
    _GooglePlayNamespace,
    _HarborFreightNamespace,
    _HebNamespace,
    _HemaNamespace,
    _HmNamespace,
    _HomeDepotNamespace,
    _HotpadsNamespace,
    _IherbNamespace,
    _IkeaNamespace,
    _IndeedNamespace,
    _InstacartNamespace,
    _InstagramNamespace,
    _JcpenneyNamespace,
    _KabumNamespace,
    _KbbNamespace,
    _KohlsNamespace,
    _KrogerNamespace,
    _KuaishouNamespace,
    _LennarNamespace,
    _LeroymerlinNamespace,
    _LinkedInNamespace,
    _LlbeanNamespace,
    _LookfantasticNamespace,
    _LowesNamespace,
    _MacysNamespace,
    _MagaluNamespace,
    _MaisonsDuMondeNamespace,
    _MarksNamespace,
    _MediaExpertNamespace,
    _MenardsNamespace,
    _MercadoLibreNamespace,
    _MercariNamespace,
    _MetaAdsNamespace,
    _MichaelsNamespace,
    _MicroCenterNamespace,
    _MovotoNamespace,
    _NaturaNamespace,
    _NellisNamespace,
    _NeweggNamespace,
    _NikeNamespace,
    _NintendoNamespace,
    _NordstromNamespace,
    _NordstromRackNamespace,
    _NotinoNamespace,
    _OfferupNamespace,
    _OlxNamespace,
    _OreillyNamespace,
    _PcexpressNamespace,
    _PetcoNamespace,
    _PetsmartNamespace,
    _PoshmarkNamespace,
    _PublicstorageNamespace,
    _PublixNamespace,
    _QvcNamespace,
    _RakutenNamespace,
    _RdsaudeNamespace,
    _RealtorNamespace,
    _ReclameaquiNamespace,
    _RedditNamespace,
    _RedfinNamespace,
    _ReiNamespace,
    _RentcafeNamespace,
    _RentcomNamespace,
    _RightmoveNamespace,
    _RockautoNamespace,
    _RonaNamespace,
    _SaksNamespace,
    _SamsClubNamespace,
    _SECNamespace,
    _SephoraNamespace,
    _SpacenkNamespace,
    _SpecsNamespace,
    _SportchekNamespace,
    _StaplesNamespace,
    _StreeteasyNamespace,
    _SweetwaterNamespace,
    _TargetNamespace,
    _TcgplayerNamespace,
    _ThreadsNamespace,
    _ThredupNamespace,
    _ThriftbooksNamespace,
    _TikTokNamespace,
    _TikTokShopNamespace,
    _TractorsupplyNamespace,
    _TrendyolNamespace,
    _TripadvisorNamespace,
    _TruecarNamespace,
    _TruliaNamespace,
    _TrustpilotNamespace,
    _UhaulNamespace,
    _UltaNamespace,
    _UniqloNamespace,
    _VevorNamespace,
    _VintedNamespace,
    _VrboNamespace,
    _WalgreensNamespace,
    _WalmartNamespace,
    _WayfairNamespace,
    _WholeFoodsNamespace,
    _WilliamssonomaNamespace,
    _XNamespace,
    _YelpNamespace,
    _YesstyleNamespace,
    _YouTubeNamespace,
    _ZapposNamespace,
    _ZaraNamespace,
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
        self.specs = _SpecsNamespace(self)
        self.lowes = _LowesNamespace(self)
        self.sams_club = _SamsClubNamespace(self)
        self.canadian_tire = _CanadianTireNamespace(self)
        self.dollar_general = _DollarGeneralNamespace(self)
        self.sephora = _SephoraNamespace(self)
        self.ulta = _UltaNamespace(self)
        self.aldi = _AldiNamespace(self)
        self.micro_center = _MicroCenterNamespace(self)
        self.walgreens = _WalgreensNamespace(self)
        self.cvs = _CvsNamespace(self)
        self.whole_foods = _WholeFoodsNamespace(self)
        self.harbor_freight = _HarborFreightNamespace(self)
        self.petsmart = _PetsmartNamespace(self)
        self.petco = _PetcoNamespace(self)
        self.iherb = _IherbNamespace(self)
        self.chewy = _ChewyNamespace(self)
        self.menards = _MenardsNamespace(self)
        self.nordstrom = _NordstromNamespace(self)
        self.nordstrom_rack = _NordstromRackNamespace(self)
        self.best_buy = _BestBuyNamespace(self)
        self.tcgplayer = _TcgplayerNamespace(self)
        self.vinted = _VintedNamespace(self)
        self.macys = _MacysNamespace(self)
        self.saks = _SaksNamespace(self)
        self.kohls = _KohlsNamespace(self)
        self.jcpenney = _JcpenneyNamespace(self)
        self.dicks = _DicksNamespace(self)
        self.footlocker = _FootlockerNamespace(self)
        self.fanatics = _FanaticsNamespace(self)
        self.carrefour = _CarrefourNamespace(self)
        self.allegro = _AllegroNamespace(self)
        self.olx = _OlxNamespace(self)
        self.company = _CompanyNamespace(self)
        self.trustpilot = _TrustpilotNamespace(self)
        self.realtor = _RealtorNamespace(self)
        self.rightmove = _RightmoveNamespace(self)
        self.mercadolibre = _MercadoLibreNamespace(self)
        self.chatgpt = _ChatGPTNamespace(self)
        self.gemini = _GeminiNamespace(self)
        self.heb = _HebNamespace(self)
        self.kroger = _KrogerNamespace(self)
        self.publix = _PublixNamespace(self)
        self.ikea = _IkeaNamespace(self)
        self.wayfair = _WayfairNamespace(self)
        self.ashley = _AshleyNamespace(self)
        self.maisonsdumonde = _MaisonsDuMondeNamespace(self)
        self.trendyol = _TrendyolNamespace(self)
        self.nintendo = _NintendoNamespace(self)
        self.hm = _HmNamespace(self)
        self.zara = _ZaraNamespace(self)
        self.asos = _AsosNamespace(self)
        self.mercari = _MercariNamespace(self)
        self.bolcom = _BolcomNamespace(self)
        self.uniqlo = _UniqloNamespace(self)
        self.depop = _DepopNamespace(self)
        self.poshmark = _PoshmarkNamespace(self)
        self.thredup = _ThredupNamespace(self)
        self.fashionnova = _FashionnovaNamespace(self)
        self.argos = _ArgosNamespace(self)
        self.mediaexpert = _MediaExpertNamespace(self)
        self.action = _ActionNamespace(self)
        self.hema = _HemaNamespace(self)
        self.autozone = _AutozoneNamespace(self)
        self.instacart = _InstacartNamespace(self)
        self.oreilly = _OreillyNamespace(self)
        self.acehardware = _AcehardwareNamespace(self)
        self.tractorsupply = _TractorsupplyNamespace(self)
        self.michaels = _MichaelsNamespace(self)
        self.nike = _NikeNamespace(self)
        self.staples = _StaplesNamespace(self)
        self.dollartree = _DollarTreeNamespace(self)
        self.discounttire = _DiscountTireNamespace(self)
        self.vevor = _VevorNamespace(self)
        self.nellis = _NellisNamespace(self)
        self.dermstore = _DermstoreNamespace(self)
        self.offerup = _OfferupNamespace(self)
        self.sportchek = _SportchekNamespace(self)
        self.marks = _MarksNamespace(self)
        self.rona = _RonaNamespace(self)
        self.pcexpress = _PcexpressNamespace(self)
        self.spacenk = _SpacenkNamespace(self)
        self.lookfantastic = _LookfantasticNamespace(self)
        self.cultbeauty = _CultbeautyNamespace(self)
        self.yesstyle = _YesstyleNamespace(self)
        self.notino = _NotinoNamespace(self)
        self.douglas = _DouglasNamespace(self)
        self.boots = _BootsNamespace(self)
        self.rockauto = _RockautoNamespace(self)
        self.carscom = _CarscomNamespace(self)
        self.autotrader = _AutotraderNamespace(self)
        self.cargurus = _CargurusNamespace(self)
        self.carmax = _CarmaxNamespace(self)
        self.carvana = _CarvanaNamespace(self)
        self.bringatrailer = _BringatrailerNamespace(self)
        self.rentcom = _RentcomNamespace(self)
        self.trulia = _TruliaNamespace(self)
        self.streeteasy = _StreeteasyNamespace(self)
        self.rentcafe = _RentcafeNamespace(self)
        self.vrbo = _VrboNamespace(self)
        self.truecar = _TruecarNamespace(self)
        self.edmunds = _EdmundsNamespace(self)
        self.kbb = _KbbNamespace(self)
        self.movoto = _MovotoNamespace(self)
        self.hotpads = _HotpadsNamespace(self)
        self.apartmentlist = _ApartmentlistNamespace(self)
        self.compass = _CompassNamespace(self)
        self.affordablehousing = _AffordablehousingNamespace(self)
        self.lennar = _LennarNamespace(self)
        self.extraspace = _ExtraspaceNamespace(self)
        self.publicstorage = _PublicstorageNamespace(self)
        self.estatesales = _EstatesalesNamespace(self)
        self.goodreads = _GoodreadsNamespace(self)
        self.expedia = _ExpediaNamespace(self)
        self.academy = _AcademyNamespace(self)
        self.bathandbodyworks = _BathandbodyworksNamespace(self)
        self.gap = _GapNamespace(self)
        self.rakuten = _RakutenNamespace(self)
        self.bjs = _BjsNamespace(self)
        self.zappos = _ZapposNamespace(self)
        self.newegg = _NeweggNamespace(self)
        self.rei = _ReiNamespace(self)
        self.qvc = _QvcNamespace(self)
        self.barnesandnoble = _BarnesandnobleNamespace(self)
        self.thriftbooks = _ThriftbooksNamespace(self)
        self.uhaul = _UhaulNamespace(self)
        self.williamssonoma = _WilliamssonomaNamespace(self)
        self.belk = _BelkNamespace(self)
        self.abercrombie = _AbercrombieNamespace(self)
        self.llbean = _LlbeanNamespace(self)
        self.sweetwater = _SweetwaterNamespace(self)
        self.bedbathbeyond = _BedbathbeyondNamespace(self)
        self.kabum = _KabumNamespace(self)
        self.magalu = _MagaluNamespace(self)
        self.casasbahia = _CasasbahiaNamespace(self)
        self.buscape = _BuscapeNamespace(self)
        self.rdsaude = _RdsaudeNamespace(self)
        self.reclameaqui = _ReclameaquiNamespace(self)
        self.leroymerlin = _LeroymerlinNamespace(self)
        self.natura = _NaturaNamespace(self)
        self.boticario = _BoticarioNamespace(self)
        self.centauro = _CentauroNamespace(self)
        self.enjoei = _EnjoeiNamespace(self)
        self.atacadao = _AtacadaoNamespace(self)
        self.carrefourbr = _CarrefourbrNamespace(self)
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
