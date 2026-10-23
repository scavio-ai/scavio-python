"""Declarative registry of every Scavio API endpoint.

This module is the single source of truth for the SDK surface: paths, HTTP
methods, and the full typed parameter set of each endpoint (mirroring the
backend zod schemas). Both the sync and async namespace classes are generated
from it by ``scripts/gen_namespaces.py``, and ``_params.build_body`` uses it to
map argument names to wire fields. To add or change an endpoint, edit here and
re-run the generator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence


@dataclass(frozen=True)
class Param:
    """A single endpoint parameter.

    Attributes:
        name: The Python argument name exposed to callers.
        annotation: The type annotation emitted into the generated signature.
        wire: The wire field name if it differs from ``name``.
        required: Whether the argument is positional/required (before ``*``).
        positional: Whether an *optional* argument is still emitted before ``*``
            (with a ``None`` default), so existing positional callers keep
            working after a second alternative param is added alongside it.
        doc: One-line description used in the generated docstring.
    """

    name: str
    annotation: str
    wire: Optional[str] = None
    required: bool = False
    positional: bool = False
    doc: str = ""

    @property
    def wire_field(self) -> str:
        return self.wire or self.name


@dataclass(frozen=True)
class Endpoint:
    """A single API endpoint.

    Attributes:
        credits: The constant credit cost, used to build the generated
            "Costs N credits." docstring line.
        credits_note: A complete sentence replacing that line on the
            BODY-PRICED surfaces (walmart, threads, kuaishou, instagram, extract), whose
            real cost is a function of the request body and cannot be stated as
            a single number. ``credits`` stays the floor so nothing that reads
            it has to learn a second type.
        min_timeout: Seconds this endpoint's request timeout is raised to when
            the client's own timeout is shorter. For endpoints that routinely
            answer slower than the 30s default (chatgpt, gemini).
    """

    key: str
    namespace: str
    method: str
    http: str
    path: str
    summary: str
    params: Sequence[Param] = field(default_factory=tuple)
    one_of: Sequence[Sequence[str]] = field(default_factory=tuple)
    credits: int = 1
    credits_note: Optional[str] = None
    min_timeout: Optional[float] = None

    @property
    def required_params(self) -> list[Param]:
        return [p for p in self.params if p.required]

    @property
    def positional_optional_params(self) -> list[Param]:
        return [p for p in self.params if not p.required and p.positional]

    @property
    def optional_params(self) -> list[Param]:
        return [p for p in self.params if not p.required and not p.positional]


# --- Param construction shorthands -----------------------------------------


def _req(name: str, doc: str, *, wire: Optional[str] = None) -> Param:
    return Param(name=name, annotation="str", wire=wire, required=True, doc=doc)


def _str(name: str, doc: str, *, wire: Optional[str] = None) -> Param:
    return Param(name=name, annotation="Optional[str]", wire=wire, doc=doc)


def _int(name: str, doc: str) -> Param:
    return Param(name=name, annotation="Optional[int]", doc=doc)


def _bool(name: str, doc: str) -> Param:
    return Param(name=name, annotation="Optional[bool]", doc=doc)


def _lit(name: str, choices: Sequence[str], doc: str, *, wire: Optional[str] = None) -> Param:
    literal = "Optional[Literal[" + ", ".join(f'"{c}"' for c in choices) + "]]"
    return Param(name=name, annotation=literal, wire=wire, doc=doc)


def _float(name: str, doc: str) -> Param:
    """A genuinely fractional number: backend ``z.number()``, not ``.int()``.

    Prices, HOA fees and half-baths all arrive here; ``_int`` would be a lie.
    """
    return Param(name=name, annotation="Optional[float]", doc=doc)


def _ilit(name: str, choices: Sequence[int], doc: str) -> Param:
    """An INT-valued literal union, e.g. ``Literal[1, 2, 3]``.

    Distinct from ``_lit``, which quotes every member: these backends are
    ``z.union([z.literal(1), ...])`` and reject the string "1".
    """
    literal = "Optional[Literal[" + ", ".join(str(c) for c in choices) + "]]"
    return Param(name=name, annotation=literal, doc=doc)


def _ilit_list(name: str, choices: Sequence[int], doc: str) -> Param:
    """An array of int literals, e.g. Yelp's price bands ``[1, 2]``."""
    literal = "Optional[list[Literal[" + ", ".join(str(c) for c in choices) + "]]]"
    return Param(name=name, annotation=literal, doc=doc)


def _str_list(name: str, doc: str, *, required: bool = False) -> Param:
    annotation = "list[str]" if required else "Optional[list[str]]"
    return Param(name=name, annotation=annotation, required=required, doc=doc)


def _int_list(name: str, doc: str) -> Param:
    return Param(name=name, annotation="Optional[list[int]]", doc=doc)


def _str_or_list(name: str, doc: str) -> Param:
    """A field the backend accepts as one value, a list, or a comma-joined string."""
    return Param(name=name, annotation="Optional[Union[str, list[str]]]", doc=doc)


def _str_or_int(name: str, doc: str) -> Param:
    """An id the backend takes as a numeric string or an integer (Walmart store_id)."""
    return Param(name=name, annotation="Optional[Union[str, int]]", doc=doc)


def _lit_or_int(name: str, choices: Sequence[str], doc: str) -> Param:
    """A named enum OR a raw numeric upstream id (Booking accommodation types)."""
    literal = "Literal[" + ", ".join(f'"{c}"' for c in choices) + "]"
    return Param(name=name, annotation=f"Optional[Union[{literal}, int]]", doc=doc)


def _lit_list(name: str, choices: Sequence[str], doc: str) -> Param:
    """An array of string literals, e.g. Costco's ``price_codes``."""
    literal = "Optional[list[Literal[" + ", ".join(f'"{c}"' for c in choices) + "]]]"
    return Param(name=name, annotation=literal, doc=doc)


# Reusable Google locale params (identical across most Google endpoints).
_HL = _str("hl", "UI language (ISO 639-1, e.g. 'en').")
_GL = _str("gl", "Country of the search (ISO 3166-1 alpha-2, e.g. 'us').")
_GOOGLE_DOMAIN = _str("google_domain", "Regional Google domain (e.g. 'google.co.uk').")
_LOCATION = _str("location", "Canonical location name; auto-encoded to a UULE string.")
_UULE = _str("uule", "Pre-encoded UULE location string (takes priority over location).")

# TikTok Shop marketplace regions with full upstream coverage (category listings
# are US/GB only and are declared inline on that endpoint).
_TIKTOK_SHOP_REGIONS = ("US", "GB", "SG", "MY", "PH", "TH", "VN", "ID")

# Marketplace selection, shared by every Amazon endpoint.
_AMAZON_COUNTRY = _str(
    "country",
    "Marketplace country code (ISO 3166-1 alpha-2, e.g. 'us', 'gb', 'de'). Defaults to 'us'.",
)
_AMAZON_DOMAIN = _str(
    "domain",
    "Deprecated: Amazon domain suffix ('com', 'co.uk'). Use country instead.",
)


# Costco site selection. Most endpoints are costco.com / costco.ca only; search,
# product and warehouses also take the six international sites.
_COSTCO_NA_COUNTRY = _lit("country", ("us", "ca"), "costco.com ('us', default) or costco.ca ('ca').")
_COSTCO_ANY_COUNTRY = _lit(
    "country",
    ("us", "ca", "uk", "au", "mx", "jp", "kr", "tw"),
    "Costco site ('us' default). us and ca support every filter; uk, au, mx, jp, kr and tw "
    "support keyword, sort and paging only.",
)

# Filters shared by costco search, category and deals (us/ca).
_COSTCO_LISTING_FILTERS = (
    _str(
        "warehouse_id",
        "Costco warehouse number (e.g. '1062'). Adds that warehouse's in-store price, stock "
        "status and price code to every result; omit for online prices only.",
    ),
    _lit(
        "sort_by",
        ("best_match", "price_low", "price_high", "top_rated", "newest"),
        "Result order (server default 'best_match'). Costco broadens matching under any other "
        "sort.",
    ),
    _str_list("brands", "Brand names to keep, up to 20 (e.g. ['Kirkland Signature'])."),
    _float("min_price", "Minimum online price, inclusive."),
    _float("max_price", "Maximum online price, inclusive."),
    _float("min_rating", "Minimum average star rating (1-5)."),
    _bool("on_sale", "Only items with an active discount."),
    _bool("in_stock", "Hide out-of-stock items."),
    _bool("in_warehouse", "Only items sold and in stock at warehouse_id (requires warehouse_id)."),
    _int("page", "Results page, 1-based (1-500)."),
    _int("page_size", "Results per page (1-120; server default 24)."),
)


