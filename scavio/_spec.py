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
        summary="Search YouTube videos, channels, and playlists.",
        params=(
            _req("query", "Search query (1-500 characters).", wire="search"),
            _lit(
                "upload_date",
                ("last_hour", "today", "this_week", "this_month", "this_year"),
                "Filter by upload date.",
            ),
            _lit("type", ("video", "channel", "playlist"), "Filter by result type."),
            _lit(
                "duration",
                ("short", "medium", "long"),
                "short (<4 min), medium (4-20 min), long (>20 min).",
            ),
            _lit("sort_by", ("relevance", "date", "view_count", "rating"), "Sort order."),
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
    ),
    Endpoint(
        key="youtube_metadata",
        namespace="youtube",
        method="metadata",
        http="POST",
        path="/api/v1/youtube/metadata",
        summary="Full metadata for a single YouTube video.",
        params=(_req("video_id", "YouTube video id (e.g. 'dQw4w9WgXcQ')."),),
    ),
    # =============================== Amazon ==============================
    Endpoint(
        key="amazon_search",
        namespace="amazon",
        method="search",
        http="POST",
        path="/api/v1/amazon/search",
        summary="Search Amazon product listings.",
        params=(
            _req("query", "Product search query (1-500 characters)."),
            _str("domain", "Amazon domain suffix (default 'com', e.g. 'co.uk')."),
            _str("country", "Country code for localization."),
            _str("language", "Language code."),
            _str("currency", "Currency code (ISO 4217, e.g. 'USD')."),
            _lit("device", ("desktop", "mobile", "tablet"), "Device to emulate."),
            _lit(
                "sort_by",
                (
                    "most_recent",
                    "price_low_to_high",
                    "price_high_to_low",
                    "featured",
                    "average_review",
                    "bestsellers",
                ),
                "Result sort order.",
            ),
            _int("start_page", "Starting page (1-indexed)."),
            _int("pages", "Number of pages to fetch."),
            _str("category_id", "Amazon category id."),
            _str("merchant_id", "Filter to a specific merchant."),
            _str("zip_code", "ZIP/postal code for localized pricing."),
            _bool("autoselect_variant", "Auto-select the default variant."),
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
            _str("domain", "Amazon domain suffix (default 'com')."),
            _str("country", "Country code for localization."),
            _str("language", "Language code."),
            _str("currency", "Currency code (ISO 4217, e.g. 'USD')."),
            _lit("device", ("desktop", "mobile", "tablet"), "Device to emulate."),
            _str("zip_code", "ZIP/postal code for localized pricing."),
            _bool("autoselect_variant", "Auto-select the default variant."),
        ),
    ),
    Endpoint(
        key="amazon_options",
        namespace="amazon",
        method="options",
        http="GET",
        path="/api/v1/amazon/options",
        summary="Supported Amazon domains, languages, currencies, and countries. No API key required.",
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
        summary="Search Reddit posts or comments. Costs 2 credits.",
        params=(
            _req("query", "Search query (1-500 characters)."),
            _lit("type", ("posts", "comments"), "Result type (server default 'posts')."),
            _lit(
                "sort",
                ("new", "relevance", "hot", "top", "comments"),
                "Sort order (server default 'new').",
            ),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=2,
    ),
    Endpoint(
        key="reddit_post",
        namespace="reddit",
        method="post",
        http="POST",
        path="/api/v1/reddit/post",
        summary="Fetch a Reddit post with its threaded comments. Costs 2 credits.",
        params=(_req("url", "Full Reddit post URL."),),
        credits=2,
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
        summary="Instagram profile. Provide username or user_id. Costs 2 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
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
        summary="Reels from an Instagram user. Provide username or user_id. Costs 2 credits.",
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
        key="instagram_user_tagged",
        namespace="instagram",
        method="user_tagged",
        http="POST",
        path="/api/v1/instagram/user/tagged",
        summary="Posts an Instagram user is tagged in. Provide username or user_id. Costs 2 credits.",
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
        key="instagram_user_stories",
        namespace="instagram",
        method="user_stories",
        http="POST",
        path="/api/v1/instagram/user/stories",
        summary="Active stories for an Instagram user. Provide username or user_id. Costs 2 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
    ),
    Endpoint(
        key="instagram_post",
        namespace="instagram",
        method="post",
        http="POST",
        path="/api/v1/instagram/post",
        summary="An Instagram post. Provide url, media_id, or shortcode. Costs 2 credits.",
        params=(
            _str("url", "Full Instagram post URL."),
            _str("media_id", "Instagram media id."),
            _str("shortcode", "Instagram shortcode (from the post URL)."),
        ),
        one_of=(("url", "media_id", "shortcode"),),
        credits=2,
    ),
    Endpoint(
        key="instagram_post_comments",
        namespace="instagram",
        method="post_comments",
        http="POST",
        path="/api/v1/instagram/post/comments",
        summary="Comments on an Instagram post. Provide shortcode or url. Costs 2 credits.",
        params=(
            _str("shortcode", "Instagram shortcode (from the post URL)."),
            _str("url", "Full Instagram post URL."),
            _str("cursor", "Pagination cursor from a prior response."),
            _lit("sort_order", ("popular", "newest"), "Comment sort order."),
        ),
        one_of=(("shortcode", "url"),),
        credits=2,
    ),
    Endpoint(
        key="instagram_comment_replies",
        namespace="instagram",
        method="comment_replies",
        http="POST",
        path="/api/v1/instagram/post/comments/replies",
        summary="Replies to an Instagram comment. Costs 2 credits.",
        params=(
            _req("media_id", "Instagram media id."),
            _req("comment_id", "Parent comment id."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=2,
    ),
    Endpoint(
        key="instagram_search_users",
        namespace="instagram",
        method="search_users",
        http="POST",
        path="/api/v1/instagram/search/users",
        summary="Search Instagram users by keyword. Costs 2 credits.",
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=2,
    ),
    Endpoint(
        key="instagram_search_hashtags",
        namespace="instagram",
        method="search_hashtags",
        http="POST",
        path="/api/v1/instagram/search/hashtags",
        summary="Search Instagram hashtags by keyword. Costs 2 credits.",
        params=(
            _req("keyword", "Search keyword (1-500 characters)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        credits=2,
    ),
    Endpoint(
        key="instagram_user_followers",
        namespace="instagram",
        method="user_followers",
        http="POST",
        path="/api/v1/instagram/user/followers",
        summary="Followers of an Instagram user. Provide username or user_id. Costs 2 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-100)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
    ),
    Endpoint(
        key="instagram_user_followings",
        namespace="instagram",
        method="user_followings",
        http="POST",
        path="/api/v1/instagram/user/followings",
        summary="Accounts an Instagram user follows. Provide username or user_id. Costs 2 credits.",
        params=(
            _str("username", "Instagram username (without the @)."),
            _str("user_id", "Instagram numeric user id."),
            _int("count", "Results per page (1-100)."),
            _str("cursor", "Pagination cursor from a prior response."),
        ),
        one_of=(("username", "user_id"),),
        credits=2,
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
    "tiktok",
    "instagram",
)


def endpoints_for(namespace: str) -> list[Endpoint]:
    return [ep for ep in _ENDPOINTS if ep.namespace == namespace]
