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



# Best Buy params shared across endpoints.
_BESTBUY_SKU = _str(
    "sku",
    "Best Buy SKU, the number after /sku/ in a product URL (a search result's `sku`).",
)
_BESTBUY_URL = _str(
    "url",
    "bestbuy.com product URL that names a SKU (/product/<name>/<id>/sku/<sku> or "
    "/site/<name>/<sku>.p?skuId=<sku>). Used when sku is not given.",
)
_BESTBUY_FILTERS = Param(
    "filters",
    "Optional[dict[str, Any]]",
    doc="Filters, the same as the site's filter sidebar: brand (as spelled in the Brand "
    "facet), on_sale, clearance, open_box (booleans), min_price and max_price (dollars, "
    "pass both), e.g. {'brand': 'Samsung', 'on_sale': True}. applied_filters in the "
    "response echoes what Best Buy applied.",
)
_BESTBUY_INCLUDE_SPONSORED = _bool(
    "include_sponsored",
    "Include the sponsored tiles Best Buy mixes into the grid (sponsored: true, position "
    "null). Defaults to false.",
)


# TCGplayer params shared across endpoints.
_TCG_PRODUCT_ID = _str_or_int(
    "product_id",
    "TCGplayer product id, the number after /product/ in a tcgplayer.com URL (a search "
    "result's product_id), e.g. 219058.",
)
_TCG_URL = _str(
    "url",
    "A tcgplayer.com product URL (/product/<id>/...). Used when product_id is not given.",
)
_TCG_GAME = _str(
    "game",
    "Game (product line) url_name from games(): pokemon, magic, yugioh, pokemon-japan, "
    "one-piece-card-game, lorcana-tcg...",
)
_TCG_SELLER_KEY = _req(
    "seller_key",
    "TCGplayer seller key, a listing's seller.key (8 characters), e.g. '58f7acae'.",
)
_TCG_CONDITIONS = (
    "Near Mint, Lightly Played, Moderately Played, Heavily Played, Damaged, Unopened "
    "(or NM, LP, MP, HP, DM, U)"
)
_TCG_SEARCH_SORT = _lit(
    "sort",
    ("relevance", "best_match", "best_selling", "name_asc", "price_asc", "price_desc"),
    "relevance (default), best_match, best_selling, name_asc, price_asc or price_desc (by "
    "market price). relevance and best_match rankings shift between calls and page 2+ drops "
    "products already seen (duplicates_removed), so a price or name sort pages more "
    "predictably.",
)
_TCG_SEARCH_PAGE = _int("page", "Results page, 1-based, up to 200. Defaults to 1.")
_TCG_SEARCH_LIMIT = _int("limit", "Products per page, 1-50. Defaults to 24.")
_TCG_PRODUCT_TYPE = _lit(
    "product_type",
    ("cards", "sealed"),
    "cards (single cards) or sealed (booster boxes, packs, decks, tins...).",
)
_TCG_PRODUCT_FIELDS = (
    "product id, name, URL, image, game, set name, code and id, card number, rarity, product "
    "type, sealed and foil-only flags, release date, market price, median price, lowest price, "
    "lowest price with shipping and listing count"
)


# Vinted params shared across endpoints.
_VINTED_COUNTRY = _lit(
    "country",
    (
        "fr", "be", "lu", "es", "nl", "lt", "de", "at", "it", "uk", "pt", "us", "cz", "sk",
        "pl", "se", "ro", "hu", "dk", "fi", "hr", "gr", "ie", "ee", "lv", "si", "au",
    ),
    "Vinted country site: fr (default), be, lu, es, nl, lt, de, at, it, uk (vinted.co.uk), "
    "pt, us (vinted.com), cz, sk, pl, se, ro, hu, dk, fi, hr, gr, ie, ee, lv, si, au "
    "(vinted.com.au). Category, condition and filter names come back in the site's language. "
    "Every site can show listings from sellers in other countries, with the price converted to "
    "the site's currency (EUR, or CZK, PLN, SEK, RON, HUF, DKK, GBP for uk, USD for us, AUD for "
    "au); the EU sites share one cross-border pool. product() returns the seller's own price "
    "and currency.",
)
_VINTED_USER_ID = Param(
    "user_id",
    "Union[str, int]",
    required=True,
    doc="Vinted member id: a search result's seller.id, a product's seller.id, or the number "
    "after /member/ in a profile URL, e.g. 65958245.",
)
_VINTED_FEE = (
    "service_fee is the Vinted fee the buyer pays on top of the price (formerly the Buyer "
    "Protection fee) and total_price is price plus that fee"
)


def _vinted_ids(name: str, doc: str) -> Param:
    """Vinted id filters: a list of ids or a comma-separated string, up to 20."""
    return Param(
        name,
        "Optional[Union[str, list[Union[str, int]]]]",
        doc=doc + " A list or a comma-separated string, up to 20.",
    )


# Macy's params shared across endpoints.
_MACYS_PRODUCT_ID = _str_or_int(
    "product_id",
    "Macy's product id: a search result's id, or the ID= number in a macys.com product URL, "
    "e.g. 25822310.",
)
_MACYS_URL = _str("url", "A macys.com product URL (its ID= is used). Alternative to product_id.")
_MACYS_SPECIAL_OFFERS = (
    "limited_time_special",
    "gift_with_purchase",
    "black_friday_deal",
    "clearance",
    "last_act",
    "our_lowest_price",
    "sales_and_discounts",
    "special_offer",
    "today_only",
)
_MACYS_SPECIAL_OFFER_LITERAL = "Literal[" + ", ".join(f'"{c}"' for c in _MACYS_SPECIAL_OFFERS) + "]"
_MACYS_SPECIAL_OFFER = Param(
    "special_offer",
    f"Optional[Union[{_MACYS_SPECIAL_OFFER_LITERAL}, list[{_MACYS_SPECIAL_OFFER_LITERAL}]]]",
    doc="Only items with this offer: " + ", ".join(_MACYS_SPECIAL_OFFERS) + ". A list matches "
    "any of them.",
)
_MACYS_GRID = (
    _int("page", "Results page, 1-based (60 organic items per page). Defaults to 1."),
    _lit(
        "sort",
        (
            "featured",
            "price_low_to_high",
            "price_high_to_low",
            "top_rated",
            "best_sellers",
            "newest",
        ),
        "featured (default), price_low_to_high, price_high_to_low, top_rated, best_sellers or "
        "newest. The total can differ between sorts, as it does on the site.",
    ),
    _str_or_list(
        "brand",
        "Only these brands, spelled as the BRAND facet lists them (e.g. \"Levi's\"). A list "
        "matches any of them.",
    ),
    _str_or_list(
        "color",
        "Only these colors, as the COLOR_NORMAL facet lists them (Black, Blue, Red...). A list "
        "matches any of them.",
    ),
    _float("min_price", "Minimum price in USD. Any bound works, not only the site's buckets."),
    _float("max_price", "Maximum price in USD."),
    _str_or_int(
        "pickup_store_id",
        "Only items available for pickup at this store (a store_id from stores()), e.g. 4592.",
    ),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any other facet from a previous response's facets: its name to one value or a "
        "list, e.g. {'GENDER': 'Women', 'CUSTRATINGS': '4 stars & up'}.",
    ),
    _bool(
        "include_sponsored",
        "Keep ad-only sponsored tiles (flagged is_sponsored). Defaults to false: they are "
        "dropped.",
    ),
)
_MACYS_GRID_FIELDS = (
    "60 organic items per page, each with id, title, brand, URL, image, price (price_max when "
    "the item sells at a range), regular and sale price, percent off, price label, on-sale "
    "flag, sale end date, deal label (Black Friday Deal, Clearance, LAST ACT, Today Only...), "
    "promotions, rating, review count, colors and is_sponsored. Also returns total, page, "
    "total_pages, the sort applied, the facets (name, label and values with counts; any value "
    "works in filters) and applied_filters. Ad-only sponsored tiles are dropped "
    "(sponsored_dropped counts them) unless include_sponsored; organic items that also hold a "
    "paid slot stay, flagged is_sponsored. Totals can differ between sorts, as on the site. "
    "Prices in USD."
)
_MACYS_LOCATION = (
    _str("zip", "US ZIP code to search around, e.g. '10001'."),
    _float("lat", "Latitude (with lng), instead of zip."),
    _float("lng", "Longitude (with lat)."),
    _str("city", "US city (with state), instead of zip, e.g. 'Atlanta'."),
    _str("state", "2-letter US state code (with city), e.g. 'GA'."),
    _int("radius", "Search radius in miles, 1-100. Defaults to 100."),
)


# Saks Fifth Avenue params shared across endpoints.
_SAKS_SORTS = (
    "featured",
    "best_sellers",
    "newest",
    "price_high_to_low",
    "price_low_to_high",
    "sale_first",
    "brand_az",
)
_SAKS_BRAND = _str_or_list(
    "brand",
    "Only these designers, spelled as the brand facet lists them (e.g. \"Prada\", \"ALICE + "
    "OLIVIA\"). A list matches any of them.",
)
_SAKS_GRID = (
    _int("page", "Results page, 1-based (24 grid positions per page). Defaults to 1."),
    _int(
        "start",
        "Item offset, instead of page: pass a previous response's next_start to walk every item "
        "without gaps (an editorial tile can take a grid position, so a page may carry 22-23 "
        "items).",
    ),
    _lit(
        "sort",
        _SAKS_SORTS,
        "featured (default, the site's own order), best_sellers, newest, price_high_to_low, "
        "price_low_to_high, sale_first or brand_az.",
    ),
    _str_or_list(
        "color",
        "Only these colors, as the colorRefinement facet lists them (Black, Blue, Red...). A "
        "list matches any of them.",
    ),
    _str_or_list(
        "size",
        "Only these sizes, spelled as the sizeRefinement facet LABEL lists them (\"Medium\", "
        "\"X-Small, 0\"; \"M\" matches nothing). A list matches any of them.",
    ),
    _float("min_price", "Minimum price in USD. Any bound works, not only the site's buckets."),
    _float("max_price", "Maximum price in USD."),
    _bool("on_sale", "Only items on sale."),
    _bool("new_arrivals", "Only new arrivals."),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any other facet from a previous response's facets: its id to one value or a list, "
        "e.g. {'refGender': \"Women's\", 'refMaterial': 'Cashmere'}.",
    ),
)
_SAKS_GRID_FIELDS = (
    "24 grid positions per page, each item with id (variant_id too when the tile shows one "
    "variant), title, brand, URL, image, price (price_max when the item sells at a range), "
    "regular and sale price, percent off, on-sale flag, review count, badge (Best Seller, "
    "Exclusive, Runway Look...), is_final_sale and is_clearance (null when the tile leaves them "
    "blank; product() is authoritative), returnable, limited_inventory, promotions, "
    "product_type and colors. Also returns total, page, total_pages, start and next_start "
    "(pass next_start as start for the next page: an editorial tile can take a grid position, "
    "so a page may carry 22-23 items), the sort applied, the facets (id, label and values with "
    "counts; any value works in filters), price_ranges and applied_filters. Review count only: "
    "review text is not available. Prices in USD."
)
_SAKS_LOCATION = (
    _str("zip", "US ZIP code to search around, e.g. '10022'."),
    _float("lat", "Latitude (with lng), instead of zip."),
    _float("lng", "Longitude (with lat)."),
    _ilit(
        "radius",
        (15, 30, 50, 100, 300),
        "Search radius in miles: 15, 30, 50, 100 or 300. Defaults to 50.",
    ),
)


# Kohl's params shared across endpoints.
_KOHLS_SORTS = (
    "featured",
    "new_arrivals",
    "best_sellers",
    "price_low_to_high",
    "price_high_to_low",
    "highest_rated",
    "percent_off",
)
_KOHLS_BRAND = _str(
    "brand",
    "Only this brand, as the Brand facet lists it (\"Levi's\", \"Hamilton Beach\", "
    "\"BLACK+DECKER\").",
)
_KOHLS_GRID = (
    _int("page", "Results page, 1-based (120 products per page). Defaults to 1."),
    _lit(
        "sort",
        _KOHLS_SORTS,
        "featured (default), new_arrivals, best_sellers, price_low_to_high, price_high_to_low, "
        "highest_rated or percent_off.",
    ),
    _str("color", "Only this color, as the Color facet lists it (Black, Blue, Beig/khaki...)."),
    _str("size", "Only this size, as the Size facet lists it (M, 32X30, 10...)."),
    _bool("on_sale", "Only items on sale."),
    _bool("clearance", "Only clearance items."),
    _str_or_list(
        "filters",
        "Any facet value id from a previous response's facets[].values[].value, e.g. "
        "'Gender:Womens', 'Price:%2425%20to%20%2450' (price buckets), 'TopRated:4', "
        "'InStoreOnline:Pick%20Up%20in%20Store'. A list combines facets (AND). Unencoded values "
        "work too ('Price:$25 to $50').",
    ),
)
_KOHLS_GRID_FIELDS = (
    "120 products per page, each with id, title, URL, image, price (price_max for a range), "
    "regular_price, sale_price, price_label (sale, clearance, clearance+regular), on_sale, "
    "is_clearance, percent_off, price_suppressed with price_note (Kohl's shows some prices only "
    "in the cart), with_code_price (the price after a public offer code) with "
    "with_code_offer_codes, promotions (BOGO...), rating, review_count, badges (best_seller, "
    "top_rated...), colors, is_sephora, coupon_eligible, available_online / available_pickup / "
    "available_ship_to_store, and is_sponsored. Sponsored placements (up to about 8) stay in "
    "the list, flagged is_sponsored and counted in sponsored_count. Also returns total, page, "
    "total_pages, the sort applied, applied_filters and every facet (id, label and values with "
    "their value id, count and a selected flag; any value id works in filters; price is a "
    "bucket such as 'Price:$25 to $50', there is no free min / max). Average rating and review "
    "count only: review text is not available. Prices in USD."
)
_KOHLS_ZIP_DOC = "US ZIP code to search around, e.g. '60601'."


# JCPenney params shared across endpoints.
_JCPENNEY_SORTS = (
    "relevance",
    "new_arrivals",
    "best_sellers",
    "rating",
    "price_low_to_high",
    "price_high_to_low",
)
_JCPENNEY_DEAL_TYPES = (
    "clearance",
    "sale",
    "black_friday",
    "big_buy",
    "limited_time_special",
    "best_value",
    "gotta_have_it",
    "closeout",
    "bogo",
)
_JCPENNEY_BRAND = _str_or_list(
    "brand",
    "Only this brand (or any of several), as the Brand facet lists it (\"levi's\", \"nike\", "
    "\"st. john's bay\").",
)
_JCPENNEY_DEAL = _str_or_list(
    "deal",
    "Only items with this Deals & Promotions label ('SALE', 'CLEARANCE', 'BIG BUY!'...), as "
    "the facet lists it.",
)
_JCPENNEY_GRID = (
    _int(
        "page",
        "Results page, 1-based (48 items per page, at most 25 pages). A page past the last one "
        "returns an empty items list with the real total. Defaults to 1.",
    ),
    _lit(
        "sort",
        _JCPENNEY_SORTS,
        "relevance (default), new_arrivals, best_sellers, rating (highest rated first), "
        "price_low_to_high or price_high_to_low. The price orders are JCPenney's own and loose: "
        "sort the items by price yourself when you need a strict order.",
    ),
    _str_or_list(
        "color",
        "Only this color (or any of several), as the Color facet lists it (black, blue, "
        "beige...).",
    ),
    _str_or_list(
        "size",
        "Only this size (or any of several), as the Size facet lists it (m, 12, 32x30...).",
    ),
    _str_or_list("price_range", "A Price Range facet value ('under $5', '$20 - $24'...)."),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any facet from a previous response: {facets[].id: facets[].values[].value, or a "
        "list of values (any of them)}, e.g. {'gender': 'women'}, {'store_availability': 'same "
        "day pickup'}, {'average_rating': '4 rating'}. Several facets combine (AND).",
    ),
)
_JCPENNEY_GRID_FIELDS = (
    "48 products per page (at most 25 pages = 1,200 items), each with id, title, brand, URL, "
    "image, sku_id, price and price_max (current), regular_price and regular_price_max, "
    "price_type (sale, clearance, original), percent_off, deal_label (BIG BUY!, CLEARANCE...), "
    "coupon_price with coupon_code (the price after today's coupon), rating, review_count, "
    "badge (Only at JCP, NEW, Few Left), availability_label (Same Day Pickup, Online Only...), "
    "colors with their SKU ids, and is_marketplace with the seller for third-party items. Also "
    "returns total, page, total_pages, the sort applied, applied_filters and every facet (id, "
    "label and values with their value, count and a selected flag; any of them works in "
    "filters). Prices are product-level ranges: JCPenney does not expose a price per size or "
    "color. Average rating and review count here; review text is reviews(). Prices in USD."
)
_JCPENNEY_ZIP_DOC = "US or Puerto Rico ZIP code to search around, e.g. '75024'."
_JCPENNEY_REVIEW_SORTS = ("most_recent", "most_helpful", "highest_rating", "lowest_rating", "relevance")
_JCPENNEY_PRODUCT_TARGET = (
    _str(
        "product_id",
        "A JCPenney product id (ppr / ppm / pp + digits): a search result's id, the last part of "
        "a product URL, e.g. 'ppr5008604049'.",
    ),
    _str("url", "A jcpenney.com product URL (its product id is used). Alternative to product_id."),
)


# Dick's Sporting Goods params shared across endpoints.
_DICKS_SORTS = (
    "relevance",
    "top_sellers",
    "savings",
    "price_low_to_high",
    "price_high_to_low",
    "featured",
    "new_arrivals",
    "brand_az",
)
_DICKS_BRAND = _str_or_list(
    "brand",
    "Only this brand (or any of several), as the Brand facet lists it (\"Nike\", \"HOKA\", "
    "\"YETI\").",
)
_DICKS_GRID = (
    _int(
        "page",
        "Results page, 1-based. A page past the last one returns an empty items list with the "
        "real total. Defaults to 1.",
    ),
    _int("page_size", "Items per page, 1-144. Defaults to 48."),
    _lit(
        "sort",
        _DICKS_SORTS,
        "relevance, top_sellers, savings (biggest discount first), price_low_to_high, "
        "price_high_to_low, featured (the site's merchandised order: pinned items first), "
        "new_arrivals or brand_az. Search and brand default to relevance; category and deals to "
        "featured, like the site.",
    ),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any facet from a previous response: {facets[].id: facets[].values[].value, or a "
        "list of values}. Values of one facet are OR, facets combine (AND). E.g. {'5495': "
        "\"Men's\"} (gender), {'3232': 'Black'} (color), {'rating': '4+'}, {'price': '50-100'}.",
    ),
    _float(
        "min_price",
        "Approximate lower price bound in USD (the site's price filter is loose: a few items just "
        "outside the range can appear).",
    ),
    _float("max_price", "Approximate upper price bound in USD."),
)
_DICKS_GRID_FIELDS = (
    "48 items per page by default (up to 144), each with id, sku (the variant the tile shows; "
    "null on style-level tiles), title, brand, URL, image, price and price_max (current), "
    "list_price and list_price_max, percent_off, map_price_applies (the lowest price only shows "
    "in the cart), rating, review_count, badge, sku_count, options, is_pinned (a merchandised "
    "placement) and scheduled_prices (the offer-price windows Dick's has planned: price, "
    "starts_at, ends_at; set by the retailer and can change, not a forecast or price history). "
    "Also returns total, page, page_size, total_pages, the sort applied, applied_filters, every "
    "facet (id, label, values with value, label, count and selected; any of them works in "
    "filters) and categories (id, name, path, count). Pinned items come first on page 1 under "
    "the featured sort, so that page can hold a few more than page_size. Prices in USD."
)
_DICKS_PRODUCT_TARGET = (
    _str(
        "product_id",
        "A Dick's product id: a search result's id, the last part of a product URL (any case), "
        "e.g. '23FHQMCLFTN9GTXBLMNS'.",
    ),
    _str(
        "url",
        "A dickssportinggoods.com product URL (its product id is used). Alternative to "
        "product_id.",
    ),
)
_DICKS_SLOW = (
    " Usually 20-75 s, up to about 2.5 minutes when a call is retried; failed calls and unknown "
    "products are not charged."
)


# Foot Locker params shared across endpoints.
_FOOTLOCKER_MARKETS = (
    "us (footlocker.com, USD, default), ca (CAD, language en or fr), gb (GBP), de, fr, it, es, "
    "nl, be (language nl or fr), at, ie (EUR), au (AUD) or nz (NZD)"
)
_FOOTLOCKER_COUNTRY = _lit(
    "country",
    ("us", "ca", "gb", "de", "fr", "it", "es", "nl", "be", "at", "ie", "au", "nz"),
    "The storefront: " + _FOOTLOCKER_MARKETS + ". Titles come in the storefront's language, "
    "prices in its currency.",
)
_FOOTLOCKER_LANGUAGE = _lit(
    "language", ("en", "fr", "nl"), "Only for ca (en default, fr) and be (nl default, fr)."
)
_FOOTLOCKER_US_ONLY = _lit("country", ("us",), "us only (the only storefront this endpoint covers).")
_FOOTLOCKER_SORTS = (
    "relevance",
    "price_low_to_high",
    "price_high_to_low",
    "new_arrivals",
    "top_rated",
    "name_az",
    "brand_az",
)
_FOOTLOCKER_BRAND = _str_or_list(
    "brand",
    "Only this brand (or any of several), e.g. \"Nike\", \"Jordan\", \"adidas\", \"New "
    "Balance\", \"HOKA\"; case does not matter.",
)
_FOOTLOCKER_GRID = (
    _int(
        "page",
        "Results page, 1-based (48 items per page, up to 200). A page past the last one returns "
        "an empty items list with the real total. Defaults to 1.",
    ),
    _lit(
        "sort",
        _FOOTLOCKER_SORTS,
        "relevance (the site's Featured order, default), price_low_to_high, price_high_to_low, "
        "new_arrivals, top_rated, name_az or brand_az.",
    ),
    _str_or_list(
        "gender",
        "Gender filter value(s) as facets.gender lists them (\"Men's\", \"Women's\"; in the "
        "storefront's language).",
    ),
    _str_or_list("color", "Color filter value(s) as facets.primaryColor lists them, e.g. 'Black'."),
    _str_or_list(
        "price_range",
        "Price bucket value(s) as facets.price lists them (25-50, 50-75, 75-100, 100-150, "
        "150-inf).",
    ),
    _bool("on_sale", "Only items on sale."),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any filter from a previous response: {facets[].id: facets[].values[].value, or a "
        "list of values}. Values of one filter are OR, filters combine (AND). E.g. "
        "{'mensShoesSize': '10.0'}, {'womensShoesSize': '8.0'}, {'style': 'Casual Sneakers'}, "
        "{'sport': 'Running'}, {'eligibleForDiscount': 'True'}.",
    ),
)
_FOOTLOCKER_GRID_FIELDS = (
    "48 items per page, each with id (the SKU, for product()), base_product, title, brand, URL, "
    "image, price, list_price, percent_off, lowest_price_30d (European storefronts: the lowest "
    "price of the last 30 days), on_sale, is_new, is_launch, member_only_sale, rating, "
    "review_count, color_count and colors (sku, color, price, list_price per colorway). Also "
    "returns total, page, page_size, total_pages, the sort applied, applied_filters, every facet "
    "(id, label, values with value, label, count; any of them works in filters), country, "
    "language, currency and data_as_of: listings can be a few hours old, data_as_of says when "
    "this one was built."
)
_FOOTLOCKER_PRODUCT_TARGET = (
    _str(
        "product_id",
        "A Foot Locker SKU: a search result's id, the last part of a product URL (Q5495005 in "
        "the US, 12 digits such as 316707025504 in Europe).",
    ),
    _str(
        "url",
        "A Foot Locker product URL on any covered storefront (its storefront and SKU are used). "
        "Alternative to product_id.",
    ),
)
_FOOTLOCKER_WHERE = (
    _str_or_int("zip", "US ZIP code to search around, e.g. '10001'."),
    _float("lat", "Latitude (with lng), instead of zip."),
    _float("lng", "Longitude (with lat)."),
    _int("radius", "Search radius in miles, 1-120. Defaults to 25."),
    _int("limit", "Stores to return, nearest first, 1-50. Defaults to 10."),
    _FOOTLOCKER_US_ONLY,
)
_FOOTLOCKER_NOT_FOUND = " Failed upstream calls are not charged; a not-found is charged."
_FOOTLOCKER_SLOW = (
    " Slow: usually 25-90 s, up to about 3-4 minutes when a call is retried; failed calls are "
    "not charged. A product without an online page is a charged 404. US only."
)


# Fanatics params shared across endpoints (merchandise / product data, not odds).
_FANATICS_MARKETS = (
    "us (fanatics.com, USD, default), gb (GBP), de, fr, es, it (EUR), jp (JPY) or ca (CAD; "
    "language en or fr)"
)
_FANATICS_STORES = (
    "fanatics (default), nflshop (NFL Shop), mlbshop (MLB Shop), nhlshop (NHL Shop) or mlsstore "
    "(MLS Store)"
)
_FANATICS_COUNTRY = _lit(
    "country",
    ("us", "gb", "de", "fr", "es", "it", "jp", "ca"),
    "The storefront: " + _FANATICS_MARKETS + ". Defaults to us. Titles come in the storefront's "
    "language, prices in its currency.",
)
_FANATICS_LANGUAGE = _lit("language", ("en", "fr"), "ca only: en (default) or fr.")
_FANATICS_SITE = _lit(
    "site",
    ("fanatics", "nflshop", "mlbshop", "nhlshop", "mlsstore"),
    "US only (country us): the store to read, " + _FANATICS_STORES + ". Same product ids on "
    "every store; each store writes its own titles. Department and filter ids are per store "
    "(Jerseys is 8011 on fanatics, 14012 on nflshop): take them from the facets of the store you "
    "query, since an id from another store is silently ignored.",
)
_FANATICS_GENDER = _lit("gender", ("men", "women", "kids", "baby"), "men, women, kids or baby.")
_FANATICS_GRID = (
    _int(
        "page",
        "Results page, 1-based (up to 375). Defaults to 1. Fanatics lists at most 9000 products "
        "per listing.",
    ),
    _ilit("page_size", (24, 48, 72), "Items per page: 24, 48 or 72. Defaults to 72."),
    _lit(
        "sort",
        ("top_sellers", "price_low_to_high", "price_high_to_low", "newest"),
        "top_sellers (default), price_low_to_high, price_high_to_low or newest. Price sorts "
        "order by the current price (price, before any promo code), not the with-code price.",
    ),
)
_FANATICS_FILTERS = Param(
    "filters",
    "Optional[dict[str, Union[str, int]]]",
    doc="Filters from a previous response: {facets[].values[].filter: facets[].values[].value}, "
    "one value per filter (up to 12). E.g. {'ga': '2'} (Women), {'ks': '126'} (a kids size), "
    "{'cs': '2'} (Fashion), {'fa': '1'} (Autographed), {'t': '3433'} (a team).",
)
_FANATICS_GRID_FIELDS = (
    "Items with id (for product() and reviews()), title, brand, url, image, price (current), "
    "regular_price, sale_price, clearance_price, with_code_price and code_percent_off (the price "
    "with the site's current promo code, when it applies), price_label (none, coupon or "
    "clearance; coupon means coupon-eligible, a null with_code_price means the code does not "
    "apply), percent_off, top_seller, customizable, ready_to_ship, ship_by, est_delivery, "
    "urgency signals and is_sponsored. Also returns total (the US site counts at most 9000: "
    "total_capped is true when the real number is 9000 or more), page, page_size, total_pages, "
    "the sort, every facet (id, label, values with label, filter, value and count: send "
    "{filter: value} in filters), country, language, currency, site and data_as_of (when "
    "Fanatics built the page; listings can be a few minutes old)."
)
_FANATICS_WHERE = " Storefronts (country): " + _FANATICS_MARKETS + ". US league stores (site): " + _FANATICS_STORES + "."
_FANATICS_CHARGE = (
    " Failed upstream calls are not charged (they are retried automatically); a not-found is "
    "charged."
)
_FANATICS_PRODUCT_ID = _str(
    "product_id",
    "A Fanatics product id: a search result's id, e.g. '3892922'. The same id works on every "
    "league store.",
)


def _fanatics_id(name: str, doc: str) -> Param:
    """A facet id: an integer, or a digit string ('8008-8084' for a sub-department)."""
    return _str_or_int(name, doc)


# Carrefour params shared across endpoints (carrefour.fr + ar / ro / be for search and product).
_CARREFOUR_MARKETS = (
    "fr (carrefour.fr, EUR, every endpoint, default), ar (Argentina, ARS, Spanish), ro (Romania, "
    "RON, Romanian) or be (Belgium, EUR, language fr or nl; 2 credits)"
)
_CARREFOUR_COUNTRY = _lit(
    "country",
    ("fr", "ar", "ro", "be"),
    "The national site: " + _CARREFOUR_MARKETS + ". Defaults to fr. Titles come in the market's "
    "language, prices in its currency.",
)
_CARREFOUR_FR = _lit("country", ("fr",), "fr only (carrefour.fr).")
_CARREFOUR_LANGUAGE = _lit("language", ("fr", "nl"), "be only: fr (default) or nl.")
_CARREFOUR_STORE = _str_or_int(
    "store",
    "fr only: price and assortment at one store. A store_ref or pickup_refs[].ref from stores(), "
    "or stores[].store.ref from store_availability(), e.g. '840093'. Without it prices are the "
    "national online price.",
)
_CARREFOUR_PAGE = _int(
    "page", "Results page, 1-based (up to 500). Defaults to 1. 30 items per page on fr (ar and ro 24, be 36)."
)
_CARREFOUR_SORT = _lit(
    "sort",
    (
        "relevance",
        "price_low_to_high",
        "price_high_to_low",
        "unit_price_low_to_high",
        "unit_price_high_to_low",
        "top_rated",
    ),
    "relevance (default), price_low_to_high, price_high_to_low, unit_price_low_to_high, "
    "unit_price_high_to_low or top_rated. ar and ro: relevance and the two price sorts; be: "
    "relevance.",
)
_CARREFOUR_FILTERS = (
    _str(
        "brand",
        "fr: one brand as the Marque facet lists it (facets[id=facet_marque].values[].label, e.g. "
        "NUTELLA, CARREFOUR BIO). Another casing is matched to the facet's own.",
    ),
    _lit("nutriscore", ("A", "B", "C", "D", "E"), "fr: only this Nutri-Score."),
    _bool("organic", "fr: only organic products."),
    _bool("carrefour_brands", "fr: only Carrefour's own brands."),
    _float("min_price", "fr: lowest price in EUR."),
    _float("max_price", "fr: highest price in EUR."),
)
_CARREFOUR_PROMOTION_FILTER = _str(
    "promotion",
    "fr: one value of the Promotions facet (facets[id=facet_promotions]): Toutes les promotions, "
    "Remises immédiates, Vu en catalogue, Avantage Fidélité...",
)
_CARREFOUR_GRID_FIELDS = (
    " Items with ean (for product(), reviews() and store_availability()), title, brand, url, "
    "image, type (product or marketplace), sponsored, price (regular price), unit_price with unit "
    "and unit_price_label (price per kg / L), packaging, format, nutriscore (A-E), ecoscore, "
    "rating, review_count, available, low_stock, promotion (type, label, loyalty_only: the price "
    "needs the Carrefour loyalty card, seen_in_catalogue, discounted_price, initial_price, "
    "discount_amount, quantity, starts_at, ends_at; on multi-buy deals such as 'Le 2ème à -50%' "
    "initial_price and discounted_price cover quantity items, and discounted_price is null when "
    "the site does not price the deal), seller (marketplace items) and category. Also total, "
    "total_pages, page, page_size, every facet (id, label, values with label, count and "
    "selected), store, price_scope, country, language and currency."
)
_CARREFOUR_SCOPE = (
    " Prices: without store, carrefour.fr's national online price; with store, that store's "
    "shelf price and assortment (they differ by store: Nutella 400 g was 3.99 national, 3.69 at "
    "two stores and 4.61 at another). The response says which (store, price_scope). Titles and "
    "labels come in French on fr, as the site writes them."
)
_CARREFOUR_CHARGE = (
    " Failed upstream calls are not charged (they are retried automatically); a not-found is "
    "charged."
)
_CARREFOUR_FR_NOTE = " fr only (carrefour.fr)."


_KROGER_BANNERS = ("kroger", "qfc", "fred_meyer")
_KROGER_BANNER_TEXT = (
    "kroger (kroger.com, default), qfc (QFC, qfc.com: Washington and Oregon) or fred_meyer "
    "(Fred Meyer, fredmeyer.com: the Pacific Northwest and Alaska)"
)
_KROGER_BANNER = _lit(
    "banner",
    _KROGER_BANNERS,
    f"The store banner: {_KROGER_BANNER_TEXT}. Defaults to kroger. Prices differ by banner and by store.",
)
_KROGER_STORE_BANNER = _lit(
    "banner",
    _KROGER_BANNERS,
    f"The store banner: {_KROGER_BANNER_TEXT}. Optional with store_id: QFC ids start with 705, "
    "Fred Meyer ids with 701, anything else is kroger.",
)


# Publix params shared across endpoints (publix.com, US; every price endpoint is store-scoped).
_PUBLIX_STORE_DOC = (
    "A Publix store number: stores[].store_id of stores(), e.g. '1614' (Miami) or '1825' "
    "(Atlanta). Prices, promotions and aisles are this store's."
)
_PUBLIX_STORE = Param("store_id", "Union[str, int]", required=True, doc=_PUBLIX_STORE_DOC)
_PUBLIX_STORE_OPT = _str_or_int("store_id", "Optional. " + _PUBLIX_STORE_DOC)
_PUBLIX_GRID_PARAMS = (
    _int(
        "page",
        "Results page, 1-based (48 products per page). A page past the last answers an empty list.",
    ),
    _lit(
        "sort",
        (
            "relevance",
            "featured",
            "name_asc",
            "name_desc",
            "popularity",
            "savings_amount",
            "most_viewed",
        ),
        "relevance (default), featured, name_asc, name_desc, popularity, savings_amount "
        "(biggest promo savings first) or most_viewed.",
    ),
    _bool(
        "on_sale",
        "Only items on sale at the store (weekly ad, BOGO, multi-buy or extra savings).",
    ),
    _bool("bogo", "Only Buy One Get One Free items at the store."),
    _str("brand", "Only this brand, as the site lists it (facets: Brand values), e.g. 'Tyson'."),
)
_PUBLIX_PRICES = (
    " Publix shows prices online only for items on sale and for order-ahead (deli and bakery) "
    "items, so price is a number only when the site shows one and None otherwise; it is never "
    "estimated (no regular shelf prices). price_text is the price as shown, price_unit lb when "
    "per pound, bundle {quantity, price} for multi-buys ('2 for $5.00'), starting_price for "
    "'Starts at' items, regular_price the crossed-out price."
)
_PUBLIX_ITEM = (
    "item_code (for product()), base_product_id, title, brand, size, description, image, url, "
    "category_path, aisle (where it sits in that store), on_sale, price, price_unit, bundle, "
    "starting_price, regular_price, price_text, regular_price_text, promo (type single, bogo or "
    "multi; message, conditions, savings, valid_from, valid_through), has_coupon and "
    "is_order_ahead"
)
_PUBLIX_GRID_FIELDS = (
    " Items with " + _PUBLIX_ITEM + ". Also store (id, name), total, page, page_size (48), "
    "total_pages, count, sort, applied_filters and facets (deals, BOGO, weekly ad, brand, type, "
    "diet, nutrition ranges)."
)
_PUBLIX_CHARGE = (
    " Failed upstream calls are not charged (they are retried automatically); a not-found is "
    "charged."
)


# IKEA params shared across endpoints (50 ikea.com markets, ikea.cn, the IKEA Islas sites
# pr / do / es_islands and IKEA Iceland). Each endpoint serves its own market list.
_IKEA_MAIN_MARKETS = (
    "us ca gb ie de at ch fr be nl dk se no fi ee lv lt pl cz sk hu hr si rs ro pt es it il ae "
    "sa kw qa bh om jo eg ma in my sg ph th jp kr au nz mx cl co"
)
_IKEA_ALL_SCOPE = (
    "55 markets: the 50 ikea.com markets (" + _IKEA_MAIN_MARKETS + "), cn (ikea.cn), pr "
    "(Puerto Rico), do (Dominican Republic), es_islands (Canary and Balearic islands, with "
    "island) and is (Iceland)"
)
_IKEA_MAIN_SCOPE = "the 50 ikea.com markets (not cn, pr, do, es_islands or is)"
_IKEA_MAIN_CN_SCOPE = "the 50 ikea.com markets and cn (not pr, do, es_islands or is)"
_IKEA_ASIS_SCOPE = "us, gb, de, fr, se, jp, nl, es, it, pl, au, ch and at"


def _ikea_country(scope: str) -> Param:
    return _str("country", "IKEA market code, lowercase (default 'us'). Served: " + scope + ".")


_IKEA_LANGUAGE = _str(
    "language",
    "The answer's language (default: the market's first), e.g. ca en/fr, be nl/fr/en, ch "
    "de/fr/it/en, us en/es, es es/en/ca/eu/gl, jp ja/en, cn zh/en. A language the market does "
    "not serve answers 400.",
)
_IKEA_ISLAND = _lit(
    "island",
    (
        "tenerife",
        "grancanaria",
        "lanzarote",
        "fuerteventura",
        "lapalma",
        "lagomera",
        "elhierro",
        "mallorca",
        "menorca",
        "ibiza",
    ),
    "Required with country 'es_islands' (the Canary and Balearic islands storefronts): which "
    "island.",
)
_IKEA_ITEM_NO_DOC = (
    "An IKEA article number: 8 digits, dots allowed, e.g. '80275887' or '802.758.87'. Pass a "
    "str to keep leading zeros ('00263850')."
)
_IKEA_STORE_DOC = "An IKEA store id: stores[].store_id of stores(), e.g. '399' (Burbank, CA)."
_IKEA_STORE = Param("store_id", "Union[str, int]", required=True, doc=_IKEA_STORE_DOC)
_IKEA_ITEM_NOS = Param(
    "item_nos",
    "Union[str, list[str]]",
    required=True,
    doc="1 to 100 IKEA article numbers: a list or a comma-separated string, e.g. "
    "['80275887', '00263850'].",
)
_IKEA_GRID_PARAMS = (
    _int("page", "Results page, 1-based."),
    _int("page_size", "Products per page (default 24, up to 100)."),
    _lit(
        "sort",
        ("relevance", "price_asc", "price_desc", "newest", "rating", "name_asc", "most_popular"),
        "relevance (default), price_asc, price_desc, newest, rating, name_asc or most_popular.",
    ),
    _str_or_list("color", "Color id(s) from facets (parameter f-colors), e.g. '10156' = white."),
    _str(
        "price_bucket",
        "A price range id from facets (parameter f-price-buckets), e.g. 'PRICE_0_5000' = 0 to "
        "49.99.",
    ),
    _bool("new_only", "Only new products."),
    _bool("last_chance", "Only last-chance (being discontinued) products."),
    _bool("family_price", "Only products with an IKEA Family member price."),
    _bool("top_seller", "Only best sellers."),
    _str_or_int(
        "store_id",
        "A store id (stores()): adds each product's availability at that store (stock level, "
        "home delivery) and enables availability.",
    ),
    _lit(
        "availability",
        ("in_store", "click_collect", "online"),
        "With store_id: in_store (in stock at the store), click_collect or online.",
    ),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any other facet, keyed by facets[].parameter, e.g. {'f-materials': ['47350']}; "
        "boolean facets take True.",
    ),
)
_IKEA_LANG_NOTE = (
    " Data comes in the market's language and prices are numbers in the market's own currency "
    "(never converted); every answer echoes country, language and currency."
)
_IKEA_ITEM = (
    "item_no, item_no_global, is_combination, name, type_name, design, measure_text, url, "
    "image, images, price, previous_price, discount_amount, discount_percent, price_tag "
    "(family_price: price is the IKEA Family member price and previous_price the regular one; "
    "new_lower_price, time_restricted_offer (a limited-time reduced price, with previous_price "
    "and valid dates), lower_price_in_store, new_product, discontinued or none), price_tag_text, "
    "lowest_price, price_valid_from, price_valid_to, rating, rating_count (per market as shown; "
    "many markets share one pool, some show none), badge, colors, variant_count, variants, "
    "last_chance, online_sellable, "
    "category_path and availability (with store_id)"
)
_IKEA_GRID_FIELDS = (
    " Items with " + _IKEA_ITEM + ". Also total, page, page_size, total_pages, count, sort, "
    "applied_filters and facets (name, parameter, type, values with id, label and count; the "
    "parameter is the key filters takes)."
)
_IKEA_CHARGE = (
    " Failed upstream calls are not charged (they are retried automatically); a not-found is "
    "charged."
)


# Wayfair params shared across endpoints (wayfair.com, wayfair.ca en/fr, wayfair.co.uk,
# wayfair.ie; the US banner sites AllModern, Birch Lane, Joss & Main and Perigold via site).
_WAYFAIR_COUNTRY = _lit(
    "country",
    ("us", "ca", "gb", "ie"),
    "Wayfair market (default 'us'): us (wayfair.com, USD), ca (wayfair.ca, CAD), gb "
    "(wayfair.co.uk, GBP), ie (wayfair.ie, EUR). Wayfair no longer sells in Germany or "
    "Austria.",
)
_WAYFAIR_LANGUAGE = _lit(
    "language",
    ("en", "fr"),
    "ca only: 'en' (default) or 'fr' (wayfair.ca in French: French names, labels and dates). "
    "Every other market is English.",
)
_WAYFAIR_SITE = _lit(
    "site",
    ("wayfair", "allmodern", "birchlane", "jossandmain", "perigold"),
    "Wayfair's US banner sites (USD, country 'us' only): allmodern, birchlane, jossandmain or "
    "perigold. Default 'wayfair'.",
)
_WAYFAIR_GRID_PARAMS = (
    _int("page", "Results page, 1-based. A page past the last returns no items and a note."),
    _lit(
        "sort",
        ("recommended", "price_asc", "price_desc", "rating"),
        "recommended (default), price_asc, price_desc or rating (customer rating). Price sorts "
        "follow Wayfair's price per item: a set is ordered by its per_item_price.",
    ),
    _bool("on_sale", "Only products on sale."),
    _bool("closeout", "Only closeout products."),
    _bool("open_box", "Only products with an open-box offer (open_box_price)."),
    _bool("new_arrivals", "Only new arrivals."),
    _bool("in_stock", "Only products in stock."),
    Param(
        "brand",
        "Optional[Union[int, str, list[Union[int, str]]]]",
        doc="1 to 5 brand ids, not names: items[].brand.id or a Brand facet option id, e.g. "
        "44308 (Ebern Designs).",
    ),
    _ilit(
        "min_rating",
        (1, 3, 4, 5),
        "Customer rating: 5 = five stars only, 4 / 3 = that many stars and up, 1 = every "
        "reviewed product.",
    ),
    _float("price_min", "Lowest price, in the market's currency."),
    _float("price_max", "Highest price, in the market's currency."),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any facet of the answer, keyed by facets[].id with facets[].options[].id values, "
        "e.g. {'2471': ['274623']}; ranges as 'min~max'.",
    ),
)
_WAYFAIR_PRICES = (
    " Prices are numbers in the market's currency (never converted). price is what Wayfair "
    "charges now (sale_price when on sale, with price_label such as Sale, Closeout or Solde); "
    "was_price is Wayfair's strikethrough price, which Wayfair's terms define as the "
    "manufacturer's suggested price or the highest price Wayfair offered or sold the item at in "
    "the past; Wayfair's Sale label means a discount against a price in the previous 90 days. "
    "No price history: Wayfair shows none, so poll price, sale_price, was_price and badge to "
    "build one."
)
_WAYFAIR_ITEM = (
    "position, sku, variant_id, name, brand (id, name), url, image, price, sale_price, "
    "was_price, price_label, discount_percent, per_item_price (sets), loyalty_savings, prices "
    "(every price line), badge (e.g. Early Black Friday, Sale), rating, review_count, "
    "stock_status, stock_text, open_box_price, option_counts, selected_options, category and "
    "sponsored"
)
_WAYFAIR_GRID_FIELDS = (
    " Items with " + _WAYFAIR_ITEM + ". Also count, total (approximate: Wayfair's own count, "
    "total_is_approximate), page, page_size, total_pages, sort, sorts_offered, "
    "requested_filters, applied_filters, unapplied_filters and facets (id, name, type, options "
    "with id and label; the ids are what filters takes; no per-option counts)."
)
_WAYFAIR_NOTE = (
    " Markets: us, ca (language en or fr), gb, ie; every answer echoes country, language, site "
    "and currency. Failed upstream calls are not charged; a not-found is charged."
)


# Ashley Furniture params shared across endpoints (ashleyfurniture.com; Ashley's licensed
# storefronts ca, mx, ph, sa, tr for search + product only). category, deals, stores and
# store are us only, so they take no country.
_ASHLEY_COUNTRY = _lit(
    "country",
    ("us", "ca", "mx", "ph", "sa", "tr"),
    "Ashley market (default 'us'): us (ashleyfurniture.com, USD), ca (ashleyhomestore.ca, "
    "CAD), mx (store.ashleyfurniture.com.mx, MXN, Spanish), ph (store.ashleyfurniture.ph, PHP), "
    "sa (store.ashley.sa, SAR, English), tr (ashleyturkiye.com, TRY, Turkish).",
)
_ASHLEY_SORTS = ("best_sellers", "price_asc", "price_desc", "newest", "rating", "name")
_ASHLEY_GRID_PARAMS = (
    _int(
        "page",
        "Grid page, 1-based (30 products per page). A page past the last returns no items and "
        "a note.",
    ),
    _lit(
        "sort",
        _ASHLEY_SORTS,
        "best_sellers (default), price_asc, price_desc, newest, rating (customer rating) or "
        "name (A to Z).",
    ),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Facet refinements keyed by facets[].id with options[].value values (a str or a "
        "list of str), e.g. {'facetUpholsteryDesign': 'Chaise'}. At most 6 facets.",
    ),
    _float(
        "price_min",
        "Lowest price (USD), applied to Ashley's own price list, so an item priced for another "
        "region can sit just outside the range.",
    ),
    _float("price_max", "Highest price (USD)."),
)
_ASHLEY_PRICES = (
    " Prices are numbers in the market's currency, never converted. price is what Ashley "
    "charges now; regular_price is Ashley's own 'Regular Price' (the struck-through price; "
    "Ashley's terms define it as its highest advertised price in store and online, offered to "
    "customers using special long-term financing), set only when it is at or above price; "
    "discount_percent is computed from the two."
)
_ASHLEY_REGION = (
    " Ashley prices vary by region (price zone) and there is no ZIP input: every us answer "
    "returns priced_for (zipcode, price_zone), the ZIP and price zone Ashley priced that "
    "answer for. Two calls can land in different price zones, so prices can differ between "
    "calls and consecutive pages can overlap slightly."
)
_ASHLEY_BADGES = (
    "badges (sale, clearance, doorbuster, outlet, hot_buy, online_only, ashley_exclusive, "
    "luxe, daily_deal)"
)
_ASHLEY_GRID_FIELDS = (
    " 30 products per page: items with position, sku, name, brand, upc, category, url, image, "
    "price, regular_price, discount_percent, color, flag, " + _ASHLEY_BADGES + ", promotion, "
    "rating, review_count, swatch_count, stock_text and delivery_method (home_delivery or "
    "direct_ship). Also priced_for, count, total, page, page_size, total_pages, sort, "
    "requested_filters and facets (id, name, options with value, label and count)."
)
_ASHLEY_MARKETS_NOTE = (
    " Markets: us, plus Ashley's licensed storefronts ca, mx, ph, sa and tr (search and "
    "product only); every answer carries country, language, currency and source_domain. "
    "Failed upstream calls are not charged; a not-found is charged."
)
_ASHLEY_US_NOTE = (
    " us only (ashleyfurniture.com). Failed upstream calls are not charged; a not-found is "
    "charged."
)
_ASHLEY_CREDITS_NOTE = "Costs 2 credits on us (the default) and mx, 1 credit on ca, ph, sa and tr."


# Maisons du Monde params shared across endpoints (maisonsdumonde.com: fr, be fr / nl, lu,
# nl, de, es, it, pt, ch fr / de / it). stores, store and availability serve fr, be, de, es,
# it, pt and ch (no store finder on nl or lu); seller and the seller / sold_by filters serve
# the marketplace markets fr, de, es and it.
_MDM_COUNTRIES = ("fr", "be", "lu", "nl", "de", "es", "it", "pt", "ch")
_MDM_STORE_COUNTRIES = ("fr", "be", "de", "es", "it", "pt", "ch")
_MDM_MARKETPLACE_COUNTRIES = ("fr", "de", "es", "it")


def _mdm_country(choices: Sequence[str], scope: str) -> Param:
    return _lit("country", choices, "Maisons du Monde market (default 'fr'). " + scope)


_MDM_ALL_SCOPE = (
    "All 9 markets: fr (EUR, French), be (EUR, fr or nl), lu (EUR, fr), nl (EUR, nl), de (EUR, "
    "de), es (EUR, es), it (EUR, it), pt (EUR, pt), ch (CHF, fr, de or it)."
)
_MDM_STORE_SCOPE = "fr, be, de, es, it, pt or ch (the store finder answers no stores on nl and lu)."
_MDM_MARKETPLACE_SCOPE = "fr, de, es or it (marketplace sellers exist there only)."
_MDM_LANGUAGE = _lit(
    "language",
    ("fr", "nl", "de", "es", "it", "pt"),
    "Language of the market's site (default its first): be fr or nl, ch fr, de or it; every "
    "other market has one language (fr and lu fr, nl nl, de de, es es, it it, pt pt). A "
    "language the market does not serve answers 400.",
)
_MDM_SORTS = ("relevance", "price_asc", "price_desc", "rating")
_MDM_PAGE = _int(
    "page",
    "Results page, 1-based, 40 items per page (at most 250 pages; a page past the last returns "
    "no items and a note).",
)
_MDM_SORT = _lit(
    "sort",
    _MDM_SORTS,
    "relevance (default), price_asc, price_desc or rating (customer rating). The site has no "
    "newest, best-seller or discount sort.",
)
_MDM_GRID_PARAMS = (
    _MDM_PAGE,
    _MDM_SORT,
    _float("price_min", "Lowest price, in the market's currency."),
    _float("price_max", "Highest price, in the market's currency."),
    _bool("on_sale", "Only discounted items."),
    _ilit("min_discount", (20, 30, 40, 50), "Only items at least this many percent off."),
    _bool("in_stock", "Only items in stock online."),
    _ilit(
        "min_rating",
        (3, 4, 5),
        "Customer rating: 5 = five stars only, 4 / 3 = that many stars and up.",
    ),
    _str_or_list("color", "1 to 5 color option ids (facet c of the answer's facets)."),
    _str_or_list("material", "1 to 5 material option ids (facet f)."),
    _str_or_list("style", "1 to 5 style option ids (facet st)."),
    _str_or_list("brand", "1 to 5 brand option ids (facet bra), e.g. 'BRAND_MAISONS_DU_MONDE'."),
    _str(
        "seller",
        "One marketplace seller's items: seller.code from seller() or a Seller facet (se) option "
        "id, e.g. 'BESTMOBILIER'. fr, de, es and it only.",
    ),
    _lit(
        "sold_by",
        ("mdm",),
        "mdm: only items sold by Maisons du Monde itself (not marketplace sellers). fr, de, es "
        "and it only (elsewhere every item is).",
    ),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="Any other facet, keyed by facets[].id with facets[].options[].id values (a str or a "
        "list of str), e.g. {'nbs': ['CAPACITY_2_places']}; dimension ranges (dd, dh, dw) as "
        "'min-max' in cm.",
    ),
)
_MDM_PRICES = (
    " Prices are numbers in the market's currency, never converted. Prices can differ by "
    "market: measured on 2026-11-14 on about 170 discounted sofas, lu, nl, de, es, it and pt "
    "matched fr on every item, be differed on 19, and ch is priced separately in CHF; read each "
    "market you report. price is what the site charges now; was_price is the crossed-out price "
    "shown next to a discount; discount_percent is the page's own percent off; "
    "eco_participation is the French furniture recycling fee included in the price (fr only). "
    "Maisons du Monde shows no 30-day lowest price and no price history: poll for changes."
)
_MDM_GRID_FIELDS = (
    " 40 items per page with position, id (digits for Maisons du Monde items, M + digits for "
    "marketplace items), name, collection, brand, url, image, price, was_price, "
    "discount_percent, currency, eco_participation (fr), badges, rating, review_count, "
    "color_count, sold_by (mdm or marketplace), offer_id, sponsored (sponsored marketplace "
    "tiles, not counted in count), condition, store_only and purchase_status. Also count, "
    "sponsored_count, total (exact), page, page_size, total_pages, sort, sorts_offered, "
    "requested_filters, applied_filters and facets (id, name, type, options with id, label and "
    "count, or a min / max range; the ids are what color, material, style, brand, seller and "
    "filters take)."
)
_MDM_NOTE = (
    " Every answer carries country, language and currency. Failed upstream calls are not "
    "charged; a not-found is charged."
)


def _carrefour_ean(doc: str = "") -> Param:
    return _req(
        "ean",
        "The product barcode (EAN / GTIN): items[].ean of a search, e.g. '3017620422003'." + doc,
    )


# Allegro params shared across endpoints (allegro.pl + allegro.cz / .sk / .hu on every endpoint).
_ALLEGRO_MARKETS = (
    "pl (allegro.pl, PLN, Polish, default), cz (allegro.cz, CZK, Czech), sk (allegro.sk, EUR, "
    "Slovak) or hu (allegro.hu, HUF, Hungarian)"
)
_ALLEGRO_COUNTRY = _lit(
    "country",
    ("pl", "cz", "sk", "hu"),
    "The Allegro site: " + _ALLEGRO_MARKETS + ". Defaults to pl. Titles and labels come in the "
    "site's language, prices in its currency.",
)
_ALLEGRO_PAGE = _int(
    "page",
    "Results page, 1-based (up to 100). 60 organic offers per page; sponsored slots come on top.",
)
_ALLEGRO_SORT = _lit(
    "sort",
    (
        "relevance",
        "price_low_to_high",
        "price_high_to_low",
        "price_with_delivery_low_to_high",
        "price_with_delivery_high_to_low",
        "popularity",
        "ending_soonest",
        "newest",
    ),
    "relevance (default), price_low_to_high, price_high_to_low, price_with_delivery_low_to_high, "
    "price_with_delivery_high_to_low, popularity, ending_soonest (auctions first to end) or "
    "newest. Sponsored slots are not sorted; where the site shows promoted offers as their own "
    "block, each block is in sort order.",
)
_ALLEGRO_PRICE_CONDITION = (
    _float("min_price", "Lowest price, in the site's currency."),
    _float("max_price", "Highest price, in the site's currency."),
    _lit("condition", ("new", "used"), "new or used."),
    _bool("smart", "Only offers with Allegro Smart! (free delivery and returns for members)."),
)
_ALLEGRO_FILTERS = (
    *_ALLEGRO_PRICE_CONDITION,
    _lit("buying_format", ("buy_now", "auction"), "pl only: buy_now (fixed price) or auction."),
    _bool(
        "deals",
        "pl only: only offers in Allegro's deals and promotions zone (seasonal campaign deals "
        "such as Black Weeks included while they run).",
    ),
)
_ALLEGRO_PRODUCT_TARGET = (
    _str(
        "product_id",
        "A catalogue product id (a uuid): items[].product_id of a search or product_id of an "
        "offer, e.g. '90d08230-e02a-4210-913d-d417453321b8'. Alternative to url.",
    ),
    _str(
        "url",
        "A product link (allegro.pl/produkt/..., any of the four sites). Alternative to "
        "product_id.",
    ),
    _ALLEGRO_COUNTRY,
)
_ALLEGRO_LOGIN = _req(
    "login",
    "A seller login: items[].seller.login of a search or seller.login of an offer, e.g. "
    "'Yupilo_pl'.",
)
_ALLEGRO_GRID_FIELDS = (
    " Items with offer_id (for offer()), product_id (for product() and product_offers()), title, "
    "url, image, price and currency, buy_now_price (auctions), price_with_delivery (when the page "
    "shows it), free_delivery, delivery_text, condition, is_auction with auction_ends_in, "
    "discount_percent and lowest_price_30d, seller (id, login, super_seller, "
    "positive_feedback_percent, is_business), rating and rating_count, sold_count ('x people "
    "bought recently' as a number; None on auctions) with sold_label, smart (Allegro Smart!), "
    "offers_count, stock, placement (regular, promoted, sponsored or featured) with "
    "is_sponsored, and source (allegro, or allegro_lokalnie for Allegro Lokalnie offers inside "
    "pl results). Also total (exact), total_pages (at most 100), page, page_size (60), sort, "
    "applied_filters, facets (every filter with its values and offer counts), country, language "
    "and currency."
)
_ALLEGRO_OMNIBUS = (
    " lowest_price_30d is the EU price disclosure Allegro shows next to a discount: the lowest "
    "price in the 30 days before the discount. It is None without a discount and is not a price "
    "history."
)
_ALLEGRO_NOTE = (
    " Titles, parameters and labels come back in the site's language (Polish on pl). Markets: "
    + _ALLEGRO_MARKETS
    + ". sk and hu calls can take up to about a minute. Failed upstream calls are not charged "
    "(they are retried automatically); a not-found is charged."
)


# OLX params shared across endpoints (OLX Europe: olx.pl + olx.ro, olx.pt, olx.bg, olx.ua,
# olx.kz, olx.uz; filters and similar are pl, ro, pt, bg and ua only).
_OLX_MARKETS = (
    "pl (olx.pl, PLN, Polish, default), ro (olx.ro, RON, Romanian), pt (olx.pt, EUR, "
    "Portuguese), bg (olx.bg, EUR, Bulgarian), ua (olx.ua, UAH, Ukrainian), kz (olx.kz, KZT, "
    "Russian or Kazakh) or uz (olx.uz, UZS, Russian or Uzbek)"
)
_OLX_MARKETS_NO_KZ_UZ = (
    "pl (olx.pl, PLN, Polish, default), ro (olx.ro, RON, Romanian), pt (olx.pt, EUR, "
    "Portuguese), bg (olx.bg, EUR, Bulgarian) or ua (olx.ua, UAH, Ukrainian); not kz or uz"
)
_OLX_COUNTRY = _lit(
    "country",
    ("pl", "ro", "pt", "bg", "ua", "kz", "uz"),
    "The OLX site: " + _OLX_MARKETS + ". Defaults to pl. Titles and labels come in the site's "
    "language, prices in its currency.",
)
_OLX_COUNTRY_NO_KZ_UZ = _lit(
    "country",
    ("pl", "ro", "pt", "bg", "ua"),
    "The OLX site: " + _OLX_MARKETS_NO_KZ_UZ + ". Defaults to pl.",
)
_OLX_LANGUAGE = _lit(
    "language",
    ("ru", "kk", "uz"),
    "kz and uz only: kk (Kazakh) on kz or uz (Uzbek) on uz; both sites default to ru "
    "(Russian). Refused on the other sites, which answer in their own language.",
)
_OLX_USER_ID = Param(
    "user_id",
    "Union[str, int]",
    required=True,
    doc="An OLX seller id: items[].seller.id of a search or seller.id of an offer, e.g. "
    "'2547532895'.",
)
_OLX_OFFER_TARGET = (
    _str_or_int(
        "offer_id",
        "An OLX ad id: items[].id of a search, e.g. '1107557408'. Alternative to url.",
    ),
    _str("url", "An OLX ad link on any of the seven sites. Alternative to offer_id."),
)
_OLX_GRID_PARAMS = (
    _int(
        "page",
        "Results page, 1-based. OLX serves the first 1000 results of a search only, so page x "
        "page_size may not exceed 1000.",
    ),
    _int(
        "page_size",
        "Ads per page, up to 50 (default 40). Promoted ads come on top of these (40 asks return "
        "about 52 items).",
    ),
    _lit(
        "sort",
        ("relevance", "newest", "price_low_to_high", "price_high_to_low"),
        "relevance (default), newest (most recently posted or refreshed first: sellers can "
        "refresh an ad to the top), price_low_to_high or price_high_to_low. Promoted ads are "
        "not sorted.",
    ),
    _float("min_price", "Lowest price, in the site's currency."),
    _float("max_price", "Highest price, in the site's currency."),
    _lit(
        "condition",
        ("new", "used", "refurbished", "damaged"),
        "new, used, refurbished or damaged (in categories that have a condition).",
    ),
    _lit("seller_type", ("private", "business"), "private (individuals) or business."),
    _bool("olx_delivery", "Only ads that can be bought with OLX delivery. Not on kz or uz."),
    _bool("with_photos", "Only ads with photos."),
    _str_or_int(
        "region_id",
        "Only ads in this region: region_id of locations() or of an item's location.",
    ),
    _str_or_int(
        "city_id",
        "Only ads in this city: city_id of locations() or of an item's location, e.g. '17871'.",
    ),
    _str_or_int("district_id", "Only ads in this district of a city: district_id of locations()."),
    _ilit(
        "distance_km",
        (0, 2, 5, 10, 15, 30, 50, 75, 100),
        "With city_id: include ads within this many km of the city.",
    ),
    Param(
        "filters",
        "Optional[dict[str, Any]]",
        doc="The category's own filters, as listed by filters() (send_as keys): a range filter "
        "as filter_float_<name>:from / :to with a number, e.g. {'filter_float_year:from': 2018, "
        "'filter_float_milage:to': 100000}; a choice filter as filter_enum_<name> with one "
        "value or a list, e.g. {'filter_enum_rooms': ['two', 'three']}. Up to 20 keys; other "
        "keys are refused.",
    ),
    _bool(
        "include_promoted",
        "Keep the promoted ads the site places on each page (default True; each is flagged "
        "is_promoted with its slot).",
    ),
)
_OLX_SCOPE = (
    " OLX Europe only (olx.pl, olx.ro, olx.pt, olx.bg, olx.ua, olx.kz, olx.uz); OLX Brasil, "
    "olx.in and other OLX-branded sites are not covered."
)
_OLX_PRICE = (
    "price (value, currency, negotiable, type price / free / exchange / budget, label as "
    "shown, previous_value when the seller lowered it; when the site converts a price, e.g. "
    "olx.uz y.e. to UZS, value is the converted figure and original_value with "
    "original_currency keep what the seller entered)"
)
_OLX_ITEM = (
    "id, url, title, description_snippet, " + _OLX_PRICE + ", salary (jobs: from, to, period, "
    "currency, gross), condition, params (key, name, value, normalized_value), category_id, "
    "location (city, district, region with their ids), created_at, refreshed_at, valid_to, "
    "status, is_promoted with promoted_position (the slot on the page), is_highlighted, "
    "is_business, olx_delivery, photos and seller (id; business_name for business sellers only)"
)
_OLX_GRID_FIELDS = (
    " Items with " + _OLX_ITEM + ". Also total (the site's count; None on kz and uz once a "
    "search reaches 1000 ads), total_capped (True when there are more ads than the 1000 OLX "
    "lets anyone page through), total_pages, page, page_size, has_next_page, count, "
    "promoted_count, sort, applied_filters, country, language and currency."
)
_OLX_PRIVACY = (
    " A seller name is returned only for business sellers (business_name); private sellers come "
    "as an id only. No phone numbers, emails, last-seen times, profile photos or map positions "
    "are returned, and phone numbers and emails in ad text are replaced with [phone removed] / "
    "[email removed]."
)
_OLX_LANG_NOTE = (
    " Titles, parameters and labels come back in the site's language as the site writes them "
    "(Polish on pl; Russian by default on kz and uz)."
)
_OLX_CHARGE = (
    " Failed upstream calls are not charged (they are retried automatically); a not-found is "
    "charged."
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
                "page Google localizes the local pack only and ranks organic results nationally; "
                "set web_only=True for organic results ranked for this location.",
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
                "Return Google's Web results only: organic results ranked for location (local rank "
                "tracking), with no local pack, ads, related questions, knowledge graph or AI "
                "Overview. Call again without it for local_results.",
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
        credits=2,
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
        credits=2,
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
        credits=2,
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
        credits=2,
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
    # ================================= HEB ================================
    # 3 endpoints, 2 credits each. Texas-based grocery chain. Product detail
    # requires product_url or slug + product_id (HEB URLs need the slug), or
    # product_id alone with store_id. store_id (store_number from stores())
    # targets one store's prices, stock, aisle and assortment; echoed in
    # data.store. US only.
    Endpoint(
        key="heb_search",
        namespace="heb",
        method="search",
        http="POST",
        path="/api/v1/heb/search",
        summary=(
            "Search HEB grocery products by keyword: price (cents), sale status, unit price, "
            "size, UPC, stock, EBT/SNAP eligibility, aisle location and product URL. Pass "
            "store_id for one store's prices, stock and assortment."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100)."),
            _int("page_size", "Results per page (1-60; server default 60)."),
            _str_or_int(
                "store_id",
                "HEB store number from heb.stores() (field store_number), e.g. '441'. Prices, "
                "stock, aisle location and assortment come from that store, echoed in "
                "data.store. US only. Omit for HEB's default store.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="heb_product",
        namespace="heb",
        method="product",
        http="POST",
        path="/api/v1/heb/product",
        summary=(
            "Full HEB product detail: nutrition facts, ingredients, description, images, "
            "similar products, coupons, EBT/SNAP eligibility and breadcrumbs. Pass product_url "
            "(from search()) or slug + product_id, or product_id alone with store_id."
        ),
        params=(
            _str(
                "product_url",
                "Full or relative product URL from heb.com (e.g. "
                "'/product-detail/central-market-organics-whole-milk-1-gal/931316'). Preferred.",
            ),
            _str(
                "product_id",
                "HEB product id (numeric id at the end of a product URL). Requires slug, "
                "unless store_id is set.",
            ),
            _str(
                "slug",
                "Product slug (readable part of the URL). Required with product_id, unless "
                "store_id is set.",
            ),
            _str_or_int(
                "store_id",
                "HEB store number from heb.stores() (field store_number), e.g. '441'. Price, "
                "stock and aisle location come from that store, echoed in data.store. US only. "
                "Omit for HEB's default store.",
            ),
        ),
        one_of=(("product_url", "product_id"),),
        credits=2,
    ),
    Endpoint(
        key="heb_stores",
        namespace="heb",
        method="stores",
        http="POST",
        path="/api/v1/heb/stores",
        summary=(
            "HEB stores near a US ZIP code or city: store number, address, phone, hours, "
            "pharmacy availability, fulfillment channels, distance and store URL."
        ),
        params=(
            _str("zip", "5-digit US ZIP code (e.g. '78701')."),
            _str("city", "City name (e.g. 'Austin'). Pass zip or city."),
        ),
        one_of=(("zip", "city"),),
        credits=2,
    ),
    # ================================ Kroger ===============================
    # 8 endpoints on /api/v1/kroger: kroger.com plus the QFC (qfc.com) and Fred
    # Meyer (fredmeyer.com) banners via `banner` on every endpoint. search and
    # product 2 credits, prices 3, the rest 1. Prices are integer cents.
    # search / product / category / deals price at a store the site chooses
    # (returned in `store`); prices() takes the store you pick. search,
    # category and deals serve page 1 only (page > 1 is an unbilled 400), no
    # sort. Cross-field rules the server enforces beyond one_of ("at least
    # one"): stores takes exactly one of zip, query or store_id; category and
    # coupons reject both alternatives together. 120 s timeout floor: search
    # and prices can take up to about a minute.
    Endpoint(
        key="kroger_search",
        namespace="kroger",
        method="search",
        http="POST",
        path="/api/v1/kroger/search",
        summary=(
            "Search Kroger, QFC or Fred Meyer products by keyword (banner): price, list and "
            "promo price with end date, n-for deals, unit price, size, UPC, stock (in_stock "
            "null without a stock record), SNAP eligibility, dietary info, category and rating "
            "(average, count, star distribution; no review text), plus total and the store "
            "that priced the results (a store the site chooses; use prices() for a specific "
            "store). Prices are integer cents. Only the first page (up to 24 products), no sort."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _KROGER_BANNER,
            _int(
                "page",
                "Results page. Only page 1 is available (up to 24 products); page above 1 is "
                "refused with a 400 before any charge.",
            ),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_product",
        namespace="kroger",
        method="product",
        http="POST",
        path="/api/v1/kroger/product",
        summary=(
            "One Kroger, QFC or Fred Meyer product by URL or UPC: the search fields plus "
            "description, nutrition facts, ingredients, allergens, images, country of origin, "
            "dimensions, weight, dietary flags, the aisle at the store (store_location), "
            "breadcrumbs, banner and store (a store the site chooses). Prices are integer "
            "cents. An unknown UPC is a charged 404."
        ),
        params=(
            _str(
                "product_url",
                "Full or relative product URL on kroger.com, qfc.com or fredmeyer.com "
                "(products[].url of search()). An absolute URL sets the banner; a banner that "
                "contradicts its host is a 400.",
            ),
            _str(
                "upc",
                "The product's UPC (products[].upc of search(), or the digits at the end of a "
                "product URL: /p/{slug}/{upc}), e.g. '0001111050438'.",
            ),
            _str("slug", "Product slug (the readable part of the product URL). Optional with upc."),
            _KROGER_BANNER,
        ),
        one_of=(("product_url", "upc"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_prices",
        namespace="kroger",
        method="prices",
        http="POST",
        path="/api/v1/kroger/prices",
        summary=(
            "Price, promotion, stock and aisle for 1 to 25 UPCs at one Kroger, QFC or Fred "
            "Meyer store you choose (store_id from stores()). Per UPC: price, promo_price, "
            "promo_ends_at, on_sale, price_display, unit_price_display, in_stock, stock_level, "
            "quantity (the site's available estimate, not a shelf count), aisle (description, "
            "number, side, bay, shelf), fulfillment and priced_at. Unknown UPCs are listed in "
            "not_found. Prices are integer cents. An unknown store_id is a charged 404."
        ),
        params=(
            _req("store_id", "A store's 8-digit location_id: stores[].location_id of stores(), e.g. '70500847'."),
            _str_list(
                "upcs",
                "1 to 25 13-digit UPCs as the site writes them (products[].upc of search() or "
                "category()), e.g. ['0001111050438'].",
                required=True,
            ),
            _KROGER_STORE_BANNER,
        ),
        credits=3,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_stores",
        namespace="kroger",
        method="stores",
        http="POST",
        path="/api/v1/kroger/stores",
        summary=(
            "Kroger, QFC or Fred Meyer stores near a ZIP or a city / address (nearest first), "
            "or one store by store_id; pass exactly one. Each store: location_id (the store_id "
            "for prices(), coupons() and suggestions()), banner, type (store or fuel_center), "
            "name, store_number, address, coordinates, phone, timezone, hours, open_24_hours, "
            "departments, has_pharmacy, has_fuel_center, pickup, delivery and distance_miles. "
            "No fuel prices. An unknown store_id is a charged 404."
        ),
        params=(
            _str("zip", "A 5-digit US ZIP code, e.g. '98101'."),
            _str("query", "A city or address, as typed in the site's store finder, e.g. 'Portland, OR'."),
            _str("store_id", "One store's 8-digit location_id, e.g. '70100011'."),
            _KROGER_STORE_BANNER,
            _int("limit", "Stores to return, 1-50. Defaults to 10."),
            _bool(
                "include_other_banners",
                "Also return nearby stores of other Kroger banners (for example Fred Meyer stores "
                "near a QFC search). Defaults to False.",
            ),
        ),
        one_of=(("zip", "query", "store_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_category",
        namespace="kroger",
        method="category",
        http="POST",
        path="/api/v1/kroger/category",
        summary=(
            "A Kroger, QFC or Fred Meyer category listing by /pl/ URL or taxonomy_id (not both): "
            "category (id, name, url) and the search fields (total, count, products, the store "
            "the site chose). Prices are integer cents. Only the first page (up to 24 "
            "products), no sort."
        ),
        params=(
            _str(
                "url",
                "A category listing URL (/pl/<name>/<id>) on kroger.com, qfc.com or "
                "fredmeyer.com. The URL's host sets the banner.",
            ),
            _str(
                "taxonomy_id",
                "The digits at the end of a /pl/ URL, e.g. '08190'. Category ids are shared "
                "across banners.",
            ),
            _str(
                "slug",
                "The name part of a /pl/ URL, e.g. 'Import-Beer'. Optional with taxonomy_id; "
                "without it category.name is None.",
            ),
            _KROGER_BANNER,
            _int("page", "Results page. Only page 1 is available; page above 1 is an unbilled 400."),
        ),
        one_of=(("url", "taxonomy_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_deals",
        namespace="kroger",
        method="deals",
        http="POST",
        path="/api/v1/kroger/deals",
        summary=(
            "This week's weekly digital deals of Kroger, QFC or Fred Meyer: deals_week (id, "
            "ends_at) and the search fields. Store promotions carry promo_price and "
            "promo_ends_at; digital-coupon deals show the shelf price (the coupon is in "
            "coupons(), tag Weekly Digital Deals). Prices are integer cents. Only the first "
            "page (up to 24 products). The printed weekly ad circular is not available."
        ),
        params=(
            _KROGER_BANNER,
            _int("page", "Results page. Only page 1 is available; page above 1 is an unbilled 400."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_coupons",
        namespace="kroger",
        method="coupons",
        http="POST",
        path="/api/v1/kroger/coupons",
        summary=(
            "The digital coupons at one Kroger, QFC or Fred Meyer store (store_id, or the "
            "banner's store nearest a zip; not both), 24 per page, optionally one department "
            "(category) or a text match (query). Each coupon: id, brand, title, description, "
            "details, savings (type, amount in cents, percent), tags, valid_for, starts_at, "
            "clip_by, expires_at and image; plus total_at_store, has_more and categories. "
            "Listing only: coupons are not clipped."
        ),
        params=(
            _str("store_id", "A store's 8-digit location_id from stores(), e.g. '70500847'."),
            _str("zip", "A 5-digit ZIP: the banner's nearest store is used."),
            _KROGER_STORE_BANNER,
            _int("page", "Page of coupons, 24 per page, 1-50. Defaults to 1. Follow has_more."),
            _str("category", "Only coupons in one department: a name from the response's categories, e.g. 'Dairy'."),
            _str("query", "Only coupons whose brand or text matches, e.g. 'coffee'."),
        ),
        one_of=(("store_id", "zip"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kroger_suggestions",
        namespace="kroger",
        method="suggestions",
        http="POST",
        path="/api/v1/kroger/suggestions",
        summary=(
            "Kroger, QFC or Fred Meyer search box suggestions for a partial query: suggestions "
            "(text, type), count and the store they were asked for. Without store_id the "
            "banner's store nearest a representative ZIP is used (Kroger 45202, QFC 98101, "
            "Fred Meyer 97201)."
        ),
        params=(
            _req("query", "What a shopper has typed so far (2-100 characters), e.g. 'almond mi'."),
            _KROGER_STORE_BANNER,
            _str("store_id", "A store's 8-digit location_id from stores(). Optional."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # ================================ Publix ===============================
    # 11 endpoints on /api/v1/publix (publix.com, US), 1 credit each. Every price
    # endpoint takes the store_id you choose (a Publix store number from
    # stores()); categories and suggestions take it optionally. Publix shows
    # prices online only for promoted and order-ahead items: price is None
    # otherwise. Cross-field rules the server enforces beyond one_of: stores
    # needs zip, city with state, or store_id. 120 s timeout floor.
    Endpoint(
        key="publix_search",
        namespace="publix",
        method="search",
        http="POST",
        path="/api/v1/publix/search",
        summary=(
            "Search Publix products at one store by keyword: sort by name, popularity, savings "
            "or views; filter to items on sale, BOGO (Buy One Get One Free) or a brand. Keywords "
            "the site sends to a category answer that category's products; keywords it sends to "
            "an order-ahead page set redirected_to (items may be empty)."
            + _PUBLIX_GRID_FIELDS + _PUBLIX_PRICES + _PUBLIX_CHARGE
        ),
        params=(
            _req("query", "Search keywords (1-100 characters), e.g. 'chicken'."),
            _PUBLIX_STORE,
            *_PUBLIX_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_product",
        namespace="publix",
        method="product",
        http="POST",
        path="/api/v1/publix/product",
        summary=(
            "One Publix product by item code at one store: the product card (" + _PUBLIX_ITEM
            + "; order-ahead items also short_description, lead_time, serves, calories) and its "
            "nutrition facts (labels with serving size, servings per container and every "
            "nutrient with amount, unit and percent daily value; a deli sub has one label per "
            "component and size; None when Publix has none), plus store. Ingredients, "
            "allergens, UPC and reviews are not published by Publix online. An unknown item "
            "code is a charged 404." + _PUBLIX_PRICES + _PUBLIX_CHARGE
        ),
        params=(
            Param(
                "item_code",
                "Union[str, int]",
                required=True,
                doc="A Publix item code (not a UPC): items[].item_code of search(), category() "
                "or order_ahead(), e.g. '90355'.",
            ),
            _PUBLIX_STORE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_category",
        namespace="publix",
        method="category",
        http="POST",
        path="/api/v1/publix/category",
        summary=(
            "One Publix category's products at one store, by category_url or category_id, with "
            "the search sorts and filters. Also category (id, name, path)."
            + _PUBLIX_GRID_FIELDS + _PUBLIX_PRICES + _PUBLIX_CHARGE
        ),
        params=(
            _PUBLIX_STORE,
            _str(
                "category_url",
                "A publix.com category link (/c/<name>/<id>), e.g. "
                "'https://www.publix.com/c/chicken/6772da29-55bf-4051-83d5-104d73ae9a96'.",
            ),
            _str(
                "category_id",
                "A category id (categories[].id of categories()), e.g. "
                "'6772da29-55bf-4051-83d5-104d73ae9a96'. Alternative to category_url.",
            ),
            *_PUBLIX_GRID_PARAMS,
        ),
        one_of=(("category_url", "category_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_categories",
        namespace="publix",
        method="categories",
        http="POST",
        path="/api/v1/publix/categories",
        summary=(
            "The Publix product category tree: departments (Bakery, Dairy, Meat, Produce ...) "
            "with their categories and sub-categories, each with id (for category()), name, "
            "url, parent_id, level and children; plus count. parent_id returns one "
            "department's or category's subtree." + _PUBLIX_CHARGE
        ),
        params=(
            _PUBLIX_STORE_OPT,
            _str(
                "parent_id",
                "Return only this department's or category's subtree (categories[].id).",
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_weekly_ad",
        namespace="publix",
        method="weekly_ad",
        http="POST",
        path="/api/v1/publix/weekly-ad",
        summary=(
            "The store's current Publix weekly ad (English), about 700 items: BOGO deals (about "
            "230 a week), sale prices, multi-buys and percent-off deals, with ad (start_date, "
            "end_date), total, count, applied_filters and departments. Weekly ads start on "
            "different days by state (Thursday to Wednesday in Florida, Wednesday to Tuesday in "
            "Georgia and North Carolina; weekly_ad_break_day of stores() gives each store's "
            "start day), and prices of some items (beer, wine) differ by store. Each item: id, "
            "item_code, base_product_id, title, description, brand, department, categories, "
            "savings_text (as shown, e.g. 'Buy 1 Get 1 FREE', '$6.89 lb', '2 for $5.00'), "
            "deal_type (bogo, b2g1, multi, price, percent_off or other), price (only when "
            "savings_text is a plain price), price_unit, bundle, save_up_to, additional_savings, "
            "min_quantity, fine_print, stacked_with_coupon, promotion, valid_from, valid_to and "
            "image." + _PUBLIX_CHARGE
        ),
        params=(
            _PUBLIX_STORE,
            _str(
                "department",
                "Only items of this department (departments of the answer, e.g. 'Meat', "
                "'Produce', 'Deli', 'Wine').",
            ),
            _bool("bogo_only", "Only Buy 1 Get 1 Free and Buy 2 Get 1 Free items."),
            _str("query", "Only items whose title, description or brand contains this text."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_extra_savings",
        namespace="publix",
        method="extra_savings",
        http="POST",
        path="/api/v1/publix/extra-savings",
        summary=(
            "The store's Publix Extra Savings (temporary price reductions), several hundred "
            "items: id, base_product_id, title, size, brand, categories, savings_text (the "
            "amount saved as shown), savings, additional_savings, final_price (the reduced "
            "price, as the site lists it), min_quantity, image and url; plus store, count and "
            "period (start_date, end_date of the current Extra Savings period)." + _PUBLIX_CHARGE
        ),
        params=(_PUBLIX_STORE,),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_coupons",
        namespace="publix",
        method="coupons",
        http="POST",
        path="/api/v1/publix/coupons",
        summary=(
            "The store's Publix digital coupons as every visitor sees them (about 100-130): id, "
            "title, description, brand, savings_text, value (the dollar amount when the coupon "
            "states one), min_quantity, limit_per_transaction, categories, valid_from, "
            "valid_to, terms and image; plus store and count. Read-only: coupons are listed, "
            "never clipped, and no account is used." + _PUBLIX_CHARGE
        ),
        params=(_PUBLIX_STORE,),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_savings_search",
        namespace="publix",
        method="savings_search",
        http="POST",
        path="/api/v1/publix/savings-search",
        summary=(
            "Find a keyword across the store's Publix weekly ad, Extra Savings and digital "
            "coupons in one call: query, store, count and items, each with saving_type "
            "(weekly_ad, extra_savings or coupon) and that feed's fields." + _PUBLIX_CHARGE
        ),
        params=(
            _req("query", "A keyword to find in the store's savings, e.g. 'coffee'."),
            _PUBLIX_STORE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_order_ahead",
        namespace="publix",
        method="order_ahead",
        http="POST",
        path="/api/v1/publix/order-ahead",
        summary=(
            "The store's Publix deli and bakery order-ahead (in-store pickup) menu with this "
            "store's prices: Pub Subs (section subs, default) or the whole catalog of subs, "
            "platters, cakes, wings and meals (section all, about 1,150 items, 60 per page). "
            "Each item: " + _PUBLIX_ITEM + ", short_description, lead_time, serves, calories and "
            "pay_online. Pub Sub prices differ by store (e.g. $12.09 in Miami, $11.99 in "
            "Atlanta). Also section, store, total, page, page_size, total_pages and count."
            + _PUBLIX_CHARGE
        ),
        params=(
            _PUBLIX_STORE,
            _lit(
                "section",
                ("subs", "all"),
                "subs (default: the Pub Sub menu) or all (the whole deli and bakery order-ahead "
                "catalog: subs, platters, cakes, meals ...).",
            ),
            _int("page", "Results page, 1-based (60 items per page)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_stores",
        namespace="publix",
        method="stores",
        http="POST",
        path="/api/v1/publix/stores",
        summary=(
            "Publix stores near a ZIP code or in a city (city with state), or one store by "
            "store_id. Each store: store_id (for every other endpoint), name, short_name, type "
            "(supermarket, liquor, pharmacy), address, phone, hours for the next 7 days, "
            "time_zone, departments, services, pharmacy (phone, hours), liquor_store, "
            "latitude, longitude, distance_miles, weekly_ad_break_day (the day the store's "
            "weekly ad starts), opening_date, closing_date and image. Publix operates in FL, "
            "GA, AL, SC, NC, TN, VA and KY. An unknown store_id is a charged 404."
            + _PUBLIX_CHARGE
        ),
        params=(
            _str("zip", "A 5-digit US ZIP code: the stores nearest to it, e.g. '33101'."),
            _str("city", "A city name, with state, e.g. 'Nashville'."),
            _str("state", "A 2-letter state code, with city, e.g. 'TN'."),
            _str_or_int("store_id", "One store by its Publix store number, e.g. '1825'."),
            _int("limit", "Stores to return, up to 30 (default 10)."),
            _int("radius_miles", "Search radius in miles, 1-100 (default 50)."),
        ),
        one_of=(("zip", "city", "store_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="publix_suggestions",
        namespace="publix",
        method="suggestions",
        http="POST",
        path="/api/v1/publix/suggestions",
        summary=(
            "The suggestions the Publix search box shows for what a user typed: up to 10 "
            "popular searches (suggestions: text, type) and, with store_id, up to 4 products "
            "(item_code, base_product_id, title, description, saving_text, image, url); plus "
            "query, store_id and count." + _PUBLIX_CHARGE
        ),
        params=(
            _req("query", "What the user has typed so far, e.g. 'chick'."),
            _str_or_int(
                "store_id",
                "Optional: with a store the answer also carries up to 4 products. "
                + _PUBLIX_STORE_DOC,
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # ================================= IKEA ================================
    # 12 endpoints on /api/v1/ikea, 1 credit each; compare costs 1 credit per market that
    # answered (credits_note). search and product serve 55 markets (50 ikea.com + cn, pr, do,
    # es_islands with island, is); category, deals, suggestions and items the 50 ikea.com
    # markets + cn; reviews, categories, stores, stock and compare the 50 ikea.com markets;
    # as-is 13 markets. A product or reviews call can take up to about 100 s: 180 s timeout
    # floor there, 120 s elsewhere.
    Endpoint(
        key="ikea_search",
        namespace="ikea",
        method="search",
        http="POST",
        path="/api/v1/ikea/search",
        summary=(
            "Search IKEA products by keyword on any of 55 markets. The 50 ikea.com markets and "
            "cn get the full grid: sort by price, newest, rating, name or popularity; filter by "
            "color, price range, category, new, last chance, IKEA Family price, best seller, "
            "store availability or any facet." + _IKEA_GRID_FIELDS + " Keyword searches also "
            "return did_you_mean, related_searches and content (inspiration pages, separate "
            "from items). The franchise sites (pr, do, es_islands, is) take query and page "
            "only: Puerto Rico, Dominican Republic and the islands return the first 40 results "
            "only; Iceland pages by 40." + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            _req("query", "Search keywords, in any language the market serves, e.g. 'kallax'."),
            _ikea_country(_IKEA_ALL_SCOPE),
            _IKEA_LANGUAGE,
            _IKEA_ISLAND,
            _str_or_list(
                "category_id",
                "Narrow to category id(s) from facets (parameter f-subcategories), e.g. 'st002'.",
            ),
            *_IKEA_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_product",
        namespace="ikea",
        method="product",
        http="POST",
        path="/api/v1/ikea/product",
        summary=(
            "One IKEA product by article number or product URL: item_no, article_number, name, "
            "full_name, type_name, summary, description, url, price, previous_price, "
            "price_valid_from / to, family_price (member price with its dates), currency, "
            "images, rating, rating_count, measurements, materials, care, good_to_know, safety, "
            "packaging (number_of_packages, packages with item_no, dimensions, weight, "
            "quantity), assembly_pdfs, manuals, designer, variants, secondary_ratings, "
            "reviews_preview (3 newest), availability_online and detail_level (basic, rare: core "
            "fields only). cn answers in Chinese; the franchise sites (pr, do, es_islands, is) "
            "answer name, description, price, currency, availability_online, images and "
            "dimensions (detail_level basic). A product call can take up to about 100 seconds. "
            "An unknown article number is a charged 404." + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            _str_or_int("item_no", _IKEA_ITEM_NO_DOC + " Alternative to url."),
            _str(
                "url",
                "An IKEA product page of a served market, e.g. "
                "'https://www.ikea.com/de/de/p/kallax-regal-weiss-80275887/' (alternative to "
                "item_no; the market and language are read from it).",
            ),
            _ikea_country(_IKEA_ALL_SCOPE),
            _IKEA_LANGUAGE,
            _IKEA_ISLAND,
        ),
        one_of=(("item_no", "url"),),
        credits=1,
        min_timeout=180.0,
    ),
    Endpoint(
        key="ikea_reviews",
        namespace="ikea",
        method="reviews",
        http="POST",
        path="/api/v1/ikea/reviews",
        summary=(
            "An IKEA product's rating, rating_count, secondary_ratings (appearance, ease of "
            "assembly, quality, value for money ...) and the 20 most recent reviews the product "
            "page shows (title, text, rating, date, author first name as shown, country), plus "
            "highlighted reviews with their country. No paging, sort or star filter: always the "
            "20 newest. rating and rating_count are what that market's site shows: many markets "
            "share one pool (KALLAX: 8,241 in Germany, Spain, Sweden), others have their own "
            "(France 2,760, Italy 1,887), and some show none (Estonia, Latvia, Lithuania, Israel, "
            "Iceland). A call can take up to about 100 seconds." + _IKEA_CHARGE
        ),
        params=(
            _str_or_int("item_no", _IKEA_ITEM_NO_DOC + " Alternative to url."),
            _str("url", "An ikea.com product page (alternative to item_no)."),
            _ikea_country(_IKEA_MAIN_SCOPE),
            _IKEA_LANGUAGE,
        ),
        one_of=(("item_no", "url"),),
        credits=1,
        min_timeout=180.0,
    ),
    Endpoint(
        key="ikea_category",
        namespace="ikea",
        method="category",
        http="POST",
        path="/api/v1/ikea/category",
        summary=(
            "One IKEA category's products by category id or category URL, with the search "
            "sorts and filters: category (id, name, url, parents)." + _IKEA_GRID_FIELDS
            + " An unknown category id is a charged 404." + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            _str(
                "category_id",
                "A category id (categories[].id of categories(), or category_path / facets ids "
                "of a search), e.g. '10382' = bookcases, 'fu003' = sofas. Alternative to url.",
            ),
            _str(
                "url",
                "An IKEA category page, e.g. 'https://www.ikea.com/us/en/cat/bookcases-10382/'. "
                "Alternative to category_id.",
            ),
            _ikea_country(_IKEA_MAIN_CN_SCOPE),
            _IKEA_LANGUAGE,
            *_IKEA_GRID_PARAMS,
        ),
        one_of=(("category_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_categories",
        namespace="ikea",
        method="categories",
        http="POST",
        path="/api/v1/ikea/categories",
        summary=(
            "The market's IKEA category tree as its site menu shows it (about 1,500 "
            "categories): id (for category()), name, url and children; plus parent_id and "
            "count. parent_id returns one category's subtree." + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            _ikea_country(_IKEA_MAIN_SCOPE),
            _IKEA_LANGUAGE,
            _str("parent_id", "Return only this category's subtree (categories[].id)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_deals",
        namespace="ikea",
        method="deals",
        http="POST",
        path="/api/v1/ikea/deals",
        summary=(
            "One of the market's IKEA deal lists, with the search sorts and filters: "
            "new_products, family_price (IKEA Family member prices), new_lower_price, "
            "last_chance, lowest_price (the lowest-price range), top_seller, limited_edition, "
            "time_restricted, in_store_price_only or reduced_price_offer. Returns type."
            + _IKEA_GRID_FIELDS + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            Param(
                "type",
                'Literal["new_products", "family_price", "new_lower_price", "last_chance", '
                '"lowest_price", "top_seller", "limited_edition", "time_restricted", '
                '"in_store_price_only", "reduced_price_offer"]',
                required=True,
                doc="The deal list, e.g. 'new_lower_price'.",
            ),
            _ikea_country(_IKEA_MAIN_CN_SCOPE),
            _IKEA_LANGUAGE,
            *_IKEA_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_suggestions",
        namespace="ikea",
        method="suggestions",
        http="POST",
        path="/api/v1/ikea/suggestions",
        summary=(
            "What the IKEA search box suggests for what a user typed: suggestions with text, "
            "type (completion, category, product, planner, content), label, url, category_id, "
            "item_no and image when given." + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            _req("query", "What the user has typed so far, e.g. 'sof'."),
            _ikea_country(_IKEA_MAIN_CN_SCOPE),
            _IKEA_LANGUAGE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_stores",
        namespace="ikea",
        method="stores",
        http="POST",
        path="/api/v1/ikea/stores",
        summary=(
            "The market's IKEA stores and pick-up / plan-and-order points: store_id (for "
            "stock(), as_is() and the store_id filter), name, display_name, type (store, "
            "small_store, plan_and_order_point, shop ...), address (street, city, zip, state, "
            "timezone), latitude, longitude, hours (normal week, exceptions, closed days), "
            "restaurant, bistro, cafe, click & collect, Swedish Food Market and Smaland hours, "
            "store_url and opening_date; plus total and count. Filter by text (query) and sort "
            "by distance from lat / lng (distance_km)." + _IKEA_CHARGE
        ),
        params=(
            _ikea_country(_IKEA_MAIN_SCOPE),
            _IKEA_LANGUAGE,
            _str(
                "query",
                "Only stores whose name, city, ZIP / postal code or address contains this "
                "text, e.g. 'Burbank'.",
            ),
            _float("lat", "With lng: stores sorted by distance from this point (distance_km)."),
            _float("lng", "With lat."),
            _int("limit", "Stores to return (default 50, up to 200)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_stock",
        namespace="ikea",
        method="stock",
        http="POST",
        path="/api/v1/ikea/stock",
        summary=(
            "Stock at one IKEA store for up to 100 article numbers in one call: store (id, "
            "name), zip and items (item_no, name, type_name, design, url, price, "
            "store_availability with status in_stock_high, in_stock_low or out_of_stock and the "
            "site's text, home_delivery with zip, click_collect). A level, not a quantity: IKEA "
            "does not publish unit counts. Numbers the market does not sell are listed in "
            "not_found; an unknown store id is a charged 404." + _IKEA_CHARGE
        ),
        params=(
            _IKEA_ITEM_NOS,
            _IKEA_STORE,
            _str("zip", "A postal code: adds home-delivery availability to that address."),
            _ikea_country(_IKEA_MAIN_SCOPE + "; the store's market"),
            _IKEA_LANGUAGE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_items",
        namespace="ikea",
        method="items",
        http="POST",
        path="/api/v1/ikea/items",
        summary=(
            "Up to 100 IKEA article numbers on one market in one call, each with the search "
            "item fields (" + _IKEA_ITEM + "); numbers the market does not sell are listed in "
            "not_found." + _IKEA_LANG_NOTE + _IKEA_CHARGE
        ),
        params=(
            _IKEA_ITEM_NOS,
            _ikea_country(_IKEA_MAIN_CN_SCOPE),
            _IKEA_LANGUAGE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_compare",
        namespace="ikea",
        method="compare",
        http="POST",
        path="/api/v1/ikea/compare",
        summary=(
            "IKEA prices by country: one article number across 2 to 10 IKEA markets in one "
            "call. Returns item_no, count, found_count, markets (country, language, currency, "
            "found, name, type_name, design, price, previous_price, price_tag, url), errors and "
            "note. Prices are in each market's own currency and never converted (measured "
            "2026-11-13: KALLAX 80275887 was EUR 49.99 in de and nl, EUR 59.99 in fr, SEK 599 in "
            "se). Some markets (us, ca, jp, au, kr, in, my, sg, ph ...) sell the same product "
            "under a different article number, so found is False there. A market that fails is "
            "listed in errors and not charged. Markets: " + _IKEA_MAIN_SCOPE + "."
        ),
        params=(
            Param("item_no", "Union[str, int]", required=True, doc=_IKEA_ITEM_NO_DOC),
            _str_list(
                "countries",
                "2 to 10 ikea.com market codes, e.g. ['de', 'fr', 'se', 'nl', 'es', 'it'].",
                required=True,
            ),
        ),
        credits=1,
        credits_note=(
            "Costs 1 credit per market that answered (the balance must cover every market "
            "asked)."
        ),
        min_timeout=120.0,
    ),
    Endpoint(
        key="ikea_as_is",
        namespace="ikea",
        method="as_is",
        http="POST",
        path="/api/v1/ikea/as-is",
        summary=(
            "One IKEA store's As-is offers (ex-display, returned and second-hand items at "
            "reduced prices): store_id, total, page, page_size, total_pages and offers, per "
            "product title, description, article_numbers, currency, original_price, min_price, "
            "max_price, image and offers (offer_id, offer_number, description, price, "
            "lowest_previous_price, condition_code, condition, condition_description, in_box, "
            "reason_discount). Read-only: nothing is reserved. A store of another market is a "
            "charged 404. Markets: " + _IKEA_ASIS_SCOPE + "." + _IKEA_CHARGE
        ),
        params=(
            _IKEA_STORE,
            _ikea_country(_IKEA_ASIS_SCOPE + "; the store's market"),
            _IKEA_LANGUAGE,
            _int("page", "Results page, 1-based."),
            _int("page_size", "Products per page (default 24, up to 48)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # ================================ Wayfair ===============================
    # 4 endpoints on /api/v1/wayfair, 1 credit each. Markets us, ca (en / fr), gb, ie;
    # site = the US banners (search, product, category). zip on product is us and ca only.
    # A grid call can take about 40 s and a slow product page longer: 120 s timeout floor.
    Endpoint(
        key="wayfair_search",
        namespace="wayfair",
        method="search",
        http="POST",
        path="/api/v1/wayfair/search",
        summary=(
            "Search Wayfair products by keyword, sorted by price or customer rating and "
            "filtered by sale, closeout, open box, new arrivals, in stock, brand id, minimum "
            "rating, price range or any facet. Keyword pages return 30 results per page; a "
            "keyword that matches a category answers that category's grid (48 per page) and "
            "says so in redirected_to (type, category_id, name, url), and a SKU answers "
            "redirected_to a product. Returns query." + _WAYFAIR_GRID_FIELDS
            + _WAYFAIR_PRICES + _WAYFAIR_NOTE
        ),
        params=(
            _req(
                "query",
                "Search keywords, e.g. 'office chair' (a SKU opens that product: redirected_to).",
            ),
            _WAYFAIR_COUNTRY,
            _WAYFAIR_LANGUAGE,
            _WAYFAIR_SITE,
            *_WAYFAIR_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="wayfair_product",
        namespace="wayfair",
        method="product",
        http="POST",
        path="/api/v1/wayfair/product",
        summary=(
            "One Wayfair product by SKU or product URL: sku, variant_id, name, brand (id, name, "
            "url), url, price, sale_price, was_price, price_label, percent_off, per_item_price, "
            "loyalty_savings, prices, badge, limited_time_deal, stock_status, max_quantity, "
            "part_number, options (category, total, selected and choices with name, option_id, "
            "stock_status, url; choices carry no price: call again with option_id for that "
            "option's price and stock, one call per option), dimensions, specifications, "
            "features, description, image, images, breadcrumbs, documents, collection, returns, "
            "rating, review_count, rating_histogram, review_summary, review_aspects and reviews "
            "(the 5 reviews the page shows; no review paging). delivery (name, date_min, "
            "date_max, text, badge) and delivery_zip come back for the ZIP / postal code sent in "
            "zip (us and ca only)." + _WAYFAIR_PRICES + _WAYFAIR_NOTE
        ),
        params=(
            _str(
                "sku",
                "A Wayfair SKU (items[].sku, or 'SKU:' on the product page), e.g. 'W005006988'. "
                "Alternative to url.",
            ),
            _str(
                "url",
                "A Wayfair product page of a served site (alternative to sku; the market, "
                "language and site are read from it).",
            ),
            _str_or_int(
                "option_id",
                "A size / color / configuration: options[].choices[].option_id (several "
                "comma-separated for multi-choice products), e.g. '1820607042'. Returns that "
                "option's price and stock.",
            ),
            _str("zip", "Delivery estimate to this ZIP / postal code, e.g. '10001' (us and ca only)."),
            _WAYFAIR_COUNTRY,
            _WAYFAIR_LANGUAGE,
            _WAYFAIR_SITE,
        ),
        one_of=(("sku", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="wayfair_category",
        namespace="wayfair",
        method="category",
        http="POST",
        path="/api/v1/wayfair/category",
        summary=(
            "One Wayfair category's products (48 per page) by category id or category URL, with "
            "the search sorts and filters: category (id, name, url, breadcrumbs)."
            + _WAYFAIR_GRID_FIELDS + " An unknown category is a charged 404; a department page "
            "(/cat/) is not a product list." + _WAYFAIR_PRICES + _WAYFAIR_NOTE
        ),
        params=(
            _str_or_int(
                "category_id",
                "A Wayfair category id, e.g. '413892' (Sofas) or 'c413892', from a category URL "
                "(...-c413892.html) or a search's redirected_to.category_id. Alternative to "
                "category_url.",
            ),
            _str(
                "category_url",
                "A category page of a served site (/sb0/, /sb1/ or /sb2/ URL; filters in it are "
                "kept). Alternative to category_id.",
            ),
            _WAYFAIR_COUNTRY,
            _WAYFAIR_LANGUAGE,
            _WAYFAIR_SITE,
            *_WAYFAIR_GRID_PARAMS,
        ),
        one_of=(("category_id", "category_url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="wayfair_deals",
        namespace="wayfair",
        method="deals",
        http="POST",
        path="/api/v1/wayfair/deals",
        summary=(
            "The market's current Wayfair sale events (the Daily Sales list): events (event_id, "
            "slug, title, url, image) and count; about 38 on us, 34 on ca, 6 on gb and ie. "
            "Events are listed, not expanded: for sale, closeout or open-box products use "
            "search() or category() with on_sale, closeout or open_box." + _WAYFAIR_NOTE
        ),
        params=(
            _WAYFAIR_COUNTRY,
            _WAYFAIR_LANGUAGE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # =========================== Ashley Furniture ==========================
    # 6 endpoints on /api/v1/ashley. search + product serve us and the licensee storefronts
    # (ca, mx, ph, sa, tr): 2 credits on us and mx, 1 on the rest (credits_note; credits is
    # the floor). category, deals, stores and store are us only, 2 credits. Each call can
    # retry once upstream: 120 s timeout floor.
    Endpoint(
        key="ashley_search",
        namespace="ashley",
        method="search",
        http="POST",
        path="/api/v1/ashley/search",
        summary=(
            "Search Ashley Furniture by keyword. us: 48 results per page with the exact total, "
            "sorted by best sellers, price, newest, customer rating or name; items carry "
            "position, sku, master_id, name, brand, url, image, swatch_image, price, "
            "regular_price, discount_percent, color, size, flag, " + _ASHLEY_BADGES + ", "
            "new_since, rating, review_count, variant_count, variants (sku, color, size, url, "
            "price, regular_price, rating, review_count) and promotions; also priced_for, "
            "total, total_pages, page_size, sorts_offered and facets (informational: search "
            "takes no facet filters, use category() for filters). ca, mx, ph, sa, tr: the "
            "storefront's best matches (up to 10; tr its first results page) with handle (for "
            "product()), product_id, name, brand, product_type, url, image, price, "
            "regular_price, discount_percent and available; no sort, paging or total."
            + _ASHLEY_PRICES + _ASHLEY_REGION + _ASHLEY_MARKETS_NOTE
        ),
        params=(
            _req("query", "Search keywords, e.g. 'sofa' (tr: Turkish keywords such as 'koltuk')."),
            _ASHLEY_COUNTRY,
            _int("page", "us only: results page, 1-based (48 per page)."),
            _lit(
                "sort",
                _ASHLEY_SORTS,
                "us only: best_sellers (default), price_asc, price_desc, newest, rating or name.",
            ),
        ),
        credits=1,
        credits_note=_ASHLEY_CREDITS_NOTE,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ashley_product",
        namespace="ashley",
        method="product",
        http="POST",
        path="/api/v1/ashley/product",
        summary=(
            "One Ashley product. us (by item number or URL): priced_for, sku, master_id, name, "
            "brand, url, price, regular_price, discount_percent, " + _ASHLEY_BADGES + ", "
            "new_since, item_status, color, size, description, features, options, variants "
            "(sku, dimension values, url, selected; call again with a variant sku for its "
            "price), is_set and components (each piece of a set with sku, name, price, "
            "regular_price, dimensions, stock_status, stock_quantity), dimensions, materials, "
            "assembly, images, category, breadcrumbs, stock (status, quantity, delivery_method, "
            "delivery_message, delivery_date, white_glove), nearest_store, rating, "
            "review_count, rating_histogram (5 to 1), reviews (the first 10 the page shows; no "
            "review paging, sort or star filter), customer_photos, questions_total and "
            "questions (customer Q&A). ca, mx, ph, sa, tr (by handle or URL, not sku): sku, "
            "handle, product_id, name, brand, product_type, url, price, regular_price, "
            "discount_percent, available, description, options, variants (sku, options, price, "
            "regular_price, available, barcode) and images. An unknown item number is a "
            "charged 404." + _ASHLEY_PRICES + _ASHLEY_REGION + _ASHLEY_MARKETS_NOTE
        ),
        params=(
            _str(
                "sku",
                "us: an Ashley item number (items[].sku), e.g. '5950418' or 'APK-29004-R3'.",
            ),
            _str(
                "handle",
                "ca, mx, ph, sa, tr: the product handle from search (items[].handle), e.g. "
                "'aviemore-sofa'. Send it with country.",
            ),
            _str(
                "url",
                "A product page on a served storefront (alternative to sku / handle; the market "
                "is read from it).",
            ),
            _ASHLEY_COUNTRY,
        ),
        one_of=(("sku", "handle", "url"),),
        credits=1,
        credits_note=_ASHLEY_CREDITS_NOTE,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ashley_category",
        namespace="ashley",
        method="category",
        http="POST",
        path="/api/v1/ashley/category",
        summary=(
            "One ashleyfurniture.com category's products by path or category URL, sorted and "
            "filtered." + _ASHLEY_GRID_FIELDS + " Also category (path, name, url, "
            "breadcrumbs). An unknown category is a charged 404." + _ASHLEY_PRICES
            + _ASHLEY_REGION + _ASHLEY_US_NOTE
        ),
        params=(
            _str(
                "path",
                "A category path: the part after /c/ in an ashleyfurniture.com category URL, "
                "e.g. 'furniture/living-room/sofas', 'bedroom/beds', 'mattresses'. Alternative "
                "to category_url.",
            ),
            _str(
                "category_url",
                "An ashleyfurniture.com category page (/c/... URL); refinements in it are kept. "
                "Alternative to path.",
            ),
            *_ASHLEY_GRID_PARAMS,
        ),
        one_of=(("path", "category_url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ashley_deals",
        namespace="ashley",
        method="deals",
        http="POST",
        path="/api/v1/ashley/deals",
        summary=(
            "The products of one Ashley deal event: black_friday (Black Friday furniture "
            "deals, the default), clearance (clearance furniture) or hot_buys (Ashley's Hot "
            "Buys), with the category sorts and filters." + _ASHLEY_GRID_FIELDS + " Also "
            "event, event_name and event_url." + _ASHLEY_PRICES + _ASHLEY_REGION
            + _ASHLEY_US_NOTE
        ),
        params=(
            _lit(
                "event",
                ("black_friday", "clearance", "hot_buys"),
                "black_friday (default), clearance or hot_buys.",
            ),
            *_ASHLEY_GRID_PARAMS,
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ashley_stores",
        namespace="ashley",
        method="stores",
        http="POST",
        path="/api/v1/ashley/stores",
        summary=(
            "Ashley stores near a point (lat and lng are required; there is no address or ZIP "
            "lookup): latitude, longitude, radius_miles, count and stores with store_id, name "
            "and url, in the order Ashley lists them (alphabetical, not by distance). Call "
            "store() with a store_id for the address, phone and hours." + _ASHLEY_US_NOTE
        ),
        params=(
            Param("lat", "float", required=True, doc="Latitude in decimal degrees, e.g. 40.7506."),
            Param("lng", "float", required=True, doc="Longitude in decimal degrees, e.g. -73.9972."),
            _ilit("radius", (10, 25, 50, 100), "Search radius in miles (default 50)."),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="ashley_store",
        namespace="ashley",
        method="store",
        http="POST",
        path="/api/v1/ashley/store",
        summary=(
            "One Ashley store by store_id or store page URL: store_id, name, url, phone, "
            "address (street, city, state, zip, country), latitude, longitude, hours (day, "
            "opens, closes), payment_accepted, services, rating, image and map_url. An unknown "
            "store is a charged 404." + _ASHLEY_US_NOTE
        ),
        params=(
            _str(
                "store_id",
                "A store id from stores() (stores[].store_id), e.g. "
                "'us/wisconsin/greenfield/4771-s-27th-st/luxe'. Alternative to url.",
            ),
            _str(
                "url",
                "A store page on stores.ashleyfurniture.com (stores[].url). Alternative to "
                "store_id.",
            ),
        ),
        one_of=(("store_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    # ========================== Maisons du Monde ==========================
    # 9 endpoints on /api/v1/maisonsdumonde, 1 credit each. search, product, category, deals
    # and reviews serve all 9 markets; stores, store and availability fr, be, de, es, it, pt,
    # ch; seller fr, de, es, it. Some calls make two upstream requests: 120 s timeout floor.
    Endpoint(
        key="maisonsdumonde_search",
        namespace="maisonsdumonde",
        method="search",
        http="POST",
        path="/api/v1/maisonsdumonde/search",
        summary=(
            "Search Maisons du Monde (furniture and home decor) by keyword, sorted by price or "
            "customer rating and filtered by price range, discount, stock, rating, color, "
            "material, style, brand, marketplace seller or any facet. A keyword that names a "
            "category answers that category's grid and says so in redirected_to (type, "
            "category_id, name, url)." + _MDM_GRID_FIELDS + " The German site does not sort "
            "keyword results: on de a sorted search comes back in relevance order with a note "
            "(sort works on category() and deals())." + _MDM_PRICES + _MDM_NOTE
        ),
        params=(
            _req(
                "query",
                "Search keywords, in the market's language, e.g. 'table' (fr), 'couchtisch' (de).",
            ),
            _mdm_country(_MDM_COUNTRIES, _MDM_ALL_SCOPE),
            _MDM_LANGUAGE,
            *_MDM_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_product",
        namespace="maisonsdumonde",
        method="product",
        http="POST",
        path="/api/v1/maisonsdumonde/product",
        summary=(
            "One Maisons du Monde product by reference or product URL: id, gtin13, name, "
            "collection, brand, url, price, was_price, discount_percent, currency, "
            "eco_participation (fr), badges, stock (status and the exact online quantity), "
            "store_only, sold_by, seller (marketplace items: id, name, url, rating, orders, "
            "member_since), offer_id, condition, variants (dimension, value, name, id, url, "
            "price_difference), dimensions, weight, materials, made_in, characteristics, "
            "composition, attributes, wood_and_finishes, assembly, care, documents, images, "
            "breadcrumbs, categories, short_description, description, rating, review_count, "
            "review_summary, questions and markets (the same product on every other market: "
            "country, language, url). An unknown product, or one not sold in that market, is a "
            "charged 404. Delivery and store stock: availability(); reviews: reviews()."
            + _MDM_PRICES + _MDM_NOTE
        ),
        params=(
            _str(
                "id",
                "A product reference (items[].id): digits for Maisons du Monde items, e.g. "
                "'186339', or M + digits for marketplace items, e.g. 'M24132196'. Alternative "
                "to url.",
            ),
            _str(
                "url",
                "A product page of any market (its market and language are used unless country "
                "/ language are sent). Alternative to id.",
            ),
            _mdm_country(_MDM_COUNTRIES, _MDM_ALL_SCOPE),
            _MDM_LANGUAGE,
        ),
        one_of=(("id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_category",
        namespace="maisonsdumonde",
        method="category",
        http="POST",
        path="/api/v1/maisonsdumonde/category",
        summary=(
            "One Maisons du Monde category's products by category hash or category URL, with "
            "the search sorts and filters. The hash is the same on every market, so a URL from "
            "any market works on any other." + _MDM_GRID_FIELDS + " Also category (id, name, "
            "url, breadcrumbs). An unknown category is a charged 404." + _MDM_PRICES + _MDM_NOTE
        ),
        params=(
            _str(
                "category",
                "A category hash (the end of a /c/ URL, the same on every market), optionally "
                "with its name, e.g. 'canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f', or "
                "redirected_to.category_id of a search. Alternative to category_url.",
            ),
            _str(
                "category_url",
                "A category page of any market (filters in it are kept). Alternative to "
                "category.",
            ),
            _mdm_country(_MDM_COUNTRIES, _MDM_ALL_SCOPE),
            _MDM_LANGUAGE,
            *_MDM_GRID_PARAMS,
        ),
        one_of=(("category", "category_url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_deals",
        namespace="maisonsdumonde",
        method="deals",
        http="POST",
        path="/api/v1/maisonsdumonde/deals",
        summary=(
            "A Maisons du Monde sale event's products: black_friday (default, on every market "
            "while it runs) or second_chance (fr only: used and returned items, condition per "
            "item); or a category's discounted items (category / category_url, on_sale unless "
            "min_discount is sent). Same sorts and filters as search()." + _MDM_GRID_FIELDS
            + " Also event (type, name, url, category_id). An event that is not running is a "
            "charged 404." + _MDM_PRICES + _MDM_NOTE
        ),
        params=(
            _lit(
                "event",
                ("black_friday", "second_chance"),
                "black_friday (default; every market while it runs) or second_chance (fr only).",
            ),
            _str("category", "A category hash: answers its discounted items instead of an event."),
            _str(
                "category_url",
                "A category page of any market: answers its discounted items instead of an "
                "event.",
            ),
            _mdm_country(_MDM_COUNTRIES, _MDM_ALL_SCOPE),
            _MDM_LANGUAGE,
            *_MDM_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_reviews",
        namespace="maisonsdumonde",
        method="reviews",
        http="POST",
        path="/api/v1/maisonsdumonde/reviews",
        summary=(
            "A Maisons du Monde product's customer reviews: product_id, sort, rating, "
            "review_count, rating_histogram (5 to 1), criteria and reviews (rating, text, date, "
            "author as the display name shown, country, source_market, syndicated, criteria "
            "scores, brand_reply, images), plus next_cursor for the next page. Reviews are "
            "pooled across every Maisons du Monde market and shown translated into the request "
            "language (source_market is where a review was written). Sorted newest, "
            "rating_desc or rating_asc; the site has no star filter. Reviews carry no id, title "
            "or verified flag. A product with no reviews (or a marketplace item) is a charged "
            "404." + _MDM_NOTE
        ),
        params=(
            _req("id", "A Maisons du Monde product reference (product id), e.g. '186339'."),
            _mdm_country(_MDM_COUNTRIES, _MDM_ALL_SCOPE),
            _MDM_LANGUAGE,
            _lit(
                "sort",
                ("newest", "rating_desc", "rating_asc"),
                "newest (default), rating_desc or rating_asc.",
            ),
            _str(
                "cursor",
                "next_cursor of the previous answer, for the next page (keep the same sort).",
            ),
            _int("limit", "Reviews per page, 1 to 30 (default 10)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_stores",
        namespace="maisonsdumonde",
        method="stores",
        http="POST",
        path="/api/v1/maisonsdumonde/stores",
        summary=(
            "Up to 10 Maisons du Monde stores nearest a postcode: postcode, count and stores "
            "with id, name, address, postcode, city, country, lat, lng, distance_km, url, "
            "open_now, hours (per day, opening slots) and click_collect. Call store() for the "
            "phone and services and availability() with a store id for an item's stock there."
            " Markets: " + _MDM_STORE_SCOPE + _MDM_NOTE
        ),
        params=(
            _req(
                "postcode",
                "A postcode of the market: 5 digits on fr / de / es / it (e.g. '75011'), 4 on "
                "be / ch, 1000-001 on pt.",
            ),
            _mdm_country(_MDM_STORE_COUNTRIES, _MDM_STORE_SCOPE),
            _MDM_LANGUAGE,
            _int("limit", "Stores to return, nearest first (1 to 10, default 10)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_store",
        namespace="maisonsdumonde",
        method="store",
        http="POST",
        path="/api/v1/maisonsdumonde/store",
        summary=(
            "One Maisons du Monde store by store id or store page URL: id, name, address, "
            "postcode, city, country, phone, lat, lng, url, hours (every day of the week, "
            "opening slots), services (as the store page lists them), click_collect and "
            "hours_today (by id). Markets: " + _MDM_STORE_SCOPE + _MDM_NOTE
        ),
        params=(
            _str(
                "store_id",
                "A store id (stores[].id of stores()) of the market in country, e.g. '41'. "
                "Alternative to url.",
            ),
            _str("url", "A store page (stores[].url). Alternative to store_id."),
            _mdm_country(_MDM_STORE_COUNTRIES, _MDM_STORE_SCOPE),
            _MDM_LANGUAGE,
        ),
        one_of=(("store_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_availability",
        namespace="maisonsdumonde",
        method="availability",
        http="POST",
        path="/api/v1/maisonsdumonde/availability",
        summary=(
            "One Maisons du Monde item's stock at one store plus the market's delivery "
            "options: product_id, store (id, name, postcode, city), in_stock, quantity (the "
            "store's stock count), stock_text, display_model (only the display piece is in "
            "store), click_collect and on_shelf (available, the site's texts) and delivery "
            "(type home, store_pickup or in_store: title, available, availability_text, "
            "from_price, currency, price_text). Home delivery is a from-price per product and "
            "market; the exact cost for a postcode is only shown in the cart and is not "
            "returned. Marketplace items are not stocked in stores. Markets: "
            + _MDM_STORE_SCOPE + _MDM_NOTE
        ),
        params=(
            _req(
                "id",
                "A Maisons du Monde item reference (digits; marketplace items are not stocked "
                "in stores), e.g. '204172'.",
            ),
            _req("store_id", "A store id from stores() (stores[].id), e.g. '125'."),
            _mdm_country(_MDM_STORE_COUNTRIES, _MDM_STORE_SCOPE),
            _MDM_LANGUAGE,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="maisonsdumonde_seller",
        namespace="maisonsdumonde",
        method="seller",
        http="POST",
        path="/api/v1/maisonsdumonde/seller",
        summary=(
            "A Maisons du Monde marketplace seller by seller id or seller URL: seller (id, "
            "name, code for search()'s seller filter, url, rating, review_count, orders, "
            "member_since, order_approval, shipping, returns, company_city, description) plus "
            "the seller's catalog as a grid (sort as search())." + _MDM_GRID_FIELDS
            + " Markets: " + _MDM_MARKETPLACE_SCOPE + _MDM_PRICES + _MDM_NOTE
        ),
        params=(
            _str("seller_id", "A marketplace seller id (a product's seller.id), e.g. '2066'."),
            _str("url", "A seller page (seller.url). Alternative to seller_id."),
            _mdm_country(_MDM_MARKETPLACE_COUNTRIES, _MDM_MARKETPLACE_SCOPE),
            _MDM_LANGUAGE,
            _MDM_PAGE,
            _MDM_SORT,
        ),
        one_of=(("seller_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    # ============================= Decathlon =============================
    # 2 endpoints, 2 credits each. Supports 7 country domains:
    # FR, ES, IT, IN, UK, PT and NET (international).
    Endpoint(
        key="decathlon_search",
        namespace="decathlon",
        method="search",
        http="POST",
        path="/api/v1/decathlon/search",
        summary=(
            "Search Decathlon products by keyword across 7 country domains (FR, ES, "
            "IT, IN, UK, PT, NET). Returns product name, brand, price (cents), "
            "currency, availability, rating, review count and image."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _req("country", 'Country domain: "fr", "es", "it", "in", "uk", "pt" or "net".'),
            _int("page", "Results page, 1-based (1-50)."),
        ),
        credits=2,
    ),
    Endpoint(
        key="decathlon_product",
        namespace="decathlon",
        method="product",
        http="POST",
        path="/api/v1/decathlon/product",
        summary=(
            "Full Decathlon product detail: description, images, SKU, GTIN, color, "
            "price (cents), list price, availability, offers/variants, rating, review "
            "count, category and breadcrumbs. Pass product_url (from search()) or "
            "product_id."
        ),
        params=(
            _req("country", 'Country domain: "fr", "es", "it", "in", "uk", "pt" or "net".'),
            _str(
                "product_url",
                "Full or relative product URL from any Decathlon domain (e.g. "
                "'/p/mens-running-shoes/123456/...'). Preferred.",
            ),
            _str("product_id", "Decathlon numeric product ID (from the /p/{slug}/{id}/... URL pattern)."),
        ),
        one_of=(("product_url", "product_id"),),
        credits=2,
    ),
    # =============================== Spec's ==============================
    # 3 endpoints, 5 credits each. Texas liquor chain. Search returns the
    # online price; product returns every store's price and stock in
    # store_prices, with store_id putting one store on top.
    Endpoint(
        key="specs_search",
        namespace="specs",
        method="search",
        http="POST",
        path="/api/v1/specs/search",
        summary=(
            "Search Spec's Wines, Spirits & Finer Foods: online price (cents), case price and "
            "quantity, promo and Keyclub flags, stock, size, SKU, UPC and slug."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-50). 24 results per page."),
        ),
        credits=5,
    ),
    Endpoint(
        key="specs_product",
        namespace="specs",
        method="product",
        http="POST",
        path="/api/v1/specs/product",
        summary=(
            "One Spec's product with every store's price and stock in store_prices (about 200 "
            "stores), the online price, and ABV, origin, region, vintage and tasting notes."
        ),
        params=(
            _str("slug", "Product slug from search(), e.g. 'titos-texas-vodka-5'."),
            _str("product_url", "Spec's product URL, https://specsonline.com/shop/<type>/<slug>/."),
            _str("store_id", "Spec's store number from specs.stores(), e.g. '169'. Puts that store's price and stock at the top."),
        ),
        one_of=(("slug", "product_url"),),
        credits=5,
    ),
    Endpoint(
        key="specs_stores",
        namespace="specs",
        method="stores",
        http="POST",
        path="/api/v1/specs/stores",
        summary=(
            "Spec's stores in a Texas region: store_id, name, status, address, phone, "
            "coordinates and opening hours."
        ),
        params=(
            Param(
                name="region",
                annotation='Literal["austin", "corpus-christi", "dallas", "el-paso", "fort-worth", "houston", "san-antonio"]',
                required=True,
                doc="Store region: austin, corpus-christi, dallas, el-paso, fort-worth, houston or san-antonio.",
            ),
        ),
        credits=5,
    ),
    # =============================== Lowe's ==============================
    # 4 endpoints. search, product and stores 2 credits each; reviews 1.
    # Prices and stock are one store's: store_id and that store's zip (both
    # from stores()) are required on search and product. Deals are
    # search(on_sale=True); there is no clearance endpoint.
    Endpoint(
        key="lowes_search",
        namespace="lowes",
        method="search",
        http="POST",
        path="/api/v1/lowes/search",
        summary=(
            "Search Lowe's by keyword or category at one store: the store's price, was-price and "
            "savings with the sale end date, brand, model number, rating, review count, and stock "
            "for pickup, truck delivery, parcel shipping and same-day delivery. Pass query or "
            "category_id; on_sale=True returns that store's deals."
        ),
        params=(
            _req("store_id", "Lowe's store number (up to 4 digits) from lowes.stores(), e.g. '0595'."),
            _req("zip", "The store's own 5-digit ZIP code from lowes.stores(), e.g. '28117'."),
            _str("query", "Search keywords (1-200 characters). Pass this or category_id."),
            _str("category_id", "Category id, the number at the end of a lowes.com/pl/ URL. Pass this or query."),
            _int("page", "Results page, 1-based (1-31). 24 results per page."),
            _bool("on_sale", "Only items on sale at this store (with a was-price). A page can then hold fewer than 24."),
        ),
        one_of=(("query", "category_id"),),
        credits=2,
    ),
    Endpoint(
        key="lowes_product",
        namespace="lowes",
        method="product",
        http="POST",
        path="/api/v1/lowes/product",
        summary=(
            "One Lowe's item at one store: price, was-price and savings, on-hand stock with lead "
            "time per fulfillment method, stock at nearby stores, aisle and bay, grouped "
            "specifications, UPC, dimensions, weight, rating, images, and the store's hours."
        ),
        params=(
            _req("item_id", "Lowe's item id (the number at the end of a lowes.com/pd/ URL) or the full product URL."),
            _req("store_id", "Lowe's store number (up to 4 digits) from lowes.stores(), e.g. '0595'."),
            _req("zip", "The store's own 5-digit ZIP code from lowes.stores(), e.g. '28117'."),
        ),
        credits=2,
    ),
    Endpoint(
        key="lowes_stores",
        namespace="lowes",
        method="stores",
        http="POST",
        path="/api/v1/lowes/stores",
        summary=(
            "Lowe's stores near a ZIP code, nearest first: store_id, name, address, phone, "
            "coordinates, distance, time zone, opening hours and features."
        ),
        params=(
            _req("zip", "5-digit US ZIP code to find stores near."),
            _int("limit", "Stores to return, nearest first (1-10; default 10)."),
        ),
        credits=2,
    ),
    Endpoint(
        key="lowes_reviews",
        namespace="lowes",
        method="reviews",
        http="POST",
        path="/api/v1/lowes/reviews",
        summary=(
            "One page of a Lowe's item's customer reviews (10 per page): rating, title, text, "
            "date, reviewer, recommended, helpful votes, verified and incentivized flags, photos "
            "and brand replies, plus the average rating and count per star."
        ),
        params=(
            _req("item_id", "Lowe's item id (the number at the end of a lowes.com/pd/ URL) or the full product URL."),
            _int("page", "Reviews page, 1-based (1-1000). 10 reviews per page."),
            _lit("sort", ("newest", "oldest", "most_helpful"), "newest (default), oldest or most_helpful."),
        ),
        credits=1,
    ),
    # ============================= Sam's Club ============================
    # 6 endpoints: clubs 1 credit, the other five 2 (since 2026-11-14).
    # search, savings and category answer for a
    # club picked by location (echoed in data.club); product(club_id=...)
    # prices and stocks one specific club. available_quantity is capped at 8
    # by the site (8 means 8 or more). Clearance is category 1150109.
    Endpoint(
        key="sams_club_search",
        namespace="sams_club",
        method="search",
        http="POST",
        path="/api/v1/samsclub/search",
        summary=(
            "Search Sam's Club: item_id, price, was_price, savings_amount, unit price, Instant "
            "Savings (amount, end date, purchase limit), rating, review count, stock, "
            "pickup/delivery/shipping availability and aisle. The club is picked by location and "
            "returned in data.club; use product(club_id=...) for a specific club."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100). Up to 45 results per page."),
            _lit(
                "sort",
                ("relevance", "price_low", "price_high", "top_selling"),
                "relevance, price_low, price_high or top_selling. Defaults to the site's own order.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="sams_club_product",
        namespace="sams_club",
        method="product",
        http="POST",
        path="/api/v1/samsclub/product",
        summary=(
            "One Sam's Club item: online price and the club shelf price (club_price) with was "
            "price, savings and unit price, Instant Savings, rating histogram, UPC, model, "
            "specifications, and per-method fulfillment with stock and aisle. available_quantity "
            "is capped at 8 by the site; 8 means 8 or more."
        ),
        params=(
            _req("item_id", "Sam's Club item id: the number at the end of a samsclub.com/ip/ URL, or item_id from search()."),
            _str("club_id", "Club number from sams_club.clubs(), e.g. '6372'. Prices and stocks that club."),
        ),
        credits=2,
    ),
    Endpoint(
        key="sams_club_clubs",
        namespace="sams_club",
        method="clubs",
        http="POST",
        path="/api/v1/samsclub/clubs",
        summary=(
            "Sam's Club clubs near a US ZIP within 100 miles, nearest first: club_id, name, "
            "address, coordinates, distance in miles, phone, opening hours, services and whether "
            "the club is temporarily closed."
        ),
        params=(
            _req("zip", "5-digit US ZIP code, e.g. '75201'."),
            _int("limit", "Clubs to return, nearest first (1-20; default 10)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="sams_club_savings",
        namespace="sams_club",
        method="savings",
        http="POST",
        path="/api/v1/samsclub/savings",
        summary=(
            "Every item on Sam's Club Instant Savings, paged: price, was price and savings "
            "amount, plus each offer's amount, end date, purchase limit and channels. The club is "
            "picked by location and returned in data.club."
        ),
        params=(
            _int("page", "Results page, 1-based (1-100). Up to 45 items per page."),
            _lit(
                "sort",
                ("relevance", "price_low", "price_high", "top_selling"),
                "relevance, price_low, price_high or top_selling. Defaults to the site's own order.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="sams_club_category",
        namespace="sams_club",
        method="category",
        http="POST",
        path="/api/v1/samsclub/category",
        summary=(
            "Products in a Sam's Club category, paged, with the same fields as search(). "
            "Clearance is category '1150109'. An empty shelf returns an empty list. The club is "
            "picked by location and returned in data.club."
        ),
        params=(
            _req("category_id", "Category id, the number at the end of a sams_club.com /browse/ or /cp/ URL. Clearance is '1150109'."),
            _int("page", "Results page, 1-based (1-100)."),
            _lit(
                "sort",
                ("relevance", "price_low", "price_high", "top_selling"),
                "relevance, price_low, price_high or top_selling. Defaults to the site's own order.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="sams_club_reviews",
        namespace="sams_club",
        method="reviews",
        http="POST",
        path="/api/v1/samsclub/reviews",
        summary=(
            "Customer reviews for a Sam's Club item, 10 per page: rating, title, text, author, "
            "date, verified purchase and helpful votes, plus the average rating, total count and "
            "1-5 star breakdown."
        ),
        params=(
            _req("item_id", "Sam's Club item id from search() or a samsclub.com/ip/ URL."),
            _int("page", "Reviews page, 1-based (1-100). 10 reviews per page."),
            _lit(
                "sort",
                ("newest", "oldest", "highest", "lowest", "most_helpful"),
                "newest, oldest, highest, lowest or most_helpful.",
            ),
        ),
        credits=2,
    ),
    # ============================ Canadian Tire ==========================
    # 6 endpoints, 1 credit each. Prices (CAD) and stock are one store's, so
    # store_id (from stores()) is required everywhere but stores(). Prices
    # differ by store and province (Quebec prices differ). No review text:
    # rating and review_count only.
    Endpoint(
        key="canadian_tire_search",
        namespace="canadian_tire",
        method="search",
        http="POST",
        path="/api/v1/canadiantire/search",
        summary=(
            "Search Canadian Tire by keyword or category at one store: the store's price and "
            "regular price (CAD), price range for multi-variant items, savings, badges "
            "(clearance, sale, rebate), rating, review count, brand, part number, SKU, and stock "
            "at the store and online. Pass query or category_id."
        ),
        params=(
            _req("store_id", "Canadian Tire store number from canadian_tire.stores(), e.g. '600'."),
            _str("query", "Search keywords (up to 200 characters). Pass this or category_id."),
            _str("category_id", "Category id (DC followed by 7 digits, e.g. 'DC0002209') or a canadian_tire.ca category URL. Pass this or query."),
            _int("page", "Results page, 1-based (1-100). 24 results per page."),
            _lit(
                "sort",
                ("relevance", "price_asc", "price_desc", "newest", "rating", "bestseller"),
                "relevance (default), price_asc, price_desc, newest, rating or bestseller.",
            ),
            _bool("in_stock_only", "Only items in stock at store_id."),
        ),
        one_of=(("query", "category_id"),),
        credits=1,
    ),
    Endpoint(
        key="canadian_tire_product",
        namespace="canadian_tire",
        method="product",
        http="POST",
        path="/api/v1/canadiantire/product",
        summary=(
            "One Canadian Tire product by code at one store: breadcrumb, images, rating, review "
            "count, descriptions, features, specifications, price and regular price, warranty, "
            "manuals, variants with their SKUs, and the store's price, stock, and pickup and "
            "ship-to-home dates."
        ),
        params=(
            _req("product_code", "Product code, the `code` field of a search result, e.g. '0547273P'."),
            _req("store_id", "Canadian Tire store number from canadian_tire.stores(), e.g. '600'."),
        ),
        credits=1,
    ),
    Endpoint(
        key="canadian_tire_stores",
        namespace="canadian_tire",
        method="stores",
        http="POST",
        path="/api/v1/canadiantire/stores",
        summary=(
            "Canadian Tire stores near a postal code or coordinates, nearest first: store_id, "
            "name, address, phone, coordinates, distance, weekly hours and services. Pass sku to "
            "get each store's stock quantity and aisle for that item."
        ),
        params=(
            _str("postal_code", "Canadian postal code or its first 3 characters, e.g. 'M5V 2T6'. Pass this or latitude and longitude."),
            _float("latitude", "Latitude (-90 to 90); pass with longitude."),
            _float("longitude", "Longitude (-180 to 180); pass with latitude."),
            _float("radius_km", "Search radius in km (1-200; default 25)."),
            _int("limit", "Stores to return, nearest first (1-50; default 10)."),
            _str("sku", "7-digit SKU, e.g. '0438858'. Adds each store's stock quantity and aisle for it."),
        ),
        one_of=(("postal_code", "latitude"),),
        credits=1,
    ),
    Endpoint(
        key="canadian_tire_availability",
        namespace="canadian_tire",
        method="availability",
        http="POST",
        path="/api/v1/canadiantire/availability",
        summary=(
            "Up to 50 Canadian Tire SKUs at one store in one call: the store's price and regular "
            "price, clearance and sale flags, price valid-until date, stock quantity, aisle, "
            "online stock, and pickup and delivery dates. Unknown SKUs are listed in not_found."
        ),
        params=(
            _req("store_id", "Canadian Tire store number from canadian_tire.stores(), e.g. '600'."),
            _str_list("skus", "1-50 SKUs (7 digits, the `sku` field of a search result or product variant).", required=True),
        ),
        credits=1,
    ),
    Endpoint(
        key="canadian_tire_clearance",
        namespace="canadian_tire",
        method="clearance",
        http="POST",
        path="/api/v1/canadiantire/clearance",
        summary=(
            "Every clearance item at one Canadian Tire store, 100 per page, with clearance price, "
            "regular price, stock at the store and the same fields as search(). In-stock items "
            "only by default."
        ),
        params=(
            _req("store_id", "Canadian Tire store number from canadian_tire.stores(), e.g. '600'."),
            _int("page", "Results page, 1-based (1-100). 100 results per page."),
            _bool("in_stock_only", "Only clearance items in stock at store_id. Defaults to True."),
        ),
        credits=1,
    ),
    Endpoint(
        key="canadian_tire_deals",
        namespace="canadian_tire",
        method="deals",
        http="POST",
        path="/api/v1/canadiantire/deals",
        summary=(
            "Items on a deal at one Canadian Tire store, 100 per page: sale prices, instant "
            "rebates, special buys or Triangle Rewards loyalty offers, with the same fields as "
            "search()."
        ),
        params=(
            _req("store_id", "Canadian Tire store number from canadian_tire.stores(), e.g. '600'."),
            Param(
                "type",
                'Literal["sale", "instant_rebate", "special_buy", "loyalty"]',
                required=True,
                doc="sale (this week's sale prices), instant_rebate, special_buy or loyalty (Triangle Rewards offers).",
            ),
            _int("page", "Results page, 1-based (1-100). 100 results per page."),
        ),
        credits=1,
    ),
    # =========================== Dollar General ==========================
    # 5 endpoints, 1 credit each. Prices (dollars) and unit counts are one
    # store's, so store_id (from stores()) is required on search, product and
    # deals. stores(upc=...) returns that product's unit count at up to 25
    # nearby stores in one call. No review text: rating and review_count only.
    Endpoint(
        key="dollar_general_search",
        namespace="dollar_general",
        method="search",
        http="POST",
        path="/api/v1/dollargeneral/search",
        summary=(
            "Search Dollar General at one store: that store's price and original price, "
            "available_quantity (units on hand at that store), inventory_status, rating, review "
            "count, categories, digital coupons and promotions, UPC and product URL."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _req("store_id", "Dollar General store number from dollar_general.stores(), e.g. '12629'."),
            _int("page", "Results page, 1-based (1-100). 24 results per page."),
            _lit(
                "sort",
                ("recommended", "price_low", "price_high", "rating"),
                "recommended (default), price_low, price_high or rating.",
            ),
            _bool("in_stock_only", "Only products with units on hand at the store. Defaults to False."),
        ),
        credits=1,
    ),
    Endpoint(
        key="dollar_general_product",
        namespace="dollar_general",
        method="product",
        http="POST",
        path="/api/v1/dollargeneral/product",
        summary=(
            "One Dollar General product by UPC at one store: price, original price, "
            "available_quantity, stock_status, nearby_stores_with_stock, rating, review count, "
            "SKU, brand, description, highlights, images, categories, digital coupons and "
            "promotions. An unknown UPC or store number is a 404."
        ),
        params=(
            _req("upc", "Product UPC, the `upc` field of a search result, e.g. '030772156629'."),
            _req("store_id", "Dollar General store number from dollar_general.stores(), e.g. '12629'."),
        ),
        credits=1,
    ),
    Endpoint(
        key="dollar_general_stores",
        namespace="dollar_general",
        method="stores",
        http="POST",
        path="/api/v1/dollargeneral/stores",
        summary=(
            "Dollar General stores near a US ZIP code or coordinates, nearest first (up to 25): "
            "store_id, address, phone, coordinates, distance in miles, opening hours and "
            "services. Pass upc and each store also carries its unit count of that product."
        ),
        params=(
            _str("zip", "US ZIP code, e.g. '75203'. Pass this or latitude and longitude."),
            _float("latitude", "Latitude (-90 to 90); pass with longitude."),
            _float("longitude", "Longitude (-180 to 180); pass with latitude."),
            _float("radius", "Search radius in miles (1-100; default 25)."),
            _str("upc", "Product UPC. Every store then carries quantity, in_stock and inventory_status for it."),
        ),
        one_of=(("zip", "latitude"),),
        credits=1,
    ),
    Endpoint(
        key="dollar_general_deals",
        namespace="dollar_general",
        method="deals",
        http="POST",
        path="/api/v1/dollargeneral/deals",
        summary=(
            "Dollar General products on sale or on clearance, priced and stocked at one store, 24 "
            "per page. available_quantity > 0 means in stock at that store; the listing covers "
            "the whole chain. Clearance items carry the current price only (no was-price)."
        ),
        params=(
            _req("store_id", "Dollar General store number from dollar_general.stores(), e.g. '12629'."),
            Param(
                "type",
                'Literal["on_sale", "clearance"]',
                required=True,
                doc="on_sale (everything on sale) or clearance (the clearance event).",
            ),
            _int("page", "Results page, 1-based (1-100). 24 results per page."),
            _lit(
                "sort",
                ("recommended", "price_low", "price_high", "rating"),
                "recommended (default), price_low, price_high or rating.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="dollar_general_coupons",
        namespace="dollar_general",
        method="coupons",
        http="POST",
        path="/api/v1/dollargeneral/coupons",
        summary=(
            "Dollar General's current digital coupons, 30 per page: offer id and code, summary, "
            "description, brand, company, value, offer type, category, minimum quantity, start "
            "and expiration dates, and whether it is a manufacturer coupon."
        ),
        params=(_int("page", "Results page, 1-based (1-50). 30 coupons per page."),),
        credits=1,
    ),
    # ============================== Sephora ==============================
    # 3 endpoints: search and category 1 credit, product 2 (since 2026-11-12).
    # sephora.com (US). Prices are national.
    # product() carries a summary of what reviews say plus pro/con sentiment
    # counts, but no review text.
    Endpoint(
        key="sephora_search",
        namespace="sephora",
        method="search",
        http="POST",
        path="/api/v1/sephora/search",
        summary=(
            "Search sephora.com (US), 60 products per page: product and sku id, brand, name, URL, "
            "price, list and sale price (price_range when sizes differ), value price for sets, "
            "rating, review count, extra colors, and bestseller, new, exclusive, online-only, "
            "limited-edition and sponsored flags, plus category facets and related searches. "
            "Pass zip for same-day delivery eligibility."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100). 60 products per page."),
            _lit(
                "sort",
                ("relevance", "best_selling", "rating", "price_low", "price_high", "newest"),
                "relevance (default), best_selling, rating, price_low, price_high or newest.",
            ),
            _str("zip", "US ZIP code. Each product then carries same_day_eligible for that ZIP."),
        ),
        credits=1,
    ),
    Endpoint(
        key="sephora_category",
        namespace="sephora",
        method="category",
        http="POST",
        path="/api/v1/sephora/category",
        summary=(
            "Products in a sephora.com (US) category, 60 per page, in the same shape as search(), "
            "plus the category's id, name and URL, total product count, parent category, "
            "subcategories with product counts and breadcrumbs. An unknown category is a 404."
        ),
        params=(
            _req(
                "category",
                "Category name as in a sephora.com/shop/ URL (e.g. 'lipstick', 'face-serum') or the full URL.",
            ),
            _int("page", "Results page, 1-based (1-100). 60 products per page."),
        ),
        credits=1,
    ),
    Endpoint(
        key="sephora_product",
        namespace="sephora",
        method="product",
        http="POST",
        path="/api/v1/sephora/product",
        summary=(
            "One sephora.com (US) product: name, brand, rating, review count, loves count, price "
            "range, description, usage, category and breadcrumbs, a summary of what reviews say "
            "with pro and con sentiment counts (no review text), and every shade or size as a sku "
            "with price, list and sale price, in_stock, only_few_left, ingredients, images and "
            "pickup and same-day eligibility. An unknown product is a 404."
        ),
        params=(
            _str("url", "sephora.com product URL (the `url` of a search result). Preferred: it answers faster."),
            _str("product_id", "Sephora product id, e.g. 'P510799'. Used when url is not given."),
        ),
        one_of=(("url", "product_id"),),
        credits=2,
    ),
    # ============================ Ulta Beauty ============================
    # 4 endpoints, 1 credit each. stores() reports in stock / out of stock for
    # one shade or size at the 10 stores nearest a ZIP, not unit counts.
    Endpoint(
        key="ulta_search",
        namespace="ulta",
        method="search",
        http="POST",
        path="/api/v1/ulta/search",
        summary=(
            "Search Ulta Beauty, 64 products per page plus sponsored placements: product_id, "
            "sku_id, brand, name, URL, image, list and sale price (with ranges when shades differ), "
            "discount, promo text, rating, review count, badge, variant label and sponsored flag. "
            "Sponsored placements can repeat across pages; dedupe by product_id."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100). 64 products per page plus sponsored placements."),
        ),
        credits=1,
    ),
    Endpoint(
        key="ulta_category",
        namespace="ulta",
        method="category",
        http="POST",
        path="/api/v1/ulta/category",
        summary=(
            "Products in an Ulta Beauty category, 64 per page plus sponsored placements, with the "
            "category title and total_results, in the same shape as search()."
        ),
        params=(
            _req(
                "category",
                "A category that lists products: the ulta.com URL or its path, e.g. "
                "'/shop/makeup/lips/lipstick'. Landing pages without a product grid are a 404.",
            ),
            _int("page", "Results page, 1-based (1-100). 64 products per page plus sponsored placements."),
        ),
        credits=1,
    ),
    Endpoint(
        key="ulta_product",
        namespace="ulta",
        method="product",
        http="POST",
        path="/api/v1/ulta/product",
        summary=(
            "One Ulta Beauty product for the selected shade or size: list and sale price, "
            "discount, availability, GTIN, rating, review count, badges, description, usage, "
            "ingredients, category and breadcrumbs, images, every shade or size variant, ship / "
            "pickup / same-day eligibility, and the five most recent reviews. An unknown product "
            "is a 404."
        ),
        params=(
            _req("url", "Ulta product page URL, /p/<name>-<productId> (the `url` of a search result)."),
            _str("sku", "Shade or size to select, by sku id (a `variants[].sku_id`). Defaults to the product's default."),
        ),
        credits=1,
    ),
    Endpoint(
        key="ulta_stores",
        namespace="ulta",
        method="stores",
        http="POST",
        path="/api/v1/ulta/stores",
        summary=(
            "In-store pickup availability of one shade or size at the 10 Ulta Beauty stores "
            "nearest a US ZIP: store id, name, address, distance in miles, open-now label, "
            "curbside label, in_stock and the availability label. In stock / out of stock per "
            "store, not unit counts."
        ),
        params=(
            _req("product_id", "Ulta product id, the `product_id` of a search or product result, e.g. 'pimprod2057119'."),
            _req("sku_id", "Sku id of the shade or size, a `sku_id` or `variants[].sku_id`."),
            _req("zip", "US ZIP code to search around, e.g. '10001'."),
        ),
        credits=1,
    ),
    # =============================== ALDI ================================
    # 3 endpoints, 1 credit each. Prices and stock are one store's and one
    # shopping mode's: service_type instore (default, the shelf price), pickup
    # or delivery (online prices, often higher). Pass store_id (from stores())
    # or zip to use the nearest store. No product ratings.
    Endpoint(
        key="aldi_search",
        namespace="aldi",
        method="search",
        http="POST",
        path="/api/v1/aldi/search",
        summary=(
            "Search ALDI US at one store (store_id, or the nearest store to zip): product_id, "
            "name, brand, size, price and was_price for that store and service_type, discount "
            "label, unit price, in_stock and stock level, category, in-store aisle location, "
            "ALDI-exclusive brand flag, dietary labels, image and URL. Exact matches only unless "
            "include_related=True."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _str("store_id", "ALDI store id from aldi.stores(), e.g. '151248'. Pass this or zip."),
            _str("zip", "US ZIP code; without store_id the nearest ALDI store is used. Pass this or store_id."),
            _lit(
                "service_type",
                ("instore", "pickup", "delivery"),
                "instore (default, the shelf price), pickup or delivery (online prices, often higher).",
            ),
            _lit("sort", ("best_match", "price_low", "price_high"), "best_match (default), price_low or price_high."),
            _int("limit", "Products per page (1-60; default 30)."),
            _int("page", "Results page, 1-based (1-100)."),
            _bool("include_related", "Also return the related items listed after the exact matches. Defaults to False."),
        ),
        one_of=(("store_id", "zip"),),
        credits=1,
    ),
    Endpoint(
        key="aldi_product",
        namespace="aldi",
        method="product",
        http="POST",
        path="/api/v1/aldi/product",
        summary=(
            "One ALDI US product at one store (store_id, or the nearest store to zip): price and "
            "was_price for that store and service_type, unit price, stock, category, brand, size, "
            "description, ingredients, allergen warnings, dietary labels and images. An unknown "
            "product id is a 404."
        ),
        params=(
            _req("product_id", "ALDI product id (the `product_id` of a search result) or an aldi.us product URL."),
            _str("store_id", "ALDI store id from aldi.stores(), e.g. '151248'. Pass this or zip."),
            _str("zip", "US ZIP code; without store_id the nearest ALDI store is used. Pass this or store_id."),
            _lit(
                "service_type",
                ("instore", "pickup", "delivery"),
                "instore (default, the shelf price), pickup or delivery (online prices, often higher).",
            ),
        ),
        one_of=(("store_id", "zip"),),
        credits=1,
    ),
    Endpoint(
        key="aldi_stores",
        namespace="aldi",
        method="stores",
        http="POST",
        path="/api/v1/aldi/stores",
        summary=(
            "ALDI US stores near a ZIP code, nearest first: store_id (for search and product), "
            "name, street address, city, state, ZIP, coordinates and distance in miles."
        ),
        params=(
            _req("zip", "5-digit US ZIP code to search around."),
            _int("limit", "Stores to return, nearest first (1-50; default 10)."),
        ),
        credits=1,
    ),
    # ============================ Micro Center ===========================
    # 3 endpoints. search and product 2 credits each, stores 1. Stock is per
    # 3-digit store_id (omit for the web store 029, shippable items only);
    # counts are capped at 25+ (quantity_capped). stores_in_stock on product
    # is a yes/no per store, not a unit count.
    Endpoint(
        key="micro_center_search",
        namespace="micro_center",
        method="search",
        http="POST",
        path="/api/v1/microcenter/search",
        summary=(
            "Search Micro Center by keyword or category at one store, up to 96 per page: "
            "product_id, SKU, name, brand, category, price and original price, image, URL, "
            "highlights, and that store's stock (label, quantity, quantity_capped at 25+, "
            "in_stock, not_carried), plus open-box count and lowest price, rebate text and an "
            "in-store-only flag where shown. Pass query, category or both."
        ),
        params=(
            _str("query", "Search keywords (1-200 characters). Pass this, category, or both."),
            _str("category", "Category id (e.g. '518' = Graphics Cards) or a microcenter.com listing URL carrying one."),
            _str("store_id", "3-digit store id from micro_center.stores(), e.g. '131' (Dallas). Omit for the web store (029)."),
            _int("page", "Results page, 1-based (1-100)."),
            _ilit("per_page", (24, 48, 96), "Results per page: 24, 48 or 96 (default)."),
            _lit(
                "sort",
                ("best_match", "rating", "review_count", "price_low", "price_high", "newest"),
                "best_match (default), rating, review_count, price_low, price_high or newest.",
            ),
            _bool(
                "include_out_of_stock",
                "Also list products the store has no stock of or does not carry. Defaults to False.",
            ),
        ),
        one_of=(("query", "category"),),
        credits=2,
    ),
    Endpoint(
        key="micro_center_product",
        namespace="micro_center",
        method="product",
        http="POST",
        path="/api/v1/microcenter/product",
        summary=(
            "One Micro Center product: SKU, MPN, UPC, name, brand, description, price, original "
            "price, ship and pickup flags, images, rating, review count, up to 10 recent reviews, "
            "breadcrumbs with category ids, the spec table, the selected store's stock (counts "
            "capped at 25+) and open-box units, and every store with an in_stock flag. An unknown "
            "product id is a 404."
        ),
        params=(
            _req("product_id", "Micro Center product id (the number after /product/ in a URL) or the product URL. Not the SKU."),
            _str("store_id", "3-digit store id from micro_center.stores(), e.g. '131' (Dallas). Omit for the web store (029)."),
        ),
        credits=2,
    ),
    Endpoint(
        key="micro_center_stores",
        namespace="micro_center",
        method="stores",
        http="POST",
        path="/api/v1/microcenter/stores",
        summary=(
            "Every Micro Center store with its 3-digit store_id (for search and product), name, "
            "city, state and store page URL; street address and ZIP where known. The web store "
            "029 is not listed but is accepted as a store_id."
        ),
        params=(_str("state", "2-letter US state code to filter by, e.g. 'TX'."),),
        credits=1,
    ),
    # ============================= Walgreens =============================
    # 4 endpoints. search, product and stores 2 credits each; stock 4. Retail
    # products only (no pharmacy). Prices are national; stock() gives live
    # unit counts at up to 20 stores in one call.
    Endpoint(
        key="walgreens_search",
        namespace="walgreens",
        method="search",
        http="POST",
        path="/api/v1/walgreens/search",
        summary=(
            "Search Walgreens retail products, up to 70 per page: product id, SKU, UPC, name, "
            "brand, size, regular and sale price (national), unit price, promotion, coupon, "
            "loyalty and rebate messages, rating, review count, image, URL, ship/pickup/delivery "
            "availability, online stock status and clearance flag. Pass store_id for that store's "
            "availability text."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100). Up to 70 results per page."),
            _lit(
                "sort",
                (
                    "relevance",
                    "top_sellers",
                    "price_low_to_high",
                    "price_high_to_low",
                    "unit_price_low_to_high",
                    "brand_name_asc",
                    "brand_name_desc",
                    "most_reviewed",
                    "highest_rated",
                    "most_viewed",
                    "newest_arrival",
                ),
                "relevance (default), top_sellers, price_low_to_high, price_high_to_low, "
                "unit_price_low_to_high, brand_name_asc, brand_name_desc, most_reviewed, "
                "highest_rated, most_viewed or newest_arrival.",
            ),
            _str("store_id", "Walgreens store number from walgreens.stores(), e.g. '9438'. Sets the availability text."),
        ),
        credits=2,
    ),
    Endpoint(
        key="walgreens_product",
        namespace="walgreens",
        method="product",
        http="POST",
        path="/api/v1/walgreens/product",
        summary=(
            "One Walgreens retail product: SKU, UPC, GTIN, name, brand, size, regular and sale "
            "price (national), savings, unit price, rewards and rebate offers, description, "
            "ingredients, warnings, rating, review count, category path, images, ship and pickup "
            "availability and clearance flag. An unknown id is a 404."
        ),
        params=(
            _req("product_id", "Walgreens product id (the `product_id` of a search result, e.g. '300452904') or a product URL."),
        ),
        credits=2,
    ),
    Endpoint(
        key="walgreens_stores",
        namespace="walgreens",
        method="stores",
        http="POST",
        path="/api/v1/walgreens/stores",
        summary=(
            "Walgreens and Duane Reade stores near a US ZIP or coordinates, nearest first: store "
            "number, name, brand, address, phone, coordinates, distance in miles, opening and "
            "closing time, time zone and store page URL. Paged with total_results and has_more."
        ),
        params=(
            _str("zip", "US ZIP code, e.g. '60601'. Pass this or latitude and longitude."),
            _float("latitude", "Latitude (-90 to 90); pass with longitude."),
            _float("longitude", "Longitude (-180 to 180); pass with latitude."),
            _float("radius", "Search radius in miles (1-100; default 25)."),
            _int("page", "Results page, 1-based (1-100)."),
            _int("limit", "Stores per page (1-25; default 10)."),
        ),
        one_of=(("zip", "latitude"),),
        credits=2,
    ),
    Endpoint(
        key="walgreens_stock",
        namespace="walgreens",
        method="stock",
        http="POST",
        path="/api/v1/walgreens/stock",
        summary=(
            "Live in-store stock of one product at up to 20 Walgreens stores in one call: per "
            "store the status (In Stock, Out of Stock, or Not Available when not carried), the "
            "unit count and in_stock. Unrecognised store numbers are listed in unknown_store_ids. "
            "An unknown product id is a 404."
        ),
        params=(
            _req("product_id", "Walgreens product id (the `product_id` of a search result) or a product URL."),
            _str_list("store_ids", "1-20 Walgreens store numbers from walgreens.stores().", required=True),
        ),
        credits=4,
    ),
    # ================================ CVS ================================
    # 3 endpoints, 1 credit each. Front-store products only (no pharmacy).
    # Prices are the same at every store; stock is one store's. There is no
    # store locator: the store number is on every cvs.com store page. search
    # defaults to store 7019 (New York). product() can take 10-30+ seconds, so
    # its timeout is raised to 120s.
    Endpoint(
        key="cvs_search",
        namespace="cvs",
        method="search",
        http="POST",
        path="/api/v1/cvs/search",
        summary=(
            "Search CVS front-store products: product_id and sku_id, name, brand, URL, regular and "
            "sale price, unit price, promotion text, rating, review count, size, image, coupons "
            "(ExtraBucks and manufacturer), and units at one store in store and for pickup, plus "
            "online ship stock; same_day_delivery is always None. Prices are the same at every "
            "store. "
            "Includes brand, price-range and rating facets."
        ),
        params=(
            _req("query", "Search keywords or a CVS item number (1-200 characters)."),
            _str(
                "store_id",
                "CVS store number for the stock fields, shown on every cvs.com store page "
                "('Store ID: #7019'). Defaults to 7019 (New York, NY).",
            ),
            _int("page", "Results page, 1-based (1-100)."),
            _int("limit", "Results per page (1-48; default 20)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="cvs_product",
        namespace="cvs",
        method="product",
        http="POST",
        path="/api/v1/cvs/product",
        summary=(
            "One CVS product by URL or id: regular and sale price, unit price, promotion and its "
            "end date, rating, review count, UPC, size, description, highlights, ingredients, "
            "directions, warnings, attributes, breadcrumbs, images and every variant (SKU id, UPC, "
            "size, price, rating). Can take 10-30+ seconds. An unknown product is a 404."
        ),
        params=(
            _str("url", "cvs.com product URL (https://www.cvs.com/shop/<name>-prodid-<id>). Pass this or product_id."),
            _str("product_id", "CVS product id or SKU id, e.g. '789787' (a search result's product_id or sku_id). Pass this or url."),
        ),
        one_of=(("url", "product_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="cvs_stock",
        namespace="cvs",
        method="stock",
        http="POST",
        path="/api/v1/cvs/stock",
        summary=(
            "Units available at one CVS store for up to 20 SKUs: in_store (on the shelf), pickup "
            "and ship (online stock, chain-wide). same_day_delivery is always None (CVS does not "
            "report it per store). An unknown SKU or store number reads as 0."
        ),
        params=(
            _str_list("sku_ids", "1-20 CVS SKU ids: a search result's sku_id or a product's variants[].sku_id.", required=True),
            _req("store_id", "CVS store number, shown on every cvs.com store page ('Store ID: #7019')."),
        ),
        credits=1,
    ),
    # ======================== Whole Foods Market =========================
    # 7 endpoints, 1 credit each. Prices are one store's (5-digit store_id,
    # default 10145, Lamar in Austin TX): regular, sale and Prime member price.
    # product() returns the in-store and the online price as separate blocks.
    # No ratings, reviews or UPCs, and no per-store unit stock.
    Endpoint(
        key="whole_foods_search",
        namespace="whole_foods",
        method="search",
        http="POST",
        path="/api/v1/wholefoods/search",
        summary=(
            "Search Whole Foods Market products at one store: ASIN, slug, name, brand, image, URL, "
            "that store's regular_price, sale_price and prime_price (Prime member price) with "
            "sale dates and multi-buy quantities, price_unit (lb when priced per pound), on_sale "
            "and is_local flags, plus total_results and category, featured and diet facets with "
            "counts. Sorts by relevance or price only."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _str("store_id", "5-digit Whole Foods store id from whole_foods.stores(). Defaults to 10145 (Lamar, Austin TX)."),
            _lit("sort", ("relevance", "price_asc", "price_desc"), "relevance (default), price_asc or price_desc."),
            _bool("on_sale", "Only products on sale at the store. Defaults to False."),
            _lit(
                "diet",
                ("vegan", "gluten-free", "organic", "dairy-free", "vegetarian"),
                "Only products with this dietary attribute: vegan, gluten-free, organic, dairy-free or vegetarian.",
            ),
            _str("category", "Restrict to one category slug, e.g. 'milk-cream' (slugs are in the category facet)."),
            _int("limit", "Products per page (1-60; default 60)."),
            _int("offset", "Products to skip, for paging (0-10000; 60 = page 2 at the default limit)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="whole_foods_category",
        namespace="whole_foods",
        method="category",
        http="POST",
        path="/api/v1/wholefoods/category",
        summary=(
            "Browse one Whole Foods Market category at one store, in the same product shape as "
            "search(), with the category breadcrumb, total_results and facets. An unknown "
            "category slug is a 404."
        ),
        params=(
            _req(
                "category",
                "Category slug, e.g. 'cheese', 'dairy-eggs' or 'produce' (slugs are in the category "
                "facet of any search); 'all-products' lists the whole store.",
            ),
            _str("store_id", "5-digit Whole Foods store id from whole_foods.stores(). Defaults to 10145 (Lamar, Austin TX)."),
            _lit(
                "sort",
                ("featured", "popular", "price_asc", "price_desc", "brand_az", "brand_za"),
                "featured (default), popular, price_asc, price_desc, brand_az or brand_za.",
            ),
            _bool("on_sale", "Only products on sale at the store. Defaults to False."),
            _lit(
                "diet",
                ("vegan", "gluten-free", "organic", "dairy-free", "vegetarian"),
                "Only products with this dietary attribute: vegan, gluten-free, organic, dairy-free or vegetarian.",
            ),
            _int("limit", "Products per page (1-60; default 60)."),
            _int("offset", "Products to skip, for paging (0-10000; 60 = page 2 at the default limit)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="whole_foods_deals",
        namespace="whole_foods",
        method="deals",
        http="POST",
        path="/api/v1/wholefoods/deals",
        summary=(
            "Every product on sale at one Whole Foods Market store, store-wide or in one category, "
            "in the same product shape as search(): regular, sale and Prime price with the sale "
            "start and end dates."
        ),
        params=(
            _str("category", "Category slug, e.g. 'cheese'. Defaults to 'all-products' (every sale item at the store)."),
            _str("store_id", "5-digit Whole Foods store id from whole_foods.stores(). Defaults to 10145 (Lamar, Austin TX)."),
            _lit(
                "sort",
                ("featured", "popular", "price_asc", "price_desc", "brand_az", "brand_za"),
                "featured (default), popular, price_asc, price_desc, brand_az or brand_za.",
            ),
            _lit(
                "diet",
                ("vegan", "gluten-free", "organic", "dairy-free", "vegetarian"),
                "Only products with this dietary attribute: vegan, gluten-free, organic, dairy-free or vegetarian.",
            ),
            _int("limit", "Products per page (1-60; default 60)."),
            _int("offset", "Products to skip, for paging (0-10000; 60 = page 2 at the default limit)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="whole_foods_product",
        namespace="whole_foods",
        method="product",
        http="POST",
        path="/api/v1/wholefoods/product",
        summary=(
            "One Whole Foods Market product by ASIN, URL or slug: name, brand, description, "
            "ingredients, nutrition facts, diets, SNAP EBT eligibility and images. With store_id, "
            "two separate price blocks: in_store (that store's shelf regular, sale and Prime "
            "price; None when the store does not list it) and online (that store's delivery and "
            "pickup price, list price, savings, Prime price, unit price and availability). Online "
            "and in-store prices often differ. An unknown ASIN is a 404."
        ),
        params=(
            _str("asin", "Product ASIN, the `asin` of a search result, e.g. 'B0BCBNG8LS'. Pass this, url or slug."),
            _str("url", "A wholefoodsmarket.com product URL."),
            _str("slug", "A product slug, the `slug` of a search result."),
            _str("store_id", "5-digit Whole Foods store id. Adds that store's in_store and online price blocks."),
        ),
        one_of=(("asin", "url", "slug"),),
        credits=1,
    ),
    Endpoint(
        key="whole_foods_stores",
        namespace="whole_foods",
        method="stores",
        http="POST",
        path="/api/v1/wholefoods/stores",
        summary=(
            "Whole Foods Market stores near a US ZIP code, nearest first (within 15 miles, "
            "widening to 50): store_id, name, address, phone, coordinates, distance in miles, "
            "time zone and seven days of in-store and pickup hours. No store in range is an "
            "empty list."
        ),
        params=(_req("zip", "US ZIP code to search around, e.g. '78703'."),),
        credits=1,
    ),
    Endpoint(
        key="whole_foods_store",
        namespace="whole_foods",
        method="store",
        http="POST",
        path="/api/v1/wholefoods/store",
        summary=(
            "One Whole Foods Market store by id: name, status, phone, Prime eligibility, opening "
            "date, address, coordinates, time zone, store page URL and sales flyer URL. An "
            "unknown store id is a 404."
        ),
        params=(_req("store_id", "5-digit Whole Foods store id from whole_foods.stores(), e.g. '10160'."),),
        credits=1,
    ),
    Endpoint(
        key="whole_foods_sales_flyer",
        namespace="whole_foods",
        method="sales_flyer",
        http="POST",
        path="/api/v1/wholefoods/sales-flyer",
        summary=(
            "The current weekly sales flyer of one Whole Foods Market store: per promotion the "
            "product name, brand, headline, description, terms, regular, sale and Prime price as "
            "printed (text such as '$3.99/lb' or '44% off'), start and end dates, image, rank "
            "and the ASINs it covers. An unknown store id is a 404."
        ),
        params=(_req("store_id", "5-digit Whole Foods store id from whole_foods.stores(), e.g. '10160'."),),
        credits=1,
    ),
    # =========================== Harbor Freight ==========================
    # 7 endpoints, 1 credit each. Prices are national: price, regular price,
    # sale (price and end date), coupon (public coupon price), member_deal
    # (Inside Track Club price) and compare_at. Store stock is a status
    # (in_stock, limited, out_of_stock, not_carried) plus aisle from a daily
    # snapshot, not a unit count.
    Endpoint(
        key="harbor_freight_search",
        namespace="harbor_freight",
        method="search",
        http="POST",
        path="/api/v1/harborfreight/search",
        summary=(
            "Search Harbor Freight by keyword and/or category: item number (sku), id, title, "
            "brand, URL, image, price, regular_price, on_sale and clearance flags, sale (price, "
            "end date, savings), coupon (public coupon price, code, expiry, limit), member_deal "
            "(Inside Track Club price), compare_at (the competitor brand, model and price quoted), "
            "badges, rating, review count and where it sells. Also total_results, facets and, "
            "when a keyword maps to a category page, redirect. Prices are national."
        ),
        params=(
            _str("query", "Search keywords (1-200 characters). Pass this, category_id, or both."),
            _str("category_id", "Category id, e.g. '1827' (Drills, Drivers & Drill Presses): the `value` of a category facet."),
            _int("page", "Results page, 1-based (1-100)."),
            _int("page_size", "Results per page (1-48; default 36)."),
            _lit(
                "sort",
                ("best_match", "price_low", "price_high", "member_price_low", "member_price_high", "top_rated", "newest"),
                "best_match (default), price_low, price_high, member_price_low, member_price_high "
                "(Inside Track Club price), top_rated or newest.",
            ),
            _str("brand", "Only this brand as listed in the brand facet, e.g. 'BAUER' (case-insensitive)."),
            _bool("clearance", "Only clearance items. Defaults to False."),
        ),
        one_of=(("query", "category_id"),),
        credits=1,
    ),
    Endpoint(
        key="harbor_freight_clearance",
        namespace="harbor_freight",
        method="clearance",
        http="POST",
        path="/api/v1/harborfreight/clearance",
        summary=(
            "Harbor Freight clearance items, optionally narrowed by keyword, category or brand, "
            "in the same shape as search(): each item's clearance price and end date are in `sale`."
        ),
        params=(
            _str("query", "Keywords to narrow the clearance list (1-200 characters)."),
            _str("category_id", "Category id, e.g. '1827': the `value` of a category facet."),
            _int("page", "Results page, 1-based (1-100)."),
            _int("page_size", "Results per page (1-48; default 36)."),
            _lit(
                "sort",
                ("best_match", "price_low", "price_high", "member_price_low", "member_price_high", "top_rated", "newest"),
                "best_match (default), price_low, price_high, member_price_low, member_price_high "
                "(Inside Track Club price), top_rated or newest.",
            ),
            _str("brand", "Only this brand as listed in the brand facet, e.g. 'BAUER' (case-insensitive)."),
        ),
        credits=1,
    ),
    Endpoint(
        key="harbor_freight_product",
        namespace="harbor_freight",
        method="product",
        http="POST",
        path="/api/v1/harborfreight/product",
        summary=(
            "One Harbor Freight product by item number, id or URL: title, brand, UPC, the full "
            "price set (price, regular_price, sale, coupon, member_deal, compare_at), rating, "
            "review count, badges, description, highlights, the specification table, warranty, "
            "shipping notes, owner's manuals, images and variants. An unknown item is a 404."
        ),
        params=(
            _str("sku", "Harbor Freight item number, the `sku` of a search result, e.g. '73216'. Pass this, id or url."),
            _int("id", "Numeric product id, the `id` of a search result, e.g. 48725."),
            _str("url", "harborfreight.com product URL."),
        ),
        one_of=(("sku", "id", "url"),),
        credits=1,
    ),
    Endpoint(
        key="harbor_freight_prices",
        namespace="harbor_freight",
        method="prices",
        http="POST",
        path="/api/v1/harborfreight/prices",
        summary=(
            "Current national prices for up to 50 Harbor Freight item numbers in one call: price, "
            "regular_price, on_sale and clearance flags, sale, coupon, member_deal and compare_at "
            "per item. Unknown item numbers are listed in not_found."
        ),
        params=(_str_list("skus", "1-50 Harbor Freight item numbers, e.g. ['73216', '59716'].", required=True),),
        credits=1,
    ),
    Endpoint(
        key="harbor_freight_stores",
        namespace="harbor_freight",
        method="stores",
        http="POST",
        path="/api/v1/harborfreight/stores",
        summary=(
            "Harbor Freight stores near a ZIP code, 'City, ST' or coordinates, nearest first: "
            "store number, name, address, phone, coordinates, distance in miles, status, opening "
            "date and hours."
        ),
        params=(
            _str("query", "US ZIP code or 'City, ST', e.g. '60601' or 'Los Angeles, CA'. Pass this or latitude and longitude."),
            _float("latitude", "Latitude (-90 to 90); pass with longitude."),
            _float("longitude", "Longitude (-180 to 180); pass with latitude."),
            _int("radius", "Search radius in miles (1-100; default 50)."),
            _int("limit", "Most stores to return (1-50; default 10)."),
        ),
        one_of=(("query", "latitude"),),
        credits=1,
    ),
    Endpoint(
        key="harbor_freight_availability",
        namespace="harbor_freight",
        method="availability",
        http="POST",
        path="/api/v1/harborfreight/availability",
        summary=(
            "In-store stock for up to 20 Harbor Freight items at chosen stores, or at the stores "
            "nearest a ZIP code or coordinates. Each store lists every item with stock_status "
            "(in_stock, limited, out_of_stock or not_carried), stock_code, aisle and a nearby "
            "store that has it. inventory_updated_at is the time of the daily stock snapshot. "
            "Stock is a status, not a unit count."
        ),
        params=(
            _str_list("skus", "1-20 Harbor Freight item numbers.", required=True),
            _str_list("store_ids", "1-20 store numbers from harbor_freight.stores(). Or pass zip, or latitude and longitude."),
            _str("zip", "US ZIP code: stock at the stores nearest to it."),
            _float("latitude", "Latitude: stock at the stores nearest to it; pass with longitude."),
            _float("longitude", "Longitude; pass with latitude."),
            _int("limit", "Nearest stores to return with zip or coordinates (1-100; default 10)."),
        ),
        one_of=(("store_ids", "zip", "latitude"),),
        credits=1,
    ),
    Endpoint(
        key="harbor_freight_reviews",
        namespace="harbor_freight",
        method="reviews",
        http="POST",
        path="/api/v1/harborfreight/reviews",
        summary=(
            "Customer reviews for one Harbor Freight item, newest first: title, text, star "
            "rating, author, review and purchase dates, incentivized flag, helpful votes and the "
            "reviewer's answers (would recommend...), plus the average rating and total review "
            "count. An unknown item is a 404."
        ),
        params=(
            _req("sku", "Harbor Freight item number, e.g. '73216'."),
            _int("limit", "Reviews per call (1-50; default 10)."),
            _int("offset", "Reviews to skip, for paging. Defaults to 0."),
        ),
        credits=1,
    ),
    # ============================== PetSmart =============================
    # 6 endpoints, 1 credit each. Prices are national, with the Autoship
    # first-order and recurring price per variant. Stock is a unit count per
    # store. deals() rows carry on_sale: the Sale section also lists points
    # and Autoship promotions whose price is not reduced.
    Endpoint(
        key="petsmart_search",
        namespace="petsmart",
        method="search",
        http="POST",
        path="/api/v1/petsmart/search",
        summary=(
            "Search PetSmart products, up to 40 per page: SKU, web_style_id, name, brand, UPC, "
            "price, original and sale price, price range across sizes, rating, review count, "
            "image, size, variations, category, pets, promotions, stores_in_stock (how many "
            "stores stock it), pickup and Autoship eligibility and URL. Prices are national. "
            "Pass store_id to list only products in stock at that store."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100)."),
            _int("limit", "Results per page (1-40; default 40)."),
            _str("store_id", "PetSmart store number from petsmart.stores(), e.g. '1658'. Lists only products in stock there."),
            _lit(
                "sort",
                ("relevance", "best_sellers", "price_low", "price_high", "top_rated", "new_arrivals"),
                "relevance (default), best_sellers, price_low, price_high, top_rated or new_arrivals.",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="petsmart_product",
        namespace="petsmart",
        method="product",
        http="POST",
        path="/api/v1/petsmart/product",
        summary=(
            "One PetSmart product by web_style_id, SKU or URL, with every variant (size, flavor): "
            "SKU, UPC, price, original price, sale price and end date, autoship (discount, "
            "first_order_price, recurring_price), ship-to-home stock, pickup and same-day "
            "options, images and promotions, plus brand, rating, review count, categories and "
            "description. Prices are national. An unknown id is a 404."
        ),
        params=(
            _str("web_style_id", "Product id, the number at the end of a product URL (...-570.html). One id covers every size and flavor."),
            _str("sku", "One size or flavor's SKU, e.g. '5154856'. Returns the whole product it belongs to."),
            _str("url", "A petsmart.com product URL. Pass exactly one of web_style_id, sku or url."),
        ),
        one_of=(("web_style_id", "sku", "url"),),
        credits=1,
    ),
    Endpoint(
        key="petsmart_stores",
        namespace="petsmart",
        method="stores",
        http="POST",
        path="/api/v1/petsmart/stores",
        summary=(
            "The 12 PetSmart stores nearest a US ZIP code: store number, name, address, phone, "
            "coordinates, distance in miles, time zone, the next 7 days of hours and services "
            "(grooming, PetsHotel, veterinary...). Pass sku and each store also carries quantity "
            "and in_stock for that SKU."
        ),
        params=(
            _req("zip", "US ZIP code to search around, e.g. '60601'."),
            _int("radius", "Search radius in miles (1-100; default 30)."),
            _str("sku", "A SKU: every store then carries its unit count of it."),
        ),
        credits=1,
    ),
    Endpoint(
        key="petsmart_store_stock",
        namespace="petsmart",
        method="store_stock",
        http="POST",
        path="/api/v1/petsmart/store-stock",
        summary=(
            "Stock of up to 20 SKUs at one PetSmart store: units for in-store pickup at that "
            "store, units to ship to home, and an alternate nearby store with its count when the "
            "store has none, plus the store's name, address, phone and pickup options. An "
            "unknown store number is a 404; an unknown SKU reads 0."
        ),
        params=(
            _req("store_id", "PetSmart store number from petsmart.stores(), e.g. '1658'."),
            _str_list("skus", "1-20 SKUs, e.g. every variant of a product.", required=True),
        ),
        credits=1,
    ),
    Endpoint(
        key="petsmart_availability",
        namespace="petsmart",
        method="availability",
        http="POST",
        path="/api/v1/petsmart/availability",
        summary=(
            "Unit counts for up to 20 PetSmart store and SKU pairs in one call, mixing stores and "
            "SKUs freely: quantity and in_stock per pair. Unknown stores or SKUs read 0."
        ),
        params=(
            Param(
                "pairs",
                "list[dict[str, str]]",
                required=True,
                doc="1-20 {'store_id': ..., 'sku': ...} pairs, e.g. [{'store_id': '1658', 'sku': '5252900'}].",
            ),
        ),
        credits=1,
    ),
    Endpoint(
        key="petsmart_deals",
        namespace="petsmart",
        method="deals",
        http="POST",
        path="/api/v1/petsmart/deals",
        summary=(
            "Products in PetSmart's Sale section, up to 40 per page, in the same shape as "
            "search(), plus the current sale events with product counts. The Sale section also "
            "holds points and Autoship promotions, so on_sale marks the rows whose price is "
            "actually reduced."
        ),
        params=(
            _lit(
                "pet",
                ("dog", "cat", "fish", "small_pet", "reptile", "bird"),
                "Only deals for this pet: dog, cat, fish, small_pet, reptile or bird.",
            ),
            _str("event", "One sale event by its exact name from a previous answer's events, e.g. 'Sale > November > Dog Sale'."),
            _str("query", "Keywords to search within the sale."),
            _int("page", "Results page, 1-based (1-100)."),
            _int("limit", "Results per page (1-40; default 40)."),
            _str("store_id", "PetSmart store number. Lists only products in stock there."),
            _lit(
                "sort",
                ("relevance", "best_sellers", "price_low", "price_high", "top_rated", "new_arrivals"),
                "relevance (default), best_sellers, price_low, price_high, top_rated or new_arrivals.",
            ),
        ),
        credits=1,
    ),
    # =============================== Petco ===============================
    # 5 endpoints, 1 credit each. Prices are national, with the Repeat
    # Delivery (autoship) price. store_inventory() takes cat_entry_id values
    # (from search or product), not part numbers. Every call can take 10-30
    # seconds, so the timeout is raised to 120s.
    Endpoint(
        key="petco_search",
        namespace="petco",
        method="search",
        http="POST",
        path="/api/v1/petco/search",
        summary=(
            "Search Petco products, 48 per page: name, brand, part_number, cat_entry_id (for "
            "store_inventory), price, list price and autoship (Repeat Delivery) price, rating, "
            "review count, fulfillment flags (pickup, same-day, autoship, in-store only), "
            "deal_group_ids and every size or flavor variation with its own prices, plus "
            "total_results, facets and matching categories. Prices are national."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-100). 48 products per page."),
            _lit(
                "sort",
                ("relevance", "price", "rating", "top_sold", "newest", "name"),
                "relevance (default), price, rating, top_sold, newest or name.",
            ),
            _lit("sort_order", ("asc", "desc"), "asc or desc. Defaults to asc for price and name, desc otherwise."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="petco_category",
        namespace="petco",
        method="category",
        http="POST",
        path="/api/v1/petco/category",
        summary=(
            "Products in a Petco category, e.g. dog/dog-food/dry-dog-food, 48 per page, in the "
            "same shape as search(). Can take 10-30 seconds. An unknown category is a 404."
        ),
        params=(
            _req(
                "path",
                "Category path ('dog/dog-food/dry-dog-food'), /category/<path>, or the petco.com URL. "
                "A result's `categories[].url` works too.",
            ),
            _int("page", "Results page, 1-based (1-100). 48 products per page."),
            _lit(
                "sort",
                ("relevance", "price", "rating", "top_sold", "newest", "name"),
                "relevance (default), price, rating, top_sold, newest or name.",
            ),
            _lit("sort_order", ("asc", "desc"), "asc or desc. Defaults to asc for price and name, desc otherwise."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="petco_product",
        namespace="petco",
        method="product",
        http="POST",
        path="/api/v1/petco/product",
        summary=(
            "One Petco product by part number or URL, with every variant (size, flavor): "
            "cat_entry_id, part number, SKU, UPC, price, list price, autoship price, "
            "first-autoship price, online quantity and status, fulfillment flags, ingredients, "
            "guaranteed analysis, directions, specifications, dimensions and images, plus brand, "
            "rating, review count and breadcrumbs. Prices are national. Can take 10-30 seconds. "
            "An unknown product is a 404."
        ),
        params=(
            _str("part_number", "Petco part number, a search result's `part_number`, e.g. '3748364'. Pass this or url."),
            _str("url", "Petco product page URL (a search result's `url`). Answers faster than part_number."),
        ),
        one_of=(("part_number", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="petco_stores",
        namespace="petco",
        method="stores",
        http="POST",
        path="/api/v1/petco/stores",
        summary=(
            "Petco stores nearest a US ZIP code (up to 10): store_id (for store_inventory), store "
            "number, name, address, phone, coordinates, distance in miles, in-store pickup and "
            "opening hours per weekday."
        ),
        params=(
            _req("zip", "US ZIP code to search around, e.g. '10001'."),
            _int("limit", "Stores to return, nearest first (1-10; default 5)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="petco_store_inventory",
        namespace="petco",
        method="store_inventory",
        http="POST",
        path="/api/v1/petco/store-inventory",
        summary=(
            "Units on hand at one Petco store for up to 10 products: qty_available, alert_level "
            "(GREEN, YELLOW, RED) and in_stock per cat_entry_id. Pass store_id, or zip to use "
            "the nearest store. Takes catalog entry ids, not part numbers; one unknown id makes "
            "the whole answer a 404."
        ),
        params=(
            _str_list(
                "cat_entry_ids",
                "1-10 catalog entry ids: the `cat_entry_id` of a search result, variation or product variant. Not the part number.",
                required=True,
            ),
            _str("store_id", "Petco store id, the `store_id` of petco.stores() (not the store number). Pass this or zip."),
            _str("zip", "US ZIP code: stock is read at the nearest store, returned as `store`."),
        ),
        one_of=(("store_id", "zip"),),
        credits=1,
        min_timeout=120.0,
    ),
    # =============================== iHerb ===============================
    # 4 endpoints, 2 credits each. Online only (no stores), US store in USD.
    # reviews() is the rating summary, star histogram and the top positive
    # and top critical review, not a full review list.
    Endpoint(
        key="iherb_search",
        namespace="iherb",
        method="search",
        http="POST",
        path="/api/v1/iherb/search",
        summary=(
            "Search iHerb (US store, USD), 48 products per page: product_id, part_number, name, "
            "brand, brand_code, URL, image, price, list price, original price and discount when "
            "discounted, rating, review count, in_stock, badges and recent_sales, plus "
            "total_results and brand_filters for narrowing with brand_code."
        ),
        params=(
            _req("query", "Search keywords (1-200 characters)."),
            _int("page", "Results page, 1-based (1-500). 48 results per page."),
            _lit(
                "sort",
                ("relevance", "best_selling", "rating", "price_asc", "price_desc", "newest", "percent_off", "review_count"),
                "relevance, best_selling, rating, price_asc, price_desc, newest, percent_off "
                "(highest discount first) or review_count. Defaults to iHerb's featured order.",
            ),
            _str("brand_code", "Only this brand by iHerb brand code, e.g. 'CGN' or 'NOW' (a result's brand_code)."),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="iherb_product",
        namespace="iherb",
        method="product",
        http="POST",
        path="/api/v1/iherb/product",
        summary=(
            "One iHerb product (US store, USD): name, brand, part number, UPC, price, list "
            "price, discount, price per serving or unit, stock status, quantity limit, "
            "expiration date, package quantity, weight and dimensions, rating, review count, "
            "breadcrumbs, best-seller rankings, badges, variants (size, potency, flavor) with "
            "their product ids, supplement facts, description, suggested use, ingredients, "
            "warnings and images. An unknown product id is a 404."
        ),
        params=(
            _str_or_int("product_id", "iHerb product id, the number at the end of an iherb.com/pr/ URL, e.g. '62118'. Pass this or url."),
            _str("url", "An iherb.com product URL. Data is always the US store's, whatever the URL's country."),
        ),
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="iherb_prices",
        namespace="iherb",
        method="prices",
        http="POST",
        path="/api/v1/iherb/prices",
        summary=(
            "Current price, list price, discount, in-stock flag, rating and review count for up "
            "to 50 iHerb products in one call (US store, USD). One row per id in request order; "
            "unknown ids come back with found False and are listed in not_found."
        ),
        params=(
            Param(
                "product_ids",
                "list[Union[str, int]]",
                required=True,
                doc="1-50 iHerb product ids, e.g. ['62118', '70316']. Duplicates are answered once.",
            ),
        ),
        credits=2,
    ),
    Endpoint(
        key="iherb_reviews",
        namespace="iherb",
        method="reviews",
        http="POST",
        path="/api/v1/iherb/reviews",
        summary=(
            "The review summary of one iHerb product: average rating, review count, star "
            "histogram (count and percent per star), review counts per language, and the full "
            "text of the top positive and top critical review. Not a full review list."
        ),
        params=(
            _str_or_int("product_id", "iHerb product id, e.g. '62118'. Pass this or url."),
            _str("url", "An iherb.com product URL."),
        ),
        one_of=(("product_id", "url"),),
        credits=2,
    ),
    # =============================== Chewy ===============================
    # 2 endpoints, 10 credits each. One-time vs Autoship vs first-Autoship
    # price, MAP fields and ratings. A search Chewy sends to a category page
    # comes back with `redirect`. No stores.
    Endpoint(
        key="chewy_search",
        namespace="chewy",
        method="search",
        http="POST",
        path="/api/v1/chewy/search",
        summary=(
            "Search Chewy by keyword, or browse a category, 36 per page: one-time, offer and "
            "strike-through price, Autoship price and discount, per-unit price, rating, rating "
            "count, in_stock, deal, new, "
            "exclusive and prescription flags, brand, image and URL. Sponsored listings are "
            "removed. The first-Autoship price, discount and savings cap are filled only on "
            "Autoship-deal rows; product always has them and MAP. When Chewy sends a query to a "
            "category, `redirect` names that category and the results are its products."
        ),
        params=(
            _str("query", "Search keywords (1-200 characters). Pass this or category_id."),
            _str("category_id", "Category to browse: the number at the end of a chewy.com /b/ URL (332 is Dog Food), or that URL."),
            _int("page", "Results page, 1-based (1-100). 36 results per page."),
            _lit(
                "sort",
                ("relevance", "bestselling", "newest", "price_low", "price_high", "rating", "most_reviewed"),
                "relevance (default), bestselling, newest, price_low, price_high, rating or most_reviewed.",
            ),
        ),
        one_of=(("query", "category_id"),),
        credits=10,
    ),
    Endpoint(
        key="chewy_product",
        namespace="chewy",
        method="product",
        http="POST",
        path="/api/v1/chewy/product",
        summary=(
            "One Chewy product: one-time, offer, list and strike-through price with savings, MAP "
            "price and whether it is enforced, Autoship price and discount, first-Autoship price, "
            "discount and savings cap, per-unit price, in_stock, rating, rating count, review "
            "count and star distribution, brand, GTIN, description, key benefits, "
            "specifications, breadcrumbs, images, promotions and every variant with its own "
            "price, Autoship price and stock. An unknown product id is a 404."
        ),
        params=(
            _str("product_id", "Chewy product id: the number after /dp/ in a product URL, e.g. '128666'. Pass this or url."),
            _str("url", "A chewy.com product URL."),
        ),
        one_of=(("product_id", "url"),),
        credits=10,
    ),
    # ============================== Menards ==============================
    # 3 endpoints. search() is always at one store (store_id required, 2
    # credits, 40 products a page). Prices carry the mail-in rebate (often 11%)
    # and the final price after it. product()'s store_id adds that store's
    # stock quantity and aisle and costs 2 credits instead of 1; it can take
    # 10-40 seconds, so product()'s timeout is raised to 120s.
    Endpoint(
        key="menards_search",
        namespace="menards",
        method="search",
        http="POST",
        path="/api/v1/menards/search",
        summary=(
            "Search menards.com at one store, 40 products a page: item id, SKU, name, URL, image, "
            "price, everyday price, sale price, price type (regular, sale, clearance, "
            "minimum_advertised), mail-in rebates, final price after rebates, and that store's "
            "stock quantity, stock message, pickup and delivery flags. Also total results, "
            "total pages and facets. An unknown store number is a 400."
        ),
        params=(
            _req("query", "Search keywords, e.g. 'sledge hammer'."),
            _req("store_id", "Menards store number from menards.stores(), e.g. '3181'. Stock is that store's."),
            _int("page", "Results page, 1-based, 40 products a page. Defaults to 1."),
            _lit("sort", ("relevance", "price_asc", "price_desc", "brand_asc", "brand_desc"),
                 "Result order. Defaults to relevance. Price sorts order by everyday_price, not the sale price."),
            _bool("in_stock_today", "Only products in stock at the store today."),
            _float("min_price", "Lowest price in dollars."),
            _float("max_price", "Highest price in dollars."),
        ),
        credits=2,
        # Usually a few seconds, but slow spells reach 30+ s; the API waits up to 40.
        min_timeout=60.0,
    ),
    Endpoint(
        key="menards_product",
        namespace="menards",
        method="product",
        http="POST",
        path="/api/v1/menards/product",
        summary=(
            "One Menards product by item id or URL: name, brand, model number, SKU, description, "
            "bullets, specifications, images, videos and documents, with everyday price, sale "
            "price and end date, mail-in rebates (text, amount, dates), final price after "
            "rebates and you-save amount, plus pickup, delivery and ship-to-store flags. With "
            "store_id, that store's stock quantity, stock message and aisle location (10-40 "
            "seconds); without it prices are the default store's and there is no stock. An "
            "unknown item id or store number is a 404."
        ),
        params=(
            _str("item_id", "Menards item id: the number after p- in a menards.com product URL. Not the SKU or model number. Pass this or url."),
            _str("url", "A menards.com product URL."),
            _str("store_id", "Menards store number from menards.stores(), e.g. '3181'. Adds stock and aisle; costs 2 credits."),
        ),
        one_of=(("item_id", "url"),),
        credits=1,
        credits_note="Costs 1 credit, or 2 when store_id is set.",
        min_timeout=120.0,
    ),
    Endpoint(
        key="menards_stores",
        namespace="menards",
        method="stores",
        http="POST",
        path="/api/v1/menards/stores",
        summary=(
            "Menards stores near a US ZIP code or a city and state, nearest first: store_id, "
            "name, address, coordinates, distance in miles, open flag and services (garden "
            "center, grocery, rental center, propane...)."
        ),
        params=(
            _str("zip", "US ZIP code, e.g. '55401'. Pass this, or city and state."),
            _str("city", "City to search around; pass with state."),
            _str("state", "2-letter US state code; pass with city."),
        ),
        one_of=(("zip", "city"),),
        credits=1,
    ),
    # ============================= Nordstrom =============================
    # 8 endpoints, 5 credits each except availability (10: the product page plus
    # the store lookup) and reviews (10: one browser render). nordstrom.com
    # (US). product() quantity is units available to ship; availability() adds
    # the pickup stores per sku (yes/no per store, quantities are chain-wide).
    # The upstream page can take ~15 s and is retried once on a block page.
    # reviews() takes 20-60 s, up to ~100 s at max_reviews 200, so its floor is
    # 150 s rather than the namespace's 120 s.
    Endpoint(
        key="nordstrom_search",
        namespace="nordstrom",
        method="search",
        http="POST",
        path="/api/v1/nordstrom/search",
        summary=(
            "Search nordstrom.com (US) products, 24 per page, sorted by relevance, rating, price, "
            "newest or percent off. Each result has style id, URL, name, brand, image, current "
            "price and price range in dollars, original price range, percent off and on-sale "
            "flag, rating, review count, badges such as new or new_markdown, a low-inventory "
            "flag, whether it is sold by a marketplace seller (and the seller's name), and every "
            "color with its color family and image. Also returns the total result count and page "
            "count. Use a result's url or style_id with product()."
        ),
        params=(
            _req("query", "Search keywords."),
            _int("page", "Results page, 1-based. Defaults to 1. 24 products per page."),
            _lit(
                "sort",
                ("relevance", "rating", "price_high", "price_low", "newest", "percent_off"),
                "relevance (default), rating, price_high, price_low, newest or percent_off.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_product",
        namespace="nordstrom",
        method="product",
        http="POST",
        path="/api/v1/nordstrom/product",
        summary=(
            "One nordstrom.com (US) product by URL or style id: name, brand, description, feature "
            "bullets, fit notes, final-sale flag, current, original and clearance price ranges, "
            "percent off, rating, review count, the star histogram, the size-fit distribution "
            "(too small to too big), the AI review summary when the site shows one, the most "
            "mentioned praised and criticized features with a quote each, breadcrumbs and "
            "images. Every color lists its images and every size as a sku with sku id, size, size "
            "type, UPC, price, original price, percent off, price type (regular, clearance, "
            "promotion), in_stock and the quantity available to ship. in_stock is true when the "
            "sku can be shipped or picked up in a store, so a sku held only in a store reads in "
            "stock with quantity 0 (availability() lists its pickup stores). Includes the reviews "
            "shown on the product page (up to about 13), with the total review count; each review "
            "has title, text, rating, size rating, author, date, helpful votes and "
            "verified-purchase flag (reviews() pages the full review history). An unknown style "
            "id is a 404."
        ),
        params=(
            _str("url", "nordstrom.com product URL (the `url` of a search result)."),
            _str(
                "style_id",
                "Nordstrom style id, the number at the end of a product URL (the `style_id` of a "
                "search result). Used when url is not given.",
            ),
        ),
        one_of=(("url", "style_id"),),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_category",
        namespace="nordstrom",
        method="category",
        http="POST",
        path="/api/v1/nordstrom/category",
        summary=(
            "Browse a nordstrom.com (US) category page, 24 products per page, sorted by relevance, "
            "rating, price, newest or percent off. Works on any /browse category, including sale "
            "(sale/women), new arrivals (/browse/new) and top-level departments (/browse/women). "
            "Returns the category's name, page title, path, URL, breadcrumbs and subcategories "
            "(name and path, for drilling down). Each product has the same fields as a search result: style id, URL, name, "
            "brand, image, current price and price range in dollars, original price range, percent "
            "off and on-sale flag, rating, review count, badges, a low-inventory flag, marketplace "
            "seller and every color. Also returns the total result count, page count, and the "
            "filter sidebar: each filter group (Product Type > Clothing, Size > Women's Clothing, "
            "Color, Brand, Discount...) with its options and product counts (price buckets carry no "
            "count on the site, so theirs are null; groups with more than 100 options, such as "
            "Brand, list the 100 with the most products and give the full option_count). An unknown category is a 404."
        ),
        params=(
            _req(
                "category",
                "A nordstrom.com category: the /browse path or full URL of a category page, e.g. "
                "/browse/women/clothing/dresses, sale/women, /browse/new or "
                "https://www.nordstrom.com/browse/men/shoes. The /browse prefix is optional. Query "
                "parameters in a URL (filters) are ignored. Each result's category.subcategories "
                "lists child paths.",
            ),
            _int("page", "Results page, 1-based. Defaults to 1. 24 products per page."),
            _lit(
                "sort",
                ("relevance", "rating", "price_high", "price_low", "newest", "percent_off"),
                "relevance (default), rating, price_high, price_low, newest or percent_off.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_brand",
        namespace="nordstrom",
        method="brand",
        http="POST",
        path="/api/v1/nordstrom/brand",
        summary=(
            "List a brand's products on nordstrom.com (US) from its brand page, 24 per page, sorted "
            "by relevance, rating, price, newest or percent off. Returns the brand's name, path, "
            "URL, breadcrumbs and sub-pages (Women, Men, Kids...). Each product has the same fields as a search result: style id, URL, name, "
            "brand, image, current price and price range in dollars, original price range, percent "
            "off and on-sale flag, rating, review count, badges, a low-inventory flag, marketplace "
            "seller and every color. Also returns the total result count, page count, and the "
            "filter sidebar: each filter group (Product Type > Clothing, Size > Women's Clothing, "
            "Color, Brand, Discount...) with its options and product counts (price buckets carry no "
            "count on the site, so theirs are null; groups with more than 100 options, such as "
            "Brand, list the 100 with the most products and give the full option_count). An unknown brand is a "
            "404."
        ),
        params=(
            _req(
                "brand",
                "A nordstrom.com brand: the /brands path or full URL of a brand page, usually ending "
                "in the brand id, e.g. /brands/astr-the-label--53360 (a product's brand_url works). "
                "A brand name without its id is a 404 except where it is the brand page's own path "
                "(/brands/ugg-australia). Sub-pages such as /brands/astr-the-label--53360/women "
                "work too.",
            ),
            _int("page", "Results page, 1-based. Defaults to 1. 24 products per page."),
            _lit(
                "sort",
                ("relevance", "rating", "price_high", "price_low", "newest", "percent_off"),
                "relevance (default), rating, price_high, price_low, newest or percent_off.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_stores",
        namespace="nordstrom",
        method="stores",
        http="POST",
        path="/api/v1/nordstrom/stores",
        summary=(
            "Find Nordstrom stores (full-line stores and Nordstrom Local) near a US ZIP code or "
            "latitude/longitude within up to 100 miles, nearest first, or look stores up by store "
            "number. Each store has store number, name, type (full_line or local), address, city, "
            "state, ZIP, country, phone, weekly hours, holiday hours when posted, open and close "
            "times for the next 8 days, time zone, distance in miles, latitude and longitude, "
            "whether it offers buy-online pickup and curbside pickup, its amenities (restaurants "
            "and services, with phone and hours) and its store page URL. A ZIP with no store in "
            "range returns an empty list."
        ),
        params=(
            _str(
                "zip",
                "US ZIP code to search around. Pass exactly one of zip, latitude and longitude, or "
                "store_numbers.",
            ),
            _float("latitude", "Latitude to search around (with longitude)."),
            _float("longitude", "Longitude to search around (with latitude)."),
            Param(
                "store_numbers",
                "Optional[Union[str, list[Union[str, int]]]]",
                doc="Look up stores by number instead of location: a list or a comma-separated "
                "string, up to 100 (an availability result's pickup_stores[].store_number).",
            ),
            _int(
                "distance_miles",
                "Search radius in miles around zip or latitude/longitude, 1-100 (the site's "
                "maximum). Defaults to 100.",
            ),
        ),
        # "At least one" here; the server rejects any mix of the three.
        one_of=(("zip", "latitude", "longitude", "store_numbers"),),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_availability",
        namespace="nordstrom",
        method="availability",
        http="POST",
        path="/api/v1/nordstrom/availability",
        summary=(
            "Online and store-pickup availability for every size and color of one nordstrom.com "
            "(US) product, by URL or style id, optionally one sku. Each sku has sku id, size, "
            "color, UPC, in_stock, whether it ships and the quantity available to ship, the "
            "quantity available for pickup, and the stores where it can be picked up (store "
            "number, name, address, city, state, ZIP, phone). Quantities are chain-wide: per store "
            "Nordstrom only says whether pickup is available, not how many. in_stock is true when "
            "the sku can be shipped or picked up, so a sku with ship_quantity 0 can still be in "
            "stock for pickup. Costs 10 credits (the product page plus the store lookup). An "
            "unknown style id or sku id is a 404."
        ),
        params=(
            _str(
                "url",
                "nordstrom.com product URL (the `url` of a search, category or brand result).",
            ),
            _str("style_id", "Nordstrom style id, used when url is not given."),
            _str(
                "sku_id",
                "Only this sku (a product's colors[].skus[].sku_id). An id that is not a sku of the "
                "product is a 404.",
            ),
        ),
        one_of=(("url", "style_id"),),
        credits=10,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_suggestions",
        namespace="nordstrom",
        method="suggestions",
        http="POST",
        path="/api/v1/nordstrom/suggestions",
        summary=(
            "The search-box autocomplete of nordstrom.com: the queries Nordstrom suggests for a "
            "partial search term, most likely first (e.g. \"dre\" -> women's dresses, dresses, "
            "cocktail dresses for women). Useful for keyword research and for building queries "
            "for search()."
        ),
        params=(
            _req("query", "What the shopper has typed so far."),
            _int(
                "limit",
                "Suggestions to return, 1-20. Defaults to 8. The site may return fewer.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_reviews",
        namespace="nordstrom",
        method="reviews",
        http="POST",
        path="/api/v1/nordstrom/reviews",
        summary=(
            "Customer reviews of one nordstrom.com (US) product by URL or style id, up to 200 per "
            "call (default 60), sorted most helpful (default), most recent, highest rated or "
            "lowest rated, optionally filtered to star ratings, verified purchases, reviews with "
            "photos, or a text search. Returns the product's review summary (average rating, "
            "total reviews, star histogram, size rating 1 runs small to 5 runs big, width rating "
            "where the site has one, the most mentioned praised and criticized features with a "
            "quote each, and the count of rating-only reviews), the AI review summary when the "
            "site shows one, the number of reviews matching the filters (total_results), "
            "returned and has_more. Each review has id, title, text, star rating, size rating, "
            "author, date, helpful votes, verified-purchase flag, reviewer badges "
            "(verified_purchaser, top_250, top_1000), size and color purchased, the reviewer's "
            "height, weight, body type and usual sizes when given, secondary ratings (Size, with "
            "its scale), the site it was syndicated from (e.g. nordstromrack.com) and photos with "
            "thumbnails. Rating-only reviews are included with title and text null. Takes "
            "20-60s, up to about 100s at max_reviews 200. A product with no reviews returns an "
            "empty list; an unknown style id is a 404."
        ),
        params=(
            _str(
                "url",
                "nordstrom.com product URL (the `url` of a search, category or brand result).",
            ),
            _str("style_id", "Nordstrom style id, used when url is not given."),
            _lit(
                "sort",
                ("most_helpful", "most_recent", "highest_rated", "lowest_rated"),
                "most_helpful (default), most_recent, highest_rated or lowest_rated. Cannot be "
                "combined with search: Nordstrom returns review search results in its own order.",
            ),
            _ilit_list(
                "stars",
                (1, 2, 3, 4, 5),
                "Only reviews with these star ratings, e.g. [1, 2] for the critical ones.",
            ),
            _bool("verified_only", "Only reviews from verified purchasers."),
            _bool("with_photos", "Only reviews that include customer photos."),
            _str(
                "search",
                "Only reviews mentioning this text (the review search box), 1-100 characters. "
                "Results come in Nordstrom's search order, so sort cannot be set with it.",
            ),
            _int(
                "max_reviews",
                "Reviews to return, 1-200. Defaults to 60. Larger values take longer (45-100s "
                "for 200).",
            ),
        ),
        one_of=(("url", "style_id"),),
        credits=10,
        min_timeout=150.0,
    ),
    # ========================== Nordstrom Rack ===========================
    # nordstromrack.com (US), a separate platform from nordstrom.com with the
    # same request shapes and credit costs: 8 endpoints, 5 credits each except
    # availability (10) and reviews (10). category() takes Rack's /shop and
    # /clearance paths (Clear the Rack, flash events /shop/flash/event-N); brand()
    # takes /brands/<slug> with no id. Stores are Rack stores only and reviews
    # are Rack's own pool. Same timeout floors as nordstrom: 120 s, reviews 150 s
    # (15-60 s typical, up to ~100 s at max_reviews 200).
    Endpoint(
        key="nordstrom_rack_search",
        namespace="nordstrom_rack",
        method="search",
        http="POST",
        path="/api/v1/nordstromrack/search",
        summary=(
            "Search nordstromrack.com (US) products, 24 per page, sorted by relevance, rating, "
            "price, newest or percent off. Each result has style id, URL, name, brand, image, "
            "current price and price range in dollars, the compare-at price range Rack strikes "
            "through, percent off and on-sale flag, the clearance price range, and any promotion "
            "on top (promotion_price_range, and promotion_percent_off: the extra percent off the "
            "clearance price during Clear the Rack, otherwise off Rack's regular price), rating, "
            "review count (Rack's own reviews), badges such as new_markdown or final_sale, a "
            "low-inventory flag, whether it is sold by a marketplace seller (and the seller's "
            "name), and every color with its color family and image. Also returns the total "
            "result count and page count. Use a result's url or style_id with product()."
        ),
        params=(
            _req("query", "Search keywords."),
            _int("page", "Results page, 1-based. Defaults to 1. 24 products per page."),
            _lit(
                "sort",
                ("relevance", "rating", "price_high", "price_low", "newest", "percent_off"),
                "relevance (default), rating, price_high, price_low, newest or percent_off.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_product",
        namespace="nordstrom_rack",
        method="product",
        http="POST",
        path="/api/v1/nordstromrack/product",
        summary=(
            "One nordstromrack.com (US) product by URL or style id: name, brand, brand page URL, "
            "description, feature bullets, fit notes, final-sale flag, current, compare-at and "
            "clearance price ranges, percent off, any promotion on top (promotion_price_range and "
            "promotion_percent_off, e.g. Clear the Rack's extra 25% off clearance), rating, "
            "review count, the star histogram, the size-fit distribution (too small to too big), "
            "the AI review summary when the site shows one, the most mentioned praised and "
            "criticized features with a quote each, breadcrumbs and images. Every color lists its "
            "images and every size as a sku with sku id, size, size type, UPC, price, compare-at "
            "price, percent off, price type (regular, clearance, promotion), in_stock and the "
            "quantity available to ship. in_stock is true when the sku can be shipped or picked "
            "up in a Rack store, so a sku held only in a store reads in stock with quantity 0 "
            "(availability() lists its pickup stores). Includes the reviews shown on the product "
            "page (up to about 13), with the total review count; each review has title, text, "
            "rating, size rating, author, date, helpful votes and verified-purchase flag "
            "(reviews() pages the full review history). Ratings and reviews are Rack's own, "
            "separate from nordstrom.com's. An unknown style id is a 404."
        ),
        params=(
            _str(
                "url",
                "nordstromrack.com product URL (the `url` of a search, category or brand result).",
            ),
            _str(
                "style_id",
                "Nordstrom Rack style id, the number at the end of a product URL (a result's "
                "`style_id`). Used when url is not given.",
            ),
        ),
        one_of=(("url", "style_id"),),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_category",
        namespace="nordstrom_rack",
        method="category",
        http="POST",
        path="/api/v1/nordstromrack/category",
        summary=(
            "Browse a nordstromrack.com (US) category page, 24 products per page, sorted by "
            "relevance, rating, price, newest or percent off. Works on every /shop and /clearance "
            "listing: departments (/shop/women), deals (/shop/deals/black-friday), new arrivals "
            "(/shop/new-arrivals), Clear the Rack (/clearance, /clearance/women/clothing) and "
            "flash events: /shop/flash lists the live events as subcategories (it has no products "
            "of its own), and each event (/shop/flash/event-7) is a listing whose first page "
            "shows the event's featured products first, then the rest, with positions running "
            "on. Returns the category's name, page title, path, URL, breadcrumbs and "
            "subcategories (name and path, for drilling down). Each product has the same fields "
            "as a search result, including the clearance and promotion price ranges. Also "
            "returns the total result count, page count, and the filter sidebar: each filter "
            "group (Product Type, Size, Color, Brand, Price...) with its options and product "
            "counts (price buckets carry no count on the site, so theirs are null; groups with "
            "more than 100 options, such as Brand, list the 100 with the most products and give "
            "the full option_count). An unknown category is a 404."
        ),
        params=(
            _req(
                "category",
                "A nordstromrack.com category: the /shop or /clearance path or full URL of a "
                "category page, e.g. /shop/women/clothing/dresses, /shop/deals/black-friday, "
                "/shop/new-arrivals, /clearance, /clearance/women/clothing, /shop/flash or a flash "
                "event such as /shop/flash/event-7. A path without a prefix "
                "(women/clothing/dresses) is read as /shop/... . Query parameters in a URL "
                "(filters) are ignored. Each result's category.subcategories lists child paths.",
            ),
            _int("page", "Results page, 1-based. Defaults to 1. 24 products per page."),
            _lit(
                "sort",
                ("relevance", "rating", "price_high", "price_low", "newest", "percent_off"),
                "relevance (default), rating, price_high, price_low, newest or percent_off.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_brand",
        namespace="nordstrom_rack",
        method="brand",
        http="POST",
        path="/api/v1/nordstromrack/brand",
        summary=(
            "List a brand's products on nordstromrack.com (US) from its brand page "
            "(/brands/adidas), 24 per page, sorted by relevance, rating, price, newest or percent "
            "off. Returns the brand's name, path, URL and breadcrumbs. Each product has the same "
            "fields as a search result, including the clearance and promotion price ranges. Also "
            "returns the total result count, page count, and the filter sidebar (filter groups "
            "with their options and product counts; groups with more than 100 options list the "
            "100 with the most products and give the full option_count). An unknown brand is a "
            "404."
        ),
        params=(
            _req(
                "brand",
                "A nordstromrack.com brand: the /brands path or full URL of a brand page, e.g. "
                "/brands/adidas, /brands/sam-edelman or https://www.nordstromrack.com/brands/ugg "
                "(a product's brand_url works). The /brands prefix is optional. Rack brand pages "
                "carry no brand id: the nordstrom.com form /brands/<name>--<id> is a 404 here.",
            ),
            _int("page", "Results page, 1-based. Defaults to 1. 24 products per page."),
            _lit(
                "sort",
                ("relevance", "rating", "price_high", "price_low", "newest", "percent_off"),
                "relevance (default), rating, price_high, price_low, newest or percent_off.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_stores",
        namespace="nordstrom_rack",
        method="stores",
        http="POST",
        path="/api/v1/nordstromrack/stores",
        summary=(
            "Find Nordstrom Rack stores near a US ZIP code or latitude/longitude within up to 100 "
            "miles, nearest first, or look Rack stores up by store number. Each store has store "
            "number, name, type (rack), address, city, state, ZIP, country, phone, weekly hours, "
            "holiday hours when posted, open and close times for the next 8 days, time zone, "
            "distance in miles, latitude and longitude, whether it offers buy-online pickup and "
            "curbside pickup, its amenities and its store page URL. A ZIP with no store in range "
            "returns an empty list."
        ),
        params=(
            _str(
                "zip",
                "US ZIP code to search around. Pass exactly one of zip, latitude and longitude, or "
                "store_numbers.",
            ),
            _float("latitude", "Latitude to search around (with longitude)."),
            _float("longitude", "Longitude to search around (with latitude)."),
            Param(
                "store_numbers",
                "Optional[Union[str, list[Union[str, int]]]]",
                doc="Look up Rack stores by number instead of location: a list or a "
                "comma-separated string, up to 100 (an availability result's "
                "pickup_stores[].store_number). Numbers of Nordstrom full-line stores are left "
                "out.",
            ),
            _int(
                "distance_miles",
                "Search radius in miles around zip or latitude/longitude, 1-100 (the site's "
                "maximum). Defaults to 100.",
            ),
        ),
        # "At least one" here; the server rejects any mix of the three.
        one_of=(("zip", "latitude", "longitude", "store_numbers"),),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_availability",
        namespace="nordstrom_rack",
        method="availability",
        http="POST",
        path="/api/v1/nordstromrack/availability",
        summary=(
            "Online and Rack store-pickup availability for every size and color of one "
            "nordstromrack.com (US) product, by URL or style id, optionally one sku. Each sku has "
            "sku id, size, color, UPC, in_stock, whether it ships and the quantity available to "
            "ship, the quantity available for pickup, and the Rack stores where it can be picked "
            "up (store number, name, address, city, state, ZIP, phone). Quantities are "
            "chain-wide: per store the site only says whether pickup is available, not how many. "
            "in_stock is true when the sku can be shipped or picked up, so a sku with "
            "ship_quantity 0 can still be in stock for pickup. Costs 10 credits (the product page "
            "plus the store lookup). An unknown style id or sku id is a 404."
        ),
        params=(
            _str(
                "url",
                "nordstromrack.com product URL (the `url` of a search, category or brand result).",
            ),
            _str("style_id", "Nordstrom Rack style id, used when url is not given."),
            _str(
                "sku_id",
                "Only this sku (a product's colors[].skus[].sku_id). An id that is not a sku of the "
                "product is a 404.",
            ),
        ),
        one_of=(("url", "style_id"),),
        credits=10,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_suggestions",
        namespace="nordstrom_rack",
        method="suggestions",
        http="POST",
        path="/api/v1/nordstromrack/suggestions",
        summary=(
            "The search-box autocomplete of nordstromrack.com: the queries Nordstrom Rack "
            "suggests for a partial search term, most likely first (e.g. \"dre\" -> dresses for "
            "women, dress, barefoot dreams, sweater dress). Useful for keyword research and for "
            "building queries for search()."
        ),
        params=(
            _req("query", "What the shopper has typed so far."),
            _int(
                "limit",
                "Suggestions to return, 1-20. Defaults to 8. The site may return fewer.",
            ),
        ),
        credits=5,
        min_timeout=120.0,
    ),
    Endpoint(
        key="nordstrom_rack_reviews",
        namespace="nordstrom_rack",
        method="reviews",
        http="POST",
        path="/api/v1/nordstromrack/reviews",
        summary=(
            "Customer reviews of one nordstromrack.com (US) product by URL or style id, up to 200 "
            "per call (default 60), sorted most helpful (default), most recent, highest rated or "
            "lowest rated, optionally filtered to star ratings, verified purchases, reviews with "
            "photos, or a text search. Rack has its own review pool, separate from "
            "nordstrom.com's. Returns the product's review summary (average rating, total "
            "reviews, star histogram, size rating 1 runs small to 5 runs big, width rating where "
            "the site has one, the most mentioned praised and criticized features with a quote "
            "each, and the count of rating-only reviews), the AI review summary when the site "
            "shows one, the number of reviews matching the filters (total_results), returned and "
            "has_more. Each review has id, title, text, star rating, size rating, author, date, "
            "helpful votes, verified-purchase flag, reviewer badges, size and color purchased, "
            "the reviewer's height, weight, body type and usual sizes when given, secondary "
            "ratings, the site it was syndicated from (e.g. a brand's own site) and photos with "
            "thumbnails. Rating-only reviews are included with title and text null. Takes "
            "15-60s, up to about 100s at max_reviews 200. A product with no reviews returns an "
            "empty list; an unknown style id is a 404."
        ),
        params=(
            _str(
                "url",
                "nordstromrack.com product URL (the `url` of a search, category or brand result).",
            ),
            _str("style_id", "Nordstrom Rack style id, used when url is not given."),
            _lit(
                "sort",
                ("most_helpful", "most_recent", "highest_rated", "lowest_rated"),
                "most_helpful (default), most_recent, highest_rated or lowest_rated. Cannot be "
                "combined with search: Nordstrom Rack returns review search results in its own "
                "order.",
            ),
            _ilit_list(
                "stars",
                (1, 2, 3, 4, 5),
                "Only reviews with these star ratings, e.g. [1, 2] for the critical ones.",
            ),
            _bool("verified_only", "Only reviews from verified purchasers."),
            _bool("with_photos", "Only reviews that include customer photos."),
            _str(
                "search",
                "Only reviews mentioning this text (the review search box), 1-100 characters. "
                "Results come in the site's search order, so sort cannot be set with it.",
            ),
            _int(
                "max_reviews",
                "Reviews to return, 1-200. Defaults to 60. Larger values take longer (about "
                "50-100s for 200).",
            ),
        ),
        one_of=(("url", "style_id"),),
        credits=10,
        min_timeout=150.0,
    ),
    # ============================== Best Buy =============================
    # bestbuy.com (US only), 9 endpoints. Credits: search, product, reviews and
    # prices 2 (prices is per call, up to 15 SKUs); category 2 for an abcat id
    # and 3 for a pcmcat page (credits_note); deals 3; stores and suggestions 1;
    # availability 2 flat for up to 8 stores. product, reviews and availability
    # take sku or url; category takes category_id or url; availability takes
    # exactly one of zip or store_ids (one_of only enforces "at least one").
    # filters is a nested object on the wire, so it is a dict here. 120 s
    # timeout floor everywhere: availability alone typically takes 5-20 s.
    Endpoint(
        key="best_buy_search",
        namespace="best_buy",
        method="search",
        http="POST",
        path="/api/v1/bestbuy/search",
        summary=(
            "Search bestbuy.com (US), 18 products per page, sorted by best match, best selling, "
            "best discount, price, rating or newest, filtered by brand, on sale, clearance, open "
            "box or a price range. Each product has SKU, BSIN, name, brand, model number, URL, "
            "image, price, regular price, savings in dollars and percent, on-sale flag, deal "
            "badge (e.g. Clearance, Holiday Deal), condition (new, refurbished excellent...), "
            "rating, review count, seller type (best_buy or marketplace), product type, badges "
            "and release date. Also returns the total result count and page count, the applied "
            "sort and filters, the category, the filter sidebar (every facet with its values and "
            "product counts; category_facet values carry category ids), the sort options, "
            "related searches and any spelling correction. Sponsored tiles are left out unless "
            "include_sponsored."
        ),
        params=(
            _req("query", "Search keywords."),
            _int("page", "Results page, 1-based, up to 100. Defaults to 1. 18 products per page."),
            _lit(
                "sort",
                (
                    "best_match",
                    "best_selling",
                    "best_discount",
                    "price_low",
                    "price_high",
                    "rating",
                    "newest",
                ),
                "best_match (default), best_selling, best_discount, price_low, price_high, "
                "rating or newest.",
            ),
            _BESTBUY_FILTERS,
            _BESTBUY_INCLUDE_SPONSORED,
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_product",
        namespace="best_buy",
        method="product",
        http="POST",
        path="/api/v1/bestbuy/product",
        summary=(
            "One bestbuy.com (US) product by SKU or URL: name, brand, model, UPC, URL, status, "
            "condition, product type, category path, price, regular price, savings, on-sale "
            "flag, deal badge, financing offer, every open-box offer by condition (fair, good, "
            "excellent) with its price, savings against new and against the regular price, other "
            "sellers' and conditions' SKUs of the same product, rating, review count, the AI "
            "review summary and what customers love, description, feature list, what's "
            "included, the full specification table by group, dimensions, full-size images, "
            "manuals and badges. An unknown SKU is a 404."
        ),
        params=(_BESTBUY_SKU, _BESTBUY_URL),
        one_of=(("sku", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_reviews",
        namespace="best_buy",
        method="reviews",
        http="POST",
        path="/api/v1/bestbuy/reviews",
        summary=(
            "Customer reviews of one bestbuy.com (US) product by SKU or URL, 20 per page, "
            "sorted most relevant (default), most helpful, newest, oldest, highest or lowest "
            "rated, optionally only one star rating. Returns the review summary (average rating, "
            "review count, recommended percent, star histogram, the most mentioned pros and cons "
            "with mention counts), total_results for the filter, page count and has_more. Each "
            "review has id, title, text, rating, author, date, recommended flag, "
            "verified-purchase and incentivized flags, days of ownership, helpful and "
            "not-helpful votes, badges, photos, the site it was syndicated from and the brand's "
            "response. An unknown SKU is a 404."
        ),
        params=(
            _BESTBUY_SKU,
            _BESTBUY_URL,
            _int("page", "Reviews page, 1-based, 20 reviews per page, up to 500. Defaults to 1."),
            _lit(
                "sort",
                (
                    "most_relevant",
                    "most_helpful",
                    "newest",
                    "oldest",
                    "highest_rated",
                    "lowest_rated",
                ),
                "most_relevant (default), most_helpful, newest, oldest, highest_rated or "
                "lowest_rated.",
            ),
            _ilit("rating", (1, 2, 3, 4, 5), "Only reviews with this many stars, 1-5."),
        ),
        one_of=(("sku", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_category",
        namespace="best_buy",
        method="category",
        http="POST",
        path="/api/v1/bestbuy/category",
        summary=(
            "Browse a bestbuy.com (US) category or deals page by category id or URL, 18 products "
            "per page, sorted by best selling, best discount, price, rating or newest, with the "
            "same filters as search. Works on catalogue categories (abcat0101001 All Flat-Screen "
            "TVs) and merchandised pages such as All Electronics on Sale (pcmcat1674241939957), "
            "whose built-in filters are read from the page itself. Products and listing fields "
            "are the same as search(). An unknown category, or a page without a product grid, "
            "is a 404."
        ),
        params=(
            _str(
                "category_id",
                "Best Buy category id: abcat... (catalogue categories, e.g. abcat0101001 All "
                "Flat-Screen TVs) or pcmcat... (merchandised pages, e.g. pcmcat1674241939957 All "
                "Electronics on Sale). A search result's facets list category ids under "
                "category_facet.",
            ),
            _str(
                "url",
                "A bestbuy.com category page URL (.../<id>.c?id=<id>). Filters in the URL (qp=...) "
                "are kept; its sort is not, use sort.",
            ),
            _int("page", "Results page, 1-based, up to 100. Defaults to 1. 18 products per page."),
            _lit(
                "sort",
                ("best_selling", "best_discount", "price_low", "price_high", "rating", "newest"),
                "best_selling (the default on most pages), best_discount, price_low, price_high, "
                "rating or newest.",
            ),
            _BESTBUY_FILTERS,
            _BESTBUY_INCLUDE_SPONSORED,
        ),
        one_of=(("category_id", "url"),),
        credits=2,
        credits_note="Costs 2 credits for an abcat id and 3 for a pcmcat page (the page is read first).",
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_deals",
        namespace="best_buy",
        method="deals",
        http="POST",
        path="/api/v1/bestbuy/deals",
        summary=(
            "Today's Best Buy Deal of the Day and the more-deals row under it, with live prices: "
            "SKU, name, URL, image, rating, review count, price, regular price, savings in "
            "dollars and percent, on-sale flag and deal badge, plus the countdown end as the "
            "page shows it. Up to 15 products. No parameters."
        ),
        params=(),
        credits=3,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_stores",
        namespace="best_buy",
        method="stores",
        http="POST",
        path="/api/v1/bestbuy/stores",
        summary=(
            "Best Buy stores near a US ZIP code, nearest first (up to 15): store id, name, "
            "address, city, state, ZIP, phone, open status, store type, distance in miles, and "
            "dated opening hours for the next 35 days (holiday hours and closed days included). "
            "Use a store_id with availability()."
        ),
        params=(_req("zip", "US ZIP code, e.g. '94103'."),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_availability",
        namespace="best_buy",
        method="availability",
        http="POST",
        path="/api/v1/bestbuy/availability",
        summary=(
            "Store pickup availability of one bestbuy.com SKU at up to 8 stores: the stores "
            "nearest a ZIP code or the store ids you pass. Each store has a status: in_stock, "
            "limited (with the real quantity when Best Buy shows \"only N left\"), ship_to_store "
            "(not on the shelf; can be shipped there for pickup by pickup_date), out_of_stock, "
            "not_available_for_pickup, or unknown (with a reason, when the store's answer did not "
            "include this SKU; never reported as out of stock). Also the pickup date, the minimum "
            "hours until pickup, and the nearby store Best Buy suggests when this one cannot "
            "fill it. Best Buy does not publish unit counts for well-stocked items, so quantity "
            "is null for in_stock. Takes 5-20s. Costs 2 credits flat. An unknown SKU is a 404."
        ),
        params=(
            _BESTBUY_SKU,
            _BESTBUY_URL,
            _str(
                "zip",
                "Check the stores nearest this US ZIP code (max_stores of them). Pass exactly one "
                "of zip or store_ids.",
            ),
            _int(
                "max_stores",
                "With zip: how many of the nearest stores to check, 1-8. Defaults to 5.",
            ),
            _str_or_list(
                "store_ids",
                "Check these stores instead (store numbers, a stores() result's store_id), up to "
                "8: a list or a comma-separated string.",
            ),
        ),
        # sku or url, and (at least) one of zip or store_ids; the server rejects both.
        one_of=(("sku", "url"), ("zip", "store_ids")),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_suggestions",
        namespace="best_buy",
        method="suggestions",
        http="POST",
        path="/api/v1/bestbuy/suggestions",
        summary=(
            "The bestbuy.com search-box autocomplete for a partial query (e.g. \"ps5 con\"): "
            "suggested search terms, each with the categories (id and name) and SKUs Best Buy "
            "shows for it, plus any spelling correction."
        ),
        params=(_req("query", "What the shopper has typed so far."),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="best_buy_prices",
        namespace="best_buy",
        method="prices",
        http="POST",
        path="/api/v1/bestbuy/prices",
        summary=(
            "Current bestbuy.com prices for up to 15 SKUs in one call: price, regular price, "
            "savings in dollars and percent, on-sale flag, deal badge and deal end time per SKU. "
            "A SKU Best Buy does not know comes back found: false; all unknown is a 404. Costs 2 "
            "credits per call, whatever the number of SKUs."
        ),
        params=(
            Param(
                "skus",
                "Union[str, list[str]]",
                required=True,
                doc="1-15 Best Buy SKUs, a list or a comma-separated string, e.g. "
                "['6607832', '6673112'].",
            ),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    # ============================== TCGplayer ============================
    # tcgplayer.com (US marketplace, USD), 13 endpoints, 1 credit each.
    # product, listings, price_history and sales take product_id or url
    # (one_of). search needs query unless game or set is given (server-side
    # rule; query is an optional positional here). 120 s timeout floor, like
    # the other retail namespaces.
    Endpoint(
        key="tcgplayer_search",
        namespace="tcgplayer",
        method="search",
        http="POST",
        path="/api/v1/tcgplayer/search",
        summary=(
            "Search TCGplayer (US marketplace, USD) for trading cards and sealed products across "
            "every game (Pokemon, Magic: The Gathering, Yu-Gi-Oh!, One Piece, Lorcana and 60+ "
            "more), up to 50 per page, sorted by relevance, best match, best selling, name or "
            "market price, filtered by game, set, rarity and cards vs sealed. query is optional "
            "when game or set is given, to browse it. Each product has " + _TCG_PRODUCT_FIELDS + ", "
            "plus up to 3 featured live listings (price, shipping, condition, printing, seller). "
            "Also returns total_results, has_more and the filter facets with counts; a facet's "
            "url_value is what game and set accept."
        ),
        params=(
            Param(
                "query",
                "Optional[str]",
                positional=True,
                doc="Search keywords, e.g. 'charizard'. Optional when game or set is given.",
            ),
            _TCG_GAME,
            _str(
                "set",
                "Only this set, by url_name from sets() (or a set facet's url_value), e.g. "
                "'base-set'.",
            ),
            _str(
                "rarity",
                "Only this rarity, as spelled in the rarity facet (e.g. Common, Rare, Holo Rare, "
                "Secret Rare).",
            ),
            _TCG_PRODUCT_TYPE,
            _TCG_SEARCH_SORT,
            _TCG_SEARCH_PAGE,
            _TCG_SEARCH_LIMIT,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_product",
        namespace="tcgplayer",
        method="product",
        http="POST",
        path="/api/v1/tcgplayer/product",
        summary=(
            "One TCGplayer product (US, USD) by product id or URL: name, URL, images (200, 400 "
            "and 1000 px), game, set, card number, rarity, product type, release date, market, "
            "median and lowest listing price, listing and seller counts, card text, flavor text, "
            "the game's card attributes (Pokemon HP, stage, attacks...; Magic color, mana value, "
            "type line...; Yu-Gi-Oh! attribute, level, ATK, DEF...) and every SKU (condition x "
            "printing x language, e.g. Near Mint / Normal / English) with its market price, "
            "lowest_sale_price and highest_sale_price over recent sales, sale_count and when it "
            "was calculated. The sale fields are sale statistics, not live listings. An unknown "
            "id is a 404 (not billed)."
        ),
        params=(_TCG_PRODUCT_ID, _TCG_URL),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_listings",
        namespace="tcgplayer",
        method="listings",
        http="POST",
        path="/api/v1/tcgplayer/listings",
        summary=(
            "Live marketplace listings for one TCGplayer product (US, USD), cheapest first by "
            "price plus shipping (default) or by item price, up to 50 per page, filtered by "
            "condition, printing, language, verified sellers or TCGplayer Direct. Each listing "
            "has listing id, price, shipping, total, quantity, condition, printing, language, "
            "listing type (standard or custom) and the seller: key, id, name, URL, rating "
            "percent, sales band, gold star, verified and Direct flags, programs and location. "
            "Also returns total_results, has_more and condition / printing / language / listing "
            "type counts."
        ),
        params=(
            _TCG_PRODUCT_ID,
            _TCG_URL,
            _str_or_list(
                "condition",
                "Only these conditions: " + _TCG_CONDITIONS + ". A list or a comma-separated "
                "string.",
            ),
            _str_or_list(
                "printing",
                "Only these printings, as a product's skus[].printing spells them (Normal, Foil, "
                "Holofoil, Reverse Holofoil, 1st Edition, Unlimited...).",
            ),
            _str_or_list(
                "language",
                "Only these languages (English, Japanese, French, German, Italian, Spanish, "
                "Portuguese, Korean, Chinese (S), Chinese (T), Russian).",
            ),
            _bool("verified_sellers", "Only verified sellers."),
            _bool("direct_only", "Only TCGplayer Direct sellers."),
            _lit(
                "sort",
                ("price_shipping", "price"),
                "price_shipping (default, cheapest price plus shipping first) or price (item "
                "price only).",
            ),
            _int("page", "Page, 1-based, up to 200. Defaults to 1."),
            _int("limit", "Listings per page, 1-50. Defaults to 10."),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_price_history",
        namespace="tcgplayer",
        method="price_history",
        http="POST",
        path="/api/v1/tcgplayer/price-history",
        summary=(
            "Sales price history for one TCGplayer product (US, USD) over a month, quarter "
            "(default), half year or year, per SKU (condition, printing, language): total "
            "quantity sold, transaction count, average daily sales, and buckets newest first "
            "(daily for month, 3-day for quarter, weekly for semi_annual and annual) with market "
            "price, quantity sold, transaction count and the low and high sale price with and "
            "without shipping (null for a bucket with no sales). Totals across SKUs included. A "
            "product with no history is a 404."
        ),
        params=(
            _TCG_PRODUCT_ID,
            _TCG_URL,
            _lit(
                "range",
                ("month", "quarter", "semi_annual", "annual"),
                "month (daily buckets), quarter (default, 3-day buckets), semi_annual (weekly) or "
                "annual (weekly).",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_sales",
        namespace="tcgplayer",
        method="sales",
        http="POST",
        path="/api/v1/tcgplayer/sales",
        summary=(
            "The 5 most recent sales of one TCGplayer product (US, USD), optionally only in some "
            "conditions: order date, condition, printing, language, quantity, sale price, "
            "shipping, total and listing type. TCGplayer shows only the newest 5, so this is not "
            "a full sold history; use price_history() for volume and daily or weekly sale ranges."
        ),
        params=(
            _TCG_PRODUCT_ID,
            _TCG_URL,
            _str_or_list(
                "condition",
                "Only sales in these conditions: " + _TCG_CONDITIONS + ". A list or a "
                "comma-separated string.",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_games",
        namespace="tcgplayer",
        method="games",
        http="POST",
        path="/api/v1/tcgplayer/games",
        summary=(
            "Every game (product line) on TCGplayer, 70+ (Magic: The Gathering, Yu-Gi-Oh!, "
            "Pokemon, One Piece, Lorcana...): game_id, name, url_name (what search(), sets() and "
            "seller_products() accept as game) and whether TCGplayer Direct carries it. No "
            "parameters."
        ),
        params=(),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_sets",
        namespace="tcgplayer",
        method="sets",
        http="POST",
        path="/api/v1/tcgplayer/sets",
        summary=(
            "Every set of one TCGplayer game, newest release first: set_id (for price_guide()), "
            "name, url_name (for search()'s set filter), abbreviation, release date and the "
            "supplemental flag. An unknown game is a 404."
        ),
        params=(
            Param(
                "game",
                "Union[str, int]",
                required=True,
                doc="Game url_name or game_id from games() (pokemon, magic, yugioh, or 3, 1, "
                "2...).",
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_price_guide",
        namespace="tcgplayer",
        method="price_guide",
        http="POST",
        path="/api/v1/tcgplayer/price-guide",
        summary=(
            "The TCGplayer price guide for one whole set (US, USD): one row per product per "
            "condition and printing with product id, name, URL, card number, rarity, market "
            "price and low price, for cards (default) or sealed products, up to 500 rows per "
            "page. total_results is given for cards (null for sealed). A set with nothing in the "
            "guide is a 404."
        ),
        params=(
            Param(
                "set_id",
                "Union[str, int]",
                required=True,
                doc="Set id from sets(), e.g. 604 (Pokemon Base Set).",
            ),
            _lit("product_type", ("cards", "sealed"), "cards (default) or sealed."),
            _int("page", "Page, 1-based, up to 100. Defaults to 1."),
            _int(
                "limit",
                "Rows per page, 1-500. Defaults to 100. One row per card per condition and "
                "printing.",
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_suggestions",
        namespace="tcgplayer",
        method="suggestions",
        http="POST",
        path="/api/v1/tcgplayer/suggestions",
        summary=(
            "The TCGplayer search-box autocomplete for a partial query (no game filter): "
            "suggested products (product id, name, URL, set, game, score), matching sets and the "
            "games the matches come from with counts."
        ),
        params=(_req("query", "What the shopper has typed so far, e.g. 'charizard'."),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_trending",
        namespace="tcgplayer",
        method="trending",
        http="POST",
        path="/api/v1/tcgplayer/trending",
        summary=(
            "What shoppers are searching on TCGplayer right now, overall or for Pokemon, Magic "
            "or Yu-Gi-Oh!: up to 10 terms with a popularity score."
        ),
        params=(
            _lit(
                "game",
                ("all", "pokemon", "magic", "yugioh"),
                "all (default), pokemon, magic or yugioh.",
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_seller",
        namespace="tcgplayer",
        method="seller",
        http="POST",
        path="/api/v1/tcgplayer/seller",
        summary=(
            "One TCGplayer seller by seller key (a listing's seller.key): store name, URL, "
            "location, member since, lifetime sales band, completed sales rank, rating percent, "
            "gold star, Direct, Pro, certified hobby shop and WPN flags, US and international "
            "shipping, store hours, games sold, social links, and the last 365 days of buyer "
            "feedback summarized (total, percent positive, count per star, as described / "
            "arrived when expected / good communication). An unknown key is a 404."
        ),
        params=(_TCG_SELLER_KEY,),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_seller_feedback",
        namespace="tcgplayer",
        method="seller_feedback",
        http="POST",
        path="/api/v1/tcgplayer/seller-feedback",
        summary=(
            "Individual buyer feedback on one TCGplayer seller from the last 365 days, newest "
            "first, up to 50 per page, optionally only one star rating or only feedback with a "
            "comment: date, rating, comment, as described / arrived when expected / good "
            "communication, and the buyer's masked nickname as the site shows it. Also "
            "total_results as TCGplayer reports it (approximate under the rating and "
            "with_comment filters) and has_more (true when the page is full)."
        ),
        params=(
            _TCG_SELLER_KEY,
            _ilit("rating", (1, 2, 3, 4, 5), "Only feedback with this many stars, 1-5."),
            _bool("with_comment", "Only feedback that has a written comment."),
            _int("page", "Page, 1-based, up to 500. Defaults to 1."),
            _int("limit", "Feedback per page, 1-50. Defaults to 10."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="tcgplayer_seller_products",
        namespace="tcgplayer",
        method="seller_products",
        http="POST",
        path="/api/v1/tcgplayer/seller-products",
        summary=(
            "The products one TCGplayer seller has listed (US, USD), optionally matching "
            "keywords or one game, up to 50 per page, sorted like search(). Each product has "
            + _TCG_PRODUCT_FIELDS + ", plus the seller's own listings of it (price, shipping, "
            "condition, printing, language, quantity). Also total_results, has_more and facets."
        ),
        params=(
            _TCG_SELLER_KEY,
            _str(
                "query",
                "Only the seller's products matching these keywords, e.g. 'charizard'.",
            ),
            _TCG_GAME,
            _TCG_SEARCH_SORT,
            _TCG_SEARCH_PAGE,
            _TCG_SEARCH_LIMIT,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # ============================== Vinted ===============================
    # 27 Vinted country sites via country (fr default on the server), 9
    # endpoints, 1 credit each. product takes item_id or url (one_of). search
    # needs query unless category_id or brand_ids is given (server-side rule;
    # query is an optional positional here). 120 s timeout floor.
    Endpoint(
        key="vinted_search",
        namespace="vinted",
        method="search",
        http="POST",
        path="/api/v1/vinted/search",
        summary=(
            "Search second-hand listings on any of 27 Vinted country sites (fr default; uk, us, "
            "de, pl, es, it, nl, au and more) by keywords, category, brand, condition, size, "
            "color, material and price range, sorted by relevance, newest or price. query is "
            "optional when category_id or brand_ids is given. 96 items per page, pages 1-10 "
            "(Vinted serves no deeper). Each item has id, title, URL, price and currency (the "
            "country site's currency), price_with_discount, service_fee, total_price, brand, "
            "size, condition, favourite count, promoted flag, photos and the seller's id and "
            "business flag; " + _VINTED_FEE + ". Also returns listed_results and total_pages "
            "(capped at 960 and 10; total_is_capped is true when the real number of matches is "
            "higher) and the filters Vinted actually applied. Live listings only: sold items are "
            "not searchable."
        ),
        params=(
            Param(
                "query",
                "Optional[str]",
                positional=True,
                doc="Search keywords, e.g. 'barbour jacket'. Optional when category_id or "
                "brand_ids is given.",
            ),
            _VINTED_COUNTRY,
            _str_or_int(
                "category_id",
                "Only this category and its subcategories, by id from categories() (1907 is "
                "Women > Clothing > Outerwear > Coats).",
            ),
            _vinted_ids(
                "brand_ids",
                "Only these brands, by id from brands() (Nike 53, Levi's 10, Barbour 46805).",
            ),
            _vinted_ids(
                "status_ids",
                "Only these conditions: 6 New with tags, 1 New without tags, 2 Very good, "
                "3 Good, 4 Satisfactory.",
            ),
            _vinted_ids(
                "size_ids",
                "Only these sizes, by option id from filters('size') (4 is women's M / UK "
                "12-14 / US 8-10).",
            ),
            _vinted_ids(
                "color_ids",
                "Only these colors, by option id from filters('color') (1 is black).",
            ),
            _vinted_ids(
                "material_ids",
                "Only these materials, by option id from filters('material') (123 is cashmere).",
            ),
            _float("price_from", "Minimum item price, in the country site's currency."),
            _float("price_to", "Maximum item price, in the country site's currency."),
            _lit(
                "sort",
                ("relevance", "newest_first", "price_low_to_high", "price_high_to_low"),
                "relevance (default), newest_first, price_low_to_high or price_high_to_low. "
                "Price sorts rank loosely matching items too (very cheap or placeholder-priced "
                "listings), so pair them with a category or price range.",
            ),
            _int("page", "Results page, 1-10 (Vinted serves at most 10 pages of 96). Defaults to 1."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_product",
        namespace="vinted",
        method="product",
        http="POST",
        path="/api/v1/vinted/product",
        summary=(
            "One Vinted listing by item id or URL: title, description, price and currency (the "
            "seller's currency, which can differ from the country site's), brand, size, "
            "condition, color, material, when it was uploaded as Vinted words it "
            "(uploaded_relative, e.g. \"8 hours ago\"), category id and path, all photos, "
            "favourite count, reserved and sold state, whether it can be bought now, and the "
            "seller (id, login, profile URL, business flag, feedback count, rating 0-1, badges). "
            "Sold listings still return their last price. A URL's own site is used whatever "
            "country says. An unknown id is a 404."
        ),
        params=(
            _str_or_int(
                "item_id",
                "Vinted item id (a search result's id, the number after /items/ in a Vinted "
                "URL), e.g. 10671938315.",
            ),
            _str(
                "url",
                "A Vinted item URL on any country site. Its own site is used (and echoed as "
                "country), whatever country says.",
            ),
            _VINTED_COUNTRY,
        ),
        one_of=(("item_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_seller",
        namespace="vinted",
        method="seller",
        http="POST",
        path="/api/v1/vinted/seller",
        summary=(
            "One Vinted member's public seller profile: login, profile URL, business flag, "
            "feedback count, rating (0-1), positive / neutral / negative feedback counts, listed "
            "item count, country, city (only when the member shows it), email / Facebook / "
            "Google verification, average response time, holiday mode and the date last seen. "
            "An unknown id is a 404."
        ),
        params=(_VINTED_USER_ID, _VINTED_COUNTRY),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_seller_products",
        namespace="vinted",
        method="seller_products",
        http="POST",
        path="/api/v1/vinted/seller-products",
        summary=(
            "The items one Vinted member has listed, newest first, cheapest first or by "
            "relevance, up to 96 per page: id, title, URL, price, currency, service_fee, "
            "total_price, brand, size, condition, favourite count, reserved, sold and promoted "
            "flags and photos; " + _VINTED_FEE + ". Also total_results, total_pages and "
            "has_more. A member with no listings (or an unknown id) returns an empty list."
        ),
        params=(
            _VINTED_USER_ID,
            _VINTED_COUNTRY,
            _lit(
                "sort",
                ("newest_first", "price_low_to_high", "relevance"),
                "newest_first (default), price_low_to_high or relevance.",
            ),
            _int("page", "Page, 1-based, up to 500. Defaults to 1."),
            _int("limit", "Items per page, 1-96. Defaults to 20."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_seller_feedback",
        namespace="vinted",
        method="seller_feedback",
        http="POST",
        path="/api/v1/vinted/seller-feedback",
        summary=(
            "Reviews left for one Vinted member, newest first, up to 50 per page: rating 1-5, "
            "review text, date, whether it is Vinted's automatic feedback, and the member's "
            "reply. Reviewer identities and the items reviewed are not included. Also "
            "total_results, total_pages and has_more."
        ),
        params=(
            _VINTED_USER_ID,
            _VINTED_COUNTRY,
            _int("page", "Page, 1-based, newest first, up to 500. Defaults to 1."),
            _int("limit", "Feedback per page, 1-50. Defaults to 20."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_brands",
        namespace="vinted",
        method="brands",
        http="POST",
        path="/api/v1/vinted/brands",
        summary=(
            "Find Vinted brands by name: brand id (what search()'s brand_ids takes), title, "
            "slug, URL, number of listings, luxury flag and whether Vinted authenticity-checks "
            "it."
        ),
        params=(_req("query", "Brand name or part of it, e.g. 'barbour'."), _VINTED_COUNTRY),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_suggestions",
        namespace="vinted",
        method="suggestions",
        http="POST",
        path="/api/v1/vinted/suggestions",
        summary=(
            "The Vinted search-box autocomplete for a partial query, in the country site's "
            "language: up to 10 suggestions, each with its type (popular_search, or the catalog "
            "match it comes from such as brand, brand+parent_cat or attr)."
        ),
        params=(_req("query", "What the shopper has typed so far, e.g. 'barb'."), _VINTED_COUNTRY),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_filters",
        namespace="vinted",
        method="filters",
        http="POST",
        path="/api/v1/vinted/filters",
        summary=(
            "The options of one Vinted search filter (size, condition, color or material) with "
            "live item counts, optionally for a query and a category: id (what search()'s "
            "size_ids, status_ids, color_ids and material_ids take), localized title, item "
            "count, the size group and, for conditions, the description."
        ),
        params=(
            Param(
                "filter",
                'Literal["size", "status", "color", "material"]',
                required=True,
                doc="size, status (condition), color or material.",
            ),
            _VINTED_COUNTRY,
            _str("query", "Count options for this search, e.g. 'dress'."),
            _str_or_int(
                "category_id",
                "Count options within this category, e.g. 1904 (Women). Sizes are grouped per "
                "category, so pass one for size.",
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="vinted_categories",
        namespace="vinted",
        method="categories",
        http="POST",
        path="/api/v1/vinted/categories",
        summary=(
            "The Vinted category tree in the country site's language (9 top-level categories, "
            "about 3,000 in all): id (what search()'s category_id takes), title, URL and "
            "children; or one category's subtree with its path."
        ),
        params=(
            _VINTED_COUNTRY,
            _str_or_int(
                "parent_id",
                "Return only this category's subtree (1904 is Women). Omit for the whole tree.",
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # =============================== Macy's ==============================
    # macys.com (US only, USD), 9 endpoints, 1 credit each. product takes
    # product_id, url or product_ids (up to 10, summary view); reviews and
    # store_availability take product_id or url; category takes category_id or
    # url; brand takes brand_id or url; stores takes one location (zip, lat +
    # lng, or city + state); store_availability takes store_id OR a location,
    # not both (one_of only enforces "at least one"). filters is a nested
    # object on the wire, so it is a dict here. 120 s timeout floor.
    Endpoint(
        key="macys_search",
        namespace="macys",
        method="search",
        http="POST",
        path="/api/v1/macys/search",
        summary=(
            "Search macys.com (US) by keyword, filtered by brand, color, special offer "
            "(clearance, Last Act, Today Only, Black Friday deal...), any price range, a pickup "
            "store and any other facet, sorted by featured, price, top rated, best sellers or "
            "newest. " + _MACYS_GRID_FIELDS + " A keyword the site maps to a category comes "
            "back with redirected_to_category (its id works with category())."
        ),
        params=(_req("query", "Search keywords, e.g. 'jeans'."), _MACYS_SPECIAL_OFFER, *_MACYS_GRID),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_product",
        namespace="macys",
        method="product",
        http="POST",
        path="/api/v1/macys/product",
        summary=(
            "One macys.com product by id or URL, or up to 10 by product_ids in one call: title, "
            "brand (with brand_page_id for brand()), type, description, bullets, category path, "
            "price, regular and sale price, percent off, on-sale flag, sale end, promotions, "
            "rating, review_count and text_review_count (ratings without text count in "
            "review_count only), rating_distribution, recommended count, fit slider, AI review "
            "summary, purchased message, question and answer counts, images, colors with their "
            "prices, sizes and every variant (UPC, color, size, available, availability message, "
            "low-stock flag, ship days). A product that belongs to a collection answers with the "
            "collection product, and requested_id echoes the id asked for. In a batch, unknown "
            "ids are listed in not_found and Macy's serves its summary view: rating and "
            "review_count but no rating histogram, and a collection without its members' "
            "variants. An unknown id is a 404."
        ),
        params=(
            _MACYS_PRODUCT_ID,
            _MACYS_URL,
            Param(
                "product_ids",
                "Optional[Union[str, list[Union[str, int]]]]",
                doc="Up to 10 product ids in one call (a list or a comma-separated string), "
                "instead of product_id / url.",
            ),
        ),
        one_of=(("product_id", "url", "product_ids"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_reviews",
        namespace="macys",
        method="reviews",
        http="POST",
        path="/api/v1/macys/reviews",
        summary=(
            "Customer reviews of one macys.com product by id or URL, newest (default), highest "
            "rated, lowest rated or with photos first, up to 100 per page, optionally only one "
            "star rating or only reviews mentioning a word: rating, title, text, date, nickname, "
            "location as the reviewer gave it, recommended, helpful yes / no votes, incentivized "
            "and syndicated flags (and the site it came from), badges, fit and other slider "
            "ratings, photo URLs and the brand's response. Also total, total_pages and has_more. "
            "total counts written reviews only: ratings without text are not returned (product() "
            "has the full rating histogram). Reviewer = nickname only."
        ),
        params=(
            _MACYS_PRODUCT_ID,
            _MACYS_URL,
            _lit(
                "sort",
                ("newest", "highest_rated", "lowest_rated", "with_photos"),
                "newest (default), highest_rated, lowest_rated or with_photos.",
            ),
            _int("page", "Page, 1-based. Defaults to 1."),
            _int("limit", "Reviews per page, 1-100. Defaults to 20."),
            _ilit("rating", (1, 2, 3, 4, 5), "Only reviews with this star rating, 1-5."),
            _str("query", "Only reviews mentioning this text, e.g. 'soft'."),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_category",
        namespace="macys",
        method="category",
        http="POST",
        path="/api/v1/macys/category",
        summary=(
            "Browse one macys.com category by id or URL, with the same filters and sorts as "
            "search(). " + _MACYS_GRID_FIELDS + " Also returns the category's id, name and URL. "
            "An unknown id is a 404."
        ),
        params=(
            _str_or_int(
                "category_id",
                "Macy's category id: the id= of a macys.com /shop/ URL, a product's "
                "categories[].id, or a search's redirected_to_category.id, e.g. 3763 (Men's Coats "
                "& Jackets).",
            ),
            _str(
                "url",
                "A macys.com category URL with its id=. Filters, page and sort already in the URL "
                "are kept.",
            ),
            _MACYS_SPECIAL_OFFER,
            *_MACYS_GRID,
        ),
        one_of=(("category_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_brand",
        namespace="macys",
        method="brand",
        http="POST",
        path="/api/v1/macys/brand",
        summary=(
            "Browse one brand's macys.com page by its page id or URL (a product's "
            "brand_page_id), with the same filters and sorts as search(). " + _MACYS_GRID_FIELDS
            + " Also returns the brand's page id, name and URL. To filter by brand name "
            "instead, use search() with brand."
        ),
        params=(
            _str_or_int(
                "brand_id",
                "The brand page id: a product's brand_page_id, or the id= of a macys.com "
                "/shop/brands/ URL, e.g. 337747 (Calvin Klein).",
            ),
            _str("url", "A macys.com brand page URL with its id=."),
            _MACYS_SPECIAL_OFFER,
            *_MACYS_GRID,
        ),
        one_of=(("brand_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_deals",
        namespace="macys",
        method="deals",
        http="POST",
        path="/api/v1/macys/deals",
        summary=(
            "Macy's sale listings: all Sales & Offers (default), Clearance, Today Only, Last Act "
            "(final-sale markdowns), Limited-Time Specials or Black Friday Deals, with the same "
            "filters and sorts as search() (except special_offer). " + _MACYS_GRID_FIELDS
            + " sale_ends carries the end date when Macy's states one."
        ),
        params=(
            _lit(
                "type",
                (
                    "sale",
                    "clearance",
                    "today_only",
                    "last_act",
                    "limited_time_special",
                    "black_friday",
                ),
                "sale (all Sales & Offers, default), clearance, today_only, last_act, "
                "limited_time_special or black_friday.",
            ),
            *_MACYS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_stores",
        namespace="macys",
        method="stores",
        http="POST",
        path="/api/v1/macys/stores",
        summary=(
            "Macy's stores near a US ZIP code, a point (lat + lng) or a city + state, nearest "
            "first (up to 15, within 100 miles by default): store_id (what "
            "store_availability() and pickup_store_id take), name, address, phone, lat / lng, "
            "distance in miles, today's and tomorrow's hours, curbside hours and the order "
            "cut-off for same-day pickup."
        ),
        params=_MACYS_LOCATION,
        one_of=(("zip", "lat", "city"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_store_availability",
        namespace="macys",
        method="store_availability",
        http="POST",
        path="/api/v1/macys/store-availability",
        summary=(
            "Can a macys.com product be picked up in store? Near a ZIP, a point or a city + "
            "state: every store with available true / false and available_items_count (how many "
            "of the product's items it has). At one store (store_id): the store's hours, pickup "
            "cut-off and pickup options, and for every variant (UPC, color, size) "
            "pickup_available and in_store_available. Macy's publishes no unit quantities, so "
            "there are no stock counts. Pass store_id or a location, not both. An unknown "
            "store_id is a 404."
        ),
        params=(
            _MACYS_PRODUCT_ID,
            _MACYS_URL,
            _str_or_int(
                "store_id",
                "One store (a store_id from stores()) for per-variant pickup and in-store flags, "
                "instead of a location, e.g. 4592.",
            ),
            *_MACYS_LOCATION,
        ),
        one_of=(("product_id", "url"), ("store_id", "zip", "lat", "city")),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="macys_suggestions",
        namespace="macys",
        method="suggestions",
        http="POST",
        path="/api/v1/macys/suggestions",
        summary=(
            "The macys.com search-box autocomplete for a partial query: up to 7 suggested "
            "searches."
        ),
        params=(_req("query", "What the shopper has typed so far, e.g. 'jea'."),),
        credits=1,
        min_timeout=120.0,
    ),
    # ========================== Saks Fifth Avenue ========================
    # saksfifthavenue.com (US only, USD), 9 endpoints, 2 credits each. product
    # takes product_id or url; category takes path or url; brand takes brand
    # or url; stores and store_availability take one location (zip, or lat +
    # lng). filters is a nested object on the wire, so it is a dict here.
    # 120 s timeout floor.
    Endpoint(
        key="saks_search",
        namespace="saks",
        method="search",
        http="POST",
        path="/api/v1/saks/search",
        summary=(
            "Search saksfifthavenue.com (US) by keyword, filtered by designer, color, size (the "
            "facet label, e.g. Medium), any price range, on sale, new arrivals and any other "
            "facet, sorted by featured, best sellers, newest, price, sale first or designer A-Z. "
            + _SAKS_GRID_FIELDS + " A keyword the site sends to a designer or category page is "
            "answered from that page, named in redirected_to."
        ),
        params=(_req("query", "Search keywords, e.g. 'coat'."), _SAKS_BRAND, *_SAKS_GRID),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_product",
        namespace="saks",
        method="product",
        http="POST",
        path="/api/v1/saks/product",
        summary=(
            "One saksfifthavenue.com product by id or URL: title, brand, type (master or "
            "variant), UPC (for a variant), price, price_max, regular and sale price, percent "
            "off, on-sale flag, is_new / is_sale / is_clearance / is_final_sale, badge, "
            "returnable, promotions, description, style code, images, colors and sizes (each "
            "with availability IN_STOCK / NOT_AVAILABLE, selectable and waitlist), every SKU in "
            "variants[] with its online warehouse unit count, in-stock and available counts, "
            "availability (units available to sell, message such as Limited Inventory, "
            "in_stock_date), available_in_store, marketplace, drop_ship, preorder, merchandising "
            "attributes (category, gender, material, length...), the average star rating and "
            "review_count. Review text is not available. Add color + size (or pass a variant "
            "sku) to resolve one variant: its sku is id, with its UPC and stock. A "
            "variants[].sku is what store_availability() takes. An unknown id is a 404."
        ),
        params=(
            _str_or_int(
                "product_id",
                "Saks product id: a search result's id (the number at the end of a product URL), "
                "or a variant sku, e.g. '0400019127312'.",
            ),
            _str(
                "url",
                "A saksfifthavenue.com product URL (its trailing id is used; a color / size it "
                "selects is kept). Alternative to product_id.",
            ),
            _str("color", "Pick one color (a colors[].value), e.g. 'BLUE OPAL'."),
            _str("size", "Pick one size (a sizes[].value). With color, the answer is that variant."),
        ),
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_category",
        namespace="saks",
        method="category",
        http="POST",
        path="/api/v1/saks/category",
        summary=(
            "Browse one Saks category by its /c/ path or URL (women's dresses, men's sweaters, "
            "beauty...), with the same filters and sorts as search(). " + _SAKS_GRID_FIELDS
            + " Also returns the category's name, path, URL and breadcrumbs. An unknown path is "
            "a 404."
        ),
        params=(
            _str(
                "path",
                "A Saks category path (/c/...): from a category URL, a suggestions() "
                "categories[].path or a breadcrumb, e.g. '/c/women-s-apparel/dresses'.",
            ),
            _str(
                "url",
                "A saksfifthavenue.com category URL. Filters, sort and page already in the URL "
                "are kept.",
            ),
            _SAKS_BRAND,
            *_SAKS_GRID,
        ),
        one_of=(("path", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_brand",
        namespace="saks",
        method="brand",
        http="POST",
        path="/api/v1/saks/brand",
        summary=(
            "Browse one designer's Saks page by slug (from designers()) or URL, with the same "
            "filters and sorts as search() (except brand). " + _SAKS_GRID_FIELDS + " Also "
            "returns the brand's name, slug and URL. An unknown slug is a 404."
        ),
        params=(
            _str(
                "brand",
                "A designer slug from designers(), e.g. 'gucci', 'chloé', 'alice-olivia'. A "
                "plain name is slugified.",
            ),
            _str(
                "url",
                "A saksfifthavenue.com /brand/ URL. Filters, sort and page already in the URL "
                "are kept.",
            ),
            *_SAKS_GRID,
        ),
        one_of=(("brand", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_deals",
        namespace="saks",
        method="deals",
        http="POST",
        path="/api/v1/saks/deals",
        summary=(
            "Saks sale and new-arrival listings: all Sale (default), Women's Clothing Sale, "
            "Men's Sale, Women's New Arrivals or Men's New Arrivals, with the same filters and "
            "sorts as search(). " + _SAKS_GRID_FIELDS + " Saks has no clearance or final-sale "
            "listing (items carry is_clearance / is_final_sale flags)."
        ),
        params=(
            _lit(
                "type",
                ("sale", "womens_sale", "mens_sale", "womens_new_arrivals", "mens_new_arrivals"),
                "sale (all sale, default), womens_sale (women's clothing), mens_sale, "
                "womens_new_arrivals or mens_new_arrivals.",
            ),
            _SAKS_BRAND,
            *_SAKS_GRID,
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_stores",
        namespace="saks",
        method="stores",
        http="POST",
        path="/api/v1/saks/stores",
        summary=(
            "Saks Fifth Avenue stores near a US ZIP code or a point (lat + lng), within 15 / 30 "
            "/ 50 / 100 / 300 miles (default 50): store_id, name, address, city, state, ZIP, "
            "lat / lng, distance in miles (pickup stores), today's opening and closing times, "
            "hours as listed, closed flag, and pickup (true for stores that offer in-store "
            "pickup; other Saks locations are listed with pickup false)."
        ),
        params=_SAKS_LOCATION,
        one_of=(("zip", "lat"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_store_availability",
        namespace="saks",
        method="store_availability",
        http="POST",
        path="/api/v1/saks/store-availability",
        summary=(
            "Can one Saks variant (sku) be picked up near a US ZIP code or a point? For each "
            "pickup store: the site's availability message (In Stock, Limited Inventory, Not "
            "Available), in_stock, limited, units_at_store when the site gives a count (it does "
            "for stores that have the item; otherwise null), and the store's address, distance "
            "and today's hours. Needs a variant sku: take it from product() variants[].sku, or "
            "from product() with color + size."
        ),
        params=(
            Param(
                "sku",
                "Union[str, int]",
                required=True,
                doc="A variant sku: a product's variants[].sku, or a product's id after picking "
                "color + size, e.g. '10781654'.",
            ),
            *_SAKS_LOCATION,
        ),
        one_of=(("zip", "lat"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_suggestions",
        namespace="saks",
        method="suggestions",
        http="POST",
        path="/api/v1/saks/suggestions",
        summary=(
            "The saksfifthavenue.com search-box suggestions for a partial query: the result "
            "count, matching designers, suggested categories (name, parent, path for "
            "category()), up to 5 featured products (id, title, brand, URL, image) and the "
            "site's popular searches."
        ),
        params=(_req("query", "What the shopper has typed so far, e.g. 'gucci'."),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="saks_designers",
        namespace="saks",
        method="designers",
        http="POST",
        path="/api/v1/saks/designers",
        summary=(
            "The Saks A-Z designer index (about 1,200 designers): name, slug (what brand() "
            "takes), URL and letter, optionally only one letter."
        ),
        params=(
            _str(
                "letter",
                "Only designers under this letter (A-Z, or '#' for names starting with a digit).",
            ),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    # =============================== Kohl's ==============================
    # kohls.com (US only, USD), 9 endpoints: stores 1 credit, the rest 2.
    # product takes product_id or url; category takes path or url; brand takes
    # brand or url; stores takes one location (zip, city + state, or lat +
    # lng); store_availability takes a required sku and zip. 120 s timeout
    # floor.
    Endpoint(
        key="kohls_search",
        namespace="kohls",
        method="search",
        http="POST",
        path="/api/v1/kohls/search",
        summary=(
            "Search kohls.com (US) by keyword, filtered by brand, color, size, on sale, "
            "clearance and any facet value (price buckets, gender, rating, store pickup...), "
            "sorted by featured, new arrivals, best sellers, price, highest rated or percent "
            "off. " + _KOHLS_GRID_FIELDS + " When the site autocorrects the keyword, "
            "corrected_query says so."
        ),
        params=(_req("query", "Search keywords, e.g. 'jeans'."), _KOHLS_BRAND, *_KOHLS_GRID),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_product",
        namespace="kohls",
        method="product",
        http="POST",
        path="/api/v1/kohls/product",
        summary=(
            "One kohls.com product by id or URL: title, brand, status, dept (what "
            "store_availability() can take), breadcrumbs, Sephora at Kohl's flag, average "
            "rating, review_count and recommended_percent (review text is not available), "
            "is_new / best_seller / top_rated, badges, description, details, ingredients "
            "(beauty), images, videos, return policy, the price block (regular, sale, "
            "sale_status, percent_off, lowest_applicable_price, price_suppressed with price_note "
            "for cart-only prices, with_code_price with its savings and offer codes), kohls_cash "
            "(earn and redeem windows, amount earned) when the product has it, the public offers "
            "that apply (code, description, terms, start and end dates), pickup / ship-to-store "
            "eligibility, online_units, and every variant: sku, UPC, color, size, availability, "
            "online_units, max_per_order, price, sale price, with-code price, Kohl's Cash earned "
            "and pickup eligibility. Add store_id (from stores()) for that store's availability "
            "and in-store price on each variant. A variants[].sku is what store_availability() "
            "takes. An unknown id is a 404 (it can take about 20 seconds)."
        ),
        params=(
            _str_or_int(
                "product_id",
                "Kohl's product id: a search result's id, the number after prd- in a product "
                "URL, e.g. '6251213'.",
            ),
            _str("url", "A kohls.com product URL (its prd-<id> is used). Alternative to product_id."),
            _str_or_int(
                "store_id",
                "A Kohl's store number (stores() stores[].store_id), e.g. '725': adds that "
                "store's availability and in-store price to every variant.",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_category",
        namespace="kohls",
        method="category",
        http="POST",
        path="/api/v1/kohls/category",
        summary=(
            "Browse one Kohl's catalog listing by its path or URL (Small Appliances, Women's "
            "Clothing, Men's Shoes...), with the same filters and sorts as search(). The path "
            "must carry its CN=... filter, the way kohls.com category links and a product's "
            "breadcrumbs[].url do. " + _KOHLS_GRID_FIELDS + " Also returns the category's name, "
            "breadcrumbs, path and URL."
        ),
        params=(
            _str(
                "path",
                "A Kohl's catalog path with its CN=... part, e.g. "
                "'/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances"
                "+Department:Kitchen%20%26%20Dining'.",
            ),
            _str(
                "url",
                "A kohls.com catalog URL. Its CN facets define the listing; a sort or page in "
                "the URL is kept.",
            ),
            _KOHLS_BRAND,
            *_KOHLS_GRID,
        ),
        one_of=(("path", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_brand",
        namespace="kohls",
        method="brand",
        http="POST",
        path="/api/v1/kohls/brand",
        summary=(
            "Browse one brand at Kohl's by name or URL (Nike, Hamilton Beach, Levi's...), with "
            "the same filters and sorts as search() (except brand). " + _KOHLS_GRID_FIELDS
            + " Also returns the brand's name, facet value and URL. An unknown brand is a 404."
        ),
        params=(
            _str(
                "brand",
                "A brand name as Kohl's lists it in the Brand facet, e.g. 'Hamilton Beach', "
                "'Nike', \"Levi's\".",
            ),
            _str("url", "A kohls.com brand page URL (its CN carries Brand:...)."),
            *_KOHLS_GRID,
        ),
        one_of=(("brand", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_deals",
        namespace="kohls",
        method="deals",
        http="POST",
        path="/api/v1/kohls/deals",
        summary=(
            "Kohl's deal listings: Clearance (default), Sale, items that earn Kohl's Cash right "
            "now, or Sephora at Kohl's, with the same filters and sorts as search(). "
            + _KOHLS_GRID_FIELDS + " To track clearance prices over time, poll and store your "
            "own: there is no price history."
        ),
        params=(
            _lit(
                "type",
                ("clearance", "sale", "kohls_cash", "sephora"),
                "clearance (default), sale, kohls_cash (items that earn Kohl's Cash now) or "
                "sephora (Sephora at Kohl's).",
            ),
            _KOHLS_BRAND,
            *_KOHLS_GRID,
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_stores",
        namespace="kohls",
        method="stores",
        http="POST",
        path="/api/v1/kohls/stores",
        summary=(
            "Kohl's stores near a US ZIP code, a city + state or a point (lat + lng), within 25 "
            "miles by default (up to 100): store_id (what product() store_id takes), name, "
            "address, city, state, ZIP, phone, lat / lng, distance in miles, weekly opening "
            "hours with the UTC offset, store badges (Sephora, Fine Jewelry, Lands' End...), "
            "services (In-Store Pickup, Amazon Returns...) and the store page URL."
        ),
        params=(
            _str_or_int("zip", _KOHLS_ZIP_DOC),
            _str("city", "City (with state), instead of zip, e.g. 'Austin'."),
            _str("state", "2-letter state code (with city), e.g. 'TX'."),
            _float("lat", "Latitude (with lng), instead of zip."),
            _float("lng", "Longitude (with lat)."),
            _int("radius", "Search radius in miles, 1-100. Defaults to 25."),
        ),
        one_of=(("zip", "city", "lat"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_store_availability",
        namespace="kohls",
        method="store_availability",
        http="POST",
        path="/api/v1/kohls/store-availability",
        summary=(
            "Pickup stock for one Kohl's SKU at every store within about 50 miles of a US ZIP "
            "code, with unit counts: per store pickup_units, stock_level (In Stock, Low Stock, "
            "Out of Stock), in_stock, ship_to_store_units with the ship-to-store pickup window, "
            "pickup and ship-to-store eligibility, clearance and Sephora flags, and the store's "
            "address, phone, distance and hours for the week. Also returns how many stores have "
            "it (in_stock_count) and total_pickup_units. Take sku (variants[].sku) and dept from "
            "product()."
        ),
        params=(
            Param(
                "sku",
                "Union[str, int]",
                required=True,
                doc="A Kohl's SKU code: a product's variants[].sku, e.g. '73519108'.",
            ),
            Param(
                "zip",
                "Union[str, int]",
                required=True,
                doc="US ZIP code: stores within about 50 miles are listed, e.g. '10001'.",
            ),
            _str_or_int("dept", "The product's department code (product() dept, e.g. '063')."),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_suggestions",
        namespace="kohls",
        method="suggestions",
        http="POST",
        path="/api/v1/kohls/suggestions",
        summary=(
            "The kohls.com search-box suggestions for a partial query: keyword completions "
            "(type terms, default), or matching products with id, title, URL and image (type "
            "products)."
        ),
        params=(
            _req("query", "What the shopper has typed so far, e.g. 'coff'."),
            _lit(
                "type",
                ("terms", "products"),
                "terms (default): keyword completions; products: matching products.",
            ),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="kohls_coupons",
        namespace="kohls",
        method="coupons",
        http="POST",
        path="/api/v1/kohls/coupons",
        summary=(
            "Today's public Kohl's coupon codes: code, description (the offer, minimum purchase "
            "and exclusions as stated), end date, whether it needs a Kohl's Card "
            "(requires_kohls_card), the terms page URL and the URL of the eligible products. "
            "Public codes only, no account offers or Kohl's Rewards balances."
        ),
        credits=2,
        min_timeout=120.0,
    ),
    # ============================== JCPenney =============================
    # jcpenney.com (US incl. Puerto Rico stores, USD), 11 endpoints, 1 credit
    # each. product takes product_id, url or product_ids (up to 20); category
    # takes path or url; brand takes brand or url; stores takes one location
    # (zip, city + state, or lat + lng); store_availability takes a required
    # sku plus zip or lat + lng; reviews and questions take product_id or url.
    # 120 s timeout floor (240 s for reviews and questions).
    Endpoint(
        key="jcpenney_search",
        namespace="jcpenney",
        method="search",
        http="POST",
        path="/api/v1/jcpenney/search",
        summary=(
            "Search jcpenney.com (US) by keyword, filtered by brand, color, size, price range, "
            "deal label (SALE, CLEARANCE...) and any facet value (gender, store availability, "
            "rating, rise...), sorted by relevance, new arrivals, best sellers, rating or price. "
            + _JCPENNEY_GRID_FIELDS + " When the site autocorrects the keyword, corrected_query "
            "says so; when it sends a keyword to a deal or category listing (doorbusters), "
            "redirected_to says where and the items are that listing's."
        ),
        params=(
            _req("query", "Search keywords, e.g. 'jeans'."),
            _JCPENNEY_BRAND,
            _JCPENNEY_DEAL,
            _bool(
                "exact",
                "JCPenney narrows many keywords to a category on its own (jeans -> the Jeans "
                "category, visible in applied_filters). True searches the keyword across every "
                "category instead.",
            ),
            *_JCPENNEY_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_product",
        namespace="jcpenney",
        method="product",
        http="POST",
        path="/api/v1/jcpenney/product",
        summary=(
            "One jcpenney.com product by id or URL, or up to 20 by product_ids in one call: "
            "title, brand, description, features, category and breadcrumbs, product and item "
            "type, images, average rating, review_count, question and answer counts (review "
            "text and Q&A: reviews() and questions()), the price block (regular, sale and clearance min / max "
            "ranges, percent off, price type, deal label, the after-coupon price with its coupon "
            "code, and when the price window starts and ends), channel (Omnichannel / "
            "OnlineOnly), in-store pickup, marketplace flag, and every variant: sku, UPC, color, "
            "size, all options, status, max per order and online_stock (high, low or out; single "
            "product only, a level, not a count). Prices are product-level ranges: JCPenney does "
            "not expose a price per size or color. A variants[].sku is what "
            "store_availability() takes. An unknown id is a 404; unknown ids in a batch are "
            "listed in not_found."
        ),
        params=(
            _str(
                "product_id",
                "A JCPenney product id (ppr / ppm / pp + digits): a search result's id, the last "
                "part of a product URL, e.g. 'ppr5008604049'.",
            ),
            _str("url", "A jcpenney.com product URL (its product id is used). Alternative to product_id."),
            _str_list(
                "product_ids",
                "Up to 20 product ids in one call (still 1 credit). Batch results carry no "
                "online stock.",
            ),
        ),
        one_of=(("product_id", "url", "product_ids"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_category",
        namespace="jcpenney",
        method="category",
        http="POST",
        path="/api/v1/jcpenney/category",
        summary=(
            "Browse one JCPenney category by its path or URL (Dresses, Sheets, Women's Boots...), "
            "with the same filters and sorts as search(). The path needs its id=cat... part, the "
            "way jcpenney.com /g/ category links and a response's breadcrumbs carry it. "
            + _JCPENNEY_GRID_FIELDS + " Also returns the category's name, id, path, URL and "
            "breadcrumbs. A department page (dept...) lists no products by itself: it needs a "
            "deal or another filter."
        ),
        params=(
            _str(
                "path",
                "A JCPenney category path with its id=cat... part, e.g. "
                "'/g/women/dresses?id=cat100210008'.",
            ),
            _str("url", "A jcpenney.com category URL. Filters, a sort or a page in the URL are kept."),
            _JCPENNEY_BRAND,
            _JCPENNEY_DEAL,
            *_JCPENNEY_GRID,
        ),
        one_of=(("path", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_brand",
        namespace="jcpenney",
        method="brand",
        http="POST",
        path="/api/v1/jcpenney/brand",
        summary=(
            "Every JCPenney product of one brand by name (Nike, St. John's Bay, Carter's...) or "
            "a brand page URL, with the same filters and sorts as search() (except brand). "
            + _JCPENNEY_GRID_FIELDS + " Also returns the brand's name, facet value and URL. An "
            "unknown brand is a 404."
        ),
        params=(
            _str(
                "brand",
                "A brand name as JCPenney lists it in the Brand facet, e.g. 'Nike', \"St. John's "
                "Bay\", \"Carter's\".",
            ),
            _str(
                "url",
                "A jcpenney.com brand page URL (JCPenney's curated brand page; its assortment can "
                "differ slightly from the brand name listing).",
            ),
            _JCPENNEY_DEAL,
            *_JCPENNEY_GRID,
        ),
        one_of=(("brand", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_deals",
        namespace="jcpenney",
        method="deals",
        http="POST",
        path="/api/v1/jcpenney/deals",
        summary=(
            "JCPenney deal listings across all products or one department: Clearance (default), "
            "Sale, Black Friday deals, Big Buy, Limited Time Special, Best Value, Gotta Have It, "
            "Closeout, Buy 1 Get 1, or any Deals & Promotions label, with the same filters and "
            "sorts as search(). " + _JCPENNEY_GRID_FIELDS + " Seasonal labels (black_friday) "
            "list nothing once the event ends. To track clearance prices over time, poll and "
            "store your own: there is no price history."
        ),
        params=(
            _lit(
                "type",
                _JCPENNEY_DEAL_TYPES,
                "clearance (default), sale, black_friday, big_buy, limited_time_special, "
                "best_value, gotta_have_it, closeout or bogo (every Buy 1 Get 1 offer).",
            ),
            _str(
                "label",
                "Any Deals & Promotions label verbatim from a previous response's facets "
                "(s1_deals_and_promotions), instead of type, e.g. 'BUY 1 GET 1 50% OFF'.",
            ),
            _str(
                "department",
                "Limit the deal to one department or category id (dept... / cat..., from "
                "breadcrumbs or a category URL), e.g. 'dept20000011'.",
            ),
            _JCPENNEY_BRAND,
            *_JCPENNEY_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_stores",
        namespace="jcpenney",
        method="stores",
        http="POST",
        path="/api/v1/jcpenney/stores",
        summary=(
            "JCPenney stores near a US or Puerto Rico ZIP code, a city + state or a point (lat + "
            "lng), within 25 miles by default (up to 100), paged: store_id, name, address, city, "
            "state, ZIP, phone, lat / lng, distance in miles, weekly opening hours, timezone, "
            "services (Curbside Pickup, salon, portrait studio, JCPenney Beauty...), curbside "
            "and in-store pickup directions, bookable appointments (Sephora, salon) and the "
            "store page URL."
        ),
        params=(
            _str_or_int("zip", _JCPENNEY_ZIP_DOC),
            _str("city", "City (with state), instead of zip, e.g. 'Austin'."),
            _str("state", "2-letter state code (with city), e.g. 'TX'."),
            _float("lat", "Latitude (with lng), instead of zip."),
            _float("lng", "Longitude (with lat)."),
            _int("radius", "Search radius in miles, 1-100. Defaults to 25."),
            _int("page", "Results page, 1-based. Defaults to 1."),
            _int("page_size", "Stores per page, 1-20. Defaults to 10."),
        ),
        one_of=(("zip", "city", "lat"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_store_availability",
        namespace="jcpenney",
        method="store_availability",
        http="POST",
        path="/api/v1/jcpenney/store-availability",
        summary=(
            "Real unit counts for one JCPenney SKU at the 5 nearest stores to a US or Puerto "
            "Rico ZIP code (or lat + lng): per store quantity, status (in_stock, low, "
            "out_of_stock, not_stocked), when the count was refreshed (updated_at), and the "
            "store's address, phone, distance and hours. Also returns how many of them have it "
            "(stores_with_stock) and total_quantity. in_stock_only drops the stores that have "
            "none. Take sku from product() variants[].sku."
        ),
        params=(
            Param(
                "sku",
                "Union[str, int]",
                required=True,
                doc="A JCPenney SKU id: a product's variants[].sku (or a search result's sku_id "
                "/ colors[].sku_id), e.g. '84630160042'.",
            ),
            _str_or_int(
                "zip",
                "US or Puerto Rico ZIP code: the 5 nearest stores are checked, e.g. '90012'.",
            ),
            _float("lat", "Latitude (with lng), instead of zip."),
            _float("lng", "Longitude (with lat)."),
            _int("radius", "Search radius in miles. Defaults to 25."),
            _bool("in_stock_only", "Drop the stores (of the 5 nearest) that have none."),
        ),
        one_of=(("zip", "lat"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_suggestions",
        namespace="jcpenney",
        method="suggestions",
        http="POST",
        path="/api/v1/jcpenney/suggestions",
        summary=(
            "The jcpenney.com search-box suggestions for a partial query: keyword completions "
            "with their search URL and, where JCPenney offers them, department refinements "
            "(nike shoes women -> sneakers, running shoes...)."
        ),
        params=(_req("query", "What the shopper has typed so far, e.g. 'jea'."),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="jcpenney_coupons",
        namespace="jcpenney",
        method="coupons",
        http="POST",
        path="/api/v1/jcpenney/coupons",
        summary=(
            "Today's public JCPenney coupons: code (null for in-store offers that need none), "
            "channel (online, in store or both), headline and details of each offer, start and "
            "end dates, the full disclaimer with its exclusions, and the URL of the eligible "
            "products. Public codes only, no account offers or JCPenney Rewards balances."
        ),
        credits=1,
        min_timeout=120.0,
    ),
    # reviews and questions are one slow render each (15-90 s, up to ~3 min
    # on a retried render), still 1 credit: 240 s timeout floor.
    Endpoint(
        key="jcpenney_reviews",
        namespace="jcpenney",
        method="reviews",
        http="POST",
        path="/api/v1/jcpenney/reviews",
        summary=(
            "Real customer review text of one jcpenney.com (US) product by id or URL, up to 98 "
            "per call (default 38), sorted most recent (default), most helpful, highest or "
            "lowest rating, or relevance, optionally only one star rating. Returns the product's "
            "review statistics: total_reviews (every language), displayed_reviews (the English "
            "reviews JCPenney lists and pages through, often fewer than total_reviews), "
            "average_rating, rating_distribution (1-5), recommended_percent, "
            "secondary_ratings_averages (Quality, Value, Apparel...), photo_count, and "
            "matching_reviews for the sort and filter. Each review has id, rating, title, text, "
            "author nickname, location, submitted_at and updated_at, recommended, helpful and "
            "unhelpful votes, verified_purchaser and incentivized badges, syndicated with "
            "syndication_source (the brand site it came from, e.g. sharkninja.com), customer "
            "photos and videos, secondary ratings, the brand's public response (name, "
            "department, text, date) and the original product name. Reviewer age, gender and IP "
            "are never returned. Slower than the other JCPenney endpoints: usually 15-90s, up "
            "to about 3 minutes; failed calls are not charged. A product with no reviews "
            "returns an empty list; an unknown product is a 404."
        ),
        params=(
            *_JCPENNEY_PRODUCT_TARGET,
            _lit(
                "sort",
                _JCPENNEY_REVIEW_SORTS,
                "most_recent (default), most_helpful, highest_rating, lowest_rating or "
                "relevance: the review list's own sort menu.",
            ),
            _int(
                "rating",
                "Only reviews with this star rating (1-5), e.g. 1 for the critical ones. A "
                "rating nobody gave returns an empty list.",
            ),
            _int(
                "max_reviews",
                "Reviews to return, 8-98. Defaults to 38. JCPenney loads 8, then 30 more per "
                "page, so 8, 38, 68 and 98 are the natural sizes; larger values take longer.",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=240.0,
    ),
    Endpoint(
        key="jcpenney_questions",
        namespace="jcpenney",
        method="questions",
        http="POST",
        path="/api/v1/jcpenney/questions",
        summary=(
            "Customer questions and every answer for one jcpenney.com (US) product by id or "
            "URL, up to 50 questions per call (default 10), newest answers first (JCPenney's "
            "order; there is no sort option). Returns total_questions and total_answers. Each "
            "question has id, question, details, author, submitted_at, answer_count and "
            "helpful_votes; each answer has id, text, author, author_type (brand for the "
            "manufacturer's product experts, retailer for JCPenney staff, ai for AI-generated "
            "answers, customer), ai_label (AI-Generated / AI-Assisted when JCPenney labels it), "
            "is_best_answer, submitted_at and helpful / unhelpful votes. Answerer IPs are never "
            "returned. Slower than the other JCPenney endpoints: usually 15-90s, up to about 3 "
            "minutes; failed calls are not charged. A product with no questions returns an "
            "empty list; an unknown product is a 404."
        ),
        params=(
            *_JCPENNEY_PRODUCT_TARGET,
            _int("max_questions", "Questions to return, 10-50 (10 per page). Defaults to 10."),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=240.0,
    ),
    # ======================== Dick's Sporting Goods =======================
    # dickssportinggoods.com (US, USD), 9 endpoints, 1 credit each except
    # product and reviews (2: one product page each). product and reviews take
    # product_id or url; category takes path, url or category_id;
    # store_availability takes skus plus zip or lat + lng. 120 s timeout floor,
    # 240 s for product and reviews (usually 20-75 s, up to ~2.5 min).
    Endpoint(
        key="dicks_search",
        namespace="dicks",
        method="search",
        http="POST",
        path="/api/v1/dicks/search",
        summary=(
            "Search dickssportinggoods.com (Dick's Sporting Goods, US) by keyword, filtered by "
            "brand, an approximate price range and any facet (gender, size, color, rating, "
            "sale...), sorted by relevance, top sellers, savings, price, featured, new arrivals "
            "or brand A-Z. " + _DICKS_GRID_FIELDS + " did_you_mean carries Dick's spelling "
            "suggestion for a misspelled query. Keywords Dick's sends to a landing page (golf "
            "balls, clearance) are followed to that page: redirected_to and category say which."
        ),
        params=(
            _req("query", "Search keywords, e.g. 'running shoes'."),
            _DICKS_BRAND,
            *_DICKS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="dicks_product",
        namespace="dicks",
        method="product",
        http="POST",
        path="/api/v1/dicks/product",
        summary=(
            "One Dick's Sporting Goods product by id or URL with every SKU: title, brand, "
            "description, features, specs, attributes, product type, category, images, rating, "
            "review_count, question and answer counts, the price block (min, max, list_min, "
            "list_max, percent_off, map_price_applies), clearance flag, the option axes (color, "
            "size, width...) and every variant: sku, UPC, options, color, size, price, "
            "list_price, percent_off, map_price_applies (the price only shows in the cart), "
            "is_clearance, online_units (units available to ship), buyable, ship_class and "
            "lead_time. Prices differ per SKU (one color on clearance, the rest at full price), "
            "so read the variant you need. A variant's sku is what store_availability() takes; "
            "review text is reviews(); products() is the cheap style-level check. An unknown "
            "id is a 404." + _DICKS_SLOW
        ),
        params=_DICKS_PRODUCT_TARGET,
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=240.0,
    ),
    Endpoint(
        key="dicks_products",
        namespace="dicks",
        method="products",
        http="POST",
        path="/api/v1/dicks/products",
        summary=(
            "Up to 5 Dick's Sporting Goods products in one call (1 credit): the fast, style-level "
            "check of title, brand, URL, image, price and list-price ranges, percent_off, "
            "map_price_applies, clearance, buyable, option axes, attributes, specs, product "
            "type, rating, review_count and description. No per-SKU prices or units: those come "
            "from product(). Unknown ids are listed in not_found; when none is found it is a "
            "404."
        ),
        params=(
            _str_list(
                "product_ids",
                "1 to 5 Dick's product ids, e.g. ['23FHQMCLFTN9GTXBLMNS', "
                "'26UNDMFITN1HRI9WUAETC'].",
                required=True,
            ),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="dicks_reviews",
        namespace="dicks",
        method="reviews",
        http="POST",
        path="/api/v1/dicks/reviews",
        summary=(
            "The 15 newest customer reviews of one Dick's Sporting Goods product by id or URL, "
            "with its review statistics: total, average, distribution (1-5 stars), recommended "
            "and not-recommended counts, photo count, first and last review dates, question and "
            "answer counts, and the average of each secondary rating (fit, comfort, quality, "
            "value...). Each review has id, rating, title, text, pros, cons, author nickname, "
            "submitted_at, recommended, helpful and unhelpful votes, verified_purchaser and "
            "incentivized badges, syndicated_from (the brand site a review came from), "
            "secondary ratings, customer photos and the brand's public response. The newest 15 "
            "only: no paging, no sort, no star filter; questions and answers are counts only. "
            "Reviewer age, gender and location are never returned. An unknown id is a 404."
            + _DICKS_SLOW
        ),
        params=_DICKS_PRODUCT_TARGET,
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=240.0,
    ),
    Endpoint(
        key="dicks_category",
        namespace="dicks",
        method="category",
        http="POST",
        path="/api/v1/dicks/category",
        summary=(
            "Browse one Dick's Sporting Goods category by its page path, URL or id (Men's "
            "Running Shoes, Golf Drivers, Kayaks...), in the site's featured order by default, "
            "with the same filters and sorts as search(). " + _DICKS_GRID_FIELDS + " Also "
            "returns the category's id, name, path and URL. An unknown category is a 404."
        ),
        params=(
            _str(
                "path",
                "A Dick's category page path (/f/<name> or /c/<name>), as dickssportinggoods.com "
                "category links and a response's categories[].path carry it, e.g. "
                "'/f/mens-running-shoes'.",
            ),
            _str(
                "url",
                "A dickssportinggoods.com category URL (its page is used; filters in the URL are "
                "not read, send them in filters).",
            ),
            _str_or_int(
                "category_id",
                "A category id: a response's categories[].id or category.id, e.g. '202105'.",
            ),
            _DICKS_BRAND,
            *_DICKS_GRID,
        ),
        one_of=(("path", "url", "category_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="dicks_brand",
        namespace="dicks",
        method="brand",
        http="POST",
        path="/api/v1/dicks/brand",
        summary=(
            "Every Dick's Sporting Goods product of one brand by name (Nike, YETI, Callaway, "
            "Under Armour...), optionally narrowed by a keyword, with the same filters and sorts "
            "as search() (except brand). " + _DICKS_GRID_FIELDS + " brand echoes the brand as "
            "Dick's writes it. An unknown brand is a 404."
        ),
        params=(
            _req(
                "brand",
                "A brand name as Dick's lists it in the Brand facet, e.g. 'Nike', 'YETI', "
                "'Callaway'; case does not matter.",
            ),
            _str("query", "Narrow the brand to a keyword, e.g. 'tumbler'."),
            *_DICKS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="dicks_deals",
        namespace="dicks",
        method="deals",
        http="POST",
        path="/api/v1/dicks/deals",
        summary=(
            "Dick's Sporting Goods deal listings: Clearance (default), Sale or This Week's "
            "Deals, in the site's featured order by default (sort savings for the biggest "
            "discounts first), with the same filters and sorts as search(). "
            + _DICKS_GRID_FIELDS + " To track clearance prices over time, poll and store your "
            "own: there is no price history."
        ),
        params=(
            _lit(
                "type",
                ("clearance", "sale", "weekly_deals"),
                "clearance (default), sale or weekly_deals (This Week's Deals).",
            ),
            _DICKS_BRAND,
            *_DICKS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="dicks_store_availability",
        namespace="dicks",
        method="store_availability",
        http="POST",
        path="/api/v1/dicks/store-availability",
        summary=(
            "Store unit counts for 1-20 Dick's Sporting Goods SKUs at up to 100 stores near a "
            "US ZIP code or a point (lat + lng), nearest first, within 25 miles by default (up "
            "to 250). chain picks DICK'S stores (default, incl. House of Sport and Going, Going, "
            "Gone!), Golf Galaxy or Public Lands. Each store has store_id, chain, name, address, "
            "shopping_center, city, state, ZIP, phone, lat / lng, distance_miles, status, weekly "
            "hours and per SKU: units (the units the store can sell) and in_store_units (the "
            "units on hand). Also returns sku_totals and how many stores have stock. There is "
            "no standalone store locator: store details come with a SKU lookup. An unknown SKU "
            "reads 0 at every store, so take SKUs from product() variants[].sku."
        ),
        params=(
            _str_list(
                "skus",
                "1 to 20 SKU ids from product() variants[].sku, e.g. ['25535758', '26810079'].",
                required=True,
            ),
            _str_or_int("zip", "US ZIP code to search around, e.g. '60601'."),
            _float("lat", "Latitude (with lng), instead of zip."),
            _float("lng", "Longitude (with lat)."),
            _int(
                "radius",
                "Search radius in miles, 1-250. Defaults to 25. Up to 100 stores are returned.",
            ),
            _lit(
                "chain",
                ("dicks", "golf_galaxy", "public_lands"),
                "dicks (DICK'S Sporting Goods, incl. House of Sport and Going, Going, Gone! "
                "stores; default), golf_galaxy or public_lands.",
            ),
            _bool("in_stock_only", "Only the stores that have at least one of the SKUs."),
        ),
        one_of=(("zip", "lat"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="dicks_suggestions",
        namespace="dicks",
        method="suggestions",
        http="POST",
        path="/api/v1/dicks/suggestions",
        summary=(
            "The dickssportinggoods.com search-box suggestions for a partial query: keyword "
            "completions, brands, categories (id, name, path, URL, product_count) and products "
            "(id, title, brand, URL, image, color, price and list-price ranges, percent_off)."
        ),
        params=(_req("query", "What the shopper has typed so far, e.g. 'yeti tum'."),),
        credits=1,
        min_timeout=120.0,
    ),
    # ============================= Foot Locker ===========================
    # footlocker.com + 12 country storefronts (local currency), 10 endpoints,
    # 1 credit each. search, product, category, brand and deals take country
    # (13 storefronts) and language (ca: en / fr, be: nl / fr); releases is
    # us, ca, gb; stores, store_availability, reviews and questions are US
    # only. 120 s timeout floor, 240 s for reviews and questions (usually
    # 25-90 s, up to ~3-4 min).
    Endpoint(
        key="footlocker_search",
        namespace="footlocker",
        method="search",
        http="POST",
        path="/api/v1/footlocker/search",
        summary=(
            "Search Foot Locker by keyword on any of 13 storefronts, filtered by brand, gender, "
            "color, price bucket, on_sale and any facet (shoe size per gender, style, sport, "
            "rating...), sorted by relevance, price, new arrivals, top rated, name or brand. "
            + _FOOTLOCKER_GRID_FIELDS
            + " A bare brand keyword (nike, hoka) is answered by the site with a landing page: "
            "the brand's listing is returned instead and redirected_to says which. A keyword the "
            "site sends to a landing page without a product listing (samba, clearance) is an "
            "unbilled 400: use brand(), category() or deals() instead."
        ),
        params=(
            _req("query", "Search keywords, e.g. 'nike dunk'."),
            _FOOTLOCKER_COUNTRY,
            _FOOTLOCKER_LANGUAGE,
            _FOOTLOCKER_BRAND,
            *_FOOTLOCKER_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_product",
        namespace="footlocker",
        method="product",
        http="POST",
        path="/api/v1/footlocker/product",
        summary=(
            "One Foot Locker product by SKU or URL on any of the 13 storefronts: title, brand, "
            "description, genders, sports, category, color, style code, images, rating, "
            "review_count, the price block (price, list_price, percent_off, lowest_price_30d on "
            "European storefronts), availability online / to ship / for pickup, launch info "
            "(is_launch, launch_type, launch_date, web_only), flags, the size chart, every "
            "colorway (sku, color, price, availability) and every size: available, ship, pickup, "
            "stores_available (how many stores show that size as available: a store count, not "
            "units), UPC and store SKU. Availability is yes / no per size: Foot Locker publishes "
            "no unit counts. A SKU without an online page (unknown, store-only or not launched "
            "yet) is a 404." + _FOOTLOCKER_NOT_FOUND
        ),
        params=(*_FOOTLOCKER_PRODUCT_TARGET, _FOOTLOCKER_COUNTRY, _FOOTLOCKER_LANGUAGE),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_category",
        namespace="footlocker",
        method="category",
        http="POST",
        path="/api/v1/footlocker/category",
        summary=(
            "Browse one Foot Locker category by its page path, URL or collection id (Men's "
            "Shoes, Women's Clothing, Kids...), in the site's order by default, with the same "
            "filters and sorts as search(). " + _FOOTLOCKER_GRID_FIELDS + " Also returns the "
            "category's id (collection id), name, path and URL. An unknown category is a 404."
            + _FOOTLOCKER_NOT_FOUND
        ),
        params=(
            _str(
                "path",
                "A Foot Locker category page path (/category/<path>.html), as the site's "
                "category links carry it, e.g. '/category/mens/shoes.html'.",
            ),
            _str("url", "A Foot Locker category URL (its storefront and page are used)."),
            _str(
                "collection_id",
                "A collection id: a previous response's category.id, e.g. 'men-s-shoes' (saves "
                "time on page 2+).",
            ),
            _FOOTLOCKER_COUNTRY,
            _FOOTLOCKER_LANGUAGE,
            _FOOTLOCKER_BRAND,
            *_FOOTLOCKER_GRID,
        ),
        one_of=(("path", "url", "collection_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_brand",
        namespace="footlocker",
        method="brand",
        http="POST",
        path="/api/v1/footlocker/brand",
        summary=(
            "Every Foot Locker product of one brand by name or brand page URL (Nike, Jordan, "
            "adidas, New Balance, HOKA...), optionally narrowed by a keyword, with the same "
            "filters and sorts as search() (except brand). " + _FOOTLOCKER_GRID_FIELDS + " brand "
            "echoes the brand as the site writes it, brand_id its id. An unknown brand is a 404."
            + _FOOTLOCKER_NOT_FOUND
        ),
        params=(
            _str(
                "brand",
                "A brand name, e.g. 'Nike', 'Jordan', 'adidas', 'New Balance', 'HOKA', 'PUMA'; "
                "case does not matter.",
            ),
            _str(
                "url",
                "A Foot Locker brand page URL (/category/brands/<brand>.html). Alternative to "
                "brand.",
            ),
            _str("query", "Narrow the brand to a keyword, e.g. 'running shoes'."),
            _FOOTLOCKER_COUNTRY,
            _FOOTLOCKER_LANGUAGE,
            *_FOOTLOCKER_GRID,
        ),
        one_of=(("brand", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_deals",
        namespace="footlocker",
        method="deals",
        http="POST",
        path="/api/v1/footlocker/deals",
        summary=(
            "Foot Locker deal listings: sale (default; every storefront), Foot Locker Exclusives "
            "(us and ca only) or discount_eligible (the items a promo code applies to), with the "
            "same filters and sorts as search(). " + _FOOTLOCKER_GRID_FIELDS + " No price "
            "history: to track prices over time, poll and store your own."
        ),
        params=(
            _lit(
                "type",
                ("sale", "exclusives", "discount_eligible"),
                "sale (default; every storefront), exclusives (Foot Locker Exclusives; us and ca "
                "only) or discount_eligible (items a promo code applies to).",
            ),
            _FOOTLOCKER_COUNTRY,
            _FOOTLOCKER_LANGUAGE,
            _FOOTLOCKER_BRAND,
            *_FOOTLOCKER_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_releases",
        namespace="footlocker",
        method="releases",
        http="POST",
        path="/api/v1/footlocker/releases",
        summary=(
            "The Foot Locker sneaker release calendar as monitoring data (us, ca, gb): sku, "
            "title, brand, colorway (style), style_code, gender, launch_at, online_at, "
            "heat_level, in_stock, image, url, retail_price and currency (us and ca; gb has no "
            "prices), the reservation status and windows where the storefront runs them (status "
            "open / closed / store_only, starts_at, ends_at, assignment_at, awarding_at, "
            "online_reveal_at, store procedures; not on gb) and sizes (us, eu, uk, participating "
            "channels). Also returns total, count and data_as_of. Filter by status (upcoming / "
            "launched), a date window and brand. Read-only: nothing here enters, reserves or "
            "buys a release."
        ),
        params=(
            _lit("country", ("us", "ca", "gb"), "us (default), ca or gb."),
            _lit("language", ("en", "fr"), "ca only: en (default) or fr."),
            _lit(
                "status",
                ("all", "upcoming", "launched"),
                "all (default), upcoming (launch date ahead) or launched.",
            ),
            _str(
                "date_from",
                "Only releases launching on or after this ISO date, e.g. '2026-11-01'.",
                wire="from",
            ),
            _str(
                "date_to",
                "Only releases launching on or before this ISO date, e.g. '2026-12-31'.",
                wire="to",
            ),
            _str("brand", "Only this brand, e.g. 'Nike' (case does not matter)."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_stores",
        namespace="footlocker",
        method="stores",
        http="POST",
        path="/api/v1/footlocker/stores",
        summary=(
            "Foot Locker stores near a US ZIP code, a city + state or a point (lat + lng), "
            "nearest first (up to 50, default 10, within 25 miles by default, up to 120): "
            "store_id, name, name_secondary, address, city, state, ZIP, phone, lat / lng, "
            "distance_miles, weekly hours, opened_at, alert and closure notices, and the store "
            "page URL. Foot Locker banner stores only (no Kids Foot Locker or Champs). US only."
        ),
        params=(
            *_FOOTLOCKER_WHERE,
            _str("city", "US city (with state), instead of zip, e.g. 'Atlanta'."),
            _str("state", "2-letter US state code (with city), e.g. 'GA'."),
        ),
        one_of=(("zip", "city", "lat"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_store_availability",
        namespace="footlocker",
        method="store_availability",
        http="POST",
        path="/api/v1/footlocker/store-availability",
        summary=(
            "Which Foot Locker stores near a US ZIP code or a point (lat + lng) show a product "
            "(or one size) as available: each store (as in stores()) with available and "
            "sizes_available, plus per size whether it ships online, can be picked up and in how "
            "many of the listed stores it shows (stores_in_results), and "
            "stores_with_availability. Yes / no only: Foot Locker publishes no unit counts. Foot "
            "Locker banner stores only. US only, prices in USD." + _FOOTLOCKER_NOT_FOUND
        ),
        params=(
            *_FOOTLOCKER_PRODUCT_TARGET,
            _str_or_int(
                "size",
                "One size as product() sizes[].size lists it (10.0, 10, XL). Without it, every "
                "size.",
            ),
            *_FOOTLOCKER_WHERE,
        ),
        one_of=(("product_id", "url"), ("zip", "lat")),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="footlocker_reviews",
        namespace="footlocker",
        method="reviews",
        http="POST",
        path="/api/v1/footlocker/reviews",
        summary=(
            "Customer reviews of one Foot Locker (US) product by SKU or URL, 1-98 per call "
            "(default 38), sorted most recent (default), most helpful, highest or lowest rating, "
            "or relevance, optionally only one star rating. Returns the review statistics: "
            "total_reviews (every language), displayed_reviews (the English reviews the site "
            "pages through), average_rating, rating_distribution, recommended_percent, secondary "
            "rating averages (fit, comfort, quality...) and photo_count, plus matching_reviews. "
            "Each review has id, rating, title, text, author nickname, submitted_at, recommended, "
            "helpful and unhelpful votes, verified_purchaser, incentivized, syndicated and its "
            "source, secondary ratings, photos, videos and the brand's response. Reviewer age, "
            "gender, location and IP are never returned. More reviews take longer (about 4 s per "
            "30)." + _FOOTLOCKER_SLOW
        ),
        params=(
            *_FOOTLOCKER_PRODUCT_TARGET,
            _FOOTLOCKER_US_ONLY,
            _lit(
                "sort",
                ("most_recent", "most_helpful", "highest_rating", "lowest_rating", "relevance"),
                "most_recent (default), most_helpful, highest_rating, lowest_rating or relevance.",
            ),
            _int("rating", "Only reviews with this many stars (1-5)."),
            _int("limit", "Reviews to return, 1-98. Defaults to 38."),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=240.0,
    ),
    Endpoint(
        key="footlocker_questions",
        namespace="footlocker",
        method="questions",
        http="POST",
        path="/api/v1/footlocker/questions",
        summary=(
            "Shopper questions about one Foot Locker (US) product by SKU or URL, 1-50 per call "
            "(default 10), newest answered first, with every answer: question, details, author, "
            "submitted_at, answer_count, helpful votes, and per answer its text, author, "
            "author_type (brand, retailer or customer), best-answer flag, date and votes. Also "
            "returns total_questions." + _FOOTLOCKER_SLOW
        ),
        params=(
            *_FOOTLOCKER_PRODUCT_TARGET,
            _FOOTLOCKER_US_ONLY,
            _int("limit", "Questions to return, 1-50. Defaults to 10."),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=240.0,
    ),
    # ============================== Fanatics =============================
    # fanatics.com + 7 country storefronts (local currency) + 4 US league
    # stores (site), 5 endpoints, 1 credit each. Merchandise / product data,
    # not odds. search, product, browse and deals take country, language (ca)
    # and site (country us); reviews is US only. 120 s timeout floor, 300 s
    # for reviews (usually 20-90 s, up to ~4 min).
    Endpoint(
        key="fanatics_search",
        namespace="fanatics",
        method="search",
        http="POST",
        path="/api/v1/fanatics/search",
        summary=(
            "Search Fanatics merchandise (jerseys, hats, fan gear, collectibles) by keyword on 8 "
            "storefronts and 4 US league stores. Narrow by gender, league_id, department_id or any "
            "facet value through filters (team, player, size, color style, autographed...). Sort "
            "by top sellers, price or newest. Misspellings come back corrected "
            "(corrected_query). " + _FANATICS_GRID_FIELDS + _FANATICS_WHERE + " Price filters are "
            "on browse() and deals() (on a keyword search the site loosens the match)."
            + _FANATICS_CHARGE
        ),
        params=(
            _req(
                "query",
                "Search keywords, e.g. 'chiefs jersey'. Misspellings are corrected by the site "
                "(corrected_query).",
            ),
            _FANATICS_COUNTRY,
            _FANATICS_LANGUAGE,
            _FANATICS_SITE,
            _FANATICS_GENDER,
            _fanatics_id(
                "league_id",
                "Narrow to one league (an id from facets: NFL 25, MLB 19, NBA 23, NHL 26, College "
                "5).",
            ),
            _fanatics_id(
                "department_id",
                "Narrow to one department (an id from the facets of the same storefront / store: on "
                "fanatics.com Jerseys 8011, Hats 8008, T-Shirts 8022; nflshop Jerseys 14012).",
            ),
            _FANATICS_FILTERS,
            *_FANATICS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="fanatics_product",
        namespace="fanatics",
        method="product",
        http="POST",
        path="/api/v1/fanatics/product",
        summary=(
            "One Fanatics product by id or URL: title, brand, league, team, player, gender, "
            "categories, breadcrumb, description, details, images, the price block (price, "
            "regular_price, sale_price, clearance_price, with_code_price, code_percent_off, "
            "percent_off, price_label), on_sale (true for sale and clearance markdowns), the site's "
            "current promo code (code, percent_off, tiered, "
            "ends_on, applies_to_product), in_stock, every size (item_id, available, stock_level "
            "low / out, price, with_code_price, ship_by, estimated delivery window, "
            "promise_ship_days), every colorway, personalization (name / number fields with their "
            "rules and the team roster; the price already includes personalization), flags "
            "(jersey_assurance, non_returnable, exclusive, authentic for autographed / "
            "authenticated items), the rating (average, count, distribution, fit, value, "
            "quality), review_count and data_as_of. Stock is a level, never a unit count."
            + _FANATICS_WHERE
            + _FANATICS_CHARGE
        ),
        params=(
            _FANATICS_PRODUCT_ID,
            _str(
                "url",
                "A product URL on any covered storefront or league store (its storefront is "
                "used). Alternative to product_id.",
            ),
            _FANATICS_COUNTRY,
            _FANATICS_LANGUAGE,
            _FANATICS_SITE,
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="fanatics_browse",
        namespace="fanatics",
        method="browse",
        http="POST",
        path="/api/v1/fanatics/browse",
        summary=(
            "Browse a Fanatics listing by its URL or by ids: a team (Lakers 5,000+ products), a "
            "player (Mahomes), a league section (NFL hats), a department, a brand ('47, Nike, New "
            "Era) or a collection, with price_band, on_sale, gender and any facet as filters "
            "(sizes, color style, autographed). The facets list the listing's teams, departments, "
            "brands, collections and sizes with their ids, plus players when the page lists them "
            "(e.g. Lakers). "
            "browse names the league, team, player, department, brand and collection the page "
            "shows. Send url or ids, not both; a league alone is a landing page: combine it with "
            "another id or a filter. " + _FANATICS_GRID_FIELDS + _FANATICS_WHERE + _FANATICS_CHARGE
        ),
        params=(
            _str(
                "url",
                "A Fanatics listing URL: a team, player, league section, department, brand or "
                "collection page, e.g. 'https://www.fanatics.com/nba/los-angeles-lakers/o-23+t-3372'. "
                "Alternative to the ids.",
            ),
            _fanatics_id(
                "league_id",
                "League id (NFL 25, MLB 19, NBA 23, NHL 26, College 5). A league alone is a "
                "landing page: combine it with another id or a filter.",
            ),
            _fanatics_id("team_id", "Team id (from facets: Los Angeles Lakers 3372, Kansas City Chiefs 3433)."),
            _fanatics_id(
                "player_id",
                "Player id, from the players facet when the page lists one (e.g. Lakers) or a "
                "product's player field: Patrick Mahomes 12072, Aaron Judge 31.",
            ),
            _fanatics_id(
                "department_id",
                "Department id from the same store's facets (fanatics.com: Hats 8008, Jerseys 8011; "
                "nflshop Jerseys 14012), or parent-child for a sub-department ('8008-8084').",
            ),
            _fanatics_id("brand_id", "Brand id (from facets.brands: '47 479, Nike 76, New Era 127)."),
            _fanatics_id("collection_id", "Collection id (from facets.productGroups: City Edition 11552)."),
            _FANATICS_COUNTRY,
            _FANATICS_LANGUAGE,
            _FANATICS_SITE,
            _bool("on_sale", "Only sale items."),
            _lit(
                "price_band",
                ("under_25", "25_50", "50_100", "100_150", "over_150"),
                "The site's bands in the storefront's currency, applied to its lowest price (the "
                "with-code price when a promo code applies, so a few items list a little above "
                "the band). Not on jp.",
            ),
            _FANATICS_GENDER,
            _FANATICS_FILTERS,
            *_FANATICS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="fanatics_deals",
        namespace="fanatics",
        method="deals",
        http="POST",
        path="/api/v1/fanatics/deals",
        summary=(
            "Fanatics deal listings: sale (default: the site's Sale listing, coupon-eligible items "
            "and clearance markdowns), clearance (each sale page's clearance-priced items; total "
            "counts the whole sale listing) or under_25 (items under 25 in the storefront's "
            "currency, by the site's lowest price; not on jp), optionally for one league, team, "
            "department or brand. " + _FANATICS_GRID_FIELDS + " No price history: to track sale "
            "prices over time, poll and store your own." + _FANATICS_WHERE + _FANATICS_CHARGE
        ),
        params=(
            _lit(
                "type",
                ("sale", "clearance", "under_25"),
                "sale (default), clearance or under_25 (not on jp).",
            ),
            _fanatics_id("league_id", "Only one league (NFL 25, MLB 19, NBA 23, NHL 26, College 5)."),
            _fanatics_id("team_id", "Only one team (Los Angeles Lakers 3372, Kansas City Chiefs 3433)."),
            _fanatics_id(
                "department_id",
                "Only one department, from the same store's facets (fanatics.com: Hats 8008, "
                "Jerseys 8011; nflshop Jerseys 14012).",
            ),
            _fanatics_id("brand_id", "Only one brand ('47 479, Nike 76, New Era 127)."),
            _FANATICS_COUNTRY,
            _FANATICS_LANGUAGE,
            _FANATICS_SITE,
            *_FANATICS_GRID,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="fanatics_reviews",
        namespace="fanatics",
        method="reviews",
        http="POST",
        path="/api/v1/fanatics/reviews",
        summary=(
            "Customer reviews of one Fanatics (fanatics.com, US) product by id or URL, 1-50 per "
            "call (default 10), sorted highest rated (default, the site's order), lowest rated, "
            "most recent or most helpful, optionally only one star rating. Returns stats "
            "(review_count, rating_count, average, distribution, fit, quality and value "
            "averages), the site's own AI-written review summary (ai_summary) and the features "
            "reviewers mention. Each review has id, product_id and product_title, rating, fit, "
            "quality, value, recommended, title, text, author nickname, submitted_at, updated_at, "
            "incentivized, helpful and unhelpful votes, features with sentiment and photos. "
            "Fanatics pools reviews across a style: the list (and matching_reviews) covers "
            "sibling products of the same cut, so check each review's product_id. Slow: usually "
            "20-90 s, up to about 4 minutes when a call is retried; when busy it returns 503 with "
            "Retry-After. Failed calls are not charged; an unknown product is a charged 404. US "
            "only."
        ),
        params=(
            _FANATICS_PRODUCT_ID,
            _str("url", "A fanatics.com product URL. Alternative to product_id."),
            _lit("country", ("us",), "us only."),
            _lit(
                "sort",
                ("highest_rated", "lowest_rated", "most_recent", "most_helpful"),
                "highest_rated (default, the site's order), lowest_rated, most_recent or "
                "most_helpful.",
            ),
            _int("rating", "Only reviews with this many stars (1-5)."),
            _int(
                "limit",
                "Reviews to return, 1-50. Defaults to 10. More than 10 takes a few seconds longer "
                "per 8.",
            ),
        ),
        one_of=(("product_id", "url"),),
        credits=1,
        min_timeout=300.0,
    ),
    # ============================== Carrefour ============================
    # carrefour.fr (every endpoint) + Argentina, Romania and Belgium (search
    # and product), 9 endpoints, 1 credit each; be search / product cost 2.
    # store (fr) scopes prices and assortment to one store. 120 s timeout
    # floor (store-scoped and retried calls can take longer than 30 s).
    Endpoint(
        key="carrefour_search",
        namespace="carrefour",
        method="search",
        http="POST",
        path="/api/v1/carrefour/search",
        summary=(
            "Search Carrefour grocery and household products by keyword: carrefour.fr with every "
            "filter (brand, promotion, Nutri-Score, organic, Carrefour brands, price range), sorts "
            "by price, unit price or rating, and store-scoped prices; also the Argentina (ARS), "
            "Romania (RON) and Belgium (EUR, French or Dutch) sites, which return the fields "
            "their site carries (no facets or store scope). Misspellings come back corrected "
            "(corrected_query); when nothing matches results_type is 'fallback'."
            + _CARREFOUR_GRID_FIELDS
            + _CARREFOUR_SCOPE
            + " Markets: "
            + _CARREFOUR_MARKETS
            + "."
            + _CARREFOUR_CHARGE
        ),
        params=(
            _req(
                "query",
                "Search keywords, e.g. 'nutella' or 'lait'. Misspellings are corrected by the site "
                "on fr (corrected_query).",
            ),
            _CARREFOUR_COUNTRY,
            _CARREFOUR_LANGUAGE,
            _CARREFOUR_STORE,
            _CARREFOUR_PAGE,
            _CARREFOUR_SORT,
            *_CARREFOUR_FILTERS,
            _CARREFOUR_PROMOTION_FILTER,
        ),
        credits=1,
        credits_note="Costs 1 credit, or 2 when country is 'be'.",
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_product",
        namespace="carrefour",
        method="product",
        http="POST",
        path="/api/v1/carrefour/product",
        summary=(
            "One Carrefour product by EAN or URL. On fr: title, brand, description, key "
            "features, breadcrumb, categories, images, packaging, format, origin, Nutri-Score, "
            "Eco-Score, regulated name, ingredients, allergens (as written in capitals in the "
            "ingredients), nutrition per 100 g / ml and per portion (with daily value %), storage "
            "and advice, characteristics (non-food), weights, the price block (price, unit price, "
            "tax note, promotion with loyalty_only), availability, the marketplace seller and "
            "every offer, and the rating (average, count, distribution)."
            + _CARREFOUR_SCOPE
            + " ar (by EAN or URL), ro and be (by URL only) return title, brand, price, list "
            "price, promotion, unit price, availability, description, images and categories as "
            "their site gives them."
            + _CARREFOUR_CHARGE
        ),
        params=(
            _str(
                "ean",
                "The product barcode (EAN / GTIN): items[].ean of a search, e.g. '3017620422003'. "
                "fr and ar.",
            ),
            _str(
                "url",
                "A product URL (items[].url of a search). Alternative to ean on fr and ar; "
                "required on ro and be.",
            ),
            _CARREFOUR_COUNTRY,
            _CARREFOUR_LANGUAGE,
            _CARREFOUR_STORE,
            _str_or_int(
                "seller",
                "fr: a marketplace seller id (items[].seller.id) to read that seller's offer.",
            ),
        ),
        one_of=(("ean", "url"),),
        credits=1,
        credits_note="Costs 1 credit, or 2 when country is 'be'.",
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_reviews",
        namespace="carrefour",
        method="reviews",
        http="POST",
        path="/api/v1/carrefour/reviews",
        summary=(
            "Verified-purchase customer reviews of one carrefour.fr product by EAN, 1-50 per call "
            "(default 10), sorted most recent (default), oldest, highest or lowest rated, "
            "optionally only one star rating, with offset paging: total, has_more and per review "
            "author (public first name and last initial, as published), rating, title, text, "
            "reviewed_at, purchased_at and source (the verified-review provider). Review text is "
            "in French." + _CARREFOUR_FR_NOTE + _CARREFOUR_CHARGE
        ),
        params=(
            _carrefour_ean(),
            _CARREFOUR_FR,
            _lit(
                "sort",
                ("most_recent", "oldest", "highest_rated", "lowest_rated"),
                "most_recent (default), oldest, highest_rated or lowest_rated.",
            ),
            _int("rating", "Only reviews with this many stars (1-5)."),
            _int("limit", "Reviews to return, 1-50. Defaults to 10."),
            _int("offset", "Reviews to skip (paging). Defaults to 0."),
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_category",
        namespace="carrefour",
        method="category",
        http="POST",
        path="/api/v1/carrefour/category",
        summary=(
            "A carrefour.fr category (aisle) grid by URL or path (/r/cremerie, "
            "/r/epicerie-sucree/petit-dejeuner), with the same filters and sorts as search() and "
            "the category's label, path, url and breadcrumb. A product's breadcrumb[].url is a "
            "valid path." + _CARREFOUR_GRID_FIELDS + _CARREFOUR_SCOPE + _CARREFOUR_FR_NOTE
            + _CARREFOUR_CHARGE
        ),
        params=(
            _str(
                "url",
                "A carrefour.fr category page URL (/r/...), e.g. "
                "'https://www.carrefour.fr/r/cremerie'. Alternative to path.",
            ),
            _str(
                "path",
                "The category path ('/r/cremerie', '/r/epicerie-sucree/petit-dejeuner') or its "
                "slug ('cremerie'): a breadcrumb[].url of a product. Alternative to url.",
            ),
            _CARREFOUR_FR,
            _CARREFOUR_STORE,
            _CARREFOUR_PAGE,
            _CARREFOUR_SORT,
            *_CARREFOUR_FILTERS,
            _CARREFOUR_PROMOTION_FILTER,
        ),
        one_of=(("url", "path"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_promotions",
        namespace="carrefour",
        method="promotions",
        http="POST",
        path="/api/v1/carrefour/promotions",
        summary=(
            "carrefour.fr items on promotion: all (default), catalogue (seen in the printed "
            "catalogue), immediate (immediate discounts), loyalty (loyalty-card offers, i.e. "
            "member prices) or festive (the site's seasonal festive selection), optionally for "
            "one aisle, with the search filters and sorts. Each promotion carries type, label, "
            "loyalty_only, discounted_price and initial_price (discounted_price is null when the site "
            "does not price the deal, as on some multi-buy offers), and its start and end dates. Not the printed leaflet itself and "
            "no price history: to track promotions over time, poll and store your own."
            + _CARREFOUR_GRID_FIELDS
            + _CARREFOUR_SCOPE
            + _CARREFOUR_FR_NOTE
            + _CARREFOUR_CHARGE
        ),
        params=(
            _lit(
                "type",
                ("all", "catalogue", "immediate", "loyalty", "festive"),
                "all (default), catalogue (Vu en catalogue), immediate (Remises immédiates), "
                "loyalty (Avantage Fidélité) or festive (Sélection festive).",
            ),
            _str(
                "category",
                "Only one aisle: a value of the Rayons facet "
                "(facets[id=product.categories.name].values[].label), e.g. 'Boissons'.",
            ),
            _CARREFOUR_FR,
            _CARREFOUR_STORE,
            _CARREFOUR_PAGE,
            _CARREFOUR_SORT,
            *_CARREFOUR_FILTERS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_suggestions",
        namespace="carrefour",
        method="suggestions",
        http="POST",
        path="/api/v1/carrefour/suggestions",
        summary=(
            "carrefour.fr search box suggestions for a partial query: suggestions (text, url) and "
            "category suggestions (category, text, url), in French." + _CARREFOUR_FR_NOTE
            + _CARREFOUR_CHARGE
        ),
        params=(
            _req("query", "What a shopper has typed so far, e.g. 'nutel'."),
            _CARREFOUR_FR,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_stores",
        namespace="carrefour",
        method="stores",
        http="POST",
        path="/api/v1/carrefour/stores",
        summary=(
            "Carrefour stores in France near a postal code or a point (lat + lng), nearest first "
            "(up to 20 per page), optionally only those with one service (drive, home delivery, "
            "fuel station...). Each store has id, store_ref and pickup_refs (pass either as store "
            "on search(), product(), category() or promotions() for that store's prices), name, "
            "banner, format, distance_km, address, lat, lng, open_today and today's opening "
            "hours, slug (for store()) and store_url." + _CARREFOUR_FR_NOTE + _CARREFOUR_CHARGE
        ),
        params=(
            _str("postal_code", "A French postal code, e.g. '69003'. Alternative to lat + lng."),
            _float("lat", "Latitude (metropolitan France), with lng."),
            _float("lng", "Longitude, with lat."),
            _int("page", "Page of stores, 1-based (up to 50)."),
            _int("limit", "Stores per page, 1-20. Defaults to 10."),
            _lit(
                "service",
                (
                    "drive",
                    "lad",
                    "Retrait2h-drive",
                    "station_service",
                    "banque_assurance",
                    "spectacles",
                    "voyages",
                    "location_vehicule",
                    "traiteur",
                    "Parapharmacie",
                    "pro",
                ),
                "Only stores with this service: drive, lad (home delivery), Retrait2h-drive, "
                "station_service (fuel station), banque_assurance, spectacles, voyages, "
                "location_vehicule, traiteur, Parapharmacie or pro.",
            ),
            _CARREFOUR_FR,
        ),
        one_of=(("postal_code", "lat"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_store_availability",
        namespace="carrefour",
        method="store_availability",
        http="POST",
        path="/api/v1/carrefour/store-availability",
        summary=(
            "Whether the Carrefour stores around a French postal code carry one product (EAN): "
            "count, available_count and per store available yes / no, distance_km and the store "
            "(id, ref, pickup_refs, name, banner, format, address, lat, lng, phone, weekly "
            "opening hours and drive hours, slug, store_url). Availability only, no price and no "
            "unit count: for a store's price call search() or product() with store set to "
            "stores[].store.ref." + _CARREFOUR_FR_NOTE + _CARREFOUR_CHARGE
        ),
        params=(
            _carrefour_ean(),
            _req("postal_code", "A French postal code, e.g. '69003': stores around it are checked."),
            _CARREFOUR_FR,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="carrefour_store",
        namespace="carrefour",
        method="store",
        http="POST",
        path="/api/v1/carrefour/store",
        summary=(
            "One Carrefour store in France by slug or URL: name, banner, format, type, status, "
            "address, lat, lng, phone, services, weekly opening hours and drive hours, the next "
            "pickup slots as shown, delivery and express delivery flags, nearby stores and, at "
            "stores with a fuel station, fuel prices per litre (Gazole, SP95, SP95-E10, SP98, "
            "E85, GPLc) with their update times (fuel is None elsewhere). No delivery-slot "
            "booking." + _CARREFOUR_FR_NOTE + _CARREFOUR_CHARGE
        ),
        params=(
            _str(
                "slug",
                "A store page slug: stores[].slug from stores(), e.g. 'venissieux' or "
                "'lyon-part-dieu'. Alternative to url.",
            ),
            _str(
                "url",
                "A carrefour.fr/magasin/... store page URL, e.g. "
                "'https://www.carrefour.fr/magasin/venissieux'. Alternative to slug.",
            ),
            _CARREFOUR_FR,
        ),
        one_of=(("slug", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    # ============================== Allegro ==============================
    # allegro.pl + allegro.cz, allegro.sk and allegro.hu on every endpoint,
    # 7 endpoints, 2 credits each. buying_format and deals are pl only (400
    # elsewhere). 120 s timeout floor (sk / hu take up to ~60 s per attempt).
    Endpoint(
        key="allegro_search",
        namespace="allegro",
        method="search",
        http="POST",
        path="/api/v1/allegro/search",
        summary=(
            "Search Allegro, the largest marketplace in Poland and Central Europe, by keyword: "
            "sort by price, price with delivery, popularity, ending soonest or newest; filter by "
            "price range, new or used, buy now or auction (pl), Allegro Smart! and deals (pl); "
            "optionally inside one category. Sponsored and promoted offers are flagged. "
            "Misspellings are not corrected." + _ALLEGRO_GRID_FIELDS + _ALLEGRO_OMNIBUS
            + _ALLEGRO_NOTE
        ),
        params=(
            _req("query", "Search keywords, in any language, e.g. 'laptop' or 'buty nike'."),
            _ALLEGRO_COUNTRY,
            _ALLEGRO_PAGE,
            _ALLEGRO_SORT,
            _str_or_int(
                "category_id",
                "Search inside one category: a category id (category.id or breadcrumb[].id of an "
                "offer, e.g. 491 = laptops) or its slug (laptopy-491).",
            ),
            *_ALLEGRO_FILTERS,
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="allegro_offer",
        namespace="allegro",
        method="offer",
        http="POST",
        path="/api/v1/allegro/offer",
        summary=(
            "One Allegro offer (one seller's listing, /oferta) by number or link: title, "
            "condition, status, price, original_price and lowest_price_30d with discount_percent "
            "on a discount, price_with_delivery, stock (units available as shown), sold_count "
            "(None on auctions and on cz, sk and hu offers), auction state (current price, "
            "minimum next bid, bid step, end time, whether anyone has bid) or buy now price, "
            "every parameter (EAN / GTIN, brand, model...), gtin, brand, the seller's description "
            "as plain text, images, breadcrumb, delivery methods with price and estimated "
            "delivery, handling time, returns (days), warranty, the product's rating and offer "
            "count (product_id for product_offers()), and the seller (login, super seller, "
            "positive feedback percent and counts for the last 12 months, is_business, "
            "company_name for business sellers). No bid history." + _ALLEGRO_OMNIBUS
            + _ALLEGRO_NOTE
        ),
        params=(
            _str_or_int(
                "offer_id",
                "An offer number: items[].offer_id of a search, category or seller answer, e.g. "
                "'17858046919'. Alternative to url.",
            ),
            _str(
                "url",
                "An offer link (allegro.pl/oferta/..., or a product link with ?offerId=; any of "
                "the four sites). Alternative to offer_id.",
            ),
            _ALLEGRO_COUNTRY,
        ),
        one_of=(("offer_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="allegro_product",
        namespace="allegro",
        method="product",
        http="POST",
        path="/api/v1/allegro/product",
        summary=(
            "One Allegro catalogue product (/produkt: one item that groups many sellers' offers) "
            "by id or link: title, brand, GTIN, parameters, images, breadcrumb, description, "
            "lowest_price and offer_count (every seller's offer is on product_offers()), the "
            "cheapest and fastest offers as the page highlights them, the featured (buy box) "
            "offer with its price, 30-day lowest price, stock, sold count and seller, how many "
            "people bought it recently, the rating (average, count, 1-5 star distribution), "
            "review aspects (topic, sentiment, mention counts) and the first 20 reviews as shown "
            "on the product page (rating, text, pros, cons, author as published e.g. 'b...y', "
            "date, helpful votes, images, is_best). Not the full review history." + _ALLEGRO_NOTE
        ),
        params=_ALLEGRO_PRODUCT_TARGET,
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="allegro_product_offers",
        namespace="allegro",
        method="product_offers",
        http="POST",
        path="/api/v1/allegro/product-offers",
        summary=(
            "Every seller's offer for one Allegro catalogue product: the price comparison page, "
            "for price monitoring across sellers. 60 offers per page, sortable by price or price "
            "with delivery and filterable by condition, price and Allegro Smart!. Each offer has "
            "price, price_with_delivery, delivery_text, condition, seller (login, super seller, "
            "positive feedback percent and count, is_business), smart, stock where shown, "
            "is_featured (the buy box offer) and the listing fields of search(). Also total, "
            "total_pages, page and facets. Promoted offers can come first as their own block."
            + _ALLEGRO_NOTE
        ),
        params=(
            *_ALLEGRO_PRODUCT_TARGET,
            _ALLEGRO_PAGE,
            _lit(
                "sort",
                (
                    "relevance",
                    "price_low_to_high",
                    "price_high_to_low",
                    "price_with_delivery_low_to_high",
                    "price_with_delivery_high_to_low",
                    "popularity",
                ),
                "relevance (default), price_low_to_high, price_high_to_low, "
                "price_with_delivery_low_to_high, price_with_delivery_high_to_low or popularity.",
            ),
            *_ALLEGRO_PRICE_CONDITION,
        ),
        one_of=(("product_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="allegro_seller",
        namespace="allegro",
        method="seller",
        http="POST",
        path="/api/v1/allegro/seller",
        summary=(
            "One Allegro seller's offers by login, with the seller (id, login, is_business, url; "
            "the super seller status, feedback score and member since are on "
            "seller_feedback()), whether the seller is active, and the categories the seller "
            "sells in (with offer counts and a slug for category); search within the seller's "
            "offers and use the search sorts and filters. No seller address or tax id."
            + _ALLEGRO_GRID_FIELDS
            + _ALLEGRO_NOTE
        ),
        params=(
            _ALLEGRO_LOGIN,
            _ALLEGRO_COUNTRY,
            _str("query", "Search within the seller's offers."),
            _str(
                "category",
                "Only one of the seller's categories: categories[].slug of a previous seller() "
                "answer (e.g. komputery).",
            ),
            _ALLEGRO_PAGE,
            _ALLEGRO_SORT,
            *_ALLEGRO_FILTERS,
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="allegro_seller_feedback",
        namespace="allegro",
        method="seller_feedback",
        http="POST",
        path="/api/v1/allegro/seller-feedback",
        summary=(
            "One Allegro seller's buyer ratings: summary (recommended and not recommended "
            "counts, unique counts, positive_percent, received, excluded and removed ratings, "
            "member_since, super_seller) and 20 ratings per page, newest first, each with "
            "recommended yes / no, comment, the reasons given (e.g. on-time delivery), date, the "
            "offers rated, and whether it was excluded from the score and why. No buyer identity "
            "is returned." + _ALLEGRO_NOTE
        ),
        params=(
            _ALLEGRO_LOGIN,
            _ALLEGRO_COUNTRY,
            _int("page", "Ratings page, 1-based (up to 500). 20 ratings per page, newest first."),
        ),
        credits=2,
        min_timeout=120.0,
    ),
    Endpoint(
        key="allegro_category",
        namespace="allegro",
        method="category",
        http="POST",
        path="/api/v1/allegro/category",
        summary=(
            "One Allegro category's offers by id or link, with the same sorts and filters as "
            "search() and an optional query, plus the category (id, name, url, breadcrumb, "
            "subcategories or sibling categories with offer counts)." + _ALLEGRO_GRID_FIELDS
            + _ALLEGRO_NOTE
        ),
        params=(
            _str_or_int(
                "category_id",
                "A category id (e.g. 491 = laptops) or its slug (laptopy-491): breadcrumb[].id "
                "of an offer or subcategories[].id of a category answer. Alternative to url.",
            ),
            _str(
                "url",
                "A category link (allegro.pl/kategoria/..., any of the four sites), e.g. "
                "'https://allegro.pl/kategoria/laptopy-491'. Alternative to category_id.",
            ),
            _ALLEGRO_COUNTRY,
            _str("query", "Search within the category."),
            _ALLEGRO_PAGE,
            _ALLEGRO_SORT,
            *_ALLEGRO_FILTERS,
        ),
        one_of=(("category_id", "url"),),
        credits=2,
        min_timeout=120.0,
    ),
    # ================================ OLX ================================
    # OLX Europe: olx.pl + olx.ro, olx.pt, olx.bg, olx.ua, olx.kz, olx.uz, 9 endpoints,
    # 1 credit each. filters() and similar() are pl, ro, pt, bg and ua only; language is
    # kz / uz only (search, seller_ads, offer); olx_delivery is refused on kz and uz.
    # 120 s timeout floor (a call can take up to about a minute with retries).
    Endpoint(
        key="olx_search",
        namespace="olx",
        method="search",
        http="POST",
        path="/api/v1/olx/search",
        summary=(
            "Search OLX classifieds (used goods, cars, real estate, jobs, services) by keyword "
            "and / or category: sort by newest or price; filter by price range, condition, "
            "private or business seller, OLX delivery, photos, region / city / district with a "
            "radius, and the category's own filters (rooms, area, year, mileage ... from "
            "filters()). Up to 1000 results per query (OLX's own cap). Promoted ads are "
            "interleaved and flagged. A query with no exact match returns the closest ads, "
            "never an empty list." + _OLX_SCOPE + _OLX_GRID_FIELDS + _OLX_LANG_NOTE
            + _OLX_PRIVACY + " Markets: " + _OLX_MARKETS + "." + _OLX_CHARGE
        ),
        params=(
            _str(
                "query",
                "Search keywords, in any language, e.g. 'iphone'. query, category_id or both.",
            ),
            _str_or_int(
                "category_id",
                "Search inside one category: categories[].id of categories() or an item's "
                "category_id, e.g. 84 = cars on olx.pl.",
            ),
            _OLX_COUNTRY,
            _OLX_LANGUAGE,
            *_OLX_GRID_PARAMS,
        ),
        one_of=(("query", "category_id"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_offer",
        namespace="olx",
        method="offer",
        http="POST",
        path="/api/v1/olx/offer",
        summary=(
            "One OLX ad by id or link: title, the full description as plain text, " + _OLX_PRICE
            + ", salary for jobs, condition, every parameter (a car's VIN is never returned), "
            "category with breadcrumb, all photos, location (city, district, region with ids), "
            "created_at, refreshed_at, valid_to, status, is_active, is_promoted, olx_delivery, "
            "is_job and the seller (id, is_business, business_name for business sellers, "
            "member_since). An ad that does not exist and an ad that has ended answer the same "
            "404 ('not found or no longer active'). No view counts, phone numbers or messaging."
            + _OLX_SCOPE + _OLX_LANG_NOTE + _OLX_PRIVACY + " Markets: " + _OLX_MARKETS + "."
            + _OLX_CHARGE
        ),
        params=(*_OLX_OFFER_TARGET, _OLX_COUNTRY, _OLX_LANGUAGE),
        one_of=(("offer_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_seller",
        namespace="olx",
        method="seller",
        http="POST",
        path="/api/v1/olx/seller",
        summary=(
            "One OLX seller by id: is_business (from the seller's own ads), business_name "
            "(business sellers only; None otherwise), member_since, active_ads (the number of "
            "live ads; None on kz and uz from 1000 ads up) and ads_url (the seller's page on "
            "OLX). OLX shows no seller ratings or reviews, so none are returned." + _OLX_PRIVACY
            + " Markets: " + _OLX_MARKETS + "." + _OLX_CHARGE
        ),
        params=(_OLX_USER_ID, _OLX_COUNTRY),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_seller_ads",
        namespace="olx",
        method="seller_ads",
        http="POST",
        path="/api/v1/olx/seller-ads",
        summary=(
            "One OLX seller's live ads, with the search() sorts and filters and an optional "
            "query." + _OLX_GRID_FIELDS + _OLX_LANG_NOTE + _OLX_PRIVACY + " Markets: "
            + _OLX_MARKETS + "." + _OLX_CHARGE
        ),
        params=(
            _OLX_USER_ID,
            _str("query", "Search within the seller's ads."),
            _str_or_int("category_id", "Only the seller's ads in this category."),
            _OLX_COUNTRY,
            _OLX_LANGUAGE,
            *_OLX_GRID_PARAMS,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_filters",
        namespace="olx",
        method="filters",
        http="POST",
        path="/api/v1/olx/filters",
        summary=(
            "The filters one OLX category offers, ready to send as search() filters: each with "
            "key, label, type, kind (range or choice), unit, send_as (the filters keys to use), "
            "suggested range steps, and for choice filters every value with its label and the "
            "number of matching ads. Also the category's ad counts per region (or per city "
            "inside region_id) and per category. Markets: " + _OLX_MARKETS_NO_KZ_UZ + "."
            + _OLX_CHARGE
        ),
        params=(
            Param(
                "category_id",
                "Union[str, int]",
                required=True,
                doc="The category (categories[].id of categories()), e.g. 14 = flats for sale "
                "on olx.pl, 84 = cars.",
            ),
            _str("query", "Count values for this keyword inside the category."),
            _str_or_int(
                "region_id",
                "Count values in this region only (locations then lists its cities).",
            ),
            _OLX_COUNTRY_NO_KZ_UZ,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_categories",
        namespace="olx",
        method="categories",
        http="POST",
        path="/api/v1/olx/categories",
        summary=(
            "The OLX category tree of one site: id, name, parent_id, level, path, url, type and "
            "count (active ads), with children. Without parent_id: the top-level categories and "
            "their direct children (children_count tells which go deeper); with parent_id: that "
            "category's whole subtree. Names come in the site's language. Markets: "
            + _OLX_MARKETS + "." + _OLX_CHARGE
        ),
        params=(
            _str_or_int(
                "parent_id",
                "Return this category's whole subtree, e.g. 5. Without it: the top-level "
                "categories with their direct children.",
            ),
            _OLX_COUNTRY,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_locations",
        namespace="olx",
        method="locations",
        http="POST",
        path="/api/v1/olx/locations",
        summary=(
            "Place autocomplete for OLX location filters: cities and districts matching a name, "
            "with city_id, district_id and region_id to send to search(), plus the "
            "municipality, county and region names. Markets: " + _OLX_MARKETS + "."
            + _OLX_CHARGE
        ),
        params=(
            _req("query", "At least 2 letters of a city or district name, e.g. 'Warszawa'."),
            _OLX_COUNTRY,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_suggestions",
        namespace="olx",
        method="suggestions",
        http="POST",
        path="/api/v1/olx/suggestions",
        summary=(
            "The suggestions the OLX search box shows for what a user typed: popular searches, "
            "each with the category it is most searched in (category_id, name and its parent "
            "categories). Markets: " + _OLX_MARKETS + "." + _OLX_CHARGE
        ),
        params=(
            _req("query", "What the user has typed so far, e.g. 'rower'."),
            _OLX_COUNTRY,
        ),
        credits=1,
        min_timeout=120.0,
    ),
    Endpoint(
        key="olx_similar",
        namespace="olx",
        method="similar",
        http="POST",
        path="/api/v1/olx/similar",
        summary=(
            "The ads OLX recommends next to one ad (about 30), in the search() item shape: "
            + _OLX_ITEM + ". Also offer_id, count, country, language and currency."
            + _OLX_PRIVACY + " Markets: " + _OLX_MARKETS_NO_KZ_UZ + "." + _OLX_CHARGE
        ),
        params=(*_OLX_OFFER_TARGET, _OLX_COUNTRY_NO_KZ_UZ),
        one_of=(("offer_id", "url"),),
        credits=1,
        min_timeout=120.0,
    ),
    # ============================== Company ==============================
    # 1 endpoint, body-priced: 10 credits from a url, 20 from a place_id (1
    # when the listing has no readable website), unreachable site free. One of
    # url / place_id is required; both are accepted (url is the site read).
    # Median ~23 s, p90 ~44 s; slow sites measured 101-125 s (2026-11-12): 180 s floor.
    Endpoint(
        key="company_enrich",
        namespace="company",
        method="enrich",
        http="POST",
        path="/api/v1/company/enrich",
        summary=(
            "Find a company's contact details and its owner from its website or a Google Maps "
            "place_id: published emails, phone numbers, social profiles and contact page, plus "
            "the owner's name and title with the page that names them. Use after a Google Maps "
            "search: pass each result's place_id. Provide url or place_id (one is required). "
            "Returns data.company (name, website, domain, emails, phones as digits only, socials "
            "keyed facebook / instagram / linkedin / x / tiktok / youtube / pinterest when found, "
            "contact_page, address, place_id), data.owner (name, title, source_url, email, "
            "email_status 'published' or 'not_found'; None when no page names an owner) and "
            "data.pages_read (home, up to 3 contact / about / team pages, privacy and terms). "
            "Usually takes 10-45s and can take over a minute."
        ),
        params=(
            Param(
                "url",
                "Optional[str]",
                positional=True,
                doc=(
                    "The company's own website (3-2048 characters); a bare domain works. Social "
                    "profile links (Facebook, Instagram, LinkedIn...) are rejected with 400. "
                    "Alternative to place_id; when both are sent, url is the site read."
                ),
            ),
            Param(
                "place_id",
                "Optional[str]",
                positional=True,
                doc=(
                    "A Google Maps place_id (10-300 characters), e.g. local_results[].place_id of "
                    "google.maps_search(). The listing (name, address, phone, website) is looked "
                    "up first, then its website is read. Alternative to url."
                ),
            ),
        ),
        one_of=(("url", "place_id"),),
        credits=10,
        credits_note=(
            "Costs 10 credits from a url and 20 from a place_id (1 when the listing has no "
            "readable website); a website that cannot be reached and a 400 are not charged. "
            "credits_used in the response is the exact charge."
        ),
        min_timeout=180.0,
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
    "decathlon",
    "specs",
    "lowes",
    "sams_club",
    "canadian_tire",
    "dollar_general",
    "sephora",
    "ulta",
    "aldi",
    "micro_center",
    "walgreens",
    "cvs",
    "whole_foods",
    "harbor_freight",
    "petsmart",
    "petco",
    "iherb",
    "chewy",
    "menards",
    "nordstrom",
    "nordstrom_rack",
    "best_buy",
    "tcgplayer",
    "vinted",
    "macys",
    "saks",
    "kohls",
    "jcpenney",
    "dicks",
    "footlocker",
    "fanatics",
    "carrefour",
    "allegro",
    "olx",
    "company",
    "trustpilot",
    "realtor",
    "rightmove",
    "mercadolibre",
    "chatgpt",
    "gemini",
    "heb",
    "kroger",
    "publix",
    "ikea",
    "wayfair",
    "ashley",
    "maisonsdumonde",
)


def endpoints_for(namespace: str) -> list[Endpoint]:
    return [ep for ep in _ENDPOINTS if ep.namespace == namespace]