_ENDPOINTS: tuple[Endpoint, ...] = (
    # ============================ Google (v2) ============================
    Endpoint(
        key="google_search",
        namespace="google",
        method="search",
        http="POST",
        path="/api/v2/google",
        summary="Google SERP search (organic results, ads, and the AI Overview when present).",
        params=(
            _req("query", "Search query (1-500 characters)."),
            _lit("device", ("desktop", "mobile"), "Device to emulate."),
            _int("start", "Result offset: 0 = page 1, 10 = page 2, ... up to 990."),
            _bool("include_html", "Include the raw Google HTML in the response."),
            _HL,
            _GL,
            _GOOGLE_DOMAIN,
            _str(
                "location",
                "Canonical location name; auto-encoded to a UULE string. On the standard results "
                "page it currently localizes the local pack only; set web_only=True for organic "
                "results localized to this location.",
            ),
            _UULE,
            _str("lr", "Language restrict (e.g. 'lang_en')."),
            _str("cr", "Country restrict (e.g. 'countryUS')."),
            _lit("safe", ("active",), "SafeSearch filter."),
            _bool("nfpr", "Disable spelling correction / auto-fixes when True."),
            _lit("filter", ("0", "1"), "'0' disables the omitted/similar-results filter."),
            _lit(
                "time_period",
                ("last_hour", "last_day", "last_week", "last_month", "last_year"),
                "Restrict results to a recent time window.",
            ),
            _bool("resolve_ai_overview", "Resolve a deferred AI Overview (server default True)."),
            _bool(
                "web_only",
                "Return Google's Web results only: organic results localized to location, with no "
                "local pack, ads, related questions, knowledge graph or AI Overview.",
            ),
        ),
    ),
    Endpoint(
        key="google_custom_search",
        namespace="google",
        method="custom_search",
        http="POST",
        path="/api/v1/google/customsearch",
        summary=(
            "Google search in the Custom Search JSON API format (drop-in for cse.list): returns "
            "customsearch#search with items[], searchInformation and queries.nextPage, plus a "
            "scavio billing object. For the full SERP (knowledge graph, AI overview, People Also "
            "Ask) use google.search. Unsupported CSE params (image search, sort, rights) raise "
            "BadRequestError."
        ),
        params=(
            _req("q", "Search query."),
            _str("cx", "Accepted and echoed back; results come from the whole web."),
            _int("num", "Results to return, 1-10 (default 10)."),
            _int("start", "1-based index of the first result (default 1); start + num <= 100."),
            _GL,
            _HL,
            _str("lr", "Language restrict (e.g. 'lang_en')."),
            _str("cr", "Country restrict, a single value (e.g. 'countryUS')."),
            _lit("safe", ("active", "off"), "SafeSearch (default 'off')."),
            _lit("filter", ("0", "1"), "'0' turns off duplicate-content filtering."),
            _str("date_restrict", "d[N], w[N], m[N] or y[N] (e.g. 'm6').", wire="dateRestrict"),
            _str("site_search", "Site to include or exclude (e.g. 'example.com'); enforced on results.", wire="siteSearch"),
            _lit("site_search_filter", ("i", "e"), "'i' include site_search (default), 'e' exclude it.", wire="siteSearchFilter"),
            _str("exact_terms", "Phrase every result must contain.", wire="exactTerms"),
            _str("exclude_terms", "Word or phrase no result may contain.", wire="excludeTerms"),
            _str("or_terms", "Space-separated terms; each result contains at least one.", wire="orTerms"),
            _str("hq", "Extra terms ANDed onto the query."),
            _str("file_type", "File extension to restrict to (e.g. 'pdf').", wire="fileType"),
            _str("googlehost", "Google domain to search (e.g. 'google.co.uk')."),
            _LOCATION,
            _lit("device", ("desktop", "mobile"), "Device to emulate."),
            _bool("nfpr", "Disable spelling autocorrection when True."),
            _bool("no_cache", "Skip the 24h result cache when True."),
        ),
    ),
    Endpoint(
        key="google_ai_mode",
        namespace="google",
        method="ai_mode",
        http="POST",
        path="/api/v2/google/ai-mode",
        summary="Google AI Mode conversational answer with references.",
        params=(
            _req("query", "Question or prompt (1-500 characters)."),
            _lit("device", ("desktop", "mobile"), "Device to emulate."),
            _bool("include_html", "Include the raw Google HTML in the response."),
            _HL,
            _GL,
            _GOOGLE_DOMAIN,
            _LOCATION,
            _UULE,
            _lit("safe", ("active",), "SafeSearch filter."),
        ),
    ),
    Endpoint(
        key="google_maps_search",
        namespace="google",
        method="maps_search",
        http="POST",
        path="/api/v2/google/maps/search",
        summary="Google Maps local business results.",
        params=(
            _req("query", "Search query (1-500 characters)."),
            _int("start", "Result offset; must be a multiple of 20 (0, 20, 40, ...)."),
            _str("ll", "Map center as '@lat,lng,zoomz'; controls where results come from."),
            _HL,
            _GL,
            _GOOGLE_DOMAIN,
        ),
    ),
    Endpoint(
        key="google_maps_place",
        namespace="google",
        method="maps_place",
        http="POST",
        path="/api/v2/google/maps/place",
        summary="Google Maps place details. Provide place_id or data_cid.",
        params=(
            _str("place_id", "Place ID (ChIJ...)."),
            _str("data_cid", "Numeric CID."),
        ),
        one_of=(("place_id", "data_cid"),),
    ),
    Endpoint(
        key="google_maps_reviews",
        namespace="google",
        method="maps_reviews",
        http="POST",
        path="/api/v2/google/maps/reviews",
        summary="Google Maps reviews for a place. Provide data_id or place_id.",
        params=(
            _str("data_id", "Data ID (0xHEX:0xHEX)."),
            _str("place_id", "Place ID (ChIJ...)."),
            _int("num", "Reviews per page (1-20)."),
            _str("next_page_token", "Pagination cursor from a prior response."),
            _lit(
                "sort_by",
                ("relevance", "newest", "highest_rating", "lowest_rating"),
                "Sort order.",
            ),
            _HL,
            _GL,
            _GOOGLE_DOMAIN,
        ),
        one_of=(("data_id", "place_id"),),
    ),
    Endpoint(
        key="google_shopping",
        namespace="google",
        method="shopping",
        http="POST",
        path="/api/v2/google/shopping",
        summary="Google Shopping product listings.",
        params=(
            _req("query", "Product search query (1-500 characters)."),
            _lit("device", ("desktop", "mobile"), "Device to emulate."),
            _int("start", "Result offset."),
            _int("min_price", "Minimum price filter."),
            _int("max_price", "Maximum price filter."),
            _int("sort_by", "0 = relevance, 1 = price ascending, 2 = price descending."),
            _bool("free_shipping", "Only items with free shipping."),
            _bool("on_sale", "Only items on sale."),
            _str("shoprs", "Opaque Google Shopping filter token."),
            _HL,
            _GL,
            _GOOGLE_DOMAIN,
            _LOCATION,
            _UULE,
        ),
    ),
    Endpoint(
        key="google_shopping_product",
        namespace="google",
        method="shopping_product",
        http="POST",
        path="/api/v2/google/shopping/product",
        summary="Google Shopping product detail and sellers. Pass catalog_id + query for full data.",
        params=(
            _str("catalog_id", "Durable product catalog id."),
            _str("query", "Product query; required when catalog_id is set."),
            _str("immersive_product_page_token", "Immersive product page token."),
            _str("page_token", "Alias for immersive_product_page_token."),
            _str("product_id", "Product id."),
            _lit("device", ("desktop", "mobile", "tablet"), "Device to emulate."),
            _GOOGLE_DOMAIN,
            _lit(
                "sort_by",
                ("base_price", "total_price", "promotion", "seller_rating"),
                "Seller sort order.",
            ),
            _bool("load_all_stores", "Load all available stores."),
            _bool("more_stores", "Fetch additional stores."),
            _HL,
            _GL,
            _LOCATION,
            _UULE,
        ),
    ),
    Endpoint(
        key="google_shopping_stores",
        namespace="google",
        method="shopping_stores",
        http="POST",
        path="/api/v2/google/shopping/product/stores",
        summary="More sellers for a shopping product (pagination of shopping_product).",
        params=(
            _req("catalog_id", "Durable product catalog id."),
            _req("next_page_token", "Pagination cursor from shopping_product."),
        ),
    ),
    Endpoint(
        key="google_flights",
        namespace="google",
        method="flights",
        http="POST",
        path="/api/v2/google/flights",
        summary="Google Flights search.",
        params=(
            _req("departure_id", "Departure IATA code(s); comma-separated allowed."),
            _req("arrival_id", "Arrival IATA code(s); comma-separated allowed."),
            _req("outbound_date", "Outbound date (YYYY-MM-DD)."),
            _int("type", "1 = round trip, 2 = one way, 3 = multi-city."),
            _str("return_date", "Return date (YYYY-MM-DD); required when type=1."),
            _int("adults", "Number of adults (1-9)."),
            _int("children", "Number of children (0-9)."),
            _int("infants_in_seat", "Infants in seat (0-4)."),
            _int("infants_on_lap", "Infants on lap (0-4)."),
            _int("travel_class", "1 = economy, 2 = premium, 3 = business, 4 = first."),
            _int("stops", "0 = any, 1 = nonstop, 2 = <=1 stop, 3 = <=2 stops."),
            _int("sort_by", "1 = top, 2 = price, 3 = departure, 4 = arrival, 5 = duration, 6 = emissions."),
            _str("include_airlines", "Comma-separated airline codes/alliances to include."),
            _str("exclude_airlines", "Comma-separated airline codes/alliances to exclude."),
            _HL,
            _GL,
            _str("currency", "Currency code (ISO 4217, e.g. 'USD')."),
        ),
    ),
    Endpoint(
        key="google_hotels",
        namespace="google",
        method="hotels",
        http="POST",
        path="/api/v2/google/hotels",
        summary="Google Hotels search.",
        params=(
            _req("query", "Search query; use a '<City> hotels' form."),
            _req("check_in_date", "Check-in date (YYYY-MM-DD)."),
            _req("check_out_date", "Check-out date (YYYY-MM-DD)."),
            _HL,
            _GL,
            _str("currency", "Currency code (ISO 4217, e.g. 'USD')."),
            _int("sort_by", "3 = lowest price, 8 = highest rating, 13 = most reviewed."),
            _int("min_price", "Minimum nightly price."),
            _int("max_price", "Maximum nightly price."),
            _int("rating", "7 = 3.5+, 8 = 4.0+, 9 = 4.5+."),
            _str("hotel_class", "Comma-separated star ratings (2-5)."),
            _str("amenities", "Comma-separated amenity ids."),
            _str("property_types", "Comma-separated property-type ids (e.g. '12' for vacation rentals)."),
            _bool("free_cancellation", "Only properties with free cancellation."),
            _bool("eco_certified", "Only eco-certified properties."),
            _bool("special_offers", "Only properties with special offers."),
            _str("next_page_token", "Pagination cursor from a prior response."),
            _int("limit", "Number of properties to return (1-20)."),
        ),
    ),
    Endpoint(
        key="google_hotels_detail",
        namespace="google",
        method="hotels_detail",
        http="POST",
        path="/api/v2/google/hotels/detail",
        summary="Google Hotels property details, from a hotels listing detail_token.",
        params=(
            _req("detail_token", "Property detail token from a hotels listing."),
            _req("check_in_date", "Check-in date (YYYY-MM-DD)."),
            _req("check_out_date", "Check-out date (YYYY-MM-DD)."),
            _str("currency", "Currency code (ISO 4217, e.g. 'USD')."),
            _GL,
            _HL,
        ),
    ),
    Endpoint(
        key="google_news",
        namespace="google",
        method="news",
        http="POST",
        path="/api/v2/google/news",
        summary="Google News results. Provide a query or a topic/story/publication token.",
        params=(
            _str("query", "Keyword search."),
            _str("topic_token", "Browse a news topic."),
            _str("section_token", "Browse a topic section."),
            _str("story_token", "Fetch full coverage of a story."),
            _str("publication_token", "Browse a publication."),
            _str("kgmid", "Knowledge Graph entity id."),
            _HL,
            _GL,
            _GOOGLE_DOMAIN,
            _int("so", "Sort order: 0 = relevance, 1 = date (only with query or kgmid)."),
        ),
    ),
    Endpoint(
        key="google_trends",
        namespace="google",
        method="trends",
        http="POST",
        path="/api/v2/google/trends",
        summary="Google Trends interest data.",
        params=(
            _req("query", "Search term(s); comma-separated for comparisons."),
            _str("geo", "Location code (e.g. 'US', 'GB', 'US-CA')."),
            _HL,
            _str("date", "Time range (e.g. 'today 12-m', 'now 7-d')."),
            _str("tz", "Timezone offset in minutes."),
            _lit(
                "data_type",
                ("TIMESERIES", "GEO_MAP", "GEO_MAP_0", "RELATED_QUERIES", "RELATED_TOPICS"),
                "Which trends dataset to return.",
            ),
            _str("cat", "Category id."),
            _lit("gprop", ("images", "news", "youtube", "froogle"), "Google property filter."),
            _lit("region", ("COUNTRY", "REGION", "DMA", "CITY"), "Resolution for GEO_MAP data."),
        ),
    ),
    Endpoint(
        key="google_trending",
        namespace="google",
        method="trending",
        http="POST",
        path="/api/v2/google/trending",
        summary="Google Trending Now for a country.",
        params=(
            _req("geo", "Country code (e.g. 'US')."),
            _HL,
            _int("hours", "Trending window: 4, 24, 48, or 168."),
            _int("cat", "Category id (0-20)."),
            _lit(
                "sort",
                ("relevance", "search_volume", "recency", "title"),
                "Sort order.",
            ),
            _lit("status", ("all", "active"), "Filter by trend status."),
        ),
    ),
    # ============================== YouTube ==============================
    Endpoint(
        key="youtube_search",
        namespace="youtube",
        method="search",
        http="POST",
        path="/api/v1/youtube/search",
        summary="Search YouTube videos, channels, and playlists. Costs 2 credits.",
        params=(
            _req("query", "Search query (1-500 characters).", wire="search"),
            _lit(
                "upload_date",
                ("last_hour", "today", "this_week", "this_month", "this_year"),
                "Filter by upload date.",
            ),
            _lit("type", ("video", "channel", "playlist", "movie"), "Filter by result type."),
            _lit(
                "duration",
                ("short", "medium", "long"),
                "short (<4 min), medium (4-20 min), long (>20 min).",
            ),
            _lit("sort_by", ("relevance", "date", "view_count", "rating"), "Sort order."),
            Param(
                "features",
                "Optional[list[str]]",
                doc=(
                    "Feature filters: hd, 4k, subtitles, creative_commons, live, "
                    "360, 3d, hdr, vr180."
                ),
            ),
            _str("cursor", "Pagination cursor from a prior response."),
            _bool("hd", "HD videos only."),
            _bool("subtitles", "Videos with subtitles/CC only."),
            _bool("creative_commons", "Creative Commons licensed only."),
            _bool("live", "Live videos only."),
            _bool("hdr", "HDR videos only."),
            _bool("vr180", "VR180 videos only."),
            Param("four_k", "Optional[bool]", wire="4k", doc="4K videos only."),
            Param("video_360", "Optional[bool]", wire="360", doc="360-degree videos only."),
            Param("video_3d", "Optional[bool]", wire="3d", doc="3D videos only."),
        ),
        credits=2,
    ),
    Endpoint(
        key="youtube_shorts",
        namespace="youtube",
        method="shorts",
        http="POST",
        path="/api/v1/youtube/shorts",
        summary="Search YouTube Shorts. Costs 2 credits.",
        params=(
            _req("query", "Search query (1-500 characters).", wire="search"),
            _lit(
                "sort_by",
                ("relevance", "date", "view_count", "rating"),
                "Sort order (passed through verbatim; no date remap here).",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=2,
    ),
    Endpoint(
        key="youtube_suggestions",
        namespace="youtube",
        method="suggestions",
        http="POST",
        path="/api/v1/youtube/suggestions",
        summary="YouTube search autocomplete suggestions.",
        params=(
            _req("query", "Search query (1-500 characters).", wire="search"),
            _str("language", "Suggestion language (ISO 639-1, default 'en')."),
            _str("region", "Region code (ISO 3166-1 alpha-2, default 'US')."),
        ),
    ),
    Endpoint(
        key="youtube_video",
        namespace="youtube",
        method="video",
        http="POST",
        path="/api/v1/youtube/video",
        summary="Full metadata for a single YouTube video.",
        params=(
            _req("video_id", "YouTube video id or full watch URL (e.g. 'dQw4w9WgXcQ')."),
        ),
    ),
    Endpoint(
        key="youtube_metadata",
        namespace="youtube",
        method="metadata",
        http="POST",
        path="/api/v1/youtube/video",
        summary="Full metadata for a single YouTube video. Deprecated alias of video().",
        params=(
            _req("video_id", "YouTube video id or full watch URL (e.g. 'dQw4w9WgXcQ')."),
        ),
    ),
    Endpoint(
        key="youtube_comments",
        namespace="youtube",
        method="comments",
        http="POST",
        path="/api/v1/youtube/comments",
        summary="Top-level comments on a YouTube video.",
        params=(
            _req("video_id", "YouTube video id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_comment_replies",
        namespace="youtube",
        method="comment_replies",
        http="POST",
        path="/api/v1/youtube/comments/replies",
        summary="Replies to a YouTube comment.",
        params=(
            _req("video_id", "YouTube video id."),
            _req("reply_cursor", "Reply cursor from a comment's reply_cursor field."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_transcript",
        namespace="youtube",
        method="transcript",
        http="POST",
        path="/api/v1/youtube/transcript",
        summary="Transcript / captions for a YouTube video. Costs 5 credits.",
        params=(
            _req("video_id", "YouTube video id."),
            _str("language", "Caption language code (default 'en')."),
            _lit("format", ("text", "srt"), "'text' plain transcript or 'srt' timed subtitles."),
        ),
        credits=5,
    ),
    Endpoint(
        key="youtube_related",
        namespace="youtube",
        method="related",
        http="POST",
        path="/api/v1/youtube/related",
        summary="Videos related to a YouTube video.",
        params=(
            _req("video_id", "YouTube video id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_channel_search",
        namespace="youtube",
        method="channel_search",
        http="POST",
        path="/api/v1/youtube/channel/search",
        summary="Search YouTube channels.",
        params=(
            _req("query", "Search query (1-500 characters).", wire="search"),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_channel",
        namespace="youtube",
        method="channel",
        http="POST",
        path="/api/v1/youtube/channel",
        summary="YouTube channel details.",
        params=(
            _req("channel_id", "Channel id, @handle, or channel URL."),
        ),
    ),
    Endpoint(
        key="youtube_channel_videos",
        namespace="youtube",
        method="channel_videos",
        http="POST",
        path="/api/v1/youtube/channel/videos",
        summary="Videos uploaded by a YouTube channel.",
        params=(
            _req("channel_id", "YouTube channel id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_channel_shorts",
        namespace="youtube",
        method="channel_shorts",
        http="POST",
        path="/api/v1/youtube/channel/shorts",
        summary="Shorts posted by a YouTube channel.",
        params=(
            _req("channel_id", "YouTube channel id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_channel_community",
        namespace="youtube",
        method="channel_community",
        http="POST",
        path="/api/v1/youtube/channel/community",
        summary="Community posts from a YouTube channel.",
        params=(
            _req("channel_id", "YouTube channel id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="youtube_channel_resolve",
        namespace="youtube",
        method="channel_resolve",
        http="POST",
        path="/api/v1/youtube/channel/resolve",
        summary="Resolve a YouTube @handle or channel URL to a channel id.",
        params=(
            _req("channel", "A @handle or channel URL to resolve."),
        ),
    ),
    Endpoint(
        key="youtube_streams",
        namespace="youtube",
        method="streams",
        http="POST",
        path="/api/v1/youtube/streams",
        summary="Playable / downloadable stream formats for a YouTube video. Costs 3 credits.",
        params=(
            _req("video_id", "YouTube video id."),
        ),
        credits=3,
    ),
    Endpoint(
        key="youtube_community_post",
        namespace="youtube",
        method="community_post",
        http="POST",
        path="/api/v1/youtube/community/post",
        summary=(
            "A single YouTube community post: text, author, likes, comment count, attached "
            "images, and a comments_cursor for community_post_comments."
        ),
        params=(
            _req("post_id", "Community post id or post URL."),
        ),
    ),
    Endpoint(
        key="youtube_community_post_comments",
        namespace="youtube",
        method="community_post_comments",
        http="POST",
        path="/api/v1/youtube/community/post/comments",
        summary="Comments on a YouTube community post, with likes, reply counts and pagination.",
        params=(
            _req("post_id", "Community post id or post URL."),
            _str("cursor", "next_cursor from a prior page, or comments_cursor from community_post."),
        ),
    ),
    # =============================== Amazon ==============================
    # The Amazon API changed in 2026-07 and now returns a normalized shape
    # instead of the old raw passthrough. Nine params were removed: language, currency, device, sort_by, pages, category_id,
    # merchant_id, zip_code and autoselect_variant. They are gone from the
    # signatures below rather than kept as no-ops - notably `sort_by`, which the
    # marketplace was verified to ignore entirely (every sort value returned the
    # same unordered set). The API answers 200 with a top-level `warnings` array
    # if a retired param is sent anyway, e.g. through **extra.
    #
    # `country` (ISO 3166-1 alpha-2) is the canonical marketplace selector;
    # `domain` and `start_page` are kept as deprecated aliases because published
    # SDK versions send them.
    Endpoint(
        key="amazon_search",
        namespace="amazon",
        method="search",
        http="POST",
        path="/api/v1/amazon/search",
        summary="Search Amazon product listings.",
        params=(
            _req("query", "Product search query (1-500 characters)."),
            _AMAZON_COUNTRY,
            _AMAZON_DOMAIN,
            _int("page", "Results page, 1-based. One page per call, 1 credit each."),
            _int("start_page", "Deprecated alias for page."),
        ),
    ),
    Endpoint(
        key="amazon_product",
        namespace="amazon",
        method="product",
        http="POST",
        path="/api/v1/amazon/product",
        summary="Full details for a single Amazon product by ASIN.",
        params=(
            _req("asin", "Amazon ASIN (e.g. 'B09XS7JWHH').", wire="query"),
            _AMAZON_COUNTRY,
            _AMAZON_DOMAIN,
        ),
    ),
    Endpoint(
        key="amazon_offers",
        namespace="amazon",
        method="offers",
        http="POST",
        path="/api/v1/amazon/offers",
        summary=(
            "Every seller offer for an Amazon ASIN: price, seller, condition, shipping, and which "
            "offer holds the buy box. Page 1 only."
        ),
        params=(
            _req("asin", "Amazon ASIN (e.g. 'B09XS7JWHH').", wire="query"),
            _AMAZON_COUNTRY,
            _AMAZON_DOMAIN,
        ),
    ),
    Endpoint(
        key="amazon_options",
        namespace="amazon",
        method="options",
        http="GET",
        path="/api/v1/amazon/options",
        summary=(
            "Supported Amazon marketplaces, as 'domains' and 'countries'. 'languages' and "
            "'currencies' remain in the payload but are always empty: neither is a request param "
            "any more. No API key required."
        ),
        params=(),
    ),
    # =============================== Reddit ==============================
    Endpoint(
        key="reddit_search",
        namespace="reddit",
        method="search",
        http="POST",
        path="/api/v1/reddit/search",
        summary="Search Reddit posts.",
        params=(
            _req("query", "Search query (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="reddit_search_suggestions",
        namespace="reddit",
        method="search_suggestions",
        http="POST",
        path="/api/v1/reddit/search/suggestions",
        summary="Autocomplete suggestions for a Reddit search query.",
        params=(_req("query", "Search query (1-500 characters)."),),
    ),
    Endpoint(
        key="reddit_post",
        namespace="reddit",
        method="post",
        http="POST",
        path="/api/v1/reddit/post",
        summary=(
            "Full details for a single Reddit post, as a flat post object (no comments). "
            "Provide url or post_id."
        ),
        params=(
            # url stays positional (with a None default) so callers written
            # against the url-only signature keep working unchanged.
            Param(
                "url",
                "Optional[str]",
                positional=True,
                doc="Full Reddit post URL.",
            ),
            _str("post_id", "Post fullname (t3_...) or bare id, as an alternative to url."),
        ),
        one_of=(("post_id", "url"),),
    ),
    Endpoint(
        key="reddit_post_comments",
        namespace="reddit",
        method="post_comments",
        http="POST",
        path="/api/v1/reddit/post/comments",
        summary="Top-level comments for a Reddit post.",
        params=(
            _req("post_id", "Post fullname (t3_...) or bare id."),
            _lit(
                "sort",
                ("HOT", "NEW", "TOP", "BEST", "CONTROVERSIAL"),
                "Comment sort order (server default 'TOP').",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="reddit_comment_replies",
        namespace="reddit",
        method="comment_replies",
        http="POST",
        path="/api/v1/reddit/post/comments/replies",
        summary="Replies to a specific Reddit comment.",
        params=(
            _req("post_id", "Post fullname (t3_...) or bare id."),
            _req("cursor", "reply_cursor from a comment in the comments endpoint."),
            _lit(
                "sort",
                ("HOT", "NEW", "TOP", "BEST", "CONTROVERSIAL"),
                "Comment sort order (server default 'TOP').",
            ),
        ),
    ),
    Endpoint(
        key="reddit_subreddit",
        namespace="reddit",
        method="subreddit",
        http="POST",
        path="/api/v1/reddit/subreddit",
        summary="Metadata for a subreddit.",
        params=(_req("subreddit", "Subreddit name (without the r/ prefix)."),),
    ),
    Endpoint(
        key="reddit_subreddit_posts",
        namespace="reddit",
        method="subreddit_posts",
        http="POST",
        path="/api/v1/reddit/subreddit/posts",
        summary="A subreddit's post feed.",
        params=(
            _req("subreddit", "Subreddit name (without the r/ prefix)."),
            _lit(
                "sort",
                ("BEST", "HOT", "NEW", "TOP", "CONTROVERSIAL", "RISING"),
                "Feed sort order (server default 'HOT').",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="reddit_user",
        namespace="reddit",
        method="user",
        http="POST",
        path="/api/v1/reddit/user",
        summary="A redditor's profile.",
        params=(_req("username", "Reddit username (without the u/ prefix)."),),
    ),
    Endpoint(
        key="reddit_user_posts",
        namespace="reddit",
        method="user_posts",
        http="POST",
        path="/api/v1/reddit/user/posts",
        summary="A redditor's submitted posts.",
        params=(
            _req("username", "Reddit username (without the u/ prefix)."),
            _lit(
                "sort",
                ("HOT", "NEW", "TOP", "BEST", "CONTROVERSIAL"),
                "Sort order (server default 'NEW').",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="reddit_user_comments",
        namespace="reddit",
        method="user_comments",
        http="POST",
        path="/api/v1/reddit/user/comments",
        summary="A redditor's comments.",
        params=(
            _req("username", "Reddit username (without the u/ prefix)."),
            _lit(
                "sort",
                ("HOT", "NEW", "TOP", "BEST", "CONTROVERSIAL"),
                "Sort order (server default 'NEW').",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="reddit_popular",
        namespace="reddit",
        method="popular",
        http="POST",
        path="/api/v1/reddit/popular",
        summary="The site-wide popular feed.",
        params=(_str("cursor", "Pagination cursor from a prior response."),),
    ),
    Endpoint(
        key="reddit_trending",
        namespace="reddit",
        method="trending",
        http="POST",
        path="/api/v1/reddit/trending",
        summary="Current trending Reddit search queries.",
        params=(),
    ),
    Endpoint(
        key="reddit_search_comments",
        namespace="reddit",
        method="search_comments",
        http="POST",
        path="/api/v1/reddit/search/comments",
        summary=(
            "Search Reddit comments by keyword. Each result carries the comment text, author, "
            "score and date, plus the post and subreddit it was left on."
        ),
        params=(
            _req("query", "Search query (1-500 characters)."),
            _lit("sort", ("RELEVANCE", "HOT", "TOP", "NEW"), "Sort order; server default 'RELEVANCE'."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="reddit_search_subreddits",
        namespace="reddit",
        method="search_subreddits",
        http="POST",
        path="/api/v1/reddit/search/subreddits",
        summary="Find subreddits by keyword, with subscriber counts, descriptions and NSFW flags.",
        params=(
            _req("query", "Search query (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    # =============================== TikTok ==============================
    Endpoint(
        key="tiktok_profile",
        namespace="tiktok",
        method="profile",
        http="POST",
        path="/api/v1/tiktok/profile",
        summary="TikTok user profile. Provide username or sec_user_id.",
        params=(
            _str("username", "TikTok @username (without the @)."),
            _str("sec_user_id", "TikTok sec_user_id."),
        ),
        one_of=(("username", "sec_user_id"),),
    ),
    Endpoint(
        key="tiktok_user_posts",
        namespace="tiktok",
        method="user_posts",
        http="POST",
        path="/api/v1/tiktok/user/posts",
        summary="Videos posted by a TikTok user.",
        params=(
            _req("sec_user_id", "TikTok sec_user_id."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Results per page (1-30)."),
            _lit("sort_type", ("0", "1"), "'0' = latest, '1' = popular."),
        ),
    ),
    Endpoint(
        key="tiktok_video",
        namespace="tiktok",
        method="video",
        http="POST",
        path="/api/v1/tiktok/video",
        summary="Details for a single TikTok video.",
        params=(_req("video_id", "TikTok video id."),),
    ),
    Endpoint(
        key="tiktok_video_transcript",
        namespace="tiktok",
        method="video_transcript",
        http="POST",
        path="/api/v1/tiktok/video/transcript",
        summary=(
            "Spoken-word transcript of a TikTok video as timestamped segments and full text. "
            "Returns available: false for videos with no spoken captions (music, dance or muted "
            "clips). Provide video_id or url."
        ),
        params=(
            Param(
                name="video_id",
                annotation="Optional[str]",
                positional=True,
                doc="TikTok video id (numeric string).",
            ),
            _str("url", "A TikTok video URL or share link (alternative to video_id)."),
            _str(
                "language",
                "Preferred transcript language (2-letter code, e.g. 'en'); defaults to the "
                "original spoken language.",
            ),
        ),
        one_of=(("video_id", "url"),),
    ),
    Endpoint(
        key="tiktok_video_comments",
        namespace="tiktok",
        method="video_comments",
        http="POST",
        path="/api/v1/tiktok/video/comments",
        summary="Comments on a TikTok video.",
        params=(
            _req("video_id", "TikTok video id."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Results per page (1-50)."),
        ),
    ),
    Endpoint(
        key="tiktok_comment_replies",
        namespace="tiktok",
        method="comment_replies",
        http="POST",
        path="/api/v1/tiktok/video/comments/replies",
        summary="Replies to a TikTok comment.",
        params=(
            _req("video_id", "TikTok video id."),
            _req("comment_id", "Parent comment id."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Results per page (1-50)."),
        ),
    ),
    Endpoint(
        key="tiktok_search_videos",
        namespace="tiktok",
        method="search_videos",
        http="POST",
        path="/api/v1/tiktok/search/videos",
        summary="Search TikTok videos by keyword.",
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Results per page (1-30)."),
            _lit("sort_type", ("0", "1"), "'0' = relevance, '1' = most likes."),
            _lit(
                "publish_time",
                ("0", "1", "7", "30", "90", "180"),
                "Age filter in days: 0 = all time, 1, 7, 30, 90, 180.",
            ),
        ),
    ),
    Endpoint(
        key="tiktok_search_users",
        namespace="tiktok",
        method="search_users",
        http="POST",
        path="/api/v1/tiktok/search/users",
        summary="Search TikTok users by keyword.",
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Results per page (1-30)."),
        ),
    ),
    Endpoint(
        key="tiktok_hashtag",
        namespace="tiktok",
        method="hashtag",
        http="POST",
        path="/api/v1/tiktok/hashtag",
        summary="TikTok hashtag details. Provide hashtag_name or hashtag_id.",
        params=(
            _str("hashtag_name", "Hashtag name (without the #)."),
            _str("hashtag_id", "Hashtag id."),
        ),
        one_of=(("hashtag_name", "hashtag_id"),),
    ),
    Endpoint(
        key="tiktok_hashtag_videos",
        namespace="tiktok",
        method="hashtag_videos",
        http="POST",
        path="/api/v1/tiktok/hashtag/videos",
        summary="Videos for a TikTok hashtag.",
        params=(
            _req("hashtag_id", "Hashtag id."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Results per page (1-30)."),
        ),
    ),
    Endpoint(
        key="tiktok_user_followers",
        namespace="tiktok",
        method="user_followers",
        http="POST",
        path="/api/v1/tiktok/user/followers",
        summary="Followers of a TikTok user.",
        params=(
            _req("sec_user_id", "TikTok sec_user_id."),
            _int("count", "Results per page (1-20)."),
            _str("page_token", "Pagination token from a prior response."),
            _int("min_time", "Minimum timestamp cursor."),
        ),
    ),
    Endpoint(
        key="tiktok_user_followings",
        namespace="tiktok",
        method="user_followings",
        http="POST",
        path="/api/v1/tiktok/user/followings",
        summary="Accounts a TikTok user follows.",
        params=(
            _req("sec_user_id", "TikTok sec_user_id."),
            _int("count", "Results per page (1-20)."),
            _str("page_token", "Pagination token from a prior response."),
            _int("min_time", "Minimum timestamp cursor."),
        ),
    ),
    # TikTok depth endpoints (2026-10). These return TikTok's raw payload: large
    # numeric ids can lose precision as JSON numbers, so use id_str / sec_uid.
    Endpoint(
        key="tiktok_trending_searches",
        namespace="tiktok",
        method="trending_searches",
        http="POST",
        path="/api/v1/tiktok/trending/searches",
        summary="Search terms trending on TikTok now (about 90 per call, US-weighted, no region filter).",
        params=(),
    ),
    Endpoint(
        key="tiktok_trending_videos",
        namespace="tiktok",
        method="trending_videos",
        http="POST",
        path="/api/v1/tiktok/trending/videos",
        summary=(
            "A sample of videos trending on TikTok now, with author, stats, sound and hashtags. "
            "Each call returns about 6 videos whatever count is set; call again for a fresh "
            "sample. No region filter."
        ),
        params=(
            _int("count", "Requested videos (1-15, server default 15); about 6 come back per call."),
        ),
    ),
    Endpoint(
        key="tiktok_search_suggestions",
        namespace="tiktok",
        method="search_suggestions",
        http="POST",
        path="/api/v1/tiktok/search/suggestions",
        summary=(
            "TikTok search autocomplete suggestions for a keyword. Long-tail keywords can "
            "return none, which is still a billed answer."
        ),
        params=(
            _req("keyword", "Seed keyword (1-500 characters)."),
        ),
    ),
    Endpoint(
        key="tiktok_music",
        namespace="tiktok",
        method="music",
        http="POST",
        path="/api/v1/tiktok/music",
        summary=(
            "A TikTok sound by id: title, artist, album, duration, how many videos use it, "
            "original vs commercial, play URL, cover, and chart rank when charting."
        ),
        params=(
            _req("music_id", "The sound's numeric id (as a string)."),
        ),
    ),
    Endpoint(
        key="tiktok_music_videos",
        namespace="tiktok",
        method="music_videos",
        http="POST",
        path="/api/v1/tiktok/music/videos",
        summary="Videos that use a TikTok sound, about 14 per page (count is ignored upstream).",
        params=(
            _req("music_id", "The sound's numeric id (as a string)."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Videos per page (1-30); ignored upstream."),
        ),
    ),
    Endpoint(
        key="tiktok_search_music",
        namespace="tiktok",
        method="search_music",
        http="POST",
        path="/api/v1/tiktok/search/music",
        summary="Search TikTok sounds by keyword: id, title, artist, duration, usage count and play URL.",
        params=(
            _req("keyword", "Search query (1-500 characters)."),
            _str("cursor", "Pagination offset (the previous response's cursor, default '0')."),
            _int("count", "Sounds per page (1-20)."),
        ),
    ),
    Endpoint(
        key="tiktok_music_chart",
        namespace="tiktok",
        method="music_chart",
        http="POST",
        path="/api/v1/tiktok/music/chart",
        summary="TikTok's Top 50 or Viral 50 sound chart, with each sound's details and trend. One global chart.",
        params=(
            _lit("chart", ("top", "viral"), "'top' = Top 50 (server default), 'viral' = Viral 50."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Sounds per page (1-50)."),
        ),
    ),
    Endpoint(
        key="tiktok_user_similar",
        namespace="tiktok",
        method="user_similar",
        http="POST",
        path="/api/v1/tiktok/user/similar",
        summary=(
            "Creators similar to a TikTok user (about 30 per page), with follower, following, "
            "video and like counts, bio and verification."
        ),
        params=(
            _req("sec_user_id", "TikTok sec_user_id."),
            _str("page_token", "next_page_token from a prior response."),
        ),
    ),
    Endpoint(
        key="tiktok_user_playlists",
        namespace="tiktok",
        method="user_playlists",
        http="POST",
        path="/api/v1/tiktok/user/playlists",
        summary=(
            "A TikTok user's playlists (series), with each playlist's id, name, video count "
            "and cover. Accounts without playlists return an empty list."
        ),
        params=(
            _req("sec_user_id", "TikTok sec_user_id."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Playlists per page (1-30)."),
        ),
    ),
    Endpoint(
        key="tiktok_playlist_videos",
        namespace="tiktok",
        method="playlist_videos",
        http="POST",
        path="/api/v1/tiktok/playlist/videos",
        summary="Videos in a TikTok playlist, with pagination.",
        params=(
            _req("playlist_id", "The playlist's numeric id (mixId from user_playlists)."),
            _str("cursor", "Pagination cursor (default '0')."),
            _int("count", "Videos per page (1-30)."),
        ),
    ),
    Endpoint(
        key="tiktok_user_live",
        namespace="tiktok",
        method="user_live",
        http="POST",
        path="/api/v1/tiktok/user/live",
        summary=(
            "Whether a TikTok user is live now: the user, live room status (2 = live, "
            "4 = not live), title, start time and viewer counts. An unknown username is a "
            "billed 404."
        ),
        params=(
            _req("username", "TikTok username, with or without the @."),
        ),
    ),
    Endpoint(
        key="tiktok_user_region",
        namespace="tiktok",
        method="user_region",
        http="POST",
        path="/api/v1/tiktok/user/region",
        summary=(
            "The region a TikTok account is registered in (ISO country code, not the "
            "creator's nationality), plus its user id and sec_user_id. An unknown username "
            "is a 404 and is not billed."
        ),
        params=(
            _req("username", "TikTok username, with or without the @."),
        ),
    ),
    # ============================= Instagram =============================
    Endpoint(
        key="instagram_profile",
        namespace="instagram",
        method="profile",
        http="POST",
        path="/api/v1/instagram/profile",
        summary=(
            'Instagram profile. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=1,
        credits_note=(
            'Typically 1 credit. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_posts",
        namespace="instagram",
        method="user_posts",
        http="POST",
        path="/api/v1/instagram/user/posts",
        summary=(
            'Posts from an Instagram user, about 12 per page; page with data.pagination_token. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-50)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
        credits_note=(
            'Typically 2 credits per page. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_reels",
        namespace="instagram",
        method="user_reels",
        http="POST",
        path="/api/v1/instagram/user/reels",
        summary=(
            'Reels from an Instagram user. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-50)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=1,
        credits_note=(
            'Typically 1 credit (2 the first time a username is looked up). Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_tagged",
        namespace="instagram",
        method="user_tagged",
        http="POST",
        path="/api/v1/instagram/user/tagged",
        summary=(
            'Posts an Instagram user is tagged in. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-50)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=1,
        credits_note=(
            'Typically 1 credit (2 the first time a username is looked up). Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_stories",
        namespace="instagram",
        method="user_stories",
        http="POST",
        path="/api/v1/instagram/user/stories",
        summary=(
            'Active stories for an Instagram user. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_post",
        namespace="instagram",
        method="post",
        http="POST",
        path="/api/v1/instagram/post",
        summary=(
            'An Instagram post. Provide url, media_id, or shortcode.'
        ),
        params=(
            _str("url", "Full Instagram post URL."),
            _str("media_id", "Instagram media id."),
            _str("shortcode", "Instagram shortcode (from the post URL)."),
        ),
        one_of=(("url", "media_id", "shortcode"),),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_post_comments",
        namespace="instagram",
        method="post_comments",
        http="POST",
        path="/api/v1/instagram/post/comments",
        summary=(
            'Comments on an Instagram post; page with next_min_id. Provide shortcode or url.'
        ),
        params=(
            _str("shortcode", "Instagram shortcode (from the post URL)."),
            _str("url", "Full Instagram post URL."),
            _str("cursor", "Pagination cursor from a prior response."),
            _lit("sort_order", ("popular", "newest"), "Comment sort order."),
        ),
        one_of=(("shortcode", "url"),),
        credits=2,
        credits_note=(
            'Typically 2 credits per page. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_comment_replies",
        namespace="instagram",
        method="comment_replies",
        http="POST",
        path="/api/v1/instagram/post/comments/replies",
        summary=(
            'Replies to an Instagram comment.'
        ),
        params=(
            _req("media_id", "Instagram media id."),
            _req("comment_id", "Parent comment id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_search_users",
        namespace="instagram",
        method="search_users",
        http="POST",
        path="/api/v1/instagram/search/users",
        summary=(
            'Search Instagram users by keyword.'
        ),
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Rank token from a prior response (next page)."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits; a request with a cursor costs 8. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_search_hashtags",
        namespace="instagram",
        method="search_hashtags",
        http="POST",
        path="/api/v1/instagram/search/hashtags",
        summary=(
            'Search Instagram hashtags by keyword.'
        ),
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Rank token from a prior response (next page)."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits; a request with a cursor costs 8. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_followers",
        namespace="instagram",
        method="user_followers",
        http="POST",
        path="/api/v1/instagram/user/followers",
        summary=(
            'Followers of an Instagram user; page with next_max_id. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-100)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
        credits_note=(
            'Typically 2 credits per page. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_followings",
        namespace="instagram",
        method="user_followings",
        http="POST",
        path="/api/v1/instagram/user/followings",
        summary=(
            'Accounts an Instagram user follows; page with next_max_id. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-100)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
        credits_note=(
            'Typically 2 credits per page. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_highlights",
        namespace="instagram",
        method="user_highlights",
        http="POST",
        path="/api/v1/instagram/user/highlights",
        summary=(
            "An Instagram user's story highlights (id, title, cover, item count). Provide username or user_id."
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_highlight_stories",
        namespace="instagram",
        method="highlight_stories",
        http="POST",
        path="/api/v1/instagram/highlight/stories",
        summary=(
            'Every story saved in one Instagram highlight, with media URLs.'
        ),
        params=(
            _req("highlight_id", "Highlight id from user_highlights, with or without the highlight: prefix (e.g. 'highlight:18149897764550869')."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_search_reels",
        namespace="instagram",
        method="search_reels",
        http="POST",
        path="/api/v1/instagram/search/reels",
        summary=(
            'Search Instagram Reels by keyword.'
        ),
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor (pagination_token) from a prior response."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits per page. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_search_music",
        namespace="instagram",
        method="search_music",
        http="POST",
        path="/api/v1/instagram/search/music",
        summary=(
            'Search Instagram audio tracks by song or artist; returns the id that music_posts takes.'
        ),
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_music_posts",
        namespace="instagram",
        method="music_posts",
        http="POST",
        path="/api/v1/instagram/music/posts",
        summary=(
            'The Reels that use an Instagram audio track, plus its total reel count.'
        ),
        params=(
            _req("music_id", "Numeric audio id (the id field from search_music)."),
            _str("cursor", "Pagination cursor (paging_info.max_id) from a prior response."),
        ),
        credits=1,
        credits_note=(
            'Typically 1 credit per page. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_search_locations",
        namespace="instagram",
        method="search_locations",
        http="POST",
        path="/api/v1/instagram/search/locations",
        summary=(
            'Search Instagram places by name (id, name, address, coordinates).'
        ),
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
        ),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_user_similar",
        namespace="instagram",
        method="user_similar",
        http="POST",
        path="/api/v1/instagram/user/similar",
        summary=(
            'Accounts similar to an Instagram user. Available for most creator accounts; some brand accounts return none. Provide username or user_id.'
        ),
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    Endpoint(
        key="instagram_post_likers",
        namespace="instagram",
        method="post_likers",
        http="POST",
        path="/api/v1/instagram/post/likers",
        summary=(
            'Accounts that liked an Instagram post (up to about 1,000 per post) and its total like count. Provide shortcode or url.'
        ),
        params=(
            _str("shortcode", "Instagram shortcode (from the post URL)."),
            _str("url", "Full Instagram post URL."),
        ),
        one_of=(("shortcode", "url"),),
        credits=2,
        credits_note=(
            'Typically 2 credits. Any request can cost up to 10 when it needs extra work; credits_used in the response is the exact charge.'
        ),
    ),
    # =============================== X ===================================
    Endpoint(
        key="x_search",
        namespace="x",
        method="search",
        http="POST",
        path="/api/v1/x/search",
        summary="Search tweets and people.",
        params=(
            _req("search", "Search query (1-500 characters)."),
            _lit(
                "search_type",
                ("Top", "Latest", "People", "Photos", "Videos"),
                "Result category (server default 'Top').",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_tweet",
        namespace="x",
        method="tweet",
        http="POST",
        path="/api/v1/x/tweet",
        summary="Full details for a single tweet.",
        params=(_req("tweet_id", "Tweet id."),),
    ),
    Endpoint(
        key="x_tweet_comments",
        namespace="x",
        method="tweet_comments",
        http="POST",
        path="/api/v1/x/tweet/comments",
        summary="Replies to a tweet (ranked or chronological).",
        params=(
            _req("tweet_id", "Tweet id."),
            _lit("rank", ("top", "latest"), "'top' (ranked) or 'latest' (chronological); server default 'top'."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_tweet_retweeters",
        namespace="x",
        method="tweet_retweeters",
        http="POST",
        path="/api/v1/x/tweet/retweeters",
        summary="Users who retweeted a tweet.",
        params=(
            _req("tweet_id", "Tweet id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_user",
        namespace="x",
        method="user",
        http="POST",
        path="/api/v1/x/user",
        summary="Profile details for a user.",
        params=(_req("screen_name", "An X handle (without the @)."),),
    ),
    Endpoint(
        key="x_user_tweets",
        namespace="x",
        method="user_tweets",
        http="POST",
        path="/api/v1/x/user/tweets",
        summary="A user's tweets.",
        params=(
            _req("screen_name", "An X handle (without the @)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_user_replies",
        namespace="x",
        method="user_replies",
        http="POST",
        path="/api/v1/x/user/replies",
        summary="A user's tweets and replies.",
        params=(
            _req("screen_name", "An X handle (without the @)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_user_media",
        namespace="x",
        method="user_media",
        http="POST",
        path="/api/v1/x/user/media",
        summary="A user's media tweets.",
        params=(
            _req("screen_name", "An X handle (without the @)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_user_followers",
        namespace="x",
        method="user_followers",
        http="POST",
        path="/api/v1/x/user/followers",
        summary="A user's followers.",
        params=(
            _req("screen_name", "An X handle (without the @)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_user_followings",
        namespace="x",
        method="user_followings",
        http="POST",
        path="/api/v1/x/user/followings",
        summary="Accounts a user follows.",
        params=(
            _req("screen_name", "An X handle (without the @)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_trending",
        namespace="x",
        method="trending",
        http="POST",
        path="/api/v1/x/trending",
        summary="Trending topics for a country.",
        params=(_str("country", "Country name (server default 'UnitedStates')."),),
    ),
    Endpoint(
        key="x_search_communities",
        namespace="x",
        method="search_communities",
        http="POST",
        path="/api/v1/x/search/communities",
        summary="Find X Communities by keyword, with member counts, topic and NSFW flag.",
        params=(
            _req("keyword", "Search query (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    Endpoint(
        key="x_community",
        namespace="x",
        method="community",
        http="POST",
        path="/api/v1/x/community",
        summary="An X Community: name, description, creation date, member count, topic and rules.",
        params=(_req("community_id", "Numeric X Community id (as a string)."),),
    ),
    Endpoint(
        key="x_community_tweets",
        namespace="x",
        method="community_tweets",
        http="POST",
        path="/api/v1/x/community/tweets",
        summary="Posts in an X Community, by relevance or recency, with pagination.",
        params=(
            _req("community_id", "Numeric X Community id (as a string)."),
            _lit("ranking", ("Relevance", "Recency"), "Ordering; server default is the community's own."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
    ),
    # =============================== LinkedIn ============================
    # The provider retired the `linkedin/web/*` namespace it was built on; these
    # now run on `linkedin/web_v2/*`, which is URL-native. Public params are
    # unchanged (the permalink is built server-side) and `url` is accepted
    # everywhere as a direct alternative. Credits are set per endpoint:
    # profile, company and single-post reads are 1, the paginated list endpoints
    # are 10 per page, and job detail is 30.
    # Five endpoints are retired and always return HTTP 410 unbilled;
    # they are kept so existing code fails loudly rather than silently vanishing.
    Endpoint(
        key="linkedin_person",
        namespace="linkedin",
        method="person",
        http="POST",
        path="/api/v1/linkedin/person",
        summary=(
            "Full profile for a LinkedIn member, including about text, experience, education, "
            "honours and links. Provide username or url."
        ),
        params=(
            _str("username", "Public identifier (vanity handle)."),
            _str("url", "Full LinkedIn profile URL, as an alternative to username."),
        ),
        one_of=(("username", "url"),),
    ),
    Endpoint(
        key="linkedin_person_about",
        namespace="linkedin",
        method="person_about",
        http="POST",
        path="/api/v1/linkedin/person/about",
        summary=(
            "About/overview metadata for a member: summary, experience, education, honours and "
            "links. Provide username or url."
        ),
        params=(
            _str("username", "Public identifier (vanity handle)."),
            _str("url", "Full LinkedIn profile URL, as an alternative to username."),
        ),
        one_of=(("username", "url"),),
    ),
    Endpoint(
        key="linkedin_person_posts",
        namespace="linkedin",
        method="person_posts",
        http="POST",
        path="/api/v1/linkedin/person/posts",
        summary=(
            "A member's posts, or the posts they commented on or reacted to. 50 per page; "
            "paginate by passing the previous response's next_cursor. Provide username or url. "
            "Costs 10 credits per page."
        ),
        params=(
            _str("username", "Public identifier (vanity handle)."),
            _str("url", "Full LinkedIn profile URL, as an alternative to username."),
            _lit(
                "type",
                ("posts", "comments", "reactions"),
                "Which feed to return: the member's own posts (default), posts they commented on, "
                "or posts they reacted to.",
            ),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
        ),
        one_of=(("username", "url"),),
        credits=10,
    ),
    Endpoint(
        key="linkedin_person_contact",
        namespace="linkedin",
        method="person_contact",
        http="POST",
        path="/api/v1/linkedin/person/contact",
        summary=(
            "RETIRED: contact-info scraping was withdrawn. This endpoint "
            "always returns HTTP 410 and is never billed."
        ),
        params=(_str("username", "Public identifier (vanity handle)."),),
        credits=0,
    ),
    Endpoint(
        key="linkedin_company",
        namespace="linkedin",
        method="company",
        http="POST",
        path="/api/v1/linkedin/company",
        summary=(
            "Profile for a LinkedIn company, including locations, specialties, similar and "
            "affiliated companies. Provide company or url."
        ),
        params=(
            _str("company", "Company universal name (slug)."),
            _str("url", "Full LinkedIn company URL, as an alternative to company."),
        ),
        one_of=(("company", "url"),),
    ),
    Endpoint(
        key="linkedin_company_posts",
        namespace="linkedin",
        method="company_posts",
        http="POST",
        path="/api/v1/linkedin/company/posts",
        summary=(
            "A company's recent posts. 50 per page; paginate by passing the previous response's "
            "next_cursor. Provide company or url. Costs 10 credits per page."
        ),
        params=(
            _str("company", "Company universal name (slug)."),
            _str("url", "Full LinkedIn company URL, as an alternative to company."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
        ),
        one_of=(("company", "url"),),
        credits=10,
    ),
    Endpoint(
        key="linkedin_company_people",
        namespace="linkedin",
        method="company_people",
        http="POST",
        path="/api/v1/linkedin/company/people",
        summary=(
            "RETIRED: the employee directory was withdrawn. This endpoint "
            "always returns HTTP 410 and is never billed. company() returns featured_employees, a "
            "small sample of staff profiles."
        ),
        params=(
            _str("company_id", "Numeric company id."),
            _str("company", "Company slug or url."),
        ),
        credits=0,
    ),
    Endpoint(
        key="linkedin_company_jobs",
        namespace="linkedin",
        method="company_jobs",
        http="POST",
        path="/api/v1/linkedin/company/jobs",
        summary=(
            "RETIRED: per-company job listings were withdrawn. This "
            "endpoint always returns HTTP 410 and is never billed. Use search_jobs() with the "
            "company name as the search term."
        ),
        params=(
            _str("company_id", "Numeric company id."),
            _str("company", "Company slug or url."),
        ),
        credits=0,
    ),
    Endpoint(
        key="linkedin_search_people",
        namespace="linkedin",
        method="search_people",
        http="POST",
        path="/api/v1/linkedin/search/people",
        summary=(
            "RETIRED: people search was withdrawn. This endpoint always "
            "returns HTTP 410 and is never billed."
        ),
        params=(
            _str("search", "Name to search for."),
            _str("title", "Job title filter."),
            _str("company", "Company filter."),
            _str("school", "School filter."),
            _str("location", "A geo name or id to filter by."),
        ),
        credits=0,
    ),
    Endpoint(
        key="linkedin_search_jobs",
        namespace="linkedin",
        method="search_jobs",
        http="POST",
        path="/api/v1/linkedin/search/jobs",
        summary=(
            "Search for jobs by keyword and optional location. 25 per page; paginate with "
            "next_cursor. The provider rotates its result set, so pages overlap slightly and "
            "repeat calls return different listings - dedupe by job id. Costs 10 credits per page."
        ),
        params=(
            _req("search", "Search keyword."),
            _str("location", "Geographic filter; omit to search everywhere."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
        ),
        credits=10,
    ),
    Endpoint(
        key="linkedin_search_posts",
        namespace="linkedin",
        method="search_posts",
        http="POST",
        path="/api/v1/linkedin/search/posts",
        summary=(
            "RETIRED: post search was withdrawn. This endpoint always "
            "returns HTTP 410 and is never billed."
        ),
        params=(_str("search", "Search keyword."),),
        credits=0,
    ),
    Endpoint(
        key="linkedin_job",
        namespace="linkedin",
        method="job",
        http="POST",
        path="/api/v1/linkedin/job",
        summary=(
            "Full details for a single job listing, including the hiring company. Provide job_id "
            "or url. Costs 30 credits. A listing with no detail record upstream returns an "
            "unbilled 404, which happens for roughly one job id in five returned by search_jobs."
        ),
        params=(
            _str("job_id", "Job id."),
            _str("url", "Full LinkedIn job URL, as an alternative to job_id."),
        ),
        one_of=(("job_id", "url"),),
        credits=30,
    ),
    Endpoint(
        key="linkedin_post",
        namespace="linkedin",
        method="post",
        http="POST",
        path="/api/v1/linkedin/post",
        summary="Full details for a single post, including its top visible comments. Provide post_id or url.",
        params=(
            _str("post_id", "Post id or activity urn."),
            _str("url", "Full LinkedIn post URL, as an alternative to post_id."),
        ),
        one_of=(("post_id", "url"),),
    ),
    Endpoint(
        key="linkedin_post_comments",
        namespace="linkedin",
        method="post_comments",
        http="POST",
        path="/api/v1/linkedin/post/comments",
        summary=(
            "Comments on a post with their replies. Paginate with a 1-based page; page size "
            "varies, so keep going until a page comes back empty. Provide post_id or url. "
            "Costs 10 credits per page."
        ),
        params=(
            _str("post_id", "Post id or activity urn."),
            _str("url", "Full LinkedIn post URL, as an alternative to post_id."),
            _int("page", "1-based page number, 10 comments per page."),
        ),
        one_of=(("post_id", "url"),),
        credits=10,
    ),
    # ============================ TikTok Shop ============================
    Endpoint(
        key="tiktok_shop_search",
        namespace="tiktok_shop",
        method="search",
        http="POST",
        path="/api/v1/tiktok-shop/search",
        summary=(
            "Search TikTok Shop products by keyword (US catalog). Returns up to 30 products per "
            "page with exact prices, ratings and shop details. Paginate with next_cursor and dedupe "
            "by product_id across pages. Product ids returned here are not guaranteed to resolve on "
            "product(): only about 44% do, so treat search as a listing source, not the first leg of "
            "a search-then-detail pipeline."
        ),
        params=(
            _req("search", "Search keyword (1-200 characters)."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
        ),
    ),
    Endpoint(
        key="tiktok_shop_search_suggestions",
        namespace="tiktok_shop",
        method="search_suggestions",
        http="POST",
        path="/api/v1/tiktok-shop/search/suggestions",
        summary=(
            "Keyword autocomplete and expansion for a partial query, across 8 marketplace regions. "
            "Suggestions are not guaranteed prefix matches: a misspelling returns typo corrections, "
            "and results can include brand and shop names."
        ),
        params=(
            _req("search", "Partial search keyword (1-100 characters)."),
            _lit(
                "region",
                _TIKTOK_SHOP_REGIONS,
                "Marketplace region (server default 'US').",
            ),
        ),
    ),
    Endpoint(
        key="tiktok_shop_product",
        namespace="tiktok_shop",
        method="product",
        http="POST",
        path="/api/v1/tiktok-shop/product",
        summary=(
            "Full product detail: description, images, variants with stock, shipping, shop profile, "
            "category path and top reviews. This endpoint does NOT return a price -- upstream masks it "
            "on the product page -- so read exact prices from search(), shop_products() or "
            "category_products() instead. It also resolves only about 44% of the product ids returned "
            "by search(): upstream has no detail data for the rest, so an HTTP 404 is a normal outcome "
            "rather than an error and must not be retried.\n"
            "\n"
            "        The SDK raises NotFoundError on that 404 -- there is no data field in the response "
            "body to test -- so a loop over search() ids must catch it or it dies on the first miss:\n"
            "\n"
            "            from scavio import NotFoundError\n"
            "\n"
            "            for product_id in product_ids:\n"
            "                try:\n"
            "                    detail = client.tiktok_shop.product(product_id)\n"
            "                except NotFoundError:\n"
            "                    continue  # no detail upstream; skip it, do not retry\n"
            "\n"
            "        product_reviews() often works for ids product() cannot resolve: of 8 such ids "
            "tested, 8 returned HTTP 200 and 7 carried at least one review, so it is a useful "
            "fallback source of product detail."
        ),
        params=(
            _req("product_id", "TikTok Shop product id (6-25 digits)."),
            _lit(
                "region",
                _TIKTOK_SHOP_REGIONS,
                "Marketplace region (server default 'US').",
            ),
        ),
    ),
    Endpoint(
        key="tiktok_shop_product_reviews",
        namespace="tiktok_shop",
        method="product_reviews",
        http="POST",
        path="/api/v1/tiktok-shop/product/reviews",
        summary=(
            "Paginated product reviews with text, images, star histogram and verified-purchase flags, "
            "up to 200 per call. total_reviews drifts between calls and must not be used to compute a "
            "page count; page with has_more instead."
        ),
        params=(
            _req("product_id", "TikTok Shop product id (6-25 digits)."),
            _int("page", "1-based page number (1-500; server default 1)."),
            _int("page_size", "Reviews per page (1-200; server default 20)."),
            _lit(
                "sort",
                ("relevant", "recent"),
                "'relevant' returns text-complete, image-heavy reviews; 'recent' is fresher but far more text-sparse. Server default 'relevant'.",
            ),
            _int("rating", "Only reviews with this star rating (1-5)."),
            _bool("has_media", "Only reviews with a photo or video."),
            _bool("verified_only", "Only verified purchases. Ignored when has_media is True (upstream allows one filter at a time)."),
            _lit(
                "region",
                _TIKTOK_SHOP_REGIONS,
                "Marketplace region (server default 'US').",
            ),
        ),
    ),
    Endpoint(
        key="tiktok_shop_categories",
        namespace="tiktok_shop",
        method="categories",
        http="POST",
        path="/api/v1/tiktok-shop/categories",
        summary=(
            "The global TikTok Shop category tree: 28 top-level categories, 240 nodes, two levels deep. "
            "Category ids are identical in every region and names are always English. Takes no parameters."
        ),
    ),
    Endpoint(
        key="tiktok_shop_category_products",
        namespace="tiktok_shop",
        method="category_products",
        http="POST",
        path="/api/v1/tiktok-shop/category/products",
        summary=(
            "Products listed under a category id from categories(), with exact prices. Page size is "
            "inconsistent upstream (15 to 20 per page), so always paginate with next_cursor rather than "
            "assuming a fixed size. Category listings are shallow: after a few pages the source stops "
            "returning new products and has_more turns false, which is the end of the listing rather "
            "than an error."
        ),
        params=(
            _req("category_id", "Category id from categories(); level 1 or 2 both work."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
            _lit(
                "region",
                ("US", "GB"),
                "Marketplace region. Category listings are served for US and GB only (server default 'US').",
            ),
        ),
    ),
    Endpoint(
        key="tiktok_shop_shop_products",
        namespace="tiktok_shop",
        method="shop_products",
        http="POST",
        path="/api/v1/tiktok-shop/shop/products",
        summary=(
            "A shop's product catalog, 30 per page, with exact prices. Shop follower count, location and "
            "shop-level rating are not available here; call product() for the full shop profile."
        ),
        params=(
            _req("shop_id", "TikTok Shop seller id (also called seller_id elsewhere on TikTok)."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
            _lit(
                "region",
                _TIKTOK_SHOP_REGIONS,
                "Marketplace region (server default 'US').",
            ),
        ),
    ),
    Endpoint(
        key="tiktok_shop_resolve",
        namespace="tiktok_shop",
        method="resolve",
        http="POST",
        path="/api/v1/tiktok-shop/resolve",
        summary=(
            "Resolve any TikTok Shop URL or share link to a product_id or shop_id, ready to pass to the "
            "other methods. Accepts canonical product and store pages, tiktok.com/view links, affiliate "
            "share links and vt.tiktok.com short links."
        ),
        params=(_req("url", "A TikTok Shop URL or share link."),),
    ),
    # ============================== Walmart ==============================
    # `device` is the only retired param: the API answers 200 with a top-level
    # `warnings` array if it is sent. delivery_zip + store_id came back in 0.17:
    # passed TOGETHER on search/product they target one store (walmart.com or
    # walmart.ca), and `stores` turns a ZIP / postal code into the store_ids.
    #
    # BODY-PRICED: a store-targeted search/product costs 2 on any domain;
    # otherwise walmartCreditCost(domain) - com=1, ca=1, com.mx=2, and only
    # /search and /category accept that domain. credits_note carries the rule
    # into the generated docstring so it never claims a flat price.
    Endpoint(
        key="walmart_search",
        namespace="walmart",
        method="search",
        http="POST",
        path="/api/v1/walmart/search",
        summary=(
            "Search Walmart and get structured product rows (products, products_count and the "
            "store the results were priced against). Pass delivery_zip + store_id to get one "
            "store's assortment and availability (walmart.com and walmart.ca)."
        ),
        params=(
            _req("query", "Product search query (1-500 characters)."),
            _lit(
                "domain",
                ("com", "ca", "com.mx"),
                "Marketplace: 'com' (US, default, 1 credit), 'ca' (1 credit), 'com.mx' "
                "(2 credits). Sets the currency and product URLs of the response.",
            ),
            _int("page", "Results page, 1-based (integer >= 1). One page per call."),
            _int("start_page", "Deprecated alias for page; send page instead."),
            _lit(
                "sort_by",
                (
                    "best_match",
                    "price_low",
                    "price_high",
                    "best_seller",
                    "rating_high",
                    "new",
                ),
                "Result sort order. Defaults to 'best_match'.",
            ),
            # Backend is z.number() (not int): decimals are accepted.
            _float(
                "min_price",
                "Minimum price filter in the marketplace's own currency; decimals allowed (e.g. "
                "19.99).",
            ),
            _float(
                "max_price",
                "Maximum price filter in the marketplace's own currency; decimals allowed (e.g. "
                "199.5).",
            ),
            _lit(
                "fulfillment_speed",
                ("today", "tomorrow"),
                "Only items deliverable today, or by tomorrow. '2_days' and 'anytime' are not "
                "accepted - for anytime, omit this parameter.",
            ),
            _lit(
                "fulfillment_type",
                ("in_store",),
                "Set to 'in_store' to return only items available for in-store pickup.",
            ),
            _str(
                "delivery_zip",
                "Shopper's postal code for store targeting: a 5-digit US ZIP, or a Canadian "
                "postal code (e.g. 'M5V 2T6') with domain 'ca'. Must be passed together with "
                "store_id.",
            ),
            _str_or_int(
                "store_id",
                "Walmart store to price and stock against, from walmart.stores() on the same "
                "domain (e.g. '1389'). Must be passed together with delivery_zip; the store "
                "used is echoed in data.location. Store-targeted calls cost 2 credits and take "
                "10-60 seconds.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 2 credits when store-targeted (delivery_zip + store_id, domain 'com' or 'ca'); "
            "otherwise 1 credit on domain 'com' or 'ca' and 2 credits on 'com.mx' - the price is "
            "a function of the request body, not a constant for the route."
        ),
    ),
    Endpoint(
        key="walmart_product",
        namespace="walmart",
        method="product",
        http="POST",
        path="/api/v1/walmart/product",
        summary=(
            "Full detail for a single Walmart product: price, rating, images, specifications, "
            "availability and seller. Pass delivery_zip + store_id for one store's view; "
            "domain 'ca' (walmart.ca) is only available together with that store pair."
        ),
        params=(
            _req("product_id", "Walmart item id (usItemId), e.g. '13544111159'."),
            _lit(
                "domain",
                ("com", "ca"),
                "Marketplace: 'com' (US, default) or 'ca'. 'ca' requires delivery_zip + "
                "store_id.",
            ),
            _str(
                "delivery_zip",
                "Shopper's postal code for store targeting: a 5-digit US ZIP, or a Canadian "
                "postal code (e.g. 'M5V 2T6') with domain 'ca'. Must be passed together with "
                "store_id.",
            ),
            _str_or_int(
                "store_id",
                "Walmart store to price and stock against, from walmart.stores() on the same "
                "domain (e.g. '1389'). Must be passed together with delivery_zip; the store "
                "used is echoed in data.location. Store-targeted calls cost 2 credits and take "
                "10-60 seconds.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit, or 2 credits when store-targeted (delivery_zip + store_id)."
        ),
    ),
    Endpoint(
        key="walmart_stores",
        namespace="walmart",
        method="stores",
        http="POST",
        path="/api/v1/walmart/stores",
        summary=(
            "Walmart stores near a US ZIP code (walmart.com) or Canadian postal code "
            "(walmart.ca), nearest first, with store_id, name, distance_miles, address, "
            "coordinates and hours. Pass a store_id with delivery_zip to search() or product() "
            "on the same domain to target that store."
        ),
        params=(
            _req(
                "zipcode",
                "A 5-digit US ZIP (e.g. '50036'), or a Canadian postal code (e.g. 'M5V 2T6', "
                "with or without the space) with domain 'ca'.",
            ),
            _lit(
                "domain",
                ("com", "ca"),
                "Marketplace: 'com' (US, default) or 'ca' (Canada). Use the returned store_id "
                "on the same domain.",
            ),
        ),
        credits=1,
        credits_note="Costs 1 credit on either domain.",
    ),
    Endpoint(
        key="walmart_reviews",
        namespace="walmart",
        method="reviews",
        http="POST",
        path="/api/v1/walmart/reviews",
        summary=(
            "Customer reviews for a Walmart product with ratings, text, author, date and the "
            "rating breakdown. 10 reviews per page; paginate with page."
        ),
        params=(
            _req("product_id", "Walmart item id (usItemId), e.g. '13544111159'."),
            _int("page", "Reviews page, 1-based (integer >= 1). 10 reviews per page."),
            _lit(
                "sort",
                (
                    "relevancy",
                    "submission-desc",
                    "submission-asc",
                    "rating-desc",
                    "rating-asc",
                    "helpful-desc",
                ),
                "Review sort order. Omit for Walmart's own default ordering.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Walmart is body-priced through `domain`, but this endpoint takes no "
            "domain, so it is always 1."
        ),
    ),
    Endpoint(
        key="walmart_category",
        namespace="walmart",
        method="category",
        http="POST",
        path="/api/v1/walmart/category",
        summary=(
            "Products within a Walmart category, in the same product shape as search. Costs 1 "
            "credit on domain 'com' or 'ca' and 2 credits on 'com.mx'; `limit` trims the "
            "response after fetching and never reduces the cost."
        ),
        params=(
            _req(
                "category_id",
                "Walmart category id: either a leaf id ('1095191') or the full "
                "underscore-joined path ('3944_133251_1095191'). Both are accepted.",
            ),
            _lit(
                "domain",
                ("com", "ca", "com.mx"),
                "Marketplace: 'com' (US, default, 1 credit), 'ca' (1 credit), 'com.mx' "
                "(2 credits). Sets the currency and product URLs of the response.",
            ),
            _int("page", "Results page, 1-based (integer >= 1). One page per call."),
            _int(
                "limit",
                "Trim the returned products to at most this many (integer >= 1). Applied after "
                "fetching, so it does not reduce the credit cost of the call.",
            ),
            _lit(
                "sort_by",
                (
                    "best_match",
                    "price_low",
                    "price_high",
                    "best_seller",
                    "rating_high",
                    "new",
                ),
                "Result sort order. Defaults to 'best_match'.",
            ),
            _float(
                "min_price",
                "Minimum price filter in the marketplace's own currency; decimals allowed (e.g. "
                "19.99).",
            ),
            _float(
                "max_price",
                "Maximum price filter in the marketplace's own currency; decimals allowed (e.g. "
                "199.5).",
            ),
            _lit(
                "fulfillment_speed",
                ("today", "tomorrow"),
                "Only items deliverable today, or by tomorrow. '2_days' and 'anytime' are not "
                "accepted - for anytime, omit this parameter.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit on domain 'com' or 'ca' and 2 credits on 'com.mx' - the price is a "
            "function of the request body, not a constant for the route."
        ),
    ),
    Endpoint(
        key="walmart_offers",
        namespace="walmart",
        method="offers",
        http="POST",
        path="/api/v1/walmart/offers",
        summary=(
            "The buy-box offer for a Walmart product: price, seller, condition and buy-box flag. "
            "BUY-BOX SELLER ONLY - this is not the full offer list, and there is no way to page "
            "through the other sellers."
        ),
        params=(
            _req("product_id", "Walmart item id (usItemId), e.g. '2979510112'."),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Walmart is body-priced through `domain`, but this endpoint takes no "
            "domain, so it is always 1."
        ),
    ),
    Endpoint(
        key="walmart_seller",
        namespace="walmart",
        method="seller",
        http="POST",
        path="/api/v1/walmart/seller",
        summary=(
            "Marketplace seller storefront: name, rating, review count, Pro Seller badge and "
            "business details."
        ),
        params=(
            _req(
                "seller_id",
                "Numeric Walmart catalog seller id, as returned in `seller_catalog_id` on a "
                "product, search or offers response (e.g. '101480084'). The GUID `seller_id` is "
                "not accepted here - it 404s.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Walmart is body-priced through `domain`, but this endpoint takes no "
            "domain, so it is always 1."
        ),
    ),
    Endpoint(
        key="walmart_seller_products",
        namespace="walmart",
        method="seller_products",
        http="POST",
        path="/api/v1/walmart/seller-products",
        summary=(
            "A marketplace seller's catalog. Roughly the first 40 items are server-rendered and "
            "returned; total_count reports the seller's real catalog size. There is no "
            "pagination - the rest of the catalog is not reachable."
        ),
        params=(
            _req(
                "seller_id",
                "Numeric Walmart catalog seller id, as returned in `seller_catalog_id` on a "
                "product, search or offers response (e.g. '101480084'). The GUID `seller_id` "
                "404s.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Walmart is body-priced through `domain`, but this endpoint takes no "
            "domain, so it is always 1."
        ),
    ),
    # ============================== Threads ==============================
    # BODY-PRICED: threadsCreditCost(hasUsername) - 2 credits addressed by
    # user_id, 4 by username, because a handle buys a second lookup. Only profile / user_posts / user_replies are
    # username-keyed; the other three are always 2. Sending both identifiers
    # bills the cheap rate (the route only charges 4 when user_id is absent).
    # credits_note carries that rule into the generated docstring on the three
    # username-keyed endpoints so it never claims a flat price.
    #
    # There is NO Threads content search. search_users (people search) is the only search.
    Endpoint(
        key="threads_profile",
        namespace="threads",
        method="profile",
        http="POST",
        path="/api/v1/threads/profile",
        summary=(
            "Profile details for a Threads user. Costs 2 credits addressed by user_id and 4 by "
            "username; pass user_id whenever you have it."
        ),
        params=(
            _str(
                "user_id",
                "Numeric Threads user id, e.g. '63625256886'. The cheap path: 2 credits.",
            ),
            _str(
                "username",
                "Threads handle without the @ (1-60 characters). Costs 2 extra credits (4 "
                "total): the handle is resolved through "
                "people search first. Pass user_id instead to avoid that.",
            ),
        ),
        one_of=(("user_id", "username"),),
        credits=2,
        credits_note=(
            "Costs 2 credits addressed by user_id and 4 credits addressed by username - the price "
            "is a function of the request body, not a constant for the route."
        ),
    ),
    Endpoint(
        key="threads_user_posts",
        namespace="threads",
        method="user_posts",
        http="POST",
        path="/api/v1/threads/user/posts",
        summary=(
            "A user's Threads posts, cursor-paginated via next_cursor. Costs 2 credits addressed "
            "by user_id and 4 by username."
        ),
        params=(
            _str(
                "user_id",
                "Numeric Threads user id, e.g. '63625256886'. The cheap path: 2 credits.",
            ),
            _str(
                "username",
                "Threads handle without the @ (1-60 characters). Costs 2 extra credits (4 "
                "total) because the handle has to be resolved through people search first.",
            ),
            _str(
                "cursor",
                "Pagination cursor from a prior response's next_cursor. Omit for the first page.",
            ),
        ),
        one_of=(("user_id", "username"),),
        credits=2,
        credits_note=(
            "Costs 2 credits addressed by user_id and 4 credits addressed by username - the price "
            "is a function of the request body, not a constant for the route."
        ),
    ),
    Endpoint(
        key="threads_user_replies",
        namespace="threads",
        method="user_replies",
        http="POST",
        path="/api/v1/threads/user/replies",
        summary=(
            "A user's Threads replies, cursor-paginated via next_cursor. Costs 2 credits "
            "addressed by user_id and 4 by username."
        ),
        params=(
            _str(
                "user_id",
                "Numeric Threads user id, e.g. '63625256886'. The cheap path: 2 credits.",
            ),
            _str(
                "username",
                "Threads handle without the @ (1-60 characters). Costs 2 extra credits (4 "
                "total) because the handle has to be resolved through people search first.",
            ),
            _str(
                "cursor",
                "Pagination cursor from a prior response's next_cursor. Omit for the first page.",
            ),
        ),
        one_of=(("user_id", "username"),),
        credits=2,
        credits_note=(
            "Costs 2 credits addressed by user_id and 4 credits addressed by username - the price "
            "is a function of the request body, not a constant for the route."
        ),
    ),
    Endpoint(
        key="threads_post",
        namespace="threads",
        method="post",
        http="POST",
        path="/api/v1/threads/post",
        summary="A single Threads post, addressed by post_id or by its threads.net URL.",
        params=(
            _str("post_id", "Threads post id, e.g. '3349029093483693129'."),
            _str(
                "url",
                "Full threads.net post URL (e.g. 'https://www.threads.net/@natgeo/post/C8xY'), "
                "as an alternative to post_id.",
            ),
        ),
        one_of=(("post_id", "url"),),
        credits=2,
        credits_note=(
            "Costs 2 credits. Threads is body-priced by identifier, but this endpoint has no "
            "username form, so it is always 2."
        ),
    ),
    Endpoint(
        key="threads_post_comments",
        namespace="threads",
        method="post_comments",
        http="POST",
        path="/api/v1/threads/post/comments",
        summary=(
            "Replies to a Threads post, cursor-paginated via next_cursor. Post-keyed only: "
            "there is no username form, so this endpoint always costs 2 credits."
        ),
        params=(
            _req("post_id", "Threads post id, e.g. '3349029093483693129'."),
            _str(
                "cursor",
                "Pagination cursor from a prior response's next_cursor. Omit for the first page.",
            ),
        ),
        credits=2,
        credits_note=(
            "Costs 2 credits. Threads is body-priced by identifier, but this endpoint has no "
            "username form, so it is always 2."
        ),
    ),
    Endpoint(
        key="threads_search_users",
        namespace="threads",
        method="search_users",
        http="POST",
        path="/api/v1/threads/search/users",
        summary=(
            "Search Threads profiles by name or handle. This is the only search Threads exposes "
            "- there is no post or content search - and it returns a single unpaginated page."
        ),
        params=(
            _req("query", "Name or handle to search for (1-200 characters)."),
        ),
        credits=2,
        credits_note=(
            "Costs 2 credits. Threads is body-priced by identifier, but this endpoint has no "
            "username form, so it is always 2."
        ),
    ),
    # ========================== Kuaishou (China) =========================
    Endpoint(
        key="kuaishou_profile",
        namespace="kuaishou",
        method="profile",
        http="POST",
        path="/api/v1/kuaishou/profile",
        summary=(
            "Profile details for a Kuaishou user. Costs 10 credits, the dearest single-object "
            "call on the platform."
        ),
        params=(
            _req(
                "user_id",
                "Kuaishou user id (non-empty); get one from user_resolve or search_users.",
            ),
        ),
        credits=10,
        credits_note=(
            "Costs 10 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_user_posts",
        namespace="kuaishou",
        method="user_posts",
        http="POST",
        path="/api/v1/kuaishou/user/posts",
        summary="A Kuaishou user's top posts, cursor-paginated via next_cursor.",
        params=(
            _req(
                "user_id",
                "Kuaishou user id (non-empty); get one from user_resolve or search_users.",
            ),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_user_live",
        namespace="kuaishou",
        method="user_live",
        http="POST",
        path="/api/v1/kuaishou/user/live",
        summary="A Kuaishou user's current live-stream status. Not paginated.",
        params=(
            _req(
                "user_id",
                "Kuaishou user id (non-empty); get one from user_resolve or search_users.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_user_resolve",
        namespace="kuaishou",
        method="user_resolve",
        http="POST",
        path="/api/v1/kuaishou/user/resolve",
        summary=(
            "Turns a Kuaishou share link into a user id. Only kuaishou.com and v.kuaishou.com "
            "links are accepted; Kwai international (kwai.com) is not served upstream."
        ),
        params=(
            _req(
                "share_link",
                "A kuaishou.com or v.kuaishou.com URL; kwai.com links are rejected.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_video",
        namespace="kuaishou",
        method="video",
        http="POST",
        path="/api/v1/kuaishou/video",
        summary=(
            "A single Kuaishou video by photo id or URL. Provide photo_id or url. "
            "Costs 2 credits."
        ),
        params=(
            _str("photo_id", "Kuaishou photo (video) id, non-empty."),
            _str("url", "Full kuaishou.com video URL, as an alternative to photo_id."),
        ),
        one_of=(("photo_id", "url"),),
        credits=2,
        credits_note=(
            "Costs 2 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_video_comments",
        namespace="kuaishou",
        method="video_comments",
        http="POST",
        path="/api/v1/kuaishou/video/comments",
        summary="Comments on a Kuaishou video, cursor-paginated via next_cursor.",
        params=(
            _req("photo_id", "Kuaishou photo (video) id, non-empty."),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_comment_replies",
        namespace="kuaishou",
        method="comment_replies",
        http="POST",
        path="/api/v1/kuaishou/video/sub-comments",
        summary=(
            "Replies under a root comment on a Kuaishou video, cursor-paginated via next_cursor; "
            "count sizes the page (1-50)."
        ),
        params=(
            _req("photo_id", "Kuaishou photo (video) id, non-empty."),
            _req(
                "root_comment_id",
                "Id of the top-level comment whose replies you want, from video_comments.",
            ),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
            _int("count", "Replies per page, 1-50. Omit to use the upstream default."),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_videos_batch",
        namespace="kuaishou",
        method="videos_batch",
        http="POST",
        path="/api/v1/kuaishou/videos/batch",
        summary=(
            "Several Kuaishou videos in one call, hard-capped at 20 photo ids. Costs 40 credits, "
            "the dearest call on the platform."
        ),
        params=(
            _str_list(
                "photo_ids",
                "Kuaishou photo (video) ids, 1-20 per call; more than 20 is rejected.",
                required=True,
            ),
        ),
        credits=40,
        credits_note=(
            "Costs 40 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_search",
        namespace="kuaishou",
        method="search",
        http="POST",
        path="/api/v1/kuaishou/search",
        summary=(
            "Mixed-result search across Kuaishou, cursor-paginated via next_cursor. "
            "Costs 10 credits per page."
        ),
        params=(
            _req("keyword", "Search keyword, 1-200 characters."),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=10,
        credits_note=(
            "Costs 10 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_search_videos",
        namespace="kuaishou",
        method="search_videos",
        http="POST",
        path="/api/v1/kuaishou/search/videos",
        summary=(
            "Kuaishou video search results, cursor-paginated via next_cursor. "
            "Costs 10 credits per page."
        ),
        params=(
            _req("keyword", "Search keyword, 1-200 characters."),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=10,
        credits_note=(
            "Costs 10 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_search_users",
        namespace="kuaishou",
        method="search_users",
        http="POST",
        path="/api/v1/kuaishou/search/users",
        summary=(
            "Kuaishou user search results, cursor-paginated via next_cursor. "
            "Costs 10 credits per page."
        ),
        params=(
            _req("keyword", "Search keyword, 1-200 characters."),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=10,
        credits_note=(
            "Costs 10 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_search_live",
        namespace="kuaishou",
        method="search_live",
        http="POST",
        path="/api/v1/kuaishou/search/live",
        summary=(
            "Kuaishou live-stream search results, cursor-paginated via next_cursor. "
            "Costs 10 credits per page."
        ),
        params=(
            _req("keyword", "Search keyword, 1-200 characters."),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=10,
        credits_note=(
            "Costs 10 credits. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_tag_feed",
        namespace="kuaishou",
        method="tag_feed",
        http="POST",
        path="/api/v1/kuaishou/tag/feed",
        summary="Posts under a Kuaishou hashtag, cursor-paginated via next_cursor.",
        params=(
            _req("tag", "Hashtag text without the leading '#', 1-200 characters."),
            _str(
                "cursor",
                "Opaque next_cursor from a prior response; omit for the first page.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    Endpoint(
        key="kuaishou_trending",
        namespace="kuaishou",
        method="trending",
        http="POST",
        path="/api/v1/kuaishou/trending",
        summary=(
            "Kuaishou hot / live / shopping / brand / music leaderboards. "
            "One board per call, not paginated."
        ),
        params=(
            _lit(
                "board",
                ("hot", "live", "shopping", "brand", "music"),
                "Leaderboard to return; defaults to 'hot' when omitted.",
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    ),
    # ================================ eBay ===============================
    Endpoint(
        key="ebay_search",
        namespace="ebay",
        method="search",
        http="POST",
        path="/api/v1/ebay/search",
        summary=(
            "Search live or SOLD eBay listings: price, condition, bids, shipping, seller, "
            "feedback. Provide query or seller; per_page accepts only 60, 120 or 240."
        ),
        params=(
            _str(
                "query",
                "Keyword to search (1-500 characters). Optional: a seller-only search pages "
                "that seller's whole catalogue.",
            ),
            _str(
                "seller",
                "Restrict results to one seller's listings (1-64 characters), as in "
                "ebay.com/usr/<name>. Can be sent with no query.",
            ),
            _int("page", "Results page, 1-based."),
            _lit(
                "sort_by",
                ("best_match", "ending_soonest", "newly_listed", "price_low", "price_high"),
                "Result sort order. Defaults to 'best_match'. eBay's 'Distance: nearest first' "
                "is deliberately unsupported (it would not rank by the location of the caller).",
            ),
            _float(
                "min_price",
                "Minimum price, inclusive. Must be 0 or greater.",
            ),
            _float(
                "max_price",
                "Maximum price, inclusive. Must be 0 or greater.",
            ),
            _lit(
                "condition",
                ("new", "open_box", "refurbished", "used", "for_parts"),
                "Item condition filter. 'refurbished' is eBay's parent condition, not one of "
                "its three graded tiers.",
            ),
            _lit(
                "buying_format",
                ("auction", "buy_it_now", "best_offer"),
                "Listing format: auction, fixed price (buy_it_now), or fixed price accepting "
                "offers (best_offer).",
            ),
            _bool("free_shipping", "Only listings with free shipping."),
            _bool(
                "sold",
                "Search completed listings that actually SOLD, for price research. eBay "
                "publishes no headline count on this view, so total_results is null.",
            ),
            _str(
                "category_id",
                "eBay category id; must be numeric (e.g. '112529'). An unrecognised id returns "
                "the UNFILTERED set under a 200.",
            ),
            _ilit(
                "per_page",
                (60, 120, 240),
                "Listings per page: 60, 120 or 240 only. Defaults to 60; eBay silently falls back "
                "to 60 for anything else.",
            ),
        ),
        one_of=(("query", "seller"),),
        credits=1,
    ),
    Endpoint(
        key="ebay_product",
        namespace="ebay",
        method="product",
        http="POST",
        path="/api/v1/ebay/product",
        summary=(
            "One eBay listing in full: price, condition, images, item specifics, shipping, "
            "returns, auction state, seller."
        ),
        params=(
            _req(
                "item_id",
                "eBay item number (e.g. '168591664725'), or a full ebay.com/itm/... listing "
                "URL; tracking parameters on a pasted URL are discarded.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="ebay_seller",
        namespace="ebay",
        method="seller",
        http="POST",
        path="/api/v1/ebay/seller",
        summary=(
            "eBay seller profile card: store name, feedback score and %, items sold, followers, "
            "location, categories. Profile only: page a catalogue with search(seller=...)."
        ),
        params=(
            _req(
                "seller",
                "eBay username as it appears in ebay.com/usr/<name> (1-64 characters), which is "
                "what seller_name on a search or product result returns.",
            ),
        ),
        credits=1,
    ),
    # =============================== Target ==============================
    Endpoint(
        key="target_search",
        namespace="target",
        method="search",
        http="POST",
        path="/api/v1/target/search",
        summary=(
            "Search Target.com, the US retailer: prices, ratings, badges and promotions. "
            "Up to 28 results per page; expect around 9 seconds."
        ),
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _int("page", "Results page, 1-based."),
            _int(
                "count",
                "Results per page, 1-28. Defaults to 24; Target rejects anything above 28 "
                "outright.",
            ),
            _lit(
                "sort",
                (
                    "relevance",
                    "featured",
                    "price_low",
                    "price_high",
                    "rating_high",
                    "best_seller",
                    "newest",
                ),
                "Result sort order. Defaults to 'relevance'.",
            ),
            _str(
                "store_id",
                "Numeric Target store id whose prices the response reflects. "
                "Defaults to '3991', the store target.com uses with no store context.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="target_category",
        namespace="target",
        method="category",
        http="POST",
        path="/api/v1/target/category",
        summary=(
            "Products in a Target category, same shape as search plus the category breadcrumb. "
            "Up to 28 per page; the slowest Target endpoint at around 37 seconds."
        ),
        params=(
            _req(
                "category_id",
                "Target category id: the segment after 'N-' in a target.com /c/ URL "
                "(target.com/c/apple/-/N-5xtg6 -> '5xtg6').",
            ),
            _int("page", "Results page, 1-based."),
            _int(
                "count",
                "Results per page, 1-28. Defaults to 24; Target rejects anything above 28 "
                "outright.",
            ),
            _lit(
                "sort",
                (
                    "relevance",
                    "featured",
                    "price_low",
                    "price_high",
                    "rating_high",
                    "best_seller",
                    "newest",
                ),
                "Result sort order. Defaults to 'relevance'.",
            ),
            _str(
                "store_id",
                "Numeric Target store id whose prices the response reflects. "
                "Defaults to '3991'.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="target_product",
        namespace="target",
        method="product",
        http="POST",
        path="/api/v1/target/product",
        summary=(
            "Target product details by TCIN: price, rating, images, specifications, variants, "
            "return policy, fulfillment. seller_id/seller_name are null for stock sold by Target."
        ),
        params=(
            _req(
                "tcin",
                "Target catalog id (tcin, e.g. '1010453160'). A colour/size child tcin is "
                "answered by its variation parent, with the child present in 'variants'.",
            ),
            _str(
                "store_id",
                "Numeric Target store id whose prices the response reflects. "
                "Defaults to '3991'.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="target_reviews",
        namespace="target",
        method="reviews",
        http="POST",
        path="/api/v1/target/reviews",
        summary=(
            "Target reviews with the rating breakdown, per-attribute averages and guest photos. "
            "8 review bodies maximum and no paging; expect around 40 seconds."
        ),
        params=(
            _req("tcin", "Target catalog id (tcin, e.g. '1010453160')."),
            _int(
                "limit",
                "Trim the returned reviews to at most this many (1 or greater). Target "
                "publishes 8 anonymously and offers no paging, so this only trims.",
            ),
            _str(
                "store_id",
                "Numeric Target store id whose prices the response reflects. "
                "Defaults to '3991'.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="target_availability",
        namespace="target",
        method="availability",
        http="POST",
        path="/api/v1/target/availability",
        summary=(
            "In-store stock for a Target product at every Target store near a ZIP: units, "
            "in-store, pickup, curbside and ship-to-store status, distance, address and hours. "
            "Up to 20 stores."
        ),
        params=(
            _req("tcin", "Target catalog id (tcin, e.g. '85978609')."),
            _req("zip", "5-digit US ZIP code to search around (e.g. '79407')."),
            _int("radius", "Search radius in miles, 1-100. Defaults to 25."),
            _str("store_id", "Return only this Target store id. It must be within radius of zip."),
        ),
        credits=1,
    ),
    # ============================= Home Depot ============================
    Endpoint(
        key="home_depot_search",
        namespace="home_depot",
        method="search",
        http="POST",
        path="/api/v1/homedepot/search",
        summary=(
            "Search Home Depot: price and promotions, brand and model, ratings, badges, "
            "per-store pickup/delivery. Page size is fixed at 12 and cannot be changed."
        ),
        params=(
            _req("query", "Search keyword (1-500 characters)."),
            _int(
                "page",
                "Results page, 1-based. Home Depot serves 12 products per page and offers no "
                "way to change that, so paging is the only way to read further.",
            ),
            _lit(
                "sort_by",
                ("best_match", "top_sellers", "top_rated", "price_low", "price_high"),
                "Result sort order. Defaults to 'best_match'. Closed enum: Home Depot answers "
                "an unknown sort with an empty page that is still billed. 'Newest' is absent - "
                "it is rejected on keyword search.",
            ),
            _float(
                "min_price",
                "Minimum price, inclusive. Must be 0 or greater.",
            ),
            _float(
                "max_price",
                "Maximum price, inclusive. Must be 0 or greater.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="home_depot_product",
        namespace="home_depot",
        method="product",
        http="POST",
        path="/api/v1/homedepot/product",
        summary=(
            "Full Home Depot item detail: pricing, images and videos, spec table, dimensions, "
            "bullets, documents, return policy. Carries a 10-review preview only."
        ),
        params=(
            _req(
                "item_id",
                "Home Depot item id (e.g. '325479354'), or a full homedepot.com/p/... product "
                "URL; tracking parameters on a pasted URL are discarded.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="home_depot_reviews",
        namespace="home_depot",
        method="reviews",
        http="POST",
        path="/api/v1/homedepot/reviews",
        summary=(
            "One page of full Home Depot review bodies, the rating distribution, per-attribute "
            "ratings, photos and seller responses. 30 reviews per page."
        ),
        params=(
            _req(
                "item_id",
                "Home Depot item id (e.g. '325479354'), or a full homedepot.com/p/... product "
                "URL; tracking parameters on a pasted URL are discarded.",
            ),
            _int(
                "page",
                "Reviews page, 1-based. 30 reviews per page; 'total_pages' in the response is "
                "the last one that exists, and asking past it is a 404.",
            ),
        ),
        credits=2,
    ),
    # =============================== Zillow ==============================
    Endpoint(
        key="zillow_search",
        namespace="zillow",
        method="search",
        http="POST",
        path="/api/v1/zillow/search",
        summary=(
            "Zillow listings in a region: price, beds, baths, living area, Zestimate, "
            "coordinates, images, days on market. A bare ZIP works alone but cannot be "
            "combined with a filter or a sort."
        ),
        params=(
            _req(
                "location",
                "Region to search (1-200 characters): a Zillow slug ('austin-tx'), a human form "
                "('Austin, TX'), a ZIP, or a pasted zillow.com search URL. A ZIP works alone but "
                "cannot be combined with a filter or sort; an unresolvable region is a 404.",
            ),
            _lit(
                "listing_status",
                ("for_sale", "for_rent", "sold"),
                "Which listings to return. Defaults to 'for_sale'.",
            ),
            _int("page", "Results page, 1-based."),
            _lit(
                "sort",
                (
                    "relevance",
                    "recommended",
                    "newest",
                    "price_low",
                    "price_high",
                    "payment_low",
                    "payment_high",
                    "beds",
                    "baths",
                    "sqft",
                    "lot_size",
                    "zestimate_low",
                    "zestimate_high",
                    "recent_change",
                ),
                "Result sort order. Sorts that rank against a signed-in profile "
                "(saved/featured/personalised) are unsupported - we are never signed in.",
            ),
            _float(
                "min_price",
                "Minimum price, inclusive (0 or greater). On listing_status='for_rent' this is "
                "MONTHLY RENT - Zillow files rent under its payment filter.",
            ),
            _float(
                "max_price",
                "Maximum price, inclusive (0 or greater). On listing_status='for_rent' this is "
                "MONTHLY RENT.",
            ),
            _int("beds_min", "Minimum bedrooms; whole number, 0 or greater."),
            _int("beds_max", "Maximum bedrooms; whole number, 0 or greater."),
            _float(
                "baths_min",
                "Minimum bathrooms, 0 or greater. Half-baths are allowed (1.5).",
            ),
            _float(
                "baths_max",
                "Maximum bathrooms, 0 or greater. Half-baths are allowed (1.5).",
            ),
            _int("sqft_min", "Minimum living area in square feet; whole number, 0 or greater."),
            _int("sqft_max", "Maximum living area in square feet; whole number, 0 or greater."),
            _int("lot_size_min", "Minimum lot size in square feet; whole number, 0 or greater."),
            _int("lot_size_max", "Maximum lot size in square feet; whole number, 0 or greater."),
            _int("year_built_min", "Earliest year built; whole number, 0 or greater."),
            _int("year_built_max", "Latest year built; whole number, 0 or greater."),
            _float(
                "max_hoa",
                "Maximum monthly HOA fee in dollars, 0 or greater.",
            ),
            _lit(
                "home_type",
                (
                    "houses",
                    "townhomes",
                    "multi_family",
                    "condos",
                    "apartments",
                    "manufactured",
                    "lots_land",
                ),
                "Property type filter.",
            ),
            _lit(
                "days_on_zillow",
                ("1", "7", "14", "30", "90", "6m", "12m", "24m", "36m"),
                "Listed - or, with listing_status='sold', sold - within the last N days. Closed "
                "enum: an unrecognised value returns the UNFILTERED set under a 200.",
            ),
            _str(
                "keywords",
                "Free-text match against the listing description (1-200 characters).",
            ),
            _bool("has_pool", "Only listings with a pool."),
            _bool("has_garage", "Only listings with a garage."),
            _bool("has_air_conditioning", "Only listings with air conditioning."),
            _bool("is_waterfront", "Only waterfront listings."),
            _bool("has_basement", "Only listings with a basement."),
            _bool("is_new_construction", "Only new-construction listings."),
            _bool("has_open_house", "Only listings with an upcoming open house."),
            _bool("price_reduced", "Only listings whose price was reduced."),
            _bool("is_3d_tour", "Only listings with a 3D tour."),
        ),
        credits=1,
    ),
    Endpoint(
        key="zillow_property",
        namespace="zillow",
        method="property",
        http="POST",
        path="/api/v1/zillow/property",
        summary=(
            "Full Zillow listing: price and price history, Zestimate, tax history, RESO facts, "
            "rooms, schools, open houses, photos. Rental buildings return floor plans instead."
        ),
        params=(
            _req(
                "zpid",
                "Zillow property id (e.g. '29414894'), a full /homedetails/ URL, or a rental "
                "building URL (zillow.com/apartments/...). The building form is required for "
                "buildings: they have no zpid a caller can see.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="zillow_agent_reviews",
        namespace="zillow",
        method="agent_reviews",
        http="POST",
        path="/api/v1/zillow/reviews",
        summary=(
            "A Zillow AGENT's profile and reviews: rating, bodies with sub-ratings, specialties, "
            "licenses, service areas, sales counts. Zillow server-renders the first five."
        ),
        params=(
            _req(
                "screen_name",
                "Zillow agent profile screen name as it appears in zillow.com/profile/<name>/ "
                "(1-200 characters, may contain spaces), or a full profile URL.",
            ),
        ),
        credits=1,
    ),
    # ============================ Booking.com ============================
    # 1 credit flat on all three endpoints. Booking prices a STAY, so every endpoint takes the
    # occupancy/date set: checkin and checkout must travel TOGETHER, because a
    # lone checkin is ignored and Booking prices a range of its own choosing,
    # returning real prices for dates the caller never asked for. currency
    # defaults to USD in the transport - without it Booking picks a currency itself and two identical requests can disagree.
    Endpoint(
        key="booking_search",
        namespace="booking",
        method="search",
        http="POST",
        path="/api/v1/booking/search",
        summary=(
            "Booking.com properties for a destination and stay: live nightly price, review score, "
            "star rating, location, room type, deal badges. 25 properties per page. Provide "
            "destination or dest_id."
        ),
        params=(
            _str("destination", "Destination to search, e.g. 'Paris' (1-200 characters). Required unless dest_id is given."),
            _str("dest_id", "Numeric Booking.com destination id, as an alternative to destination."),
            _lit(
                "dest_type",
                ("city", "region", "country", "district", "landmark", "airport", "hotel"),
                "What dest_id refers to. Requires dest_id and is rejected without it, because Booking silently ignores a lone dest_type.",
            ),
            _int("page", "Results page, 1-based. 25 properties per page, 1 credit each."),
            _lit(
                "sort_by",
                (
                    "popularity",
                    "price_low",
                    "price_high",
                    "stars_high",
                    "stars_low",
                    "stars_and_price",
                    "distance",
                    "review_score",
                ),
                "Result sort order (default 'popularity').",
            ),
            _float(
                "min_price",
                "Minimum price PER NIGHT in `currency`, >= 0. Must not exceed max_price.",
            ),
            _float(
                "max_price",
                "Maximum price PER NIGHT in `currency`, >= 0.",
            ),
            _int_list(
                "stars",
                "Star ratings to include, each 1-5, 1-5 values, OR'd together (e.g. [4, 5]).",
            ),
            _lit(
                "min_review_score",
                ("6", "7", "8", "9"),
                "Minimum guest review score. Only '6', '7', '8' and '9' exist upstream; any other threshold is silently dropped.",
            ),
            _lit_or_int(
                "property_type",
                (
                    "apartments",
                    "hostels",
                    "hotels",
                    "motels",
                    "resorts",
                    "bed_and_breakfasts",
                    "villas",
                    "campgrounds",
                    "vacation_homes",
                    "lodges",
                    "homestays",
                ),
                "Accommodation type by name, or a raw numeric Booking accommodation-type id (>= "
                "1).",
            ),
            _bool("free_cancellation", "Only properties offering free cancellation."),
            _bool("no_prepayment", "Only properties that take no prepayment."),
            _bool("breakfast_included", "Only rates that include breakfast."),
            _str("checkin", "Check-in date, YYYY-MM-DD. Must be sent together with checkout: a lone checkin is ignored and Booking prices a default range of its own."),
            _str("checkout", "Check-out date, YYYY-MM-DD. Must be later than checkin and sent together with it."),
            _int("adults", "Adult guests, >= 1 (default 2)."),
            _int_list(
                "children_ages",
                "AGES of accompanying children, each 0-17, max 10 entries. Ages, not a count.",
            ),
            _int("rooms", "Rooms required, >= 1 (default 1)."),
            _str("currency", "ISO 4217 currency for prices, 3 letters (default 'USD'). Without it Booking picks a currency itself and identical requests can disagree."),
        ),
        one_of=(("destination", "dest_id"),),
        credits=1,
    ),
    Endpoint(
        key="booking_hotel",
        namespace="booking",
        method="hotel",
        http="POST",
        path="/api/v1/booking/hotel",
        summary=(
            "One Booking.com property in full: rooms and rate plans, facilities, house rules, "
            "check-in windows, policies, images, location and review scores, priced for the stay "
            "asked for. Chaining the `url` a search row returns is cheaper than a bare slug."
        ),
        params=(
            _req("hotel", "Booking.com property URL or the bare page slug (1-500 characters); query params are discarded."),
            _str("country_code", "Two-letter country code for the property page (default 'us'). Only consulted for a bare slug, where a wrong one is a real, BILLED 404."),
            _str("checkin", "Check-in date, YYYY-MM-DD. Must be sent together with checkout; omitting both prices a two-night range Booking chose, echoed back in the response."),
            _str("checkout", "Check-out date, YYYY-MM-DD. Must be later than checkin and sent together with it."),
            _int("adults", "Adult guests, >= 1 (default 2)."),
            _int_list(
                "children_ages",
                "AGES of accompanying children, each 0-17, max 10 entries. Ages, not a count.",
            ),
            _int("rooms", "Rooms required, >= 1 (default 1)."),
            _str("currency", "ISO 4217 currency for prices, 3 letters (default 'USD'). Without it Booking picks a currency itself and identical requests can disagree."),
        ),
        credits=1,
    ),
    Endpoint(
        key="booking_reviews",
        namespace="booking",
        method="reviews",
        http="POST",
        path="/api/v1/booking/reviews",
        summary=(
            "Booking.com guest reviews for a property with the score breakdown by category and "
            "Booking's own praise/complaint summary. No page param: total_count is the whole "
            "review history, count is what this response holds."
        ),
        params=(
            _req("hotel", "Booking.com property URL or the bare page slug (1-500 characters); query params are discarded."),
            _str("country_code", "Two-letter country code for the property page (default 'us'). Only consulted for a bare slug, where a wrong one is a real, BILLED 404."),
            _str("checkin", "Check-in date, YYYY-MM-DD. Must be sent together with checkout; it prices the stay the review page is rendered for."),
            _str("checkout", "Check-out date, YYYY-MM-DD. Must be later than checkin and sent together with it."),
            _int("adults", "Adult guests, >= 1 (default 2)."),
            _int_list(
                "children_ages",
                "AGES of accompanying children, each 0-17, max 10 entries. Ages, not a count.",
            ),
            _int("rooms", "Rooms required, >= 1 (default 1)."),
            _str("currency", "ISO 4217 currency for prices, 3 letters (default 'USD')."),
        ),
        credits=1,
    ),
    # ============================ Tripadvisor ============================
    # 2 credits flat on all four endpoints. LOOKUP FIRST: every
    # endpoint below locations() is keyed by ids that exist only inside
    # TripAdvisor's own URLs, so a caller holding a place NAME has no other entry
    # point. A geo row from locations() answers geo_id for search(); a business
    # row answers the geo_id + location_id pair location() and reviews() take.
    Endpoint(
        key="tripadvisor_locations",
        namespace="tripadvisor",
        method="locations",
        http="POST",
        path="/api/v1/tripadvisor/locations",
        summary=(
            "START HERE: resolve a place or business NAME to the TripAdvisor geo_id / location_id "
            "pair every other TripAdvisor endpoint is keyed by. Up to 20 rows."
        ),
        params=(
            _req("query", "Place or business name to resolve (1-120 characters)."),
            _int("limit", "Rows to return, 1-20 (default 12). Sizes the response only; there is no paging here."),
        ),
        credits=2,
    ),
    Endpoint(
        key="tripadvisor_search",
        namespace="tripadvisor",
        method="search",
        http="POST",
        path="/api/v1/tripadvisor/search",
        summary=(
            "Restaurants, hotels or attractions in a TripAdvisor geo, TripAdvisor-ranked: rating, "
            "review count, price band, address, coordinates, phone, hours, Travelers' Choice badge; "
            "each row carries the location_id + geo_id pair. 30 locations per page. Provide geo_id "
            "or url."
        ),
        params=(
            _str("geo_id", "TripAdvisor geo id (1-500 characters): 30196, g30196, or a URL carrying one. Required unless url is given."),
            _lit(
                "category",
                ("restaurants", "hotels", "attractions"),
                "Listing family to search (default 'restaurants').",
            ),
            _int("page", "Results page, 1-based. 30 locations per page; a page beyond the last is a 404, not an empty result."),
            _str("url", "Full tripadvisor.com listing URL (1-500 characters), as an alternative to geo_id; country sites are accepted."),
        ),
        one_of=(("geo_id", "url"),),
        credits=2,
    ),
    Endpoint(
        key="tripadvisor_location",
        namespace="tripadvisor",
        method="location",
        http="POST",
        path="/api/v1/tripadvisor/location",
        summary=(
            "One TripAdvisor location in full: rating, review histogram and per-aspect sub-ratings, "
            "city ranking, price band, cuisines, amenities, address, coordinates, contact, photos, "
            "and the FIRST PAGE OF REVIEWS. Provide location_id or url."
        ),
        params=(
            _str("location_id", "TripAdvisor location id (1-500 characters): 1899234, d1899234, or a full _Review URL. Required unless url is given."),
            _str("geo_id", "Geo the location sits in; required when location_id is a bare d-id."),
            _lit(
                "category",
                ("restaurants", "hotels", "attractions"),
                "Location family (default 'restaurants'); match the location's own type.",
            ),
            _str("url", "Full tripadvisor.com _Review URL (1-500 characters), as an alternative to location_id."),
        ),
        one_of=(("location_id", "url"),),
        credits=2,
    ),
    Endpoint(
        key="tripadvisor_reviews",
        namespace="tripadvisor",
        method="reviews",
        http="POST",
        path="/api/v1/tripadvisor/reviews",
        summary=(
            "A page of TripAdvisor reviews: rating, trip date and type, reviewer home town and "
            "contribution count, management response. Page 1 already rides along in location(), so "
            "use this to page PAST it; consecutive pages can repeat one review at the boundary, so "
            "de-duplicate on review_id. Provide location_id or url."
        ),
        params=(
            _str("location_id", "TripAdvisor location id (1-500 characters): 1899234, d1899234, or a full _Review URL. Required unless url is given."),
            _str("geo_id", "Geo the location sits in; required when location_id is a bare d-id."),
            _lit(
                "category",
                ("restaurants", "hotels", "attractions"),
                "Location family (default 'restaurants'). It sets the page size, so it must match the location's own type on any page past the first.",
            ),
            _str("url", "Full tripadvisor.com _Review URL (1-500 characters), as an alternative to location_id."),
            _int("page", "Reviews page, 1-based. 15 per page for restaurants, 10 for hotels and attractions; past the last page is a 404."),
        ),
        one_of=(("location_id", "url"),),
        credits=2,
    ),
    # =============================== Indeed ==============================
    # 2 credits flat on all four endpoints. radius and max_age_days
    # are CLOSED sets: Indeed ignores any other value and returns the unfiltered
    # set, so a caller asking for 7 miles is billed for a search covering fifty.
    # An unknown job key or company slug is a real 404 and IS BILLED.
    Endpoint(
        key="indeed_search",
        namespace="indeed",
        method="search",
        http="POST",
        path="/api/v1/indeed/search",
        summary=(
            "Indeed job postings: title, employer, rating, location, salary range, job type, "
            "benefits, posting age, apply route. 10 postings per page. Provide query or location - "
            "a location-only search (every posting in a metro) is valid."
        ),
        params=(
            _str("query", "Job title, keywords or employer (1-500 characters). Required unless location is given."),
            _str("location", "City and state, postal code, state, country, or 'Remote' (1-200 characters). Valid on its own with no query."),
            _int("page", "Results page, 1-based. 10 postings per page, 1 call each."),
            _ilit(
                "radius",
                (0, 5, 10, 15, 25, 35, 50, 100),
                "Search radius in miles around location. Closed set: Indeed IGNORES any other "
                "value and returns the unfiltered set. Upstream default 50.",
            ),
            _ilit(
                "max_age_days",
                (1, 3, 7, 14),
                "Maximum posting age in days. Closed set: Indeed IGNORES any other value and "
                "returns postings of every age.",
            ),
            _lit(
                "job_type",
                ("full_time", "part_time", "contract", "temporary", "internship"),
                "Employment type filter.",
            ),
            _float(
                "min_salary",
                "Minimum annual salary, >= 0. Filters on INDEED'S OWN ESTIMATE for the role, not "
                "a posted figure, so postings publishing no salary still match.",
            ),
            _bool("remote", "Remote postings only."),
        ),
        one_of=(("query", "location"),),
        credits=2,
    ),
    Endpoint(
        key="indeed_job",
        namespace="indeed",
        method="job",
        http="POST",
        path="/api/v1/indeed/job",
        summary=(
            "One Indeed posting in full: description text and HTML, structured salary, employment "
            "types, benefits, geocoded address, employer rating, applicant count, original ATS "
            "link. An unknown job key is a real 404 that is still billed."
        ),
        params=(
            _req("job_id", "16-hex Indeed job key, or any indeed.com URL carrying jk= (/viewjob, /rc/clk, /pagead/clk)."),
        ),
        credits=2,
    ),
    Endpoint(
        key="indeed_company",
        namespace="indeed",
        method="company",
        http="POST",
        path="/api/v1/indeed/company",
        summary=(
            "Indeed employer profile: description, industry, HQ, size, revenue, CEO approval, "
            "overall and per-category ratings, reported salaries, open roles, locations. An unknown "
            "slug is a real 404 that is still billed."
        ),
        params=(
            _req("company", "indeed.com/cmp/<slug> slug or a full profile URL (1-200 characters); slugs are untidy, e.g. 'Tata-Consultancy-Services-(tcs)'."),
        ),
        credits=2,
    ),
    Endpoint(
        key="indeed_company_reviews",
        namespace="indeed",
        method="company_reviews",
        http="POST",
        path="/api/v1/indeed/company/reviews",
        summary=(
            "Indeed employee reviews, 20 per page, with per-category ratings, pros/cons, reviewer "
            "job title and location, plus aggregated sentiment and topic/location/job-title "
            "breakdowns."
        ),
        params=(
            _req("company", "indeed.com/cmp/<slug> slug or a full profile URL (1-200 characters)."),
            _int("page", "Reviews page, 1-based. 20 reviews per page."),
        ),
        credits=2,
    ),
    # =============================== Airbnb ==============================
    # 1 credit flat on all three endpoints. PRICES ARE SEARCH-ONLY: the room page carries no nightly rate
    # under any parameters, with or without dates. check_in
    # and check_out must travel together - a dateless search defaults to +30d for
    # 5 nights and A/Bs both the window and the prices, which the response flags
    # as dates_are_defaulted. room_type and amenity names are validated before
    # the scrape because an unrecognised value returns the UNFILTERED set under a
    # 200.
    Endpoint(
        key="airbnb_search",
        namespace="airbnb",
        method="search",
        http="POST",
        path="/api/v1/airbnb/search",
        summary=(
            "Airbnb stays: stay-total and per-night price with the full discount ledger, rating and "
            "review count, bedrooms/beds/baths, coordinates, badges, images, dates_are_defaulted. "
            "18 listings per page; page and cursor are mutually exclusive."
        ),
        params=(
            _req("location", "City, region, ZIP, or a pasted airbnb.com/s/ URL (1-200 characters). An unresolvable location is a 404."),
            _str("check_in", "Check-in date, YYYY-MM-DD. Must be sent with check_out; omitting both defaults to +30 days and flags dates_are_defaulted in the response."),
            _str("check_out", "Check-out date, YYYY-MM-DD. Must be later than check_in; defaults to check_in plus 5 nights when omitted."),
            _int("adults", "Adult guests, >= 1."),
            _int("children", "Children aged 2-12, >= 0."),
            _int("infants", "Infants under 2, >= 0."),
            _int("pets", "Pets, >= 0."),
            _float(
                "min_price",
                "Minimum price for the WHOLE STAY in `currency`, not per night, >= 0. Must not "
                "exceed max_price.",
            ),
            _float(
                "max_price",
                "Maximum price for the WHOLE STAY in `currency`, not per night, >= 0.",
            ),
            _lit(
                "room_type",
                ("entire_home", "private_room", "shared_room", "hotel_room"),
                "Room type. Validated before the scrape, because an unrecognised value returns the UNFILTERED set under a 200.",
            ),
            _int("min_bedrooms", "Minimum bedrooms, >= 0."),
            _int("min_beds", "Minimum beds, >= 0."),
            _int("min_bathrooms", "Minimum bathrooms, >= 0."),
            _bool("superhost", "Superhost listings only."),
            _bool("instant_book", "Instant Book listings only."),
            _bool("guest_favorite", "Guest Favorite listings only."),
            _bool("free_cancellation", "Listings with free cancellation only."),
            _str("amenities", "Comma-separated amenities (1-200 characters): wifi, air_conditioning, pool, kitchen, free_parking, washer, self_check_in, tv, or raw numeric Airbnb amenity ids. An unrecognised NAME is rejected before the scrape."),
            _str("currency", "ISO 4217 currency for prices, 3 letters (default 'USD'). Without it Airbnb picks a currency itself and identical requests can disagree."),
            _int("page", "Results page, 1-based. 18 listings per page. Cannot be combined with cursor."),
            _str("cursor", "next_cursor from a previous response (1-500 characters); wins over page, so sending both is rejected."),
        ),
        credits=1,
    ),
    Endpoint(
        key="airbnb_listing",
        namespace="airbnb",
        method="listing",
        http="POST",
        path="/api/v1/airbnb/listing",
        summary=(
            "One Airbnb listing in full: description, property/room type, capacity and room counts, "
            "the complete grouped amenity list (including what the place does NOT have), host "
            "profile and stats, house rules, cancellation policy, sleeping arrangements, photo tour "
            "and the RATING BREAKDOWN. Carries NO nightly price - prices are search-only."
        ),
        params=(
            _req("listing_id", "Airbnb listing id or a full /rooms/ URL (1-500 characters); query params are discarded, since they carry someone else's dates."),
            _str("check_in", "Check-in date, YYYY-MM-DD. Must be sent with check_out. Does not produce a price: the room page has no nightly rate."),
            _str("check_out", "Check-out date, YYYY-MM-DD. Must be later than check_in and sent together with it."),
            _int("adults", "Adult guests, >= 1."),
            _int("children", "Children aged 2-12, >= 0."),
            _int("infants", "Infants under 2, >= 0."),
            _int("pets", "Pets, >= 0."),
            _str("currency", "ISO 4217 currency, 3 letters (default 'USD')."),
        ),
        credits=1,
    ),
    Endpoint(
        key="airbnb_reviews",
        namespace="airbnb",
        method="reviews",
        http="POST",
        path="/api/v1/airbnb/reviews",
        summary=(
            "Airbnb review BODIES with per-review rating, date and reviewer name/photo/location, "
            "limit/offset paged at up to 50 per call. `count` is the listing's TOTAL review count, "
            "`returned` is how many this page holds. The rating breakdown lives on listing(), not here."
        ),
        params=(
            _req("listing_id", "Airbnb listing id or a full /rooms/ URL (1-500 characters)."),
            _str("currency", "ISO 4217 currency, 3 letters (default 'USD')."),
            _int("limit", "Reviews to return, 1-50 (default 30). Upstream returns a fixed 7 when no explicit limit is sent."),
            _int("offset", "Reviews to skip before this page, >= 0 (default 0)."),
        ),
        credits=1,
    ),
    # ============================= Glassdoor =============================
    Endpoint(
        key="glassdoor_companies",
        namespace="glassdoor",
        method="companies",
        http="POST",
        path="/api/v1/glassdoor/companies",
        summary=(
            "START HERE. Resolve a company NAME to the employer_id every other Glassdoor method is "
            "keyed by, ranked by Glassdoor and de-duplicated."
        ),
        params=(
            _req("query", "Company name to resolve (1-120 characters)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="glassdoor_company",
        namespace="glassdoor",
        method="company",
        http="POST",
        path="/api/v1/glassdoor/company",
        summary=(
            "Glassdoor employer profile: description, mission, industry, sector, HQ, size and revenue "
            "bands, stock symbol, year founded, overall and per-category ratings, star distribution, "
            "CEO approval, awards, FAQ and the five server-rendered reviews. Also returns reviews_url "
            "and salaries_url, which reviews() and salaries() accept as url to save a fetch. Provide "
            "employer_id or url."
        ),
        params=(
            _str(
                "employer_id",
                "Glassdoor employer id (1-50 characters) in any form Glassdoor writes it: '1699', "
                "'E1699' or 'IE1699'. Must be a STRING - a JSON number is rejected.",
            ),
            _str(
                "company",
                "Employer name as it appears in a Glassdoor slug (1-200 characters). COSMETIC: the "
                "profile resolves on employer_id alone, it is ignored entirely when url is set, and it "
                "does not satisfy the employer_id-or-url requirement.",
            ),
            _str(
                "url",
                "Any glassdoor.com employer URL (1-500 characters): /Overview/, /Reviews/ or /Salary/. "
                "A non-glassdoor.com host is rejected.",
            ),
        ),
        one_of=(("employer_id", "url"),),
        credits=1,
    ),
    Endpoint(
        key="glassdoor_reviews",
        namespace="glassdoor",
        method="reviews",
        http="POST",
        path="/api/v1/glassdoor/reviews",
        summary=(
            "Up to THREE full Glassdoor reviews - the cap is Glassdoor's login wall - with per-axis "
            "scores, pros, cons, advice, job title, location, employment status and employer response, "
            "plus complete rating statistics, star distribution, aggregate pro/con highlight terms and "
            "per-job-title review counts. There is no page param: move the window with category and "
            "employment_status. Provide employer_id or url."
        ),
        params=(
            _str(
                "employer_id",
                "Glassdoor employer id (1-50 characters): '1699', 'E1699' or 'IE1699'. Must be a "
                "STRING - a JSON number is rejected. Addressing by id costs two lookups; the "
                "customer price is unchanged.",
            ),
            _str(
                "company",
                "Employer name as it appears in a Glassdoor slug (1-200 characters). COSMETIC: ignored "
                "when url is set, and it does not satisfy the employer_id-or-url requirement.",
            ),
            _str(
                "url",
                "Any glassdoor.com employer URL (1-500 characters). Pass back reviews_url from "
                "company() to skip the resolve fetch. A non-glassdoor.com host is rejected.",
            ),
            _lit(
                "category",
                (
                    "career_development",
                    "compensation",
                    "culture",
                    "diversity_and_inclusion",
                    "management",
                    "work_life_balance",
                ),
                "Restrict to reviews Glassdoor files under one topic. Closed enum: Glassdoor IGNORES an "
                "unknown value and serves the unfiltered set under a 200. Read filtered_review_count on "
                "the response to see how many match.",
            ),
            _lit(
                "employment_status",
                ("full_time", "part_time", "contract", "intern"),
                "Restrict to one kind of employment. Closed enum for the same reason as category; "
                "FREELANCE is deliberately absent because it was never confirmed to change the result "
                "set.",
            ),
        ),
        one_of=(("employer_id", "url"),),
        credits=1,
    ),
    Endpoint(
        key="glassdoor_salaries",
        namespace="glassdoor",
        method="salaries",
        http="POST",
        path="/api/v1/glassdoor/salaries",
        summary=(
            "Glassdoor salaries by job title, 10 titles per page: base-pay and total-pay percentiles "
            "P10-P90 with medians called out, sample counts, currency, pay period and last-reported "
            "date. The figures are Glassdoor's ESTIMATES for the title, not individual reported "
            "salaries. Provide employer_id or url."
        ),
        params=(
            _str(
                "employer_id",
                "Glassdoor employer id (1-50 characters): '1699', 'E1699' or 'IE1699'. Must be a "
                "STRING - a JSON number is rejected. Addressing by id costs two lookups; the "
                "customer price is unchanged.",
            ),
            _str(
                "company",
                "Employer name as it appears in a Glassdoor slug (1-200 characters). COSMETIC: ignored "
                "when url is set, and it does not satisfy the employer_id-or-url requirement.",
            ),
            _str(
                "url",
                "Any glassdoor.com employer URL (1-500 characters). Pass back salaries_url from "
                "company() to skip the resolve fetch. A non-glassdoor.com host is rejected.",
            ),
            _int(
                "page",
                "Results page, 1-based. Ten job titles per page; page_count on the response is how many "
                "pages exist.",
            ),
        ),
        one_of=(("employer_id", "url"),),
        credits=1,
    ),
    # ================================ Yelp ===============================
    Endpoint(
        key="yelp_search",
        namespace="yelp",
        method="search",
        http="POST",
        path="/api/v1/yelp/search",
        summary=(
            "Businesses in Yelp's ranked order: rating, review count, price band, categories, address, "
            "contact rails, hours, photos and a review snippet; every row carries both business_id and "
            "alias. Yelp fixes the page size at 10. Provide term and location, or url. Costs 2 credits."
        ),
        params=(
            _str(
                "term",
                "What to look for (1-200 characters): a category ('plumbers'), a dish, or a business "
                "name. Required together with location unless url is given.",
            ),
            _str(
                "location",
                "Where to look (1-200 characters): city and region, a full address, or a postcode. "
                "Effectively required - without it Yelp picks a location itself, so the same request can answer about a different metro run to run.",
            ),
            _int("page", "Results page, 1-based. Yelp fixes the page size at 10."),
            _lit(
                "sort",
                ("recommended", "rating", "review_count"),
                "Result ordering (upstream default 'recommended'). Closed enum: Yelp IGNORES an "
                "unrecognised sortby and serves default ranking under a 200, billing a premium scrape "
                "for a sort that never ran.",
            ),
            _ilit_list(
                "price",
                (1, 2, 3, 4),
                "Price bands to include, 1 ($) to 4 ($$$$); 1-4 values, combined freely - [1, 2] "
                "means $ or $$.",
            ),
            _bool("open_now", "Only businesses open at the moment of the request."),
            _str_list(
                "attributes",
                "Raw Yelp filter aliases, max 20, each 1-100 characters ('RestaurantsDelivery', "
                "'GoodForKids', 'WheelchairAccessible'). A deliberate PASSTHROUGH, not an enum - "
                "Yelp's vocabulary runs to ~117 values per vertical and an alias it does not know "
                "is ignored upstream, returning unfiltered results.",
            ),
            _str(
                "url",
                "A full yelp.com/search URL (1-1000 characters) as an alternative to term + location; "
                "the query, offset and sort are read out of it and the URL is rebuilt.",
            ),
        ),
        one_of=(("term", "url"), ("location", "url")),
        credits=2,
    ),
    Endpoint(
        key="yelp_business",
        namespace="yelp",
        method="business",
        http="POST",
        path="/api/v1/yelp/business",
        summary=(
            "One business in full: rating and per-star histogram, review count, price band, categories, "
            "address and coordinates, phone, website and menu links, hours and holidays, amenities, "
            "photos and videos, popular items, health inspections, Q&A, licences and claim status - "
            "plus the first page of reviews at no extra cost. Provide business_id or url. "
            "Costs 2 credits."
        ),
        params=(
            _str(
                "business_id",
                "A Yelp business alias ('desnudo-coffee-austin-2'), its opaque encid, or any "
                "yelp.com/biz URL carrying one (1-500 characters). Search rows return both id forms.",
            ),
            _str(
                "url",
                "A full yelp.com/biz URL (1-1000 characters) as an alternative to business_id.",
            ),
        ),
        one_of=(("business_id", "url"),),
        credits=2,
    ),
    Endpoint(
        key="yelp_reviews",
        namespace="yelp",
        method="reviews",
        http="POST",
        path="/api/v1/yelp/reviews",
        summary=(
            "A page of reviews: rating, full text, language, author profile and expertise counts, "
            "attached photos, reaction counts and owner response. 10 per page. PAGE 1 IS REDUNDANT - it "
            "re-fetches the document business() already returned - so start at page 2. Provide "
            "business_id or url. Costs 2 credits."
        ),
        params=(
            _str(
                "business_id",
                "A Yelp business alias ('desnudo-coffee-austin-2'), its opaque encid, or any "
                "yelp.com/biz URL carrying one (1-500 characters).",
            ),
            _str(
                "url",
                "A full yelp.com/biz URL (1-1000 characters) as an alternative to business_id.",
            ),
            _int(
                "page",
                "Reviews page, 1-based, 10 per page. Page 1 duplicates the reviews business() already "
                "returned and costs another 2 credits - start at 2. A page past the last review is a "
                "404, not an empty result.",
            ),
            _lit(
                "sort",
                ("relevance", "newest", "oldest", "rating_high", "rating_low", "elites"),
                "Review ordering (upstream default 'relevance'). Closed enum: Yelp IGNORES an "
                "unrecognised value and serves default ranking under a billed 200.",
            ),
            _ilit(
                "rating",
                (1, 2, 3, 4, 5),
                "Only reviews at this star rating, 1-5. Changes filtered_review_count on the "
                "response, not review_count.",
            ),
        ),
        one_of=(("business_id", "url"),),
        credits=2,
    ),
    # ========================== Apple App Store ==========================
    Endpoint(
        key="app_store_search",
        namespace="app_store",
        method="search",
        http="POST",
        path="/api/v1/appstore/search",
        summary=(
            "Search the App Store and get up to 200 fully-shaped app rows - the same 43-field row as "
            "app() - so a search doubles as a bulk metadata fetch and as a publisher lookup. NO "
            "PAGINATION: raise limit, there is no second page."
        ),
        params=(
            _req(
                "term",
                "What to search for (1-500 characters). Apple matches an app name, a keyword OR a "
                "publisher name, so searching a developer returns their catalogue.",
            ),
            _int(
                "limit",
                "Apps to return, 1-200 (default 25). The ONLY lever on result volume: the search API "
                "has no pagination and every offset spelling is silently ignored.",
            ),
            _str(
                "country",
                "Two-letter ISO storefront code (default 'us'); decides price, currency, localised "
                "title and whether the app is sold there at all. Anything that is not exactly two "
                "letters is rejected with a free 400.",
            ),
            _lit(
                "entity",
                ("software", "ipad_software", "mac_software"),
                "Which catalogue to search: iPhone/iPad apps ('software', the default), iPad apps, or "
                "Mac App Store apps. These are separate stores, not a filter - Mac rows carry no "
                "iPad/Apple TV screenshots, advisories, features, supported devices or Game Center "
                "flag, returning them empty rather than absent.",
            ),
            _str(
                "lang",
                "Listing text language as a five-letter code ('en_us', 'ja_jp'); any other shape is "
                "rejected. Independent of country: the storefront sets the price, this sets the words.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="app_store_app",
        namespace="app_store",
        method="app",
        http="POST",
        path="/api/v1/appstore/app",
        summary=(
            "Full App Store listing: title, description, developer and seller identity, price and "
            "currency, all-time and current-version ratings, version and release notes, genres, content "
            "rating and advisories, icons at three sizes, screenshots, download size, minimum OS, "
            "languages, supported devices and the Game Center and VPP flags."
        ),
        params=(
            _req(
                "app_id",
                "App Store id - the digits after 'id' in an apps.apple.com URL - or the app's bundle id "
                "('notion.id', 'com.burbn.instagram'); both resolve to the identical payload. 1-255 "
                "characters matching ^[A-Za-z0-9][A-Za-z0-9._-]*$, so a pasted apps.apple.com URL is "
                "rejected with a free 400. An id Apple cannot resolve is a billed 404.",
            ),
            _str(
                "country",
                "Two-letter ISO storefront code (default 'us'); decides price, currency, localised "
                "title and whether the app is sold there at all. Anything that is not exactly two "
                "letters is rejected with a free 400.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="app_store_reviews",
        namespace="app_store",
        method="reviews",
        http="POST",
        path="/api/v1/appstore/reviews",
        summary=(
            "A page of App Store reviews: star rating, title, full text, author and the APP VERSION the "
            "review was written against. 50 per page, hard-stopped at page 10 - 500 reviews per "
            "storefront is Apple's anonymous ceiling. This endpoint cannot 404: an unknown id and a "
            "real app with no reviews return the same empty feed."
        ),
        params=(
            _req(
                "app_id",
                "App Store id, NUMERIC ONLY - unlike app(), the reviews feed has no bundle-id form.",
            ),
            _str(
                "country",
                "Two-letter ISO storefront code (default 'us'). Anything that is not exactly two "
                "letters is rejected with a free 400. Ask a different country to reach past the "
                "500-review ceiling.",
            ),
            _int(
                "page",
                "Reviews page, 1-10, 50 reviews each (default 1). Apple hard-stops at page 10.",
            ),
            _lit(
                "sort",
                ("most_recent", "most_helpful"),
                "Review ordering (default 'most_recent'). The choice decides whether the vote fields "
                "mean anything: under most_recent almost every review is too new to have been voted on "
                "and returns zeroes, while most_helpful returns them densely populated.",
            ),
        ),
        credits=1,
    ),
    # ============================ Google Play ============================
    Endpoint(
        key="google_play_search",
        namespace="google_play",
        method="search",
        http="POST",
        path="/api/v1/googleplay/search",
        summary=(
            "Ranked Google Play apps: package name, title, developer, rating, install count, price and "
            "IAP range, content rating, icon and screenshots. A branded query returns the hero card as "
            "result 1 in the same row shape, plus Play's related-query rail. NO PAGINATION - one shelf "
            "of about 30 apps. Costs 2 credits."
        ),
        params=(
            _req(
                "query",
                "What to search the store for (1-200 characters): an app name, a publisher, or a "
                "category phrase. Apps only - games are folded into the apps vertical, but books and "
                "films use a different card shape and are not covered.",
            ),
            _str(
                "hl",
                "UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not only the "
                "strings: at hl=pt-BR the title, description, install formatting and content rating all "
                "move with it. Play silently falls back to English on a value it does not serve.",
            ),
            _str(
                "gl",
                "Country code, 2-10 characters (default 'us'), deciding which storefront's price and "
                "availability are returned. Play silently falls back to the US storefront on a country "
                "it does not serve.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="google_play_app",
        namespace="google_play",
        method="app",
        http="POST",
        path="/api/v1/googleplay/app",
        summary=(
            "Full Google Play store listing: installs including the REAL count Play publishes but never "
            "renders, rating and star histogram, description, developer identity and legal contact, "
            "price and IAPs, categories and gameplay tags, screenshots and trailer, version and Android "
            "requirement, release and update dates, changelog, the full permission tree, the Data "
            "safety table, the 20 server-rendered reviews and the similar-apps and more-by-developer "
            "rails. Costs 2 credits."
        ),
        params=(
            _req(
                "app_id",
                "Android package name ('com.spotify.music') or any play.google.com URL carrying one in "
                "its id param (1-500 characters).",
            ),
            _str(
                "hl",
                "UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not only the "
                "strings: title, description, install formatting and content rating all move with it. "
                "Play silently falls back to English on a value it does not serve.",
            ),
            _str(
                "gl",
                "Country code, 2-10 characters (default 'us'), deciding which storefront's price and "
                "availability are returned. Play silently falls back to the US storefront on a country "
                "it does not serve.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="google_play_reviews",
        namespace="google_play",
        method="reviews",
        http="POST",
        path="/api/v1/googleplay/reviews",
        summary=(
            "A page of Google Play reviews: star score, full text, author, thumbs-up count, developer "
            "reply and the APP VERSION the reviewer was running. Paged by cursor, up to 200 per call. "
            "app() already returns the 20 reviews Play server-renders; use this to page past them or "
            "sort differently. Costs 2 credits."
        ),
        params=(
            _req(
                "app_id",
                "Android package name ('com.spotify.music') or any play.google.com URL carrying one in "
                "its id param (1-500 characters).",
            ),
            _lit(
                "sort",
                ("relevance", "newest", "rating"),
                "Review ordering (default 'newest'). Closed enum. The cursor encodes the sort, so keep "
                "this identical when paging.",
            ),
            _int(
                "count",
                "Reviews to return, 1-200 (default 50); 200 is our cap, not Play's. Play honours more, "
                "but a single page that large is megabytes for one credit - page with cursor instead.",
            ),
            _str(
                "cursor",
                "Continuation token from a prior response's next_cursor (1-4000 characters). Opaque and "
                "SINGLE-USE, and it encodes the sort as well as the position - send it back with the "
                "SAME sort it came from. A cursor past the last review is a 404, not an empty page.",
            ),
            _str(
                "hl",
                "UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not only the "
                "strings. Play silently falls back to English on a value it does not serve.",
            ),
            _str(
                "gl",
                "Country code, 2-10 characters (default 'us'), deciding which storefront's price and "
                "availability are returned. Play silently falls back to the US storefront on a country "
                "it does not serve.",
            ),
        ),
        credits=2,
    ),
    # ============================= SEC EDGAR =============================
    Endpoint(
        key="sec_lookup",
        namespace="sec",
        method="lookup",
        http="POST",
        path="/api/v1/sec/lookup",
        summary=(
            "START HERE. Resolve a company name or ticker (AAPL) to the CIK (0000320193) every "
            "other SEC EDGAR endpoint is keyed by. Up to 100 rows, tiered by match quality."
        ),
        params=(
            _req(
                "query",
                "Ticker ('AAPL', 'BRK.B'), company name, or a fragment of one (1-200 characters); "
                "each row carries its match tier as 'match'.",
            ),
            _int("limit", "Rows to return, 1-100. Defaults to 10. Sizes the response; it is not a page param."),
            _lit(
                "exchange",
                ("NASDAQ", "NYSE", "OTC", "CBOE"),
                "Restrict to one listing venue; matched case-insensitively, so 'Nasdaq' also "
                "works. Filers the SEC lists with no exchange at all are excluded by any value.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="sec_company",
        namespace="sec",
        method="company",
        http="POST",
        path="/api/v1/sec/company",
        summary=(
            "SEC filer profile: legal and former names, SIC industry, filer category, EIN, LEI, "
            "state of incorporation, fiscal year end, addresses, every ticker with its exchange, "
            "and a preview of its 10 most recent filings. Provide cik or ticker."
        ),
        params=(
            _str(
                "cik",
                "Filer CIK in any spelling (1-20 characters): 320193, 0000320193 or CIK0000320193. "
                "A ticker is accepted here too.",
            ),
            _str(
                "ticker",
                "Ticker symbol (1-20 characters), dotted or dashed (BRK.B / BRK-B). Wins over cik "
                "when both are given.",
            ),
        ),
        one_of=(("cik", "ticker"),),
        credits=1,
    ),
    Endpoint(
        key="sec_filings",
        namespace="sec",
        method="filings",
        http="POST",
        path="/api/v1/sec/filings",
        summary=(
            "A page of one filer's filings: accession number, form and root form, filing and "
            "period dates, 8-K item codes, direct links to the primary document, filing index and "
            "attachment directory. Up to 500 per page. Provide cik or ticker."
        ),
        params=(
            _str("cik", "Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted here too."),
            _str("ticker", "Ticker symbol (1-20 characters), as an alternative to cik."),
            _str_or_list(
                "form",
                "Form types to keep: '10-K', ['10-K', '10-Q'] or the comma-joined '10-K,8-K'; "
                "each value 1-50 characters, at most 25 values. Matched against the form AND its "
                "root form, so 10-K also returns 10-K/A amendments; ask for '10-K/A' to get only "
                "amendments.",
            ),
            _str("date_from", "Earliest filing date, inclusive (YYYY-MM-DD)."),
            _str("date_to", "Latest filing date, inclusive (YYYY-MM-DD)."),
            _int("page", "Results page, 1-based; page size is whatever limit is set to. No upper bound."),
            _int("limit", "Filings per page, 1-500. Defaults to 50."),
            _bool(
                "include_history",
                "Also fetch the archived filing history beyond EDGAR's 'recent' block, which is "
                "not a fixed window (a decade for a quiet filer, about a year for a prolific one). "
                "Off by default; at most 10 archived shards are fetched, history_truncated says "
                "when a filer had more, and it is still 1 credit.",
            ),
        ),
        one_of=(("cik", "ticker"),),
        credits=1,
    ),
    Endpoint(
        key="sec_concept",
        namespace="sec",
        method="concept",
        http="POST",
        path="/api/v1/sec/concept",
        summary=(
            "Every value a filer reported for one XBRL concept, newest period first, with the form "
            "and filing each number came from. Restatements are kept, not collapsed. Up to 2000 "
            "rows. Provide cik or ticker."
        ),
        params=(
            _req(
                "concept",
                "XBRL concept tag, CASE-SENSITIVE (1-120 characters, ^[A-Za-z][A-Za-z0-9]*$): "
                "'NetIncomeLoss' matches, 'netincomeloss' is a 404 upstream. Use facts() to list "
                "what a filer actually reports.",
            ),
            _str("cik", "Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted here too."),
            _str("ticker", "Ticker symbol (1-20 characters), as an alternative to cik."),
            _str(
                "taxonomy",
                "Reporting taxonomy (1-40 characters, ^[A-Za-z][A-Za-z0-9-]*$): us-gaap, dei, "
                "ifrs-full or srt. Defaults to 'us-gaap'.",
            ),
            _str("unit", "Unit of measure to keep (1-40 characters), e.g. 'USD' vs 'USD/shares'."),
            _str(
                "form",
                "Form to keep (1-50 characters). EXACT match here, unlike filings(), so '10-K' "
                "excludes 10-K/A.",
            ),
            _int("limit", "Rows to return, 1-2000. Defaults to 250. Sizes the response; it is not a page param."),
        ),
        one_of=(("cik", "ticker"),),
        credits=1,
    ),
    Endpoint(
        key="sec_facts",
        namespace="sec",
        method="facts",
        http="POST",
        path="/api/v1/sec/facts",
        summary=(
            "The index of every XBRL concept a filer reports - tag, label, description, units and "
            "most recent value - across us-gaap, dei and any other taxonomy it uses. This is how "
            "you find what to ask concept() for. Up to 2000 rows. Provide cik or ticker."
        ),
        params=(
            _str("cik", "Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted here too."),
            _str("ticker", "Ticker symbol (1-20 characters), as an alternative to cik."),
            _str("taxonomy", "Restrict to one taxonomy (1-40 characters), e.g. 'us-gaap' or 'dei'."),
            _str(
                "query",
                "Case-insensitive substring matched against the tag name and label (1-200 characters).",
            ),
            _int("limit", "Rows to return, 1-2000. Defaults to 250. Sizes the response; it is not a page param."),
        ),
        one_of=(("cik", "ticker"),),
        credits=1,
    ),
    Endpoint(
        key="sec_search",
        namespace="sec",
        method="search",
        http="POST",
        path="/api/v1/sec/search",
        summary=(
            "EDGAR full-text search, coverage starting 2001: each hit is the matching DOCUMENT "
            "with its URL, form, filing date and filer identity, plus facets by company, form, "
            "industry and state. 100 documents per page, last page is 100."
        ),
        params=(
            _str(
                "query",
                "Full-text query over filing documents (1-500 characters); a quoted phrase is "
                "matched exactly, bare words as a bag of terms. Optional - a cik, ticker, form or "
                "date filter on its own is a valid search.",
            ),
            _str_or_list(
                "cik",
                "Restrict to one or more filers by CIK: a single value, a list, or a comma-joined "
                "string; each 1-20 characters, at most 25 values. Tickers are accepted here too.",
            ),
            _str_or_list(
                "ticker",
                "Restrict to one or more filers by ticker symbol: a single value, a list, or a "
                "comma-joined string; each 1-20 characters, at most 25 values.",
            ),
            _str_or_list(
                "form",
                "Form types to keep: '8-K', ['10-K', '10-Q'] or the comma-joined '10-K,10-Q'; "
                "each 1-50 characters, at most 25 values.",
            ),
            _str("date_from", "Earliest filing date, inclusive (YYYY-MM-DD). Full-text coverage starts in 2001."),
            _str("date_to", "Latest filing date, inclusive (YYYY-MM-DD)."),
            _str_or_list(
                "location",
                "Filer business-address locations as EDGAR's own 2-character codes (CA, NY, and "
                "its alphanumeric codes for foreign jurisdictions): a single value, a list, or a "
                "comma-joined string; at most 25 values.",
            ),
            _lit(
                "sort",
                ("relevance", "newest", "oldest"),
                "Result ordering. Defaults to the index's own relevance ranking.",
            ),
            _int(
                "page",
                "Results page, 1-based, 1-100, 100 documents per page. The SEC's index refuses a "
                "result window past 10,000, so 100 is the last page for any query.",
            ),
        ),
        credits=1,
    ),
    # =============================== Redfin ==============================
    Endpoint(
        key="redfin_search",
        namespace="redfin",
        method="search",
        http="POST",
        path="/api/v1/redfin/search",
        summary=(
            "Redfin listings: price, price per sqft, beds, baths, living area, lot size, year "
            "built, coordinates, listing remarks and full photo galleries, for sale, sold or for "
            "rent. Up to 350 per page. Provide location, or region_id together with region_type."
        ),
        params=(
            _str(
                "location",
                "A redfin.com region URL (/city/, /neighborhood/, /county/, /zipcode/) or a bare "
                "5-digit ZIP (1-500 characters). CITY NAMES ARE NOT ACCEPTED - Redfin's own name "
                "lookup is blocked to us; use region_id + region_type instead.",
            ),
            _int(
                "region_id",
                "Redfin internal region id (>= 1), used together with region_type. NOT a ZIP code "
                "- the two are different number spaces and a ZIP here resolves to another city "
                "rather than failing.",
            ),
            _ilit(
                "region_type",
                (1, 2, 5, 6),
                "Region kind that region_id belongs to: 1 neighborhood, 2 ZIP, 5 county, 6 city. "
                "Must be sent together with region_id or both are ignored in favour of location.",
            ),
            _lit(
                "listing_status",
                ("for_sale", "sold", "for_rent"),
                "Market to search. Defaults to 'for_sale'.",
            ),
            _int(
                "sold_within_days",
                "Sold within the last N days (>= 1). REJECTED unless listing_status='sold', where "
                "it defaults to 90.",
            ),
            _int("page", "Results page, 1-based; page size is whatever limit is set to. No upper bound."),
            _int("limit", "Listings per page, 1-350. Defaults to 100."),
            _lit(
                "sort",
                (
                    "recommended",
                    "price_low",
                    "price_high",
                    "newest",
                    "oldest",
                    "sqft_low",
                    "sqft_high",
                    "price_per_sqft_low",
                    "price_per_sqft_high",
                ),
                "Result sort order. Defaults to 'recommended', Redfin's own ranking.",
            ),
            _float(
                "min_price",
                "Minimum price, inclusive (>= 0). Monthly rent when listing_status='for_rent'.",
            ),
            _float(
                "max_price",
                "Maximum price, inclusive (>= 0). Monthly rent when listing_status='for_rent'.",
            ),
            _int("beds_min", "Minimum bedrooms (whole number >= 0); fractional values are rejected."),
            _int("beds_max", "Maximum bedrooms (whole number >= 0); fractional values are rejected."),
            _int(
                "baths_min",
                "Minimum bathrooms (whole number >= 0). WHOLE BATHS ONLY - 1.5 is rejected rather "
                "than silently truncated to 1. There is no baths_max.",
            ),
            _int("sqft_min", "Minimum living area in square feet (whole number >= 0)."),
            _int("sqft_max", "Maximum living area in square feet (whole number >= 0)."),
            _int("lot_size_min", "Minimum lot size in square feet (whole number >= 0). There is no lot_size_max."),
            _int("year_built_min", "Earliest year built (whole number >= 0)."),
            _int("year_built_max", "Latest year built (whole number >= 0)."),
            _float(
                "max_hoa",
                "Maximum monthly HOA fee in dollars (>= 0).",
            ),
            _lit(
                "property_type",
                ("house", "condo", "townhouse", "multi_family", "land", "other", "co_op"),
                "Restrict to one property type.",
            ),
            _bool("has_pool", "Only listings with a pool."),
            _int(
                "max_days_on_market",
                "Listed at most N days ago (whole number >= 0). Cannot be combined with "
                "min_days_on_market - Redfin expresses both bounds through one param.",
            ),
            _int(
                "min_days_on_market",
                "Listed at least N days ago (whole number >= 0). Cannot be combined with "
                "max_days_on_market.",
            ),
        ),
        one_of=(("location", "region_id"),),
        credits=1,
    ),
    Endpoint(
        key="redfin_property",
        namespace="redfin",
        method="property",
        http="POST",
        path="/api/v1/redfin/property",
        summary=(
            "One Redfin listing in full: price, Redfin Estimate and rental estimate, complete MLS "
            "fact sheet, price and tax history, listing agents, open houses, schools, climate "
            "risk, walkability, sun exposure, monthly weather, permits, zoning, comparable sales "
            "and photos."
        ),
        params=(
            _req(
                "property_id",
                "Redfin property id, or any redfin.com listing URL carrying one (1-500 characters).",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="redfin_market",
        namespace="redfin",
        method="market",
        http="POST",
        path="/api/v1/redfin/market",
        summary=(
            "Redfin housing-market stats for a region: median list and sale price, price per sqft, "
            "sale-to-list ratio, average offers and days on market, YoY movement, 0-100 compete "
            "score, live inventory by property type and by bedroom count, and Redfin agent "
            "presence. Provide location, or region_id together with region_type."
        ),
        params=(
            _str(
                "location",
                "A redfin.com region URL (/city/, /neighborhood/, /county/, /zipcode/) or a bare "
                "5-digit ZIP (1-500 characters). City names are not accepted.",
            ),
            _int("region_id", "Redfin internal region id (>= 1), used together with region_type. Not a ZIP code."),
            _ilit(
                "region_type",
                (1, 2, 5, 6),
                "Region kind that region_id belongs to: 1 neighborhood, 2 ZIP, 5 county, 6 city. "
                "Must be sent together with region_id or both are ignored in favour of location.",
            ),
        ),
        one_of=(("location", "region_id"),),
        credits=1,
    ),
    # ========================== Companies House ==========================
    Endpoint(
        key="companies_house_search",
        namespace="companies_house",
        method="search",
        http="POST",
        path="/api/v1/companieshouse/search",
        summary=(
            "START HERE. Search the UK register by name and get the company_number every other "
            "Companies House endpoint is keyed by, plus status, incorporation or dissolution "
            "date, registered office and matched former names. 20 per page, last page is 50."
        ),
        params=(
            _req(
                "query",
                "Company name or fragment (1-200 characters, non-blank). Matches CURRENT AND "
                "FORMER names.",
            ),
            _int(
                "page",
                "Results page, 1-based, 1-50, 20 results per page. Defaults to 1. The register "
                "serves only a 1000-result window per term whatever hit count it prints, and "
                "answers page 51 with HTTP 416.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="companies_house_company",
        namespace="companies_house",
        method="company",
        http="POST",
        path="/api/v1/companieshouse/company",
        summary=(
            "Full UK register entry: status, type, incorporation and dissolution dates, registered "
            "office, SIC codes, previous names, accounts and confirmation-statement due dates with "
            "overdue flags, and whether it has charges, insolvency history, officers or UK "
            "establishments."
        ),
        params=(
            _req(
                "company_number",
                "UK company number (1-20 characters), zero-padded and upper-cased for you, so "
                "'445790' and 'sc090312' both work. Registry prefixes supported: SC, NI, OC, SO, "
                "NC, FC, BR, CE.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="companies_house_officers",
        namespace="companies_house",
        method="officers",
        http="POST",
        path="/api/v1/companieshouse/officers",
        summary=(
            "UK company officers, current and resigned, 35 per page: name, role, appointment and "
            "resignation dates, correspondence address, nationality, country of residence, "
            "month-and-year date of birth and identity-verification status."
        ),
        params=(
            _req(
                "company_number",
                "UK company number (1-20 characters), zero-padded and upper-cased for you.",
            ),
            _int(
                "page",
                "Results page, 1-based, 35 per page. Defaults to 1. No upper bound: past the last "
                "page the register answers an ordinary 200 with an empty list, identical to a "
                "company with no officers.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="companies_house_filing_history",
        namespace="companies_house",
        method="filing_history",
        http="POST",
        path="/api/v1/companieshouse/filing-history",
        summary=(
            "UK filings, most recent first: date, filing type code (AA, CS01, SH03), description, "
            "register annotations and child documents, and a link to the filed PDF with its page "
            "count. A filing the register has not finished processing carries a processing_note "
            "instead of a document."
        ),
        params=(
            _req(
                "company_number",
                "UK company number (1-20 characters), zero-padded and upper-cased for you.",
            ),
            _int(
                "page",
                "Results page, 1-based. Defaults to 1. No upper bound: past the last page the "
                "register answers an ordinary 200 with an empty list.",
            ),
        ),
        credits=1,
    ),
    # ================================= G2 ================================
    Endpoint(
        key="g2_search",
        namespace="g2",
        method="search",
        http="POST",
        path="/api/v1/g2/search",
        summary=(
            "Search G2, the B2B software review site, for products: star rating, review count, "
            "vendor, categories, seller description and logo, with product_id and slug on every "
            "row. Up to 100 results per page (server default 20) and page-paginated; "
            "total_results is G2's Products-tab headline and caps at 10000, while total_by_type "
            "splits the query across products, sellers, categories and discussions. Provide "
            "query or url."
        ),
        params=(
            _str("query", "Search term (1-200 characters). Provide this or url."),
            _int(
                "page",
                "1-based page number; page size follows limit (server default 20). G2 keeps "
                "paginating well past its own widget's page links.",
            ),
            _int(
                "limit",
                "Results per page (1-100; server default 20). The 100 ceiling is ours, to keep a "
                "single request inside the 60s deadline; G2 itself paginates at any size.",
            ),
            _lit(
                "sort",
                ("relevance", "popular", "alphabetical", "rating"),
                "Result sort order (server default 'relevance'). Closed enum: G2 silently accepts "
                "an unknown sort and answers 200 with an unstated ordering.",
            ),
            _ilit(
                "rating",
                (1, 2, 3, 4, 5),
                "Only products at or above this star rating (1-5, sent as an integer). Omit for "
                "no rating floor.",
            ),
            _str(
                "url",
                "Full g2.com/search URL, as an alternative to query (1-1000 characters; the host "
                "is checked by the transport).",
            ),
        ),
        one_of=(("query", "url"),),
        credits=5,
    ),
    Endpoint(
        key="g2_product",
        namespace="g2",
        method="product",
        http="POST",
        path="/api/v1/g2/product",
        summary=(
            "Full G2 product profile: rating with per-star histogram, review count, vendor, "
            "description and seller website, pricing editions with parsed amounts, feature "
            "groups, categories and breadcrumbs, supported languages, integrations, "
            "alternatives, head-to-head comparisons, media, community discussions and G2's "
            "AI-derived pros and cons. Carries NO review text at all -- G2 loads review bodies in "
            "a separate frame, so call reviews() for those. Provide product_id or url."
        ),
        params=(
            _str(
                "product_id",
                "G2 product slug ('notion') or the numeric G2 id ('82623') as a string "
                "(1-200 characters); both resolve on the same upstream path.",
            ),
            _str(
                "url",
                "Full g2.com product URL, as an alternative to product_id (1-1000 characters).",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=5,
    ),
    Endpoint(
        key="g2_reviews",
        namespace="g2",
        method="reviews",
        http="POST",
        path="/api/v1/g2/reviews",
        summary=(
            "A page of G2 reviews: rating, title, likes and dislikes, problems solved, reviewer "
            "job title, industry and company size, validated and incentivized flags -- plus what "
            "the profile page has no form of: exact per-star counts, pros and cons with per-theme "
            "counts, and company-size, role, industry, region and category facets with counts. "
            "Fixed at 10 reviews per page and paginates well past the 10 pages G2's own widget "
            "links to. Provide product_id or url."
        ),
        params=(
            _str(
                "product_id",
                "G2 product slug or numeric G2 id as a string (1-200 characters).",
            ),
            _str(
                "url",
                "Full g2.com reviews URL, as an alternative to product_id (1-1000 characters).",
            ),
            _int("page", "1-based page number; fixed at 10 reviews per page."),
            _lit(
                "sort",
                ("relevance", "newest", "most_helpful", "rating_high", "rating_low"),
                "Review sort order (server default 'relevance'). Closed enum: an unknown sort is "
                "silently accepted upstream and never runs.",
            ),
            _ilit(
                "rating",
                (1, 2, 3, 4, 5),
                "Only reviews in this star bucket (1-5, sent as an integer). Buckets are half- "
                "star-inclusive: 1 returns 0, 0.5 and 1-star reviews.",
            ),
            _lit(
                "company_size",
                ("small_business", "mid_market", "enterprise"),
                "Reviewer company size: small_business is 50 employees or fewer, mid_market "
                "51-1000, enterprise over 1000. Closed enum -- an unknown value matches nothing "
                "and returns a billed 'Reviews (0)'.",
            ),
            _lit(
                "role",
                (
                    "user",
                    "administrator",
                    "executive_sponsor",
                    "internal_consultant",
                    "consultant",
                    "agency",
                    "industry_analyst",
                ),
                "Reviewer role. Closed enum -- an unknown value matches nothing rather than "
                "erroring.",
            ),
            _lit(
                "region",
                (
                    "north_america",
                    "europe",
                    "asia",
                    "latin_america",
                    "anz",
                    "middle_east",
                    "africa",
                ),
                "Reviewer region. Closed enum -- an unknown value matches nothing rather than "
                "erroring.",
            ),
            _str(
                "query",
                "Full-text search within this product's reviews (1-200 characters); narrows the "
                "review list AND every facet count.",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=5,
    ),
    # ============================== Capterra =============================
    Endpoint(
        key="capterra_search",
        namespace="capterra",
        method="search",
        http="POST",
        path="/api/v1/capterra/search",
        summary=(
            "Search Capterra, the B2B software review site: 20 ranked products with name, vendor "
            "description, rating, review count, logo and paid-placement flag, each row carrying "
            "product_id and slug. The result set is fixed at 20 and does NOT paginate -- Capterra "
            "serves identical rows for page 2, so there is deliberately no page parameter. "
            "Provide query or url."
        ),
        params=(
            _str(
                "query",
                "Search term (1-200 characters). Required in practice: a term-less Capterra "
                "search serves a fixed popular-products list unrelated to the caller.",
            ),
            _str(
                "url",
                "Full capterra.com search URL, as an alternative to query (1-1000 characters; "
                "the transport also accepts capterra.co.uk and capterra.com.br hosts).",
            ),
        ),
        one_of=(("query", "url"),),
        credits=2,
    ),
    Endpoint(
        key="capterra_product",
        namespace="capterra",
        method="product",
        http="POST",
        path="/api/v1/capterra/product",
        summary=(
            "Full Capterra profile: rating with per-star histogram and the four scored criteria, "
            "likelihood to recommend, review sentiment and topics, the complete pricing table "
            "with every plan and its features, every rated feature and integration, AI-derived "
            "pros and cons with the quoted review, FAQs, screenshots, badges and awards, "
            "competitor comparisons and alternatives, and the buyer profile by company size, "
            "industry and job function -- PLUS the 25 most recent reviews at no extra cost. "
            "vendor is always null here: Capterra does not publish it as structured data on the "
            "product page. Provide product_id or url."
        ),
        params=(
            _str(
                "product_id",
                "The number in a Capterra product path such as /p/186596/Notion/ (1-50 "
                "characters). Must be a STRING -- a JSON number is rejected.",
            ),
            _str(
                "slug",
                "Product slug (1-200 characters). Cosmetic on this endpoint -- a wrong slug still "
                "returns the right profile -- but load-bearing on reviews().",
            ),
            _str(
                "url",
                "Full Capterra product URL, as an alternative to product_id (1-1000 characters).",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=2,
    ),
    Endpoint(
        key="capterra_reviews",
        namespace="capterra",
        method="reviews",
        http="POST",
        path="/api/v1/capterra/reviews",
        summary=(
            "A page of Capterra reviews: overall score plus five per-criterion scores, title, "
            "pros, cons, advice, usage duration, incentivized flag, alternatives considered and "
            "what they switched from, reviewer job title, industry and company size, and the "
            "vendor response -- plus a competitor list richer than the profile's, each "
            "alternative with its own rating histogram and starting price. 25 reviews per page, "
            "capped at page 100. Page 1 already rides along inside product(), so use this to page "
            "past it. Provide product_id or url."
        ),
        params=(
            _str("product_id", "Capterra product id as a string (1-50 characters)."),
            _str(
                "slug",
                "Product slug (1-200 characters). LOAD-BEARING here: it is case-sensitive "
                "upstream and a wrong one silently serves page one under a billed 200. Pass back "
                "the slug from search() or product().",
            ),
            _str(
                "url",
                "Full Capterra reviews URL, as an alternative to product_id (1-1000 characters). "
                "Passing back reviews_url from product() is the reliable way to page.",
            ),
            _int(
                "page",
                "1-based page number (1-100); 25 reviews per page. 100 is a hard cap whatever the "
                "review count says -- past it Capterra answers 200 with page one.",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=2,
    ),
    # ====================== Google Ads Transparency ======================
    Endpoint(
        key="google_ads_advertisers",
        namespace="google_ads",
        method="advertisers",
        http="POST",
        path="/api/v1/googleads/advertisers",
        summary=(
            "Resolve a brand name or domain to the advertiser_id that search() and creative() are "
            "keyed by. Returns two row kinds in one list: 'advertiser' rows carrying the id, "
            "verified name, verification country and total ad count as a range, and 'domain' rows "
            "carrying a website. A name query returns both kinds; a domain-shaped query returns "
            "domains only. Autocomplete-backed, roughly 20 rows per arm, and it does not "
            "paginate."
        ),
        params=(
            _req("query", "Brand name or domain to resolve (1-200 characters)."),
            _str(
                "region",
                "ISO 3166-1 alpha-2 country ('US', 'GB', 'DE') or a Google geo criteria id as a "
                "string (2-12 characters). Defaults to the UNITED STATES, not worldwide -- the "
                "lookup runs against one country's index at a time, so an advertiser who runs no "
                "US ads comes back as an empty list. Set it to a country the advertiser "
                "actually advertises in.",
            ),
            _int(
                "limit",
                "Rows per arm (1-20; server default 10). Advertisers and domains are capped "
                "separately, so a name query can return up to twice this many rows.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="google_ads_search",
        namespace="google_ads",
        method="search",
        http="POST",
        path="/api/v1/googleads/search",
        summary=(
            "Every ad Google Ads Transparency holds for one advertiser: the creative (archived "
            "image, rich-media bundle, Google's renderer link, dimensions), advertiser id and "
            "name, format, first and last seen dates and days actually run, plus total_ads_min "
            "and total_ads_max -- Google publishes the advertiser's ad total as a range, never an "
            "exact figure. Up to 100 ads per page (server default 40); paginate by sending "
            "next_cursor back as cursor alongside the SAME filters. Provide domain or "
            "advertiser_id."
        ),
        params=(
            _str(
                "domain",
                "Advertiser website (1-253 characters): bare host, www host or full URL, reduced "
                "to the registrable host. The only way to get `domain` back on each row.",
            ),
            _str(
                "advertiser_id",
                "Google advertiser id, e.g. 'AR16735076323512287233' (3-40 characters). The shape "
                "is checked before any request, so a typo costs no credits. Querying by id drops "
                "`domain` from every row.",
            ),
            _str(
                "region",
                "ISO 3166-1 alpha-2 country ('US', 'GB', 'DE') or a Google geo criteria id as a "
                "string (2-12 characters). Scopes the deep links on every row, and the same "
                "advertiser can share zero creatives between two countries. Default: worldwide.",
            ),
            _lit(
                "format",
                ("text", "image", "video"),
                "Creative format. The three sets are disjoint -- an advertiser's text, image and "
                "video ads share no creatives. Default: all formats.",
            ),
            _lit(
                "platform",
                ("play", "maps", "search", "shopping", "youtube"),
                "Google surface the ad ran on. Default: all surfaces.",
            ),
            _lit(
                "topic",
                ("all", "political"),
                "Ad topic (server default 'all').",
            ),
            _int(
                "limit",
                "Ads per page (1-100; server default 40). 100 is a hard upstream ceiling, not our "
                "policy: Google answers a larger request with zero rows rather than an error.",
            ),
            _str(
                "cursor",
                "next_cursor from the previous response (1-4000 characters), 100 ads per page. "
                "Re-send the same filters alongside it; next_cursor is null once exhausted.",
            ),
        ),
        one_of=(("domain", "advertiser_id"),),
        credits=1,
    ),
    Endpoint(
        key="google_ads_creative",
        namespace="google_ads",
        method="creative",
        http="POST",
        path="/api/v1/googleads/creative",
        summary=(
            "One creative in full, and the only endpoint carrying its history: every size "
            "variation of the asset, the impression bucket, the per-region breakdown with first "
            "and last shown dates and a per-surface impression split inside each region, the "
            "format, Google's category label and the funder disclosure on political ads. "
            "Impressions and first_shown are EEA-only (DSA-compelled) and come back null for US "
            "creatives, and an impression bucket may carry only a lower or only an upper bound."
        ),
        params=(
            _req(
                "advertiser_id",
                "Google advertiser id, e.g. 'AR16735076323512287233' (3-40 characters).",
            ),
            _req(
                "creative_id",
                "Creative id (3-40 characters). It must belong to the advertiser_id sent with it "
                "-- the lookup is keyed by the pair and a mismatched pair is a 404.",
            ),
        ),
        credits=1,
    ),
    # ========================== Meta Ad Library ==========================
    Endpoint(
        key="meta_ads_search",
        namespace="meta_ads",
        method="search",
        http="POST",
        path="/api/v1/meta-ads/search",
        summary=(
            "Search the Meta Ad Library by keyword: 30 ads on page 1 with the full creative -- "
            "page name, ad copy, headline, CTA, images and videos, the platforms each ran on and "
            "its run dates -- then 10 ads per cursor page, walking has_next_page to the end of "
            "the query. total_results caps at 50000 with total_is_capped true, because Meta only "
            "reports '>50,000'; never present it as an exact count. Every page costs 1 credit."
        ),
        params=(
            _req("query", "Keyword to search the ad library for (1-200 characters)."),
            _str(
                "country",
                "Ad library country as an exactly 2-character ISO 3166-1 alpha-2 code (server "
                "default 'US').",
            ),
            _lit(
                "active_status",
                ("all", "active", "inactive"),
                "Whether the ad is still running (server default 'all').",
            ),
            _lit(
                "ad_type",
                ("all", "political_and_issue_ads"),
                "Set 'political_and_issue_ads' to expose spend, reach, impressions and the "
                "paid-for-by disclosure; commercial ads leave all four null (server default "
                "'all').",
            ),
            _lit(
                "media_type",
                ("all", "image", "video", "meme", "image_and_meme", "none"),
                "Creative media filter. Default: no media filter.",
            ),
            _lit(
                "search_type",
                ("keyword_unordered", "keyword_exact_phrase"),
                "How the query is matched (server default 'keyword_unordered').",
            ),
            _str(
                "cursor",
                "next_cursor from the previous response: page 1 is 30 ads, every cursor page is "
                "10. The cursor is a self-contained blob, so ALL other filters are ignored when "
                "it is present.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="meta_ads_advertiser",
        namespace="meta_ads",
        method="advertiser",
        http="POST",
        path="/api/v1/meta-ads/advertiser",
        summary=(
            "Every ad a Facebook Page is running, by numeric page id: 30 ads on page 1 with the "
            "same creative detail as search(), then 10 ads per cursor page, walking has_next_page "
            "to the end of the advertiser. Every page costs 1 credit."
        ),
        params=(
            _req(
                "page_id",
                "The advertiser's numeric Facebook Page id (3-25 digits, as a string).",
            ),
            _str(
                "country",
                "Ad library country as an exactly 2-character ISO 3166-1 alpha-2 code (server "
                "default 'US').",
            ),
            _lit(
                "active_status",
                ("all", "active", "inactive"),
                "Whether the ad is still running (server default 'all').",
            ),
            _lit(
                "ad_type",
                ("all", "political_and_issue_ads"),
                "Set 'political_and_issue_ads' to expose spend, reach, impressions and the "
                "paid-for-by disclosure; commercial ads leave all four null (server default "
                "'all').",
            ),
            _lit(
                "media_type",
                ("all", "image", "video", "meme", "image_and_meme", "none"),
                "Creative media filter. Default: no media filter.",
            ),
            _str(
                "cursor",
                "next_cursor from the previous response: page 1 is 30 ads, every cursor page is "
                "10. ALL other filters are ignored when it is present.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="meta_ads_ad",
        namespace="meta_ads",
        method="ad",
        http="POST",
        path="/api/v1/meta-ads/ad",
        summary=(
            "One Meta ad in full by archive id: creative, advertiser, run dates, the platforms it "
            "ran on, and the political disclosure when the ad carries one. Commercial ads leave "
            "spend, reach and impressions null."
        ),
        params=(
            _req("ad_archive_id", "Meta ad archive id (3-25 digits, as a string)."),
        ),
        credits=1,
    ),
    # ============================== Costco ===============================
    # 13 endpoints. Most cost 1 credit; the multi-warehouse ones are
    # BODY-PRICED (backend costcoRequestCost): prices/availability/gas scale
    # with warehouse_ids, and country "ca" warehouses/gas cost 2 per lookup.
    # credits_note states the rule wherever the price is not a constant.
    Endpoint(
        key="costco_search",
        namespace="costco",
        method="search",
        http="POST",
        path="/api/v1/costco/search",
        summary=(
            "Search Costco by keyword or item number: online price and original price, ratings, "
            "member-only and stock flags, promotions and facets. Pass warehouse_id to add that "
            "warehouse's in-store price, stock status and price code to every result. US and "
            "Canada support every filter; UK, Australia, Mexico, Japan, Korea and Taiwan support "
            "keyword, sort and paging only."
        ),
        params=(
            _req("query", "Keywords, or a Costco item number (1-200 characters)."),
            _COSTCO_ANY_COUNTRY,
            *_COSTCO_LISTING_FILTERS,
        ),
        credits=1,
    ),
    Endpoint(
        key="costco_category",
        namespace="costco",
        method="category",
        http="POST",
        path="/api/v1/costco/category",
        summary=(
            "Products in a Costco category, with the same sort, filters and per-warehouse "
            "pricing as search()."
        ),
        params=(
            _req(
                "category",
                "Category slug from categories() (e.g. 'televisions'), or a costco.com category "
                "URL (1-200 characters).",
            ),
            _COSTCO_NA_COUNTRY,
            *_COSTCO_LISTING_FILTERS,
        ),
        credits=1,
    ),
    Endpoint(
        key="costco_categories",
        namespace="costco",
        method="categories",
        http="POST",
        path="/api/v1/costco/categories",
        summary=(
            "The Costco department list, or the full subcategory tree under one department."
        ),
        params=(
            _str(
                "category_id",
                "Numeric Costco category id (e.g. '30001'). Omit for the top-level departments; "
                "pass one for its full subcategory tree.",
            ),
            _COSTCO_NA_COUNTRY,
        ),
        credits=1,
    ),
    Endpoint(
        key="costco_product",
        namespace="costco",
        method="product",
        http="POST",
        path="/api/v1/costco/product",
        summary=(
            "Full details for up to 20 Costco items: description, features, specifications, "
            "variants, member-only and purchase limits, delivery fee, and promotions with start "
            "and end dates. Pass item_id for one item or item_ids for several."
        ),
        params=(
            # item_id stays positional (with a None default) so the common
            # single-item call is costco.product("100334960").
            Param(
                "item_id",
                "Optional[str]",
                positional=True,
                doc="Costco item number or product id, or a costco.com product URL.",
            ),
            _str_list(
                "item_ids",
                "Up to 20 item numbers / product ids in one call (us and ca only; the other "
                "countries look up one product per call).",
            ),
            _COSTCO_ANY_COUNTRY,
        ),
        one_of=(("item_id", "item_ids"),),
        credits=1,
    ),
    Endpoint(
        key="costco_prices",
        namespace="costco",
        method="prices",
        http="POST",
        path="/api/v1/costco/prices",
        summary=(
            "Online price versus in-warehouse price for up to 20 items across up to 10 "
            "warehouses, with each location's discount, final price, promotion dates and price "
            "code. Pass item_id or item_ids."
        ),
        params=(
            _str("item_id", "Costco item number or product id, or a costco.com product URL."),
            _str_list("item_ids", "Up to 20 item numbers / product ids in one call."),
            # Required, but keyword-only: a positional list here would let
            # prices("1492456") silently send an item number as warehouse_ids.
            # The one-member one_of group enforces it client-side.
            _str_list(
                "warehouse_ids",
                "Required. Costco warehouse numbers to price (1-10, e.g. ['1062', '1107']), "
                "from warehouses(). The online price is always included.",
            ),
            _COSTCO_NA_COUNTRY,
        ),
        one_of=(("item_id", "item_ids"), ("warehouse_ids",)),
        credits=1,
        credits_note=(
            "Costs 1 credit for up to 9 warehouses and 2 credits for 10 (the online price is "
            "always included and does not count toward the 10)."
        ),
    ),
    Endpoint(
        key="costco_availability",
        namespace="costco",
        method="availability",
        http="POST",
        path="/api/v1/costco/availability",
        summary=(
            "In-warehouse stock status for one item at up to 10 warehouses, plus pickup and "
            "same-day delivery availability. Stock is a status, never a quantity."
        ),
        params=(
            _req(
                "item_number",
                "Costco item number or product id, or a costco.com product URL.",
            ),
            _str_list(
                "warehouse_ids",
                "Costco warehouse numbers to check (1-10), from warehouses().",
                required=True,
            ),
            _COSTCO_NA_COUNTRY,
        ),
        credits=1,
        credits_note="Costs 1 credit per 5 warehouses (2 credits for 6-10).",
    ),
    Endpoint(
        key="costco_reviews",
        namespace="costco",
        method="reviews",
        http="POST",
        path="/api/v1/costco/reviews",
        summary=(
            "Customer reviews for a Costco product with the rating distribution and recommend "
            "count; sort, star filter and up to 100 reviews per page."
        ),
        params=(
            _req(
                "product_id",
                "Costco product id (the product_id field from search() or product()).",
            ),
            _lit(
                "sort_by",
                ("newest", "oldest", "highest_rating", "lowest_rating", "most_helpful"),
                "Review order (server default 'newest').",
            ),
            _int("rating", "Only reviews with this star rating (1-5)."),
            _int("page", "Results page, 1-based (1-500)."),
            _int("limit", "Reviews per page (1-100; server default 25)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="costco_warehouses",
        namespace="costco",
        method="warehouses",
        http="POST",
        path="/api/v1/costco/warehouses",
        summary=(
            "Costco warehouses near a US zip code or coordinates, nearest first: warehouse_id, "
            "address, hours, departments, services, and gas station hours and prices. Pass zip, "
            "or latitude and longitude."
        ),
        params=(
            _str("zip", "US zip code (5-10 characters). Zip lookup is US-only."),
            _float("latitude", "Latitude (-90 to 90); pass with longitude."),
            _float("longitude", "Longitude (-180 to 180); pass with latitude."),
            _COSTCO_ANY_COUNTRY,
            _int("limit", "Nearest warehouses to return (1-50; server default 10)."),
        ),
        one_of=(("zip", "latitude"),),
        credits=1,
        credits_note="Costs 1 credit, or 2 credits with country 'ca'.",
    ),
    Endpoint(
        key="costco_gas",
        namespace="costco",
        method="gas",
        http="POST",
        path="/api/v1/costco/gas",
        summary=(
            "Current regular, premium and diesel prices at Costco gas stations near a location, "
            "or at specific warehouses. Pass zip, latitude and longitude, or warehouse_ids."
        ),
        params=(
            _str("zip", "US zip code (5-10 characters)."),
            _float("latitude", "Latitude (-90 to 90); pass with longitude."),
            _float("longitude", "Longitude (-180 to 180); pass with latitude."),
            _str_list(
                "warehouse_ids",
                "Specific Costco warehouse numbers instead of a location (1-10).",
            ),
            _COSTCO_NA_COUNTRY,
            _int("limit", "Nearest stations to return (1-50)."),
        ),
        one_of=(("zip", "latitude", "warehouse_ids"),),
        credits=1,
        credits_note=(
            "Costs 1 credit by location (2 with country 'ca'); by warehouse_ids, 1 credit per 5 "
            "warehouses on us and 2 credits per warehouse on ca."
        ),
    ),
    Endpoint(
        key="costco_coupons",
        namespace="costco",
        method="coupons",
        http="POST",
        path="/api/v1/costco/coupons",
        summary=(
            "The current Costco member coupon book (US): every offer with its item number, "
            "discount, final price, warehouse/online scope, limits and the book's valid dates. "
            "Takes no parameters."
        ),
        params=(),
        credits=1,
    ),
    Endpoint(
        key="costco_deals",
        namespace="costco",
        method="deals",
        http="POST",
        path="/api/v1/costco/deals",
        summary=(
            "Costco deal feeds: new items, while supplies last, treasure hunt, member favorites, "
            "online-only and everything on sale, with the same filters and optional "
            "per-warehouse pricing as search()."
        ),
        params=(
            Param(
                "type",
                'Literal["new", "while_supplies_last", "treasure_hunt", "member_favorites", '
                '"online_only", "on_sale"]',
                required=True,
                doc="Deal feed: new, while_supplies_last, treasure_hunt, member_favorites, "
                "online_only or on_sale.",
            ),
            _COSTCO_NA_COUNTRY,
            *_COSTCO_LISTING_FILTERS,
        ),
        credits=1,
    ),
    Endpoint(
        key="costco_clearance",
        namespace="costco",
        method="clearance",
        http="POST",
        path="/api/v1/costco/clearance",
        summary=(
            "Markdown finder for one warehouse: scans a query or category and keeps the items "
            "whose in-warehouse price ends in a markdown code -- .97 clearance and .00/.88 "
            "manager markdown by default, .49/.79/.89 special buys on request. The codes are the "
            "member-community decode; Costco does not publish them. Only items Costco lists "
            "online are covered."
        ),
        params=(
            _req(
                "warehouse_id",
                "Costco warehouse number to scan, from warehouses() (e.g. '1062').",
            ),
            _str("query", "Keywords to scan (1-200 characters)."),
            _str("category", "Category slug to scan instead of a query."),
            _int("pages", "Result pages of 120 to scan (1-5; server default 3)."),
            _lit_list(
                "price_codes",
                ("clearance", "manager_markdown", "special_buy"),
                "Markdown codes to keep. Server default clearance + manager_markdown; add "
                "special_buy for .49/.79/.89 endings, which are common on regular grocery "
                "prices.",
            ),
            _COSTCO_NA_COUNTRY,
        ),
        one_of=(("query", "category"),),
        credits=1,
    ),
    Endpoint(
        key="costco_autocomplete",
        namespace="costco",
        method="autocomplete",
        http="POST",
        path="/api/v1/costco/autocomplete",
        summary="Costco search-box suggestions for a partial query.",
        params=(
            _req("query", "Partial search text (1-100 characters)."),
            _COSTCO_NA_COUNTRY,
        ),
        credits=1,
    ),
    # ============================= Trustpilot ============================
    # 6 endpoints, 2 credits each. business() and reviews() take exactly one
    # of domain or url (the server rejects both); one_of only enforces "at
    # least one" client-side, the backend enforces "not both".
    Endpoint(
        key="trustpilot_search",
        namespace="trustpilot",
        method="search",
        http="POST",
        path="/api/v1/trustpilot/search",
        summary=(
            "Search Trustpilot businesses by keyword in one country: TrustScore, star rating, "
            "review count, categories, website, and the email, phone and address the business "
            "published. Up to 100 businesses per page."
        ),
        params=(
            _req("query", "Business name, keyword or category (1-200 characters)."),
            _str("country", "2-letter country code to search in (server default 'US')."),
            _int("page", "Results page, 1-based (1-1000)."),
            _int("page_size", "Businesses per page (1-100; server default 20)."),
        ),
        credits=2,
    ),
    Endpoint(
        key="trustpilot_business",
        namespace="trustpilot",
        method="business",
        http="POST",
        path="/api/v1/trustpilot/business",
        summary=(
            "A Trustpilot business profile: TrustScore, rating distribution, review languages, "
            "categories, contact details, claimed and verification status, reply rate and reply "
            "speed on negative reviews, consumer alerts, the AI review summary and topics, "
            "similar businesses, and the 20 newest reviews in the chosen language. Pass exactly "
            "one of domain or url."
        ),
        params=(
            _str(
                "domain",
                "The business's website domain as listed on Trustpilot (e.g. 'www.amazon.com').",
            ),
            _str(
                "url",
                "A trustpilot.com/review/<domain> page URL, from any Trustpilot country site. "
                "Alternative to domain.",
            ),
            _str(
                "language",
                "2-letter language code (server default 'en'). The 20 included reviews are this "
                "language's newest, and the AI summary and topics come back in it when Trustpilot "
                "has them for that language (null / empty otherwise). The rating distribution and "
                "review-language breakdown cover every language.",
            ),
        ),
        one_of=(("domain", "url"),),
        credits=2,
    ),
    Endpoint(
        key="trustpilot_reviews",
        namespace="trustpilot",
        method="reviews",
        http="POST",
        path="/api/v1/trustpilot/reviews",
        summary=(
            "One page of 20 Trustpilot reviews for a business, filtered by stars, language, date "
            "range, topics, text search, verified-only and with-replies, sorted by recency or "
            "relevance. Returns total_filtered, so a date range doubles as review velocity. Up "
            "to 10 pages (200 reviews) per filter combination; slice by stars, language, topics "
            "or search to reach more. Pass exactly one of domain or url."
        ),
        params=(
            _str(
                "domain",
                "The business's website domain as listed on Trustpilot (e.g. 'www.amazon.com').",
            ),
            _str(
                "url",
                "A trustpilot.com/review/<domain> page URL, from any Trustpilot country site. "
                "Alternative to domain.",
            ),
            _int("page", "Reviews page, 1-10 (20 per page)."),
            _ilit_list("stars", (1, 2, 3, 4, 5), "Only reviews with these star ratings (e.g. [1, 2])."),
            _str("language", "Review language (2-letter code) or 'all' (server default 'all')."),
            _lit(
                "date_range",
                ("last30days", "last3months", "last6months", "last12months"),
                "Only reviews published in this window.",
            ),
            _lit("sort", ("recency", "relevance"), "Review order (server default 'recency')."),
            _bool("verified_only", "Only verified reviews."),
            _bool("with_replies", "Only reviews the business replied to."),
            _str_list(
                "topics",
                "Topic ids from business()'s topics, up to 10 (e.g. ['delivery_service']).",
            ),
            _str("search", "Only reviews containing this text (1-100 characters)."),
        ),
        one_of=(("domain", "url"),),
        credits=2,
    ),
    Endpoint(
        key="trustpilot_categories",
        namespace="trustpilot",
        method="categories",
        http="POST",
        path="/api/v1/trustpilot/categories",
        summary=(
            "The full Trustpilot category tree (top-level categories and their subcategories), "
            "or categories matching a name. Every category_id works with category()."
        ),
        params=(
            _str("query", "Find categories by name (1-100 characters). Omit for the full tree."),
            _str("country", "2-letter country code for the name lookup (server default 'US')."),
        ),
        credits=2,
    ),
    Endpoint(
        key="trustpilot_category",
        namespace="trustpilot",
        method="category",
        http="POST",
        path="/api/v1/trustpilot/category",
        summary=(
            "Businesses ranked in a Trustpilot category for one country, with TrustScore, review "
            "count, location, website, email and phone. Sort by relevance, review count or latest "
            "review, set a minimum star rating, or keep claimed profiles only. 20 per page."
        ),
        params=(
            _req("category_id", "Category id from categories() (e.g. 'vpn_service')."),
            _str("country", "2-letter country code (server default 'US')."),
            _lit(
                "sort",
                ("most_relevant", "reviews_count", "latest_review"),
                "Result order (server default 'most_relevant').",
            ),
            # z.union([z.literal(3), z.literal(4), z.literal(4.5)]): a float
            # literal is not valid typing, so the annotation is the honest float.
            _float(
                "min_trust_score",
                "Minimum star rating: 3, 4 or 4.5. Trustpilot rounds TrustScore to stars, so 4 "
                "includes TrustScore 3.8 and up.",
            ),
            _bool("claimed_only", "Only businesses that have claimed their Trustpilot profile."),
            _int("page", "Results page, 1-based (20 businesses per page)."),
        ),
        credits=2,
    ),
    Endpoint(
        key="trustpilot_review",
        namespace="trustpilot",
        method="review",
        http="POST",
        path="/api/v1/trustpilot/review",
        summary=(
            "One Trustpilot review by id: rating, title, full text, dates, verification, the "
            "reviewer's public profile summary, the business reply, and the business it is about."
        ),
        params=(
            _req(
                "review_id",
                "24-character review id, as returned in review_id by business() or reviews().",
            ),
        ),
        credits=2,
    ),
    # ============================ Realtor.com ============================
    # 6 endpoints, 1 credit each. search() takes location, a point
    # (latitude + longitude + radius_miles) or agent_id; one_of only enforces
    # "at least one" client-side and the backend enforces the rest. property()
    # takes exactly one of property_id or url.
    Endpoint(
        key="realtor_search",
        namespace="realtor",
        method="search",
        http="POST",
        path="/api/v1/realtor/search",
        summary=(
            "Search Realtor.com for-sale, pending, for-rent and sold listings by location, radius "
            "or agent, filtered by price, beds, baths, square feet, lot size, year built, garage, "
            "HOA, property type, listing/sold/price-cut recency, listing-text keywords, new "
            "construction, foreclosure and open houses. Up to 200 listings per call with price, "
            "sold price and date, lot size, address with coordinates, MLS id and listing agent. "
            "Realtor.com serves the first 10,000 results of a search. Sold prices are null in US "
            "sold-price non-disclosure states (Texas, Utah, Wyoming and others); sold dates are "
            "still returned."
        ),
        params=(
            _str(
                "location",
                "City ('Austin, TX'), county ('Travis County, TX'), ZIP code, state or "
                "neighborhood. Alternative to latitude/longitude/radius_miles and agent_id.",
            ),
            _float("latitude", "Center latitude for a radius search (with longitude and radius_miles)."),
            _float("longitude", "Center longitude for a radius search."),
            _float("radius_miles", "Radius around latitude/longitude, 0.1 to 50 miles."),
            _str("agent_id", "Only this agent's listings (numeric agent_id from search rows or agents())."),
            _lit(
                "listing_status",
                ("for_sale", "pending", "for_rent", "sold"),
                "for_sale (server default; includes pending and contingent listings, as on the "
                "site), pending (only pending or contingent), for_rent, or sold.",
            ),
            _bool("exclude_pending", "for_sale only: leave out pending and contingent listings."),
            _float(
                "min_price",
                "Minimum price in USD: list price, sold price on sold, monthly rent on for_rent.",
            ),
            _float("max_price", "Maximum price in USD (same meaning as min_price)."),
            _int("beds_min", "Minimum bedrooms."),
            _int("beds_max", "Maximum bedrooms."),
            _float("baths_min", "Minimum bathrooms."),
            _float("baths_max", "Maximum bathrooms."),
            _int("sqft_min", "Minimum interior square feet."),
            _int("sqft_max", "Maximum interior square feet."),
            _int("lot_sqft_min", "Minimum lot size in square feet (1 acre = 43,560)."),
            _int("lot_sqft_max", "Maximum lot size in square feet."),
            _int("year_built_min", "Built in or after this year (1700-2100)."),
            _int("year_built_max", "Built in or before this year (1700-2100)."),
            _int("garage_min", "Minimum garage spaces."),
            _float(
                "max_hoa",
                "Maximum monthly HOA fee in USD (listings without an HOA fee are kept).",
            ),
            _lit_list(
                "property_types",
                ("single_family", "condos", "townhomes", "multi_family", "land", "mobile", "farm"),
                "Only these property types (e.g. ['land']).",
            ),
            _int("listed_within_days", "Only listings listed in the last N days (1-3650)."),
            _int("sold_within_days", "sold only: only sales in the last N days (1-3650)."),
            _int("price_reduced_within_days", "Only listings with a price cut in the last N days (1-3650)."),
            _str_list(
                "keywords",
                "Only listings whose listing text contains ALL of these keywords, up to 10 "
                "(e.g. ['workshop']); each extra keyword narrows the results.",
            ),
            _bool("new_construction", "Only new construction."),
            _bool("foreclosure", "Only foreclosures."),
            _bool("has_open_house", "Only listings with an open house in the next 7 days."),
            _lit(
                "sort",
                (
                    "relevance",
                    "newest",
                    "price_low",
                    "price_high",
                    "sold_newest",
                    "sqft_high",
                    "lot_size_high",
                    "year_built_new",
                    "recently_updated",
                    "recently_reduced",
                ),
                "Result order (server default 'relevance'). price_high uses sold price on sold; "
                "sold_newest is sold only.",
            ),
            _int("page", "Results page, 1-based."),
            _int(
                "page_size",
                "Listings per page (1-200; server default 50). page x page_size may not exceed "
                "10,000.",
            ),
        ),
        one_of=(("location", "latitude", "agent_id"),),
        credits=1,
    ),
    Endpoint(
        key="realtor_property",
        namespace="realtor",
        method="property",
        http="POST",
        path="/api/v1/realtor/property",
        summary=(
            "One Realtor.com property: description and detail groups, price history, tax history "
            "with assessed and market values, three home value estimates with ranges plus their "
            "history and forecast, nearby schools with ratings, flood/wildfire/noise risk, listing "
            "popularity, the listing agent and office, mortgage estimate and photos. Valuations, "
            "schools and risk can be null for land or new construction. Pass exactly one of "
            "property_id or url."
        ),
        params=(
            _str("property_id", "Numeric property id from search() or locations()."),
            _str("url", "A realtor.com property or rental URL. Alternative to property_id."),
        ),
        one_of=(("property_id", "url"),),
        credits=1,
    ),
    Endpoint(
        key="realtor_locations",
        namespace="realtor",
        method="locations",
        http="POST",
        path="/api/v1/realtor/locations",
        summary=(
            "Location suggestions for a partial name: cities, counties, ZIP codes, neighborhoods, "
            "schools and addresses, each with its slug_id (for market()) and, for an address, the "
            "property_id (for property())."
        ),
        params=(
            _req("query", "City, county, ZIP, neighborhood, school or street address (1-200 characters)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="realtor_market",
        namespace="realtor",
        method="market",
        http="POST",
        path="/api/v1/realtor/market",
        summary=(
            "Housing market statistics for a city, county or ZIP: median listing, sold and rent "
            "price, price per square foot, days on market, lot size, listing and rental counts, "
            "year-over-year and month-over-month changes, and a breakdown by property type. Some "
            "medians are null at some geography levels."
        ),
        params=(
            _req(
                "location",
                "A slug_id from locations() (e.g. 'Austin_TX', 'Travis-County_TX') or 'City, ST'.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="realtor_agents",
        namespace="realtor",
        method="agents",
        http="POST",
        path="/api/v1/realtor/agents",
        summary=(
            "Find real estate agents by city, ZIP code or name: rating, review and recommendation "
            "counts, active listing count and price range, homes sold in the last year, broker and "
            "office, first year in business and services. Pass exactly one of location, "
            "postal_code or name."
        ),
        params=(
            _str("location", "City as 'City, ST' (e.g. 'Austin, TX')."),
            _str("postal_code", "5-digit ZIP code."),
            _str("name", "Agent name (2-100 characters)."),
            _int("page", "Results page, 1-based (1-1000)."),
            _int("page_size", "Agents per page (1-50; server default 20)."),
        ),
        one_of=(("location", "postal_code", "name"),),
        credits=1,
    ),
    Endpoint(
        key="realtor_agent",
        namespace="realtor",
        method="agent",
        http="POST",
        path="/api/v1/realtor/agent",
        summary=(
            "One agent's profile with all reviews: bio, phones, website, license number and state, "
            "MLS memberships, languages, specializations, served areas, designations, office "
            "address, social links, listing and sales stats, and every review with "
            "responsiveness, market expertise, negotiation and professionalism sub-ratings and the "
            "agent's reply."
        ),
        params=(
            _req("agent_id", "Numeric agent id from search rows (agent.agent_id) or agents()."),
        ),
        credits=1,
    ),
    # ============================== Rightmove ============================
    # 7 endpoints, 1 credit each, UK. search() and agents() take exactly one
    # place selector; property(), sold_property() and agent() take exactly one
    # of an id or a URL. Rightmove search has NO keyword filter: the backend
    # rejects a keywords field with a free 400, so none is declared here.
    Endpoint(
        key="rightmove_locations",
        namespace="rightmove",
        method="locations",
        http="POST",
        path="/api/v1/rightmove/locations",
        summary=(
            "Look up UK places by name, outcode, postcode or station and get the location_id that "
            "search() and agents() take."
        ),
        params=(
            _req("query", "Town, area, outcode (SW11), postcode or station (1-100 characters)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="rightmove_search",
        namespace="rightmove",
        method="search",
        http="POST",
        path="/api/v1/rightmove/search",
        summary=(
            "Search Rightmove properties for sale or to rent by location_id, place name or agent "
            "branch, filtered by price (GBP; monthly on for_rent), beds, baths, property type, "
            "must-have and exclude features, tenure, days since added, under offer, radius, and "
            "furnishing and let type for rentals. 24 listings per page, up to 42 pages (about "
            "1,000 listings) per search. Pass exactly one of location_id, location or branch_id. "
            "There is no keyword filter; match on summary and key_features in the results."
        ),
        params=(
            _str(
                "location_id",
                "A location_id from locations() (REGION^, OUTCODE^, POSTCODE^ or STATION^, "
                "e.g. 'REGION^219').",
            ),
            _str(
                "location",
                "A place name, resolved to its first location match (echoed in the response). "
                "Alternative to location_id.",
            ),
            _str("branch_id", "Only this agent branch's listings (numeric branch_id from agents())."),
            _lit("listing_status", ("for_sale", "for_rent"), "for_sale (server default) or for_rent."),
            _float("min_price", "Minimum price in GBP (monthly rent on for_rent)."),
            _float("max_price", "Maximum price in GBP (monthly rent on for_rent)."),
            _int("beds_min", "Minimum bedrooms (0-10)."),
            _int("beds_max", "Maximum bedrooms (0-10)."),
            _int("baths_min", "Minimum bathrooms (1-5)."),
            _lit_list(
                "property_types",
                ("detached", "semi_detached", "terraced", "flat", "bungalow", "land", "park_home"),
                "Only these property types (e.g. ['detached', 'semi_detached']).",
            ),
            _lit_list("must_have", ("garden", "parking", "new_home"), "Only listings with all of these."),
            _lit_list(
                "exclude",
                ("auction", "retirement", "shared_ownership", "new_home"),
                "Leave these listing kinds out.",
            ),
            _lit("tenure", ("freehold", "leasehold"), "for_sale only: freehold or leasehold."),
            _ilit("added_within_days", (1, 3, 7, 14), "Only listings added in the last 1, 3, 7 or 14 days."),
            _bool(
                "include_under_offer",
                "Include listings under offer / sold STC (for_sale) or let agreed (for_rent).",
            ),
            # One of 0, 0.25, 0.5, 1, 3, 5, 10, 15, 20, 30, 40: a float literal
            # is not valid typing, so the annotation is the honest float.
            _float(
                "radius_miles",
                "Widen the area by this many miles: 0 (default), 0.25, 0.5, 1, 3, 5, 10, 15, 20, "
                "30 or 40.",
            ),
            _lit_list(
                "furnishing",
                ("furnished", "part_furnished", "unfurnished"),
                "for_rent only.",
            ),
            _lit("let_type", ("long_term", "short_term"), "for_rent only: long_term or short_term."),
            _lit(
                "sort",
                ("newest", "oldest", "price_low", "price_high"),
                "Result order (server default 'newest').",
            ),
            _int("page", "Results page, 1-42 (24-25 per page)."),
        ),
        one_of=(("location_id", "location", "branch_id"),),
        credits=1,
    ),
    Endpoint(
        key="rightmove_property",
        namespace="rightmove",
        method="property",
        http="POST",
        path="/api/v1/rightmove/property",
        summary=(
            "One Rightmove listing in full: price and qualifier, description, key features, "
            "rooms, images, floorplans, brochures, EPC, tenure and lease years remaining, council "
            "tax band, service charge and ground rent, heating, parking, garden, accessibility and "
            "flood-risk details, broadband, nearest stations, letting terms and the agent branch "
            "with phone. Live listings carry no price history; use sold_property() for an "
            "address's past sales. A removed listing is a 404. Pass exactly one of property_id or "
            "url."
        ),
        params=(
            _str("property_id", "Numeric listing id from search()."),
            _str("url", "A rightmove.co.uk/properties/<id> URL. Alternative to property_id."),
        ),
        one_of=(("property_id", "url"),),
        credits=1,
    ),
    Endpoint(
        key="rightmove_sold",
        namespace="rightmove",
        method="sold",
        http="POST",
        path="/api/v1/rightmove/sold",
        summary=(
            "Sold house prices for a town, outcode or postcode in England or Wales: every address "
            "with its sale history since 1995 (price, date, tenure, new build) plus an area "
            "summary. 25 addresses per page, up to 40 pages per search."
        ),
        params=(
            _req(
                "location",
                "A town, outcode (SW11) or full postcode (SW11 1AA) in England or Wales.",
            ),
            _lit(
                "property_type",
                ("flat", "detached", "semi_detached", "terraced", "other"),
                "Only this property type.",
            ),
            _lit("tenure", ("freehold", "leasehold"), "freehold or leasehold."),
            _ilit(
                "sold_within_years",
                (1, 2, 3, 5, 10, 15, 20, 30),
                "Only addresses sold in the last 1, 2, 3, 5, 10, 15, 20 or 30 years.",
            ),
            _float(
                "radius_miles",
                "Widen the area by this many miles: 0 (default), 0.25, 0.5, 1, 3, 5, 10, 15, 20, "
                "30 or 40.",
            ),
            _lit(
                "sort",
                ("newest", "price_low", "price_high"),
                "Newest sale first (server default), price_low or price_high.",
            ),
            _int("page", "Results page, 1-40 (25 addresses per page)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="rightmove_sold_property",
        namespace="rightmove",
        method="sold_property",
        http="POST",
        path="/api/v1/rightmove/sold-property",
        summary=(
            "One sold address on Rightmove: every recorded sale with price, date, tenure, new "
            "build flag and percent change, plus the last listing's beds, baths, key features, "
            "photos and floorplans when it was advertised. Pass exactly one of sold_id or url."
        ),
        params=(
            _str("sold_id", "sold_id from sold() (36-character id)."),
            _str(
                "url",
                "A rightmove.co.uk/house-prices/details/<id> URL. Alternative to sold_id.",
            ),
        ),
        one_of=(("sold_id", "url"),),
        credits=1,
    ),
    Endpoint(
        key="rightmove_agents",
        namespace="rightmove",
        method="agents",
        http="POST",
        path="/api/v1/rightmove/agents",
        summary=(
            "Estate agent branches in a Rightmove area: name, brand, phones, address, sales and "
            "lettings flags, description and profile URL. 20 branches per page, up to 50 pages. "
            "Pass exactly one of location_id or location."
        ),
        params=(
            _str(
                "location_id",
                "A location_id from locations() (REGION^, OUTCODE^, POSTCODE^ or STATION^).",
            ),
            _str(
                "location",
                "A place name, resolved to its first location match. Alternative to location_id.",
            ),
            _int("page", "Results page, 1-50 (20 branches per page)."),
        ),
        one_of=(("location_id", "location"),),
        credits=1,
    ),
    Endpoint(
        key="rightmove_agent",
        namespace="rightmove",
        method="agent",
        http="POST",
        path="/api/v1/rightmove/agent",
        summary=(
            "One Rightmove agent branch: address, phones, coordinates, company, "
            "sales/lettings/commercial/development flags, descriptions, logo, industry "
            "affiliations, and the count plus a teaser of its listings for sale and to rent. Use "
            "search(branch_id=...) for the full listings. Pass exactly one of url or branch_id."
        ),
        params=(
            _str("url", "A branch profile URL (profile_url from agents())."),
            _str("branch_id", "Numeric branch_id from agents() or a listing's agent. Alternative to url."),
        ),
        one_of=(("url", "branch_id"),),
        credits=1,
    ),
    # ============================ Mercado Libre ==========================
    # 5 endpoints: reviews 1 credit, every other endpoint 2. Countries mx, br
    # (Mercado Livre), ar, co; Chile is not supported. search() takes query,
    # seller_id or seller_nickname (query stays positional, as the Playground
    # snippet passes it); country is required but keyword-only, enforced by a
    # one-member one_of group. product()/reviews() take exactly one of url,
    # product_id or item_id; questions() one of item_id or url (the backend
    # enforces "exactly one"). best_sellers() is mx, ar or co only.
    Endpoint(
        key="mercadolibre_search",
        namespace="mercadolibre",
        method="search",
        http="POST",
        path="/api/v1/mercadolibre/search",
        summary=(
            "Search Mercado Libre listings in Mexico, Brazil (Mercado Livre), Argentina or "
            "Colombia by keyword or seller, with condition, price range, discount, free shipping, "
            "Full fulfillment, official stores and interest-free installment filters, sorted by "
            "relevance or price. Each row has price, list price, discount, installments, seller "
            "and official-store flag where shown, rating, units sold as a lower bound (\"at least "
            "500\"), shipping flags, a sponsored flag and catalog ids. About 48 rows per page and "
            "42 pages (about 2,000 results) per query. Pass country and one of query, seller_id "
            "or seller_nickname."
        ),
        params=(
            Param(
                "query",
                "Optional[str]",
                positional=True,
                doc=(
                    "Keywords (1-200 characters). Mercado Libre may narrow a query to a category, "
                    "brand or line on its own; the response lists those in auto_applied_filters."
                ),
            ),
            _lit(
                "country",
                ("mx", "br", "ar", "co"),
                "Required. Mexico (mx), Brazil (br, Mercado Livre), Argentina (ar) or Colombia "
                "(co). Prices come back in MXN, BRL, ARS or COP. Chile is not supported.",
            ),
            _str(
                "seller_id",
                "Only this seller's listings (numeric id, as returned in product's "
                "seller.seller_id). Combines with query, filters, sort and page.",
            ),
            _str(
                "seller_nickname",
                "A seller's public nickname. Returns the seller's first page of listings without "
                "filters, plus their seller_id; use seller_id for filters, sort and further pages.",
            ),
            _lit(
                "condition",
                ("new", "used", "refurbished", "open_box"),
                "Item condition. Without it, Mercado Libre may show new items only for some "
                "queries (listed in auto_applied_filters).",
            ),
            _int("min_price", "Minimum price in the country's currency (MXN, BRL, ARS or COP)."),
            _int("max_price", "Maximum price in the country's currency."),
            _ilit(
                "min_discount",
                (5, 10, 15, 20, 25, 30, 40),
                "Only listings at least this many percent off: 5, 10, 15, 20, 25, 30 or 40.",
            ),
            _bool("free_shipping", "Only listings with free shipping."),
            _bool("full_fulfillment", "Only listings shipped by Mercado Libre Full fulfillment."),
            _bool("official_stores_only", "Only listings from official brand stores."),
            _bool("interest_free_installments", "Only listings payable in interest-free installments."),
            _lit(
                "sort",
                ("relevance", "price_asc", "price_desc"),
                "relevance (server default), price_asc or price_desc. Mercado Libre offers no "
                "newest or best-selling sort.",
            ),
            _int(
                "page",
                "Results page, 1-42 (about 48 per page, so about 2,000 results per query). Narrow "
                "by price range, condition or seller to reach more.",
            ),
        ),
        one_of=(("query", "seller_id", "seller_nickname"), ("country",)),
        credits=2,
    ),
    Endpoint(
        key="mercadolibre_product",
        namespace="mercadolibre",
        method="product",
        http="POST",
        path="/api/v1/mercadolibre/product",
        summary=(
            "One Mercado Libre catalog product or listing: title, price, list price, "
            "installments, promotions, the buy-box seller with reputation level and seller tier, "
            "stock, shipping, rating with its star distribution, variations with sibling product "
            "ids, specs, description, pictures and categories. Only the buy-box seller is "
            "returned; units sold is a lower bound. Some fields are null where the page omits "
            "them. Pass exactly one of url, product_id or item_id; the id prefix (MLM, MLB, MLA, "
            "MCO) sets the country."
        ),
        params=(
            _str(
                "product_id",
                "Catalog product id, as returned in product_id by search() (e.g. 'MLM1027172667').",
            ),
            _str(
                "item_id",
                "Item (listing) id, as returned in item_id by search() (e.g. 'MLM2746152281'; "
                "'MLM-2746152281' is accepted too).",
            ),
            _str(
                "url",
                "A Mercado Libre or Mercado Livre product (/p/), user product (/up/) or listing "
                "page URL.",
            ),
        ),
        one_of=(("url", "product_id", "item_id"),),
        credits=2,
    ),
    Endpoint(
        key="mercadolibre_reviews",
        namespace="mercadolibre",
        method="reviews",
        http="POST",
        path="/api/v1/mercadolibre/reviews",
        summary=(
            "One page of up to 15 Mercado Libre product reviews (page until a page comes back "
            "empty), optionally filtered by star rating: rating, text, the original text when "
            "Mercado Libre translated it, exact date, likes, the review's country and photos. "
            "Catalog products pool reviews from several countries. Totals and the star "
            "distribution come from product(). Pass exactly one of url, product_id or item_id."
        ),
        params=(
            _str("product_id", "Catalog product id, as returned in product_id by search()."),
            _str("item_id", "Item (listing) id, as returned in item_id by search()."),
            _str(
                "url",
                "A Mercado Libre or Mercado Livre product (/p/), user product (/up/) or listing "
                "page URL.",
            ),
            _ilit("rating", (1, 2, 3, 4, 5), "Only reviews with this star rating (1-5)."),
            _int(
                "page",
                "Reviews page, 1-based (up to 15 per page; a page past the last one comes back "
                "empty).",
            ),
        ),
        one_of=(("url", "product_id", "item_id"),),
        credits=1,
    ),
    Endpoint(
        key="mercadolibre_questions",
        namespace="mercadolibre",
        method="questions",
        http="POST",
        path="/api/v1/mercadolibre/questions",
        summary=(
            "A page of buyer questions on a Mercado Libre listing with the seller's answers and "
            "answer dates (Mercado Libre shows no question dates). Page through with next_offset. "
            "A listing with no public questions returns 404. Pass exactly one of item_id or url."
        ),
        params=(
            Param(
                "item_id",
                "Optional[str]",
                positional=True,
                doc=(
                    "Item (listing) id, as returned in item_id by search() (e.g. "
                    "'MLM3571336480')."
                ),
            ),
            _str(
                "url",
                "A listing page URL, or a product (/p/, /up/) URL: a product's questions are those "
                "of the listing in its buy box. Alternative to item_id.",
            ),
            _int("offset", "Where to start, from next_offset of the previous page. Defaults to 0."),
        ),
        one_of=(("item_id", "url"),),
        credits=2,
    ),
    Endpoint(
        key="mercadolibre_best_sellers",
        namespace="mercadolibre",
        method="best_sellers",
        http="POST",
        path="/api/v1/mercadolibre/best-sellers",
        summary=(
            "The ranked top 20 best sellers in a Mercado Libre category in Mexico, Argentina or "
            "Colombia, with price, discount, installments, rating, units sold as a lower bound "
            "and seller where shown. Not available for Brazil."
        ),
        params=(
            _req(
                "category_id",
                "Category id, as returned in category_id or category_path by search(), or "
                "category_id by product() (e.g. 'MLM1055'). Its prefix must match the country.",
            ),
            _lit(
                "country",
                ("mx", "ar", "co"),
                "Required. mx, ar or co. Not available for Brazil.",
            ),
        ),
        one_of=(("country",),),
        credits=2,
    ),
    # =========================== Extract (core) ==========================
    # NOT a platform and NOT a namespace: surfaced as the top-level method
    # scavio.extract(url, format=, mode=). namespace="_core" keeps it out of
    # NAMESPACES so the generator never emits a class for it -- the method is
    # hand-written on the client. Cost is TIER-PRICED by `mode`
    # (normal 1, advanced 1, ultra 2), so credits=1 is only the floor and
    # credits_note carries the tiers.
    Endpoint(
        key="extract",
        namespace="_core",
        method="extract",
        http="POST",
        path="/api/v1/extract",
        summary=(
            "Read any URL and get the page back as raw HTML, readability Markdown or plain text: "
            "{ url, format, mode, content, content_length }. Tier-priced by mode -- normal and "
            "advanced cost 1 credit, ultra costs 2 -- and only a successful extraction is billed, "
            "so a dead link, bot wall or timeout costs nothing."
        ),
        params=(
            _req(
                "url",
                "Page to read (1-2048 characters). http(s) only; a bare host is upgraded to "
                "https, and loopback, private, link-local and metadata hosts are rejected with a "
                "400.",
            ),
            _lit(
                "format",
                ("html", "markdown", "text"),
                "Output format: 'html' is the raw page, 'markdown' a readability extraction, "
                "'text' that markdown flattened to plain text (server default 'markdown').",
            ),
            _lit(
                "mode",
                ("normal", "advanced", "ultra"),
                "Tier, and the price-bearing parameter: 'normal' (1 credit), 'advanced' for "
                "JavaScript-built pages (1 credit), 'ultra' for the hardest pages (2 credits). "
                "Server default 'normal'.",
            ),
        ),
        credits=1,
        credits_note=(
            "Tier-priced by mode: 'normal' and 'advanced' cost 1 credit, 'ultra' costs 2. Only a "
            "successful extraction is billed - a dead link, bot wall or timeout costs nothing."
        ),
    ),
    # ================= Extract: map / crawl / batch (core) ================
    # The request bodies of the Extract family's multi-page operations,
    # mirroring backend/src/routes/extract-web.ts. Like `extract` these are
    # namespace "_core": they hang off the callable client.extract namespace
    # (client.extract.map / .crawl / .batch), which is hand-written in
    # scavio/_extract.py together with the status and cancel calls, so the
    # generator never emits a class for them. build_body uses these entries for
    # the argument -> wire mapping, and tests pin the hand-written signatures
    # to them.
    Endpoint(
        key="extract_map",
        namespace="_core",
        method="map",
        http="POST",
        path="/api/v1/extract/map",
        summary=(
            "List a site's page URLs, gathered from its sitemaps and its start page, deduplicated, "
            "filtered by path and limited: { url, links: [{ url, source, lastmod? }], total_found, "
            "returned, truncated, sitemaps_read }. Pages disallowed by robots.txt are left out."
        ),
        params=(
            _req("url", "The site to map (1-2048 characters). A bare host is upgraded to https."),
            _str("search", "Only return URLs containing every word of this text (case-insensitive)."),
            _int(
                "limit",
                "Maximum links to return, 1-5,000. Server default 1,000 (or the plan's limit if "
                "lower): Free 500, PAYG 1,000, paid plans 5,000.",
            ),
            _lit(
                "sitemap",
                ("include", "only", "skip"),
                "'include' (default) combines sitemaps with the start page's links; 'only' uses "
                "sitemaps alone; 'skip' uses page links alone.",
            ),
            _bool(
                "include_subdomains",
                "Also return URLs on subdomains (server default False; www and the bare domain "
                "always count as one site).",
            ),
            _str_list(
                "include_paths",
                "Path globs to keep (max 20), e.g. ['/blog/**']. '*' matches within one segment, "
                "'**' across segments.",
            ),
            _str_list("exclude_paths", "Path globs to drop (max 20). Excludes win over includes."),
            _bool(
                "ignore_query_parameters",
                "Treat URLs that differ only by query string as one URL (server default True).",
            ),
            _lit(
                "mode",
                ("normal", "advanced", "ultra"),
                "Tier, as on extract: 'normal' (default), 'advanced' for JavaScript-built pages, "
                "'ultra' for the hardest pages.",
            ),
        ),
        credits=1,
        credits_note=(
            "1 credit on the normal tier; up to 2 on 'advanced' and up to 10 on 'ultra'."
        ),
    ),
    Endpoint(
        key="extract_crawl",
        namespace="_core",
        method="crawl",
        http="POST",
        path="/api/v1/extract/crawl",
        summary=(
            "Start a crawl from one URL: same-site pages are discovered and extracted breadth-first "
            "within the depth, page and path limits, each returned as Markdown, text or HTML "
            "exactly like extract. Pages disallowed by robots.txt are skipped. Returns the queued "
            "job: { data: { id, status, status_url, credits_per_page, webhook_secret? }, "
            "credits_used: 0 }."
        ),
        params=(
            _req(
                "url",
                "Where the crawl starts (1-2048 characters). Only pages on the same site are "
                "crawled; URLs under the start path go first.",
            ),
            _int(
                "max_pages",
                "Maximum pages to fetch, 1-10,000 (server default 100). Plan limits: Free 10, "
                "PAYG 100, Project 500, Bootstrap 2,000, Startup 5,000, Growth 10,000.",
            ),
            _int(
                "max_depth",
                "Links away from the start page to follow, 0-10 (server default 3). 0 fetches "
                "only the start page.",
            ),
            _str_list(
                "include_paths",
                "Path globs to crawl (max 20), e.g. ['/docs/**']. '*' matches within one segment, "
                "'**' across segments.",
            ),
            _str_list("exclude_paths", "Path globs to skip (max 20)."),
            _bool("allow_subdomains", "Also crawl subdomains of the site (server default False)."),
            _bool(
                "ignore_query_parameters",
                "Treat URLs that differ only by query string as one page (server default True).",
            ),
            _lit(
                "sitemap",
                ("include", "skip", "only"),
                "'include' (default) also starts from the sitemap; 'skip' follows links only; "
                "'only' fetches sitemap pages without following links.",
            ),
            _lit(
                "format",
                ("html", "markdown", "text"),
                "Format of each page, as on extract (server default 'markdown').",
            ),
            _lit(
                "mode",
                ("normal", "advanced", "ultra"),
                "Price-bearing tier for every page: 'normal' (default) and 'advanced' (JavaScript-"
                "built pages) cost 1 credit per page, 'ultra' (hardest pages) 2.",
            ),
            _str(
                "webhook_url",
                "Optional https URL that gets a signed POST when the job completes, fails or is "
                "cancelled. Verify it with scavio.verify_webhook().",
            ),
        ),
        credits=1,
        credits_note=(
            "Billed per SUCCESSFUL page at extract's price for the tier: 'normal' and 'advanced' "
            "1 credit, 'ultra' 2. Failed and skipped pages are free; starting the job costs "
            "nothing, and it stops cleanly if the balance runs out."
        ),
    ),
    Endpoint(
        key="extract_batch",
        namespace="_core",
        method="batch",
        http="POST",
        path="/api/v1/extract/batch",
        summary=(
            "Extract a list of URLs in one job, each returned as Markdown, text or HTML exactly "
            "like extract. Invalid URLs are reported in invalid_urls and never billed. Returns the "
            "queued job: { data: { id, status, status_url, urls_count, invalid_urls, "
            "credits_per_page, webhook_secret? }, credits_used: 0 }."
        ),
        params=(
            _str_list(
                "urls",
                "The pages to extract, 1-1,000 (duplicates removed). Plan limits: Free 10, PAYG "
                "50, Project 100, Bootstrap 500, Startup and Growth 1,000.",
                required=True,
            ),
            _lit(
                "format",
                ("html", "markdown", "text"),
                "Format of each page, as on extract (server default 'markdown').",
            ),
            _lit(
                "mode",
                ("normal", "advanced", "ultra"),
                "Price-bearing tier for every page: 'normal' (default) and 'advanced' cost 1 "
                "credit per page, 'ultra' 2.",
            ),
            _str(
                "webhook_url",
                "Optional https URL that gets a signed POST when the job completes, fails or is "
                "cancelled. Verify it with scavio.verify_webhook().",
            ),
        ),
        credits=1,
        credits_note=(
            "Billed per SUCCESSFUL page at extract's price for the tier: 'normal' and 'advanced' "
            "1 credit, 'ultra' 2. Failed pages and invalid URLs are free; starting the job costs "
            "nothing."
        ),
    ),
    # ========================== ChatGPT + Gemini ==========================
    # 1 endpoint each: ChatGPT 2 credits, Gemini 5 per answered prompt (failed prompts are free).
    # Answers take 10-40s, so both raise the request timeout to 120s.
    Endpoint(
        key="chatgpt_prompt",
        namespace="chatgpt",
        method="prompt",
        http="POST",
        path="/api/v1/chatgpt/prompt",
        summary=(
            "Send a prompt to ChatGPT and get the answer it gives: the full Markdown answer, every "
            "page it cites (title, publisher, date), the web searches it ran and the products it "
            "recommended. Built for AI visibility monitoring. Failed prompts are not charged."
        ),
        params=(
            _req("prompt", "The prompt (1-1024 characters)."),
            _str("model", "Model to answer with (server default 'auto')."),
            _str("country", "2-letter country code the answer is localized for (server default 'us')."),
            _bool("include_html", "Also return the answer as HTML in data.answer.html."),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="gemini_prompt",
        namespace="gemini",
        method="prompt",
        http="POST",
        path="/api/v1/gemini/prompt",
        summary=(
            "Send a prompt to Google Gemini and get the answer it gives as Markdown, with the URLs "
            "it cites and the products it recommended. Same response shape as chatgpt.prompt(). "
            "Failed prompts are not charged."
        ),
        params=(_req("prompt", "The prompt (1-4000 characters)."),),
        credits=5,
        min_timeout=120.0,
    ),
)


ENDPOINTS: Mapping[str, Endpoint] = {ep.key: ep for ep in _ENDPOINTS}

# Namespaces in the order they are exposed on the client.
#
# `extract` is deliberately absent: it is a CORE endpoint (namespace "_core"),
# surfaced as the top-level method client.extract(...), never a namespace. The
# generator emits one class per entry here, so listing it would produce a
# client.extract.extract().
NAMESPACES: tuple[str, ...] = (
    "google",
    "amazon",
    "walmart",
    "youtube",
    "reddit",
    "x",
    "tiktok",
    "instagram",
    "linkedin",
    "tiktok_shop",
    "threads",
    "kuaishou",
    "ebay",
    "target",
    "home_depot",
    "zillow",
    "booking",
    "tripadvisor",
    "indeed",
    "airbnb",
    "glassdoor",
    "yelp",
    "app_store",
    "google_play",
    "sec",
    "redfin",
    "companies_house",
    "g2",
    "capterra",
    "google_ads",
    "meta_ads",
    "costco",
    "trustpilot",
    "realtor",
    "rightmove",
    "mercadolibre",
    "chatgpt",
    "gemini",
)


def endpoints_for(namespace: str) -> list[Endpoint]:
    return [ep for ep in _ENDPOINTS if ep.namespace == namespace]
