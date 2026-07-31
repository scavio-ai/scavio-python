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
        doc: One-line description used in the generated docstring.
    """

    name: str
    annotation: str
    wire: Optional[str] = None
    required: bool = False
    doc: str = ""

    @property
    def wire_field(self) -> str:
        return self.wire or self.name


@dataclass(frozen=True)
class Endpoint:
    key: str
    namespace: str
    method: str
    http: str
    path: str
    summary: str
    params: Sequence[Param] = field(default_factory=tuple)
    one_of: Sequence[Sequence[str]] = field(default_factory=tuple)
    credits: int = 1

    @property
    def required_params(self) -> list[Param]:
        return [p for p in self.params if p.required]

    @property
    def optional_params(self) -> list[Param]:
        return [p for p in self.params if not p.required]


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
            _LOCATION,
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
            _bool("location", "Videos with location metadata only."),
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
            _str("sort_by", "Sort order."),
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
        summary="Transcript / captions for a YouTube video. Costs 8 credits.",
        params=(
            _req("video_id", "YouTube video id."),
            _str("language", "Caption language code (default 'en')."),
            _lit("format", ("text", "srt"), "'text' plain transcript or 'srt' timed subtitles."),
        ),
        credits=8,
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
    # =============================== Amazon ==============================
    # Amazon moved to a new upstream in 2026-07 and the API now returns a
    # normalized shape instead of the old raw passthrough. Nine params went with
    # the old provider: language, currency, device, sort_by, pages, category_id,
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
    # ============================== Walmart ==============================
    Endpoint(
        key="walmart_search",
        namespace="walmart",
        method="search",
        http="POST",
        path="/api/v1/walmart/search",
        summary="Search Walmart product listings.",
        params=(
            _req("query", "Product search query (1-500 characters)."),
            _str("domain", "Walmart domain."),
            _lit("device", ("desktop", "mobile", "tablet"), "Device to emulate."),
            _lit(
                "sort_by",
                ("best_match", "price_low", "price_high", "best_seller"),
                "Result sort order.",
            ),
            _int("start_page", "Starting page (1-indexed)."),
            _int("min_price", "Minimum price filter (USD)."),
            _int("max_price", "Maximum price filter (USD)."),
            _lit(
                "fulfillment_speed",
                ("today", "tomorrow", "2_days", "anytime"),
                "Delivery speed filter.",
            ),
            _lit("fulfillment_type", ("in_store",), "Fulfillment type filter."),
            _str("delivery_zip", "ZIP code for localized results."),
            _str("store_id", "Store id for in-store availability."),
        ),
    ),
    Endpoint(
        key="walmart_product",
        namespace="walmart",
        method="product",
        http="POST",
        path="/api/v1/walmart/product",
        summary="Full details for a single Walmart product.",
        params=(
            _req("product_id", "Walmart product id."),
            _str("domain", "Walmart domain."),
            _lit("device", ("desktop", "mobile", "tablet"), "Device to emulate."),
            _str("delivery_zip", "ZIP code for localized pricing."),
            _str("store_id", "Store id for in-store availability."),
        ),
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
        summary="Full details for a single Reddit post.",
        params=(_req("url", "Full Reddit post URL."),),
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
    # ============================= Instagram =============================
    Endpoint(
        key="instagram_profile",
        namespace="instagram",
        method="profile",
        http="POST",
        path="/api/v1/instagram/profile",
        summary="Instagram profile. Provide username or user_id. Costs 10 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=10,
    ),
    Endpoint(
        key="instagram_user_posts",
        namespace="instagram",
        method="user_posts",
        http="POST",
        path="/api/v1/instagram/user/posts",
        summary="Posts from an Instagram user. Provide username or user_id. Costs 2 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-50)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
    ),
    Endpoint(
        key="instagram_user_reels",
        namespace="instagram",
        method="user_reels",
        http="POST",
        path="/api/v1/instagram/user/reels",
        summary="Reels from an Instagram user. Provide username or user_id. Costs 10 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-50)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=10,
    ),
    Endpoint(
        key="instagram_user_tagged",
        namespace="instagram",
        method="user_tagged",
        http="POST",
        path="/api/v1/instagram/user/tagged",
        summary="Posts an Instagram user is tagged in. Provide username or user_id. Costs 10 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-50)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=10,
    ),
    Endpoint(
        key="instagram_user_stories",
        namespace="instagram",
        method="user_stories",
        http="POST",
        path="/api/v1/instagram/user/stories",
        summary="Active stories for an Instagram user. Provide username or user_id. Costs 10 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=10,
    ),
    Endpoint(
        key="instagram_post",
        namespace="instagram",
        method="post",
        http="POST",
        path="/api/v1/instagram/post",
        summary="An Instagram post. Provide url, media_id, or shortcode. Costs 8 credits.",
        params=(
            _str("url", "Full Instagram post URL."),
            _str("media_id", "Instagram media id."),
            _str("shortcode", "Instagram shortcode (from the post URL)."),
        ),
        one_of=(("url", "media_id", "shortcode"),),
        credits=8,
    ),
    Endpoint(
        key="instagram_post_comments",
        namespace="instagram",
        method="post_comments",
        http="POST",
        path="/api/v1/instagram/post/comments",
        summary="Comments on an Instagram post. Provide shortcode or url. Costs 10 credits.",
        params=(
            _str("shortcode", "Instagram shortcode (from the post URL)."),
            _str("url", "Full Instagram post URL."),
            _str("cursor", "Pagination cursor from a prior response."),
            _lit("sort_order", ("popular", "newest"), "Comment sort order."),
        ),
        one_of=(("shortcode", "url"),),
        credits=10,
    ),
    Endpoint(
        key="instagram_comment_replies",
        namespace="instagram",
        method="comment_replies",
        http="POST",
        path="/api/v1/instagram/post/comments/replies",
        summary="Replies to an Instagram comment. Costs 8 credits.",
        params=(
            _req("media_id", "Instagram media id."),
            _req("comment_id", "Parent comment id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=8,
    ),
    Endpoint(
        key="instagram_search_users",
        namespace="instagram",
        method="search_users",
        http="POST",
        path="/api/v1/instagram/search/users",
        summary="Search Instagram users by keyword. Costs 10 credits.",
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=10,
    ),
    Endpoint(
        key="instagram_search_hashtags",
        namespace="instagram",
        method="search_hashtags",
        http="POST",
        path="/api/v1/instagram/search/hashtags",
        summary="Search Instagram hashtags by keyword. Costs 10 credits.",
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=10,
    ),
    Endpoint(
        key="instagram_user_followers",
        namespace="instagram",
        method="user_followers",
        http="POST",
        path="/api/v1/instagram/user/followers",
        summary="Followers of an Instagram user. Provide username or user_id. Costs 10 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-100)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=10,
    ),
    Endpoint(
        key="instagram_user_followings",
        namespace="instagram",
        method="user_followings",
        http="POST",
        path="/api/v1/instagram/user/followings",
        summary="Accounts an Instagram user follows. Provide username or user_id. Costs 10 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-100)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=10,
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
    # =============================== LinkedIn ============================
    # The provider retired the `linkedin/web/*` namespace it was built on; these
    # now run on `linkedin/web_v2/*`, which is URL-native. Public params are
    # unchanged (the permalink is built server-side) and `url` is accepted
    # everywhere as a direct alternative. All live endpoints are 1 credit.
    # Five endpoints have no upstream left and always return HTTP 410 unbilled;
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
            "paginate by passing the previous response's next_cursor. Provide username or url."
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
    ),
    Endpoint(
        key="linkedin_person_contact",
        namespace="linkedin",
        method="person_contact",
        http="POST",
        path="/api/v1/linkedin/person/contact",
        summary=(
            "RETIRED: contact-info scraping was withdrawn by the upstream provider. This endpoint "
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
            "next_cursor. Provide company or url."
        ),
        params=(
            _str("company", "Company universal name (slug)."),
            _str("url", "Full LinkedIn company URL, as an alternative to company."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
        ),
        one_of=(("company", "url"),),
    ),
    Endpoint(
        key="linkedin_company_people",
        namespace="linkedin",
        method="company_people",
        http="POST",
        path="/api/v1/linkedin/company/people",
        summary=(
            "RETIRED: the employee directory was withdrawn by the upstream provider. This endpoint "
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
            "RETIRED: per-company job listings were withdrawn by the upstream provider. This "
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
            "RETIRED: people search was withdrawn by the upstream provider. This endpoint always "
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
            "repeat calls return different listings - dedupe by job id."
        ),
        params=(
            _req("search", "Search keyword."),
            _str("location", "Geographic filter; omit to search everywhere."),
            _str("cursor", "Opaque cursor from a prior response's next_cursor."),
        ),
    ),
    Endpoint(
        key="linkedin_search_posts",
        namespace="linkedin",
        method="search_posts",
        http="POST",
        path="/api/v1/linkedin/search/posts",
        summary=(
            "RETIRED: post search was withdrawn by the upstream provider. This endpoint always "
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
        summary="Full details for a single job listing, including the hiring company. Provide job_id or url.",
        params=(
            _str("job_id", "Job id."),
            _str("url", "Full LinkedIn job URL, as an alternative to job_id."),
        ),
        one_of=(("job_id", "url"),),
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
            "varies, so keep going until a page comes back empty. Provide post_id or url."
        ),
        params=(
            _str("post_id", "Post id or activity urn."),
            _str("url", "Full LinkedIn post URL, as an alternative to post_id."),
            _int("page", "1-based page number, 10 comments per page."),
        ),
        one_of=(("post_id", "url"),),
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
)


ENDPOINTS: Mapping[str, Endpoint] = {ep.key: ep for ep in _ENDPOINTS}

# Namespaces in the order they are exposed on the client.
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
)


def endpoints_for(namespace: str) -> list[Endpoint]:
    return [ep for ep in _ENDPOINTS if ep.namespace == namespace]
