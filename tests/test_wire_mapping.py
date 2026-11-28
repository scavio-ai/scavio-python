"""Every endpoint, every parameter -> wire-field mapping, on sync and async."""

from __future__ import annotations

import inspect
import re

import pytest

from scavio import AsyncScavioClient, ScavioClient, ScavioError
from scavio._spec import ENDPOINTS

from ._endpoint_cases import POST_KEYS, values_and_expected
from .conftest import patch_async, patch_sync


@pytest.mark.parametrize("key", POST_KEYS)
def test_wire_body_sync(key, monkeypatch):
    ep = ENDPOINTS[key]
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    values, expected = values_and_expected(ep)
    getattr(getattr(client, ep.namespace), ep.method)(**values)
    assert captured["method"] == "POST"
    assert captured["path"] == ep.path
    assert captured["json"] == expected


@pytest.mark.parametrize("key", POST_KEYS)
async def test_wire_body_async(key, monkeypatch):
    ep = ENDPOINTS[key]
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    values, expected = values_and_expected(ep)
    await getattr(getattr(client, ep.namespace), ep.method)(**values)
    assert captured["method"] == "POST"
    assert captured["path"] == ep.path
    assert captured["json"] == expected


def test_none_values_dropped(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.google.search("openai", gl="us", hl=None, device=None)
    assert captured["json"] == {"query": "openai", "gl": "us"}


def test_extra_passthrough(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.google.search("openai", **{"tbm": "nws", "custom": 1})
    assert captured["json"] == {"query": "openai", "tbm": "nws", "custom": 1}


def test_extra_collision_raises(monkeypatch):
    patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(TypeError):
        client.youtube.search("cats", four_k=True, **{"4k": False})


def test_youtube_digit_aliases(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.search("cats", four_k=True, video_360=True, video_3d=True)
    assert captured["path"] == "/api/v1/youtube/search"
    assert captured["json"] == {"search": "cats", "4k": True, "360": True, "3d": True}


def test_youtube_search_features_and_cursor(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.search("cats", features=["hd", "4k"], cursor="c1")
    assert captured["path"] == "/api/v1/youtube/search"
    assert captured["json"] == {"search": "cats", "features": ["hd", "4k"], "cursor": "c1"}


def test_youtube_search_has_no_location_flag():
    """location was never in the backend schema; it must not be offered."""
    sig = inspect.signature(ScavioClient(api_key="sk_test").youtube.search)
    assert "location" not in sig.parameters


def test_youtube_shorts_sort_by_is_typed(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.shorts("funny cats", sort_by="view_count", cursor="c1")
    assert captured["path"] == "/api/v1/youtube/shorts"
    assert captured["json"] == {"search": "funny cats", "sort_by": "view_count", "cursor": "c1"}


def test_youtube_video_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.video("dQw4w9WgXcQ")
    assert captured["path"] == "/api/v1/youtube/video"
    assert captured["json"] == {"video_id": "dQw4w9WgXcQ"}


def test_youtube_metadata_alias_posts_to_video(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.metadata("dQw4w9WgXcQ")
    assert captured["path"] == "/api/v1/youtube/video"
    assert captured["json"] == {"video_id": "dQw4w9WgXcQ"}


def test_youtube_comment_replies_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.comment_replies("vid", "rc1", cursor="c2")
    assert captured["path"] == "/api/v1/youtube/comments/replies"
    assert captured["json"] == {"video_id": "vid", "reply_cursor": "rc1", "cursor": "c2"}


def test_youtube_transcript_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.transcript("vid", language="en", format="srt")
    assert captured["path"] == "/api/v1/youtube/transcript"
    assert captured["json"] == {"video_id": "vid", "language": "en", "format": "srt"}


def test_youtube_channel_resolve_param(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.channel_resolve("@mkbhd")
    assert captured["path"] == "/api/v1/youtube/channel/resolve"
    assert captured["json"] == {"channel": "@mkbhd"}


def test_youtube_streams_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.youtube.streams("vid")
    assert captured["path"] == "/api/v1/youtube/streams"
    assert captured["json"] == {"video_id": "vid"}


def test_amazon_product_asin_alias(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.amazon.product("B09XS7JWHH", country="gb")
    assert captured["path"] == "/api/v1/amazon/product"
    assert captured["json"] == {"query": "B09XS7JWHH", "country": "gb"}


def test_amazon_offers_asin_alias(monkeypatch):
    """offers carries the ASIN in `query` too, exactly like product."""
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.amazon.offers("B09XS7JWHH")
    assert captured["path"] == "/api/v1/amazon/offers"
    assert captured["json"] == {"query": "B09XS7JWHH"}


def test_amazon_search_page(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.amazon.search("wireless headphones", country="us", page=2)
    assert captured["json"] == {"query": "wireless headphones", "country": "us", "page": 2}


def test_amazon_domain_alias_still_accepted(monkeypatch):
    """`domain` is deprecated in favour of `country` but must keep working:
    published SDK versions send it and the API still translates it."""
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.amazon.search("laptop", domain="co.uk", start_page=3)
    assert captured["json"] == {"query": "laptop", "domain": "co.uk", "start_page": 3}


@pytest.mark.parametrize(
    "method,retired",
    [
        ("search", "sort_by"),
        ("search", "pages"),
        ("search", "category_id"),
        ("search", "merchant_id"),
        ("search", "language"),
        ("search", "currency"),
        ("search", "device"),
        ("search", "zip_code"),
        ("search", "autoselect_variant"),
        ("product", "language"),
        ("product", "currency"),
        ("product", "device"),
        ("product", "zip_code"),
        ("product", "autoselect_variant"),
    ],
)
def test_amazon_retired_params_are_not_typed_args(method, retired):
    """The Amazon provider swap removed these. They must not reappear as typed
    arguments: `sort_by` in particular was verified to be a no-op upstream, and
    a typed argument reads as a supported filter. Anything still sent lands in
    **extra and the API answers with a `warnings` array."""
    client = ScavioClient(api_key="sk_test")
    params = inspect.signature(getattr(client.amazon, method)).parameters
    assert retired not in params


def test_amazon_options_is_get(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.amazon.options()
    assert captured["method"] == "GET"
    assert captured["path"] == "/api/v1/amazon/options"


@pytest.mark.parametrize(
    "method,kwargs",
    [
        ("profile", {}),
        ("hashtag", {}),
    ],
)
def test_tiktok_one_of_required(method, kwargs, monkeypatch):
    from scavio import ScavioError

    patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(ScavioError):
        getattr(client.tiktok, method)(**kwargs)


def test_instagram_post_one_of_required(monkeypatch):
    from scavio import ScavioError

    patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(ScavioError):
        client.instagram.post()
    # Any one of the three satisfies it.
    client.instagram.post(shortcode="abc")


# --- Reddit (upgrade: existing search/post kept, 10 new endpoints) ----------


def test_reddit_search_backward_compatible(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.reddit.search("serpapi alternative", cursor="c1")
    assert captured["path"] == "/api/v1/reddit/search"
    assert captured["json"] == {"query": "serpapi alternative", "cursor": "c1"}


def test_reddit_post_backward_compatible(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.reddit.post("https://www.reddit.com/r/programming/comments/abc123/x/")
    assert captured["path"] == "/api/v1/reddit/post"
    assert captured["json"] == {"url": "https://www.reddit.com/r/programming/comments/abc123/x/"}


def test_reddit_post_accepts_post_id(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.reddit.post(post_id="t3_1v6ngaf")
    assert captured["path"] == "/api/v1/reddit/post"
    assert captured["json"] == {"post_id": "t3_1v6ngaf"}


def test_reddit_post_one_of_required(monkeypatch):
    from scavio import ScavioError

    patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(ScavioError):
        client.reddit.post()


def test_reddit_search_has_no_filter_params():
    """The backend accepts only query and cursor; any type/sort control is a lie."""
    sig = inspect.signature(ScavioClient(api_key="sk_test").reddit.search)
    assert [n for n in sig.parameters if n != "extra"] == ["query", "cursor"]


def test_reddit_post_comments_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.reddit.post_comments("t3_1v6ngaf", sort="TOP", cursor="c1")
    assert captured["path"] == "/api/v1/reddit/post/comments"
    assert captured["json"] == {"post_id": "t3_1v6ngaf", "sort": "TOP", "cursor": "c1"}


def test_reddit_comment_replies_requires_cursor(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.reddit.comment_replies("t3_1v6ngaf", "reply_cursor_1")
    assert captured["path"] == "/api/v1/reddit/post/comments/replies"
    assert captured["json"] == {"post_id": "t3_1v6ngaf", "cursor": "reply_cursor_1"}


def test_reddit_trending_empty_body(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.reddit.trending()
    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v1/reddit/trending"
    assert captured["json"] == {}


# --- X (new) ----------------------------------------------------------------


def test_x_search_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.x.search("artificial intelligence", search_type="Latest", cursor="c1")
    assert captured["path"] == "/api/v1/x/search"
    assert captured["json"] == {
        "search": "artificial intelligence",
        "search_type": "Latest",
        "cursor": "c1",
    }


def test_x_user_tweets_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.x.user_tweets("elonmusk")
    assert captured["path"] == "/api/v1/x/user/tweets"
    assert captured["json"] == {"screen_name": "elonmusk"}


# --- LinkedIn ---------------------------------------------------------------
#
# The provider retired the `linkedin/web/*` namespace these were built on. The
# live endpoints now run on `web_v2`, which is URL-native: public params are
# unchanged, `url` is accepted everywhere, and the include_* flags / cursors that
# web_v2 has no equivalent for are gone. Five endpoints are retired upstream and
# answer 410; the SDK keeps them so old code fails loudly.


def test_linkedin_person_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.linkedin.person(username="williamhgates")
    assert captured["path"] == "/api/v1/linkedin/person"
    assert captured["json"] == {"username": "williamhgates"}


def test_linkedin_accepts_url_instead_of_handle(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.linkedin.person(url="https://www.linkedin.com/in/williamhgates/")
    assert captured["json"] == {"url": "https://www.linkedin.com/in/williamhgates/"}


@pytest.mark.parametrize(
    "method",
    [
        "person",
        "person_about",
        "person_posts",
        "company",
        "company_posts",
        "job",
        "post",
        "post_comments",
    ],
)
def test_linkedin_one_of_required(method, monkeypatch):
    from scavio import ScavioError

    patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(ScavioError):
        getattr(client.linkedin, method)()


def test_linkedin_search_jobs_location_is_optional(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.linkedin.search_jobs("engineer")
    assert captured["json"] == {"search": "engineer"}
    client.linkedin.search_jobs("engineer", location="United States")
    assert captured["json"] == {"search": "engineer", "location": "United States"}


def test_linkedin_post_comments_page_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.linkedin.post_comments(post_id="7488618410256523265", page=2)
    assert captured["path"] == "/api/v1/linkedin/post/comments"
    assert captured["json"] == {"post_id": "7488618410256523265", "page": 2}


def test_linkedin_company_slug_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.linkedin.company(company="microsoft")
    assert captured["path"] == "/api/v1/linkedin/company"
    assert captured["json"] == {"company": "microsoft"}


@pytest.mark.parametrize(
    "method", ["person_contact", "company_people", "company_jobs", "search_people", "search_posts"]
)
def test_linkedin_retired_endpoints_still_callable(method, monkeypatch):
    """Retired upstream, but kept in the SDK so callers get the API's 410 rather
    than an AttributeError. They must not impose one_of validation locally."""
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    getattr(client.linkedin, method)()
    assert captured["path"].startswith("/api/v1/linkedin/")


def test_linkedin_retired_endpoints_documented_as_retired():
    from scavio._spec import ENDPOINTS

    retired = {
        "linkedin_person_contact",
        "linkedin_company_people",
        "linkedin_company_jobs",
        "linkedin_search_people",
        "linkedin_search_posts",
    }
    # Live costs: 1, 10 or 30 credits. Pinned per key so a drift from the
    # backend's COST map shows up here.
    live_credits = {
        "linkedin_person": 1,
        "linkedin_person_about": 1,
        "linkedin_person_posts": 10,
        "linkedin_company": 1,
        "linkedin_company_posts": 10,
        "linkedin_search_jobs": 10,
        "linkedin_job": 30,
        "linkedin_post": 1,
        "linkedin_post_comments": 10,
    }
    for ep in ENDPOINTS.values():
        if ep.key in retired:
            assert ep.summary.startswith("RETIRED:"), ep.key
            assert ep.credits == 0, ep.key
        elif ep.namespace == "linkedin":
            assert ep.credits == live_credits[ep.key], ep.key


# --- TikTok Shop (new) ------------------------------------------------------


def test_tiktok_shop_search_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.search("phone case", cursor="c1")
    assert captured["path"] == "/api/v1/tiktok-shop/search"
    assert captured["json"] == {"search": "phone case", "cursor": "c1"}


def test_tiktok_shop_search_has_no_typed_region():
    # Search is US-only upstream, so region is deliberately not a typed argument
    # (it can still be forced through **extra, like any forward-compat param).
    assert [p.name for p in ENDPOINTS["tiktok_shop_search"].params] == ["search", "cursor"]
    assert [p.name for p in ENDPOINTS["tiktok_shop_categories"].params] == []


def test_tiktok_shop_suggestions_region_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.search_suggestions("wireless", region="GB")
    assert captured["path"] == "/api/v1/tiktok-shop/search/suggestions"
    assert captured["json"] == {"search": "wireless", "region": "GB"}


def test_tiktok_shop_product_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.product("1732293553906094315")
    assert captured["path"] == "/api/v1/tiktok-shop/product"
    assert captured["json"] == {"product_id": "1732293553906094315"}


def test_tiktok_shop_product_reviews_filters_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.product_reviews(
        "1732293553906094315",
        page=2,
        page_size=200,
        sort="recent",
        rating=5,
        has_media=True,
        verified_only=False,
    )
    assert captured["path"] == "/api/v1/tiktok-shop/product/reviews"
    assert captured["json"] == {
        "product_id": "1732293553906094315",
        "page": 2,
        "page_size": 200,
        "sort": "recent",
        "rating": 5,
        "has_media": True,
        "verified_only": False,
    }


def test_tiktok_shop_categories_empty_body(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.categories()
    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v1/tiktok-shop/categories"
    assert captured["json"] == {}


def test_tiktok_shop_category_products_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.category_products("601450", cursor="c1", region="GB")
    assert captured["path"] == "/api/v1/tiktok-shop/category/products"
    assert captured["json"] == {"category_id": "601450", "cursor": "c1", "region": "GB"}


def test_tiktok_shop_shop_products_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.shop_products("7495514739648989419")
    assert captured["path"] == "/api/v1/tiktok-shop/shop/products"
    assert captured["json"] == {"shop_id": "7495514739648989419"}


def test_tiktok_shop_resolve_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.tiktok_shop.resolve("https://vt.tiktok.com/ZT2AHoGsE/")
    assert captured["path"] == "/api/v1/tiktok-shop/resolve"
    assert captured["json"] == {"url": "https://vt.tiktok.com/ZT2AHoGsE/"}


async def test_tiktok_shop_search_wire_async(monkeypatch):
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    await client.tiktok_shop.search("phone case")
    assert captured["path"] == "/api/v1/tiktok-shop/search"
    assert captured["json"] == {"search": "phone case"}


def test_tiktok_shop_endpoints_are_one_credit():
    tiktok_shop = [ep for ep in ENDPOINTS.values() if ep.namespace == "tiktok_shop"]
    assert len(tiktok_shop) == 8
    for ep in tiktok_shop:
        assert ep.credits == 1, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path.startswith("/api/v1/tiktok-shop/"), ep.key


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_tiktok_shop_product_docstring_carries_both_caveats(module):
    """The price and partial-coverage caveats must reach anyone reading inline docs."""
    import importlib

    cls = getattr(importlib.import_module(module), "_TikTokShopNamespace", None)
    if cls is None:
        cls = importlib.import_module(module)._AsyncTikTokShopNamespace
    doc = cls.product.__doc__ or ""
    assert "does NOT return a price" in doc
    assert "44%" in doc
    assert "an HTTP 404 is a normal outcome" in doc
    # The 404 body has no data field; describing it by one is unfollowable advice.
    assert "data null" not in doc
    assert "data: null" not in doc
    # The 404 raises, so the docstring must name the exception and show the catch.
    assert "NotFoundError" in doc
    assert "except NotFoundError" in doc
    search_doc = cls.search.__doc__ or ""
    assert "exact prices" in search_doc
    assert "not guaranteed to resolve" in search_doc


# --- Extract (core, hand-written top-level method) --------------------------


def test_extract_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.extract("https://example.com/post", format="markdown", mode="ultra")
    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v1/extract"
    assert captured["json"] == {
        "url": "https://example.com/post",
        "format": "markdown",
        "mode": "ultra",
    }


def test_extract_drops_unset_tiers(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.extract("https://example.com")
    assert captured["json"] == {"url": "https://example.com"}


async def test_extract_wire_async(monkeypatch):
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    await client.extract("https://example.com", format="text")
    assert captured["path"] == "/api/v1/extract"
    assert captured["json"] == {"url": "https://example.com", "format": "text"}


@pytest.mark.parametrize("client_cls", [ScavioClient, AsyncScavioClient])
def test_extract_signature_is_url_plus_two_keywords(client_cls):
    sig = inspect.signature(client_cls(api_key="sk_test").extract)
    assert list(sig.parameters) == ["url", "format", "mode"]
    assert sig.parameters["format"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["mode"].kind is inspect.Parameter.KEYWORD_ONLY


# --- Body-priced surfaces: no flat "Costs N credits." -----------------------

BODY_PRICED = {"walmart", "threads", "kuaishou", "instagram", "zara", "_core"}
# Namespaces priced per endpoint: only these keys scale with the body
# (warehouse count, or country "ca"); the rest of the namespace is flat.
BODY_PRICED_KEYS = {
    "costco_prices",
    "costco_availability",
    "costco_warehouses",
    "costco_gas",
    "menards_product",
    "best_buy_category",
    "carrefour_search",
    "carrefour_product",
    "company_enrich",
    "ikea_compare",
    "ashley_search",
    "ashley_product",
    "bolcom_product",
    "uniqlo_store_stock",
    "uniqlo_prices",
    "depop_search",
    "depop_product",
    "depop_category",
    "depop_brand",
    "depop_explore",
    "mediaexpert_search",
    "mediaexpert_category",
    "mediaexpert_brand",
    "mediaexpert_promotions",
    "mediaexpert_outlet",
    "mediaexpert_seller",
    "autozone_search",
    "autozone_product",
    "instacart_search",
    "instacart_cross_search",
    "oreilly_cross_reference",
    "oreilly_product",
    "oreilly_brand",
    "oreilly_store_stock",
    "oreilly_stores",
    "acehardware_search",
    "acehardware_store_stock",
    "acehardware_stores",
    "tractorsupply_product",
    "tractorsupply_store_prices",
    "michaels_category",
    "michaels_deals",
    "offerup_listing",
    "rona_search",
    "rona_category",
    "rona_deals",
    "boots_product",
    "boots_store",
    "boots_store_stock",
    "boots_stores",
    "douglas_brand",
    "douglas_brands",
    "douglas_category",
    "douglas_deals",
    "douglas_product",
    "douglas_review_summary",
    "douglas_search",
    "douglas_suggestions",
    "notino_brand",
    "notino_brands",
    "notino_category",
    "notino_product",
    "notino_promo",
    "notino_reviews",
    "notino_search",
    "notino_suggestions",
    "spacenk_brand",
    "spacenk_category",
    "spacenk_search",
    "yesstyle_product",
    "kbb_car_value",
    "kbb_reviews",
    "vrbo_search",
    "expedia_price_calendar",
    "expedia_property",
    "expedia_search",
    "expedia_suggestions",
    "abercrombie_reviews",
    "bedbathbeyond_deals",
    "bedbathbeyond_product",
    "belk_product",
    "belk_store_availability",
    "belk_variant",
    "leroymerlin_category",
    "leroymerlin_product",
    "leroymerlin_reviews",
    "leroymerlin_search",
    "leroymerlin_store",
    "leroymerlin_stores",
    "leroymerlin_suggestions",
    "reclameaqui_complaints",
    "boticario_categories",
    "boticario_category",
    "boticario_deals",
    "boticario_prices",
    "boticario_product",
    "boticario_promotions",
    "boticario_search",
    "estantevirtual_copies",
    "pcexpress_product",
    "home_depot_search",
    "home_depot_product",
    "home_depot_reviews",
    "home_depot_stores",
    "home_depot_availability",
    "best_buy_search",
    "best_buy_product",
    "best_buy_reviews",
    "best_buy_deals",
    "best_buy_availability",
    "best_buy_prices",
    "ferguson_search",
    "ferguson_product",
    "digikey_product",
}


def test_every_body_priced_endpoint_carries_a_credits_note():
    for ep in ENDPOINTS.values():
        if ep.namespace in BODY_PRICED or ep.key in BODY_PRICED_KEYS:
            assert ep.credits_note, ep.key
            assert ep.credits_note.endswith("."), ep.key
        else:
            assert ep.credits_note is None, ep.key


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
@pytest.mark.parametrize(
    ("namespace", "method"),
    [("walmart", "search"), ("walmart", "category")],
)
def test_walmart_domain_priced_docstrings_state_the_domain_rule(module, namespace, method):
    """domain=com.mx costs 2; a flat 'Costs 1 credit.' would understate it by 2x."""
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_WalmartNamespace", None) or mod._AsyncWalmartNamespace
    doc = getattr(cls, method).__doc__ or ""
    assert "Costs 1 credit." not in doc
    assert "com.mx" in doc
    assert "2 credits" in doc


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
@pytest.mark.parametrize("method", ["profile", "user_posts", "user_replies"])
def test_threads_username_priced_docstrings_state_both_rates(module, method):
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_ThreadsNamespace", None) or mod._AsyncThreadsNamespace
    doc = getattr(cls, method).__doc__ or ""
    assert "Costs 2 credits." not in doc
    assert "2 credits addressed by user_id" in doc
    assert "4 credits addressed by username" in doc


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_instagram_docstrings_state_typical_and_ceiling(module):
    """Instagram is 1-2 credits typically, up to 10; a flat line would be wrong."""
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_InstagramNamespace", None) or mod._AsyncInstagramNamespace
    for method in ("profile", "user_reels", "music_posts", "post", "search_users", "post_likers"):
        doc = " ".join((getattr(cls, method).__doc__ or "").split())
        assert "Typically" in doc, method
        assert "up to 10" in doc, method
    assert "costs 8" in (cls.search_users.__doc__ or "")


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_kuaishou_docstrings_carry_their_own_cost(module):
    """Kuaishou prices per endpoint across a 40x range; one platform line is wrong."""
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_KuaishouNamespace", None) or mod._AsyncKuaishouNamespace
    for ep in ENDPOINTS.values():
        if ep.namespace != "kuaishou":
            continue
        doc = getattr(cls, ep.method).__doc__ or ""
        plural = "s" if ep.credits != 1 else ""
        assert f"Costs {ep.credits} credit{plural}." in doc, ep.key
        assert "PER ENDPOINT" in doc, ep.key
    assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == "kuaishou"} == {1, 2, 10, 40}


@pytest.mark.parametrize("client_cls", [ScavioClient, AsyncScavioClient])
def test_extract_docstring_states_the_tiers_not_a_flat_price(client_cls):
    doc = client_cls.extract.__doc__ or ""
    assert "Costs 1 credit." not in doc
    assert "'ultra' costs 2" in doc
    assert "only a successful extraction is billed" in doc


# --- New-platform shape guards ----------------------------------------------


def test_ebay_sold_listings_are_reachable_and_typed(monkeypatch):
    """sold=True is the price-research differentiator; it must be a typed bool."""
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.ebay.search(query="airpods pro 2", sold=True, per_page=240)
    assert captured["path"] == "/api/v1/ebay/search"
    assert captured["json"] == {"query": "airpods pro 2", "sold": True, "per_page": 240}
    per_page = next(p for p in ENDPOINTS["ebay_search"].params if p.name == "per_page")
    # Numeric literals, unquoted: the backend is z.union([z.literal(60), ...]).
    assert per_page.annotation == "Optional[Literal[60, 120, 240]]"


def test_ebay_search_requires_query_or_seller():
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(ScavioError):
        client.ebay.search()


def test_ebay_seller_only_search_needs_no_query(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.ebay.search(seller="mytechstore", page=2)
    assert captured["json"] == {"seller": "mytechstore", "page": 2}


def test_meta_ads_paths_are_hyphenated_not_derived_from_the_route_key():
    """The route key is `metaads`; the served path is /api/v1/meta-ads/*."""
    meta = [ep for ep in ENDPOINTS.values() if ep.namespace == "meta_ads"]
    assert len(meta) == 3
    for ep in meta:
        assert ep.path.startswith("/api/v1/meta-ads/"), ep.key
        assert "metaads" not in ep.path, ep.key


def test_meta_ads_cursor_paging(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.meta_ads.search("black friday", cursor="c1")
    assert captured["path"] == "/api/v1/meta-ads/search"
    assert captured["json"] == {"query": "black friday", "cursor": "c1"}


def test_costco_method_names_match_the_dashboard_playground():
    """The Playground advertises costco.<endpoint>(); a rename breaks its snippets."""
    costco = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "costco"}
    assert sorted(costco) == sorted(
        [
            "search", "category", "categories", "product", "prices", "availability",
            "reviews", "warehouses", "gas", "coupons", "deals", "clearance", "autocomplete",
        ]
    )
    for method, ep in costco.items():
        assert ep.path == f"/api/v1/costco/{method}", method
    # The positional argument the Playground snippet passes first, per method.
    positional = {
        "search": "query",
        "category": "category",
        "product": "item_id",
        "availability": "item_number",
        "reviews": "product_id",
        "deals": "type",
        "autocomplete": "query",
    }
    client = ScavioClient(api_key="sk_test")
    for method, name in positional.items():
        params = list(inspect.signature(getattr(client.costco, method)).parameters.values())
        assert params[0].name == name, method
        assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD, method


def test_costco_search_with_warehouse_pricing(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.costco.search(
        "olive oil", warehouse_id="1062", page_size=5, brands=["Kirkland Signature"]
    )
    assert captured["path"] == "/api/v1/costco/search"
    assert captured["json"] == {
        "query": "olive oil",
        "warehouse_id": "1062",
        "page_size": 5,
        "brands": ["Kirkland Signature"],
    }


def test_costco_product_takes_one_id_positionally_or_a_list(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.costco.product("100334960")
    assert captured["json"] == {"item_id": "100334960"}
    client.costco.product(item_ids=["100334960", "1492456"])
    assert captured["json"] == {"item_ids": ["100334960", "1492456"]}
    with pytest.raises(ScavioError):
        client.costco.product()


def test_costco_prices_requires_ids_and_keyword_only_warehouses(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.costco.prices(item_id="1492456", warehouse_ids=["1062", "1107"])
    assert captured["path"] == "/api/v1/costco/prices"
    assert captured["json"] == {"item_id": "1492456", "warehouse_ids": ["1062", "1107"]}
    with pytest.raises(ScavioError):
        client.costco.prices(item_id="1492456")
    with pytest.raises(ScavioError):
        client.costco.prices(warehouse_ids=["1062"])
    # An item number passed positionally must never land in warehouse_ids.
    with pytest.raises(TypeError):
        client.costco.prices("1492456")  # type: ignore[misc]


def test_costco_availability_item_and_warehouses_positional(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.costco.availability("1492456", ["1062"])
    assert captured["json"] == {"item_number": "1492456", "warehouse_ids": ["1062"]}


def test_costco_location_endpoints_need_a_location(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    with pytest.raises(ScavioError):
        client.costco.warehouses()
    with pytest.raises(ScavioError):
        client.costco.gas()
    client.costco.gas(warehouse_ids=["1062"])
    assert captured["json"] == {"warehouse_ids": ["1062"]}
    client.costco.warehouses(latitude=40.8, longitude=-73.96, limit=3)
    assert captured["json"] == {"latitude": 40.8, "longitude": -73.96, "limit": 3}


def test_costco_coupons_sends_an_empty_body(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.costco.coupons()
    assert captured["path"] == "/api/v1/costco/coupons"
    assert captured["json"] == {}


def test_costco_clearance_price_codes_are_a_list(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.costco.clearance("1062", query="snacks", price_codes=["clearance", "special_buy"])
    assert captured["json"] == {
        "warehouse_id": "1062",
        "query": "snacks",
        "price_codes": ["clearance", "special_buy"],
    }
    annotation = next(
        p for p in ENDPOINTS["costco_clearance"].params if p.name == "price_codes"
    ).annotation
    assert annotation.startswith("Optional[list[Literal[")
    with pytest.raises(ScavioError):
        client.costco.clearance("1062")


@pytest.mark.parametrize("method", ["prices", "availability", "warehouses", "gas"])
def test_costco_body_priced_docstrings_do_not_claim_a_flat_price(method):
    from scavio._namespaces_sync import _CostcoNamespace

    doc = getattr(_CostcoNamespace, method).__doc__ or ""
    assert "Costs 1 credit. Returns" not in doc
    assert "2" in doc


def test_trustpilot_method_names_match_the_dashboard_playground():
    """The Playground advertises trustpilot.<endpoint>(); a rename breaks its snippets."""
    tp = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "trustpilot"}
    assert sorted(tp) == sorted(
        ["search", "business", "reviews", "categories", "category", "review"]
    )
    for method, ep in tp.items():
        assert ep.path == f"/api/v1/trustpilot/{method}", method
        assert ep.credits == 2, method
        assert ep.credits_note is None, method
    # The positional argument the Playground snippet passes first, per method.
    positional = {"search": "query", "category": "category_id", "review": "review_id"}
    client = ScavioClient(api_key="sk_test")
    for method, name in positional.items():
        params = list(inspect.signature(getattr(client.trustpilot, method)).parameters.values())
        assert params[0].name == name, method
        assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD, method
    # business / reviews / categories take keywords only.
    for method in ("business", "reviews", "categories"):
        params = list(inspect.signature(getattr(client.trustpilot, method)).parameters.values())
        assert params[0].kind is inspect.Parameter.KEYWORD_ONLY, method


def test_trustpilot_search(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.trustpilot.search("vpn", country="GB", page_size=50)
    assert captured["path"] == "/api/v1/trustpilot/search"
    assert captured["json"] == {"query": "vpn", "country": "GB", "page_size": 50}


def test_trustpilot_business_needs_domain_or_url(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.trustpilot.business(domain="nordvpn.com", language="de")
    assert captured["path"] == "/api/v1/trustpilot/business"
    assert captured["json"] == {"domain": "nordvpn.com", "language": "de"}
    client.trustpilot.business(url="https://www.trustpilot.com/review/nordvpn.com")
    assert captured["json"] == {"url": "https://www.trustpilot.com/review/nordvpn.com"}
    with pytest.raises(ScavioError):
        client.trustpilot.business()
    with pytest.raises(ScavioError):
        client.trustpilot.reviews(stars=[1])


def test_trustpilot_reviews_filters(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.trustpilot.reviews(
        domain="nordvpn.com",
        stars=[1, 2],
        language="en",
        date_range="last30days",
        verified_only=True,
        topics=["customer_service"],
        search="refund",
        page=3,
    )
    assert captured["path"] == "/api/v1/trustpilot/reviews"
    assert captured["json"] == {
        "domain": "nordvpn.com",
        "page": 3,
        "stars": [1, 2],
        "language": "en",
        "date_range": "last30days",
        "verified_only": True,
        "topics": ["customer_service"],
        "search": "refund",
    }
    annotation = next(
        p for p in ENDPOINTS["trustpilot_reviews"].params if p.name == "stars"
    ).annotation
    assert annotation == "Optional[list[Literal[1, 2, 3, 4, 5]]]"


def test_trustpilot_categories_takes_no_required_args(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.trustpilot.categories()
    assert captured["path"] == "/api/v1/trustpilot/categories"
    assert captured["json"] == {}
    client.trustpilot.categories(query="insurance")
    assert captured["json"] == {"query": "insurance"}


def test_trustpilot_category_and_review_positional(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.trustpilot.category(
        "vpn_service", sort="reviews_count", min_trust_score=4.5, claimed_only=True
    )
    assert captured["path"] == "/api/v1/trustpilot/category"
    assert captured["json"] == {
        "category_id": "vpn_service",
        "sort": "reviews_count",
        "min_trust_score": 4.5,
        "claimed_only": True,
    }
    client.trustpilot.review("6aca2504b52cc4b518bf4b75")
    assert captured["path"] == "/api/v1/trustpilot/review"
    assert captured["json"] == {"review_id": "6aca2504b52cc4b518bf4b75"}


async def test_trustpilot_async_reviews(monkeypatch):
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    await client.trustpilot.reviews(url="https://www.trustpilot.com/review/nordvpn.com")
    assert captured["path"] == "/api/v1/trustpilot/reviews"
    assert captured["json"] == {"url": "https://www.trustpilot.com/review/nordvpn.com"}


def test_realtor_rightmove_method_names_match_the_dashboard_playground():
    """The Playground advertises realtor.<m>() / rightmove.<m>(); a rename breaks its snippets."""
    expected = {
        "realtor": {
            "search": "search",
            "property": "property",
            "locations": "locations",
            "market": "market",
            "agents": "agents",
            "agent": "agent",
        },
        "rightmove": {
            "locations": "locations",
            "search": "search",
            "property": "property",
            "sold": "sold",
            "sold_property": "sold-property",
            "agents": "agents",
            "agent": "agent",
        },
    }
    for ns, methods in expected.items():
        eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == ns}
        assert sorted(eps) == sorted(methods), ns
        for method, slug in methods.items():
            assert eps[method].path == f"/api/v1/{ns}/{slug}", method
            assert eps[method].credits == 1, method
            assert eps[method].credits_note is None, method
    # The positional argument the Playground snippet passes first, per method.
    positional = {
        ("realtor", "locations"): "query",
        ("realtor", "market"): "location",
        ("realtor", "agent"): "agent_id",
        ("rightmove", "locations"): "query",
        ("rightmove", "sold"): "location",
    }
    client = ScavioClient(api_key="sk_test")
    for (ns, method), name in positional.items():
        params = list(inspect.signature(getattr(getattr(client, ns), method)).parameters.values())
        assert params[0].name == name, method
        assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD, method
    for ns, methods in expected.items():
        for method in methods:
            if (ns, method) in positional:
                continue
            fn = getattr(getattr(client, ns), method)
            params = list(inspect.signature(fn).parameters.values())
            assert params[0].kind is inspect.Parameter.KEYWORD_ONLY, (ns, method)


def test_realtor_search_filters(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.realtor.search(
        location="Maricopa County, AZ",
        listing_status="sold",
        property_types=["land"],
        sold_within_days=365,
        lot_sqft_min=43560,
        max_price=150000,
        keywords=["workshop"],
        sort="sold_newest",
        page_size=200,
    )
    assert captured["path"] == "/api/v1/realtor/search"
    assert captured["json"] == {
        "location": "Maricopa County, AZ",
        "listing_status": "sold",
        "max_price": 150000,
        "lot_sqft_min": 43560,
        "property_types": ["land"],
        "sold_within_days": 365,
        "keywords": ["workshop"],
        "sort": "sold_newest",
        "page_size": 200,
    }
    client.realtor.search(latitude=30.27, longitude=-97.74, radius_miles=2.5)
    assert captured["json"] == {"latitude": 30.27, "longitude": -97.74, "radius_miles": 2.5}
    client.realtor.search(agent_id="1918615")
    assert captured["json"] == {"agent_id": "1918615"}
    with pytest.raises(ScavioError):
        client.realtor.search(beds_min=3)


def test_realtor_property_locations_market_agents_agent(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.realtor.property(property_id="9564057635")
    assert captured["path"] == "/api/v1/realtor/property"
    assert captured["json"] == {"property_id": "9564057635"}
    with pytest.raises(ScavioError):
        client.realtor.property()
    client.realtor.locations("Austin")
    assert captured["path"] == "/api/v1/realtor/locations"
    assert captured["json"] == {"query": "Austin"}
    client.realtor.market("Austin_TX")
    assert captured["path"] == "/api/v1/realtor/market"
    assert captured["json"] == {"location": "Austin_TX"}
    client.realtor.agents(postal_code="78744", page_size=50)
    assert captured["path"] == "/api/v1/realtor/agents"
    assert captured["json"] == {"postal_code": "78744", "page_size": 50}
    with pytest.raises(ScavioError):
        client.realtor.agents(page=2)
    client.realtor.agent("1918615")
    assert captured["path"] == "/api/v1/realtor/agent"
    assert captured["json"] == {"agent_id": "1918615"}


def test_rightmove_search_filters(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.rightmove.search(
        location_id="REGION^219",
        listing_status="for_rent",
        max_price=1800,
        beds_min=2,
        property_types=["flat"],
        furnishing=["furnished"],
        let_type="long_term",
        added_within_days=7,
        radius_miles=0.5,
        page=2,
    )
    assert captured["path"] == "/api/v1/rightmove/search"
    assert captured["json"] == {
        "location_id": "REGION^219",
        "listing_status": "for_rent",
        "max_price": 1800,
        "beds_min": 2,
        "property_types": ["flat"],
        "added_within_days": 7,
        "radius_miles": 0.5,
        "furnishing": ["furnished"],
        "let_type": "long_term",
        "page": 2,
    }
    with pytest.raises(ScavioError):
        client.rightmove.search(beds_min=2)
    # No keyword filter is declared: Rightmove ignores it and the API rejects it.
    assert "keywords" not in {p.name for p in ENDPOINTS["rightmove_search"].params}


def test_rightmove_sold_and_sold_property(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.rightmove.sold("SW11", property_type="flat", sold_within_years=5, sort="price_high")
    assert captured["path"] == "/api/v1/rightmove/sold"
    assert captured["json"] == {
        "location": "SW11",
        "property_type": "flat",
        "sold_within_years": 5,
        "sort": "price_high",
    }
    client.rightmove.sold_property(sold_id="921d33f4-d206-4991-be4d-75cbe71981ce")
    assert captured["path"] == "/api/v1/rightmove/sold-property"
    assert captured["json"] == {"sold_id": "921d33f4-d206-4991-be4d-75cbe71981ce"}
    with pytest.raises(ScavioError):
        client.rightmove.sold_property()


def test_rightmove_property_agents_agent(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.rightmove.property(url="https://www.rightmove.co.uk/properties/93577917")
    assert captured["path"] == "/api/v1/rightmove/property"
    assert captured["json"] == {"url": "https://www.rightmove.co.uk/properties/93577917"}
    client.rightmove.agents(location="Bristol", page=3)
    assert captured["path"] == "/api/v1/rightmove/agents"
    assert captured["json"] == {"location": "Bristol", "page": 3}
    with pytest.raises(ScavioError):
        client.rightmove.agents(page=1)
    client.rightmove.agent(branch_id="201404")
    assert captured["path"] == "/api/v1/rightmove/agent"
    assert captured["json"] == {"branch_id": "201404"}
    with pytest.raises(ScavioError):
        client.rightmove.agent()


async def test_realtor_rightmove_async(monkeypatch):
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    await client.realtor.locations("Austin")
    assert captured["path"] == "/api/v1/realtor/locations"
    assert captured["json"] == {"query": "Austin"}
    await client.rightmove.sold_property(sold_id="921d33f4-d206-4991-be4d-75cbe71981ce")
    assert captured["path"] == "/api/v1/rightmove/sold-property"
    assert captured["json"] == {"sold_id": "921d33f4-d206-4991-be4d-75cbe71981ce"}


def test_mercadolibre_method_names_match_the_dashboard_playground():
    """The Playground advertises mercadolibre.<m>(); a rename breaks its snippets."""
    expected = {
        "search": ("search", 2),
        "product": ("product", 2),
        "reviews": ("reviews", 1),
        "questions": ("questions", 2),
        "best_sellers": ("best-sellers", 2),
    }
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "mercadolibre"}
    assert sorted(eps) == sorted(expected)
    for method, (slug, credits) in expected.items():
        assert eps[method].path == f"/api/v1/mercadolibre/{slug}", method
        assert eps[method].credits == credits, method
        assert eps[method].credits_note is None, method
    # The positional argument the Playground snippet passes first, per method.
    positional = {"search": "query", "questions": "item_id", "best_sellers": "category_id"}
    client = ScavioClient(api_key="sk_test")
    for method in expected:
        params = list(inspect.signature(getattr(client.mercadolibre, method)).parameters.values())
        if method in positional:
            assert params[0].name == positional[method], method
            assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD, method
        else:
            assert params[0].kind is inspect.Parameter.KEYWORD_ONLY, method
    # country is required by the API but keyword-only, so search("iphone 15")
    # can never send the query as the country.
    for method in ("search", "best_sellers"):
        sig = inspect.signature(getattr(client.mercadolibre, method))
        assert sig.parameters["country"].kind is inspect.Parameter.KEYWORD_ONLY, method


def test_mercadolibre_search(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.mercadolibre.search(
        "iphone 15",
        country="mx",
        condition="new",
        min_price=5000,
        max_price=30000,
        min_discount=10,
        free_shipping=True,
        full_fulfillment=True,
        official_stores_only=True,
        interest_free_installments=True,
        sort="price_asc",
        page=2,
    )
    assert captured["path"] == "/api/v1/mercadolibre/search"
    assert captured["json"] == {
        "query": "iphone 15",
        "country": "mx",
        "condition": "new",
        "min_price": 5000,
        "max_price": 30000,
        "min_discount": 10,
        "free_shipping": True,
        "full_fulfillment": True,
        "official_stores_only": True,
        "interest_free_installments": True,
        "sort": "price_asc",
        "page": 2,
    }
    client.mercadolibre.search(country="br", seller_id="527927603")
    assert captured["json"] == {"country": "br", "seller_id": "527927603"}
    client.mercadolibre.search(country="mx", seller_nickname="MERCADOLIBRE ELECTRONICA_MX")
    assert captured["json"] == {"country": "mx", "seller_nickname": "MERCADOLIBRE ELECTRONICA_MX"}
    with pytest.raises(ScavioError):
        client.mercadolibre.search(country="mx")
    with pytest.raises(ScavioError):
        client.mercadolibre.search("iphone 15")


def test_mercadolibre_product_reviews_questions_best_sellers(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.mercadolibre.product(product_id="MLM1027172667")
    assert captured["path"] == "/api/v1/mercadolibre/product"
    assert captured["json"] == {"product_id": "MLM1027172667"}
    client.mercadolibre.product(item_id="MLM-2746152281")
    assert captured["json"] == {"item_id": "MLM-2746152281"}
    with pytest.raises(ScavioError):
        client.mercadolibre.product()
    client.mercadolibre.reviews(product_id="MLM1027172667", rating=1, page=3)
    assert captured["path"] == "/api/v1/mercadolibre/reviews"
    assert captured["json"] == {"product_id": "MLM1027172667", "rating": 1, "page": 3}
    with pytest.raises(ScavioError):
        client.mercadolibre.reviews(rating=5)
    client.mercadolibre.questions("MLM3571336480", offset=20)
    assert captured["path"] == "/api/v1/mercadolibre/questions"
    assert captured["json"] == {"item_id": "MLM3571336480", "offset": 20}
    client.mercadolibre.questions(url="https://www.mercadolibre.com.mx/x/p/MLM1027172667")
    assert captured["json"] == {"url": "https://www.mercadolibre.com.mx/x/p/MLM1027172667"}
    with pytest.raises(ScavioError):
        client.mercadolibre.questions()
    client.mercadolibre.best_sellers("MLM1055", country="mx")
    assert captured["path"] == "/api/v1/mercadolibre/best-sellers"
    assert captured["json"] == {"category_id": "MLM1055", "country": "mx"}
    with pytest.raises(ScavioError):
        client.mercadolibre.best_sellers("MLM1055")


async def test_mercadolibre_async(monkeypatch):
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    await client.mercadolibre.search("iphone 15", country="mx")
    assert captured["path"] == "/api/v1/mercadolibre/search"
    assert captured["json"] == {"query": "iphone 15", "country": "mx"}
    await client.mercadolibre.best_sellers("MCO1055", country="co")
    assert captured["path"] == "/api/v1/mercadolibre/best-sellers"
    assert captured["json"] == {"category_id": "MCO1055", "country": "co"}


def test_walmart_seller_products_path_is_hyphenated():
    assert ENDPOINTS["walmart_seller_products"].path == "/api/v1/walmart/seller-products"


def test_companies_house_and_kuaishou_divergent_paths():
    assert ENDPOINTS["companies_house_filing_history"].path == (
        "/api/v1/companieshouse/filing-history"
    )
    assert ENDPOINTS["kuaishou_comment_replies"].path == "/api/v1/kuaishou/video/sub-comments"
    assert ENDPOINTS["zillow_agent_reviews"].path == "/api/v1/zillow/reviews"


def test_home_depot_namespace_maps_to_unhyphenated_route():
    for ep in ENDPOINTS.values():
        if ep.namespace == "home_depot":
            assert ep.path.startswith("/api/v1/homedepot/"), ep.key


def test_kuaishou_videos_batch_takes_a_list(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.kuaishou.videos_batch(["p1", "p2"])
    assert captured["path"] == "/api/v1/kuaishou/videos/batch"
    assert captured["json"] == {"photo_ids": ["p1", "p2"]}
    param = ENDPOINTS["kuaishou_videos_batch"].params[0]
    assert param.annotation == "list[str]" and param.required


def test_price_filters_are_floats_not_ints():
    """Backends are z.number(), not z.number().int(): 19.99 and 1.5 baths are legal."""
    for key, names in {
        "walmart_search": ("min_price", "max_price"),
        "ebay_search": ("min_price", "max_price"),
        "zillow_search": ("min_price", "max_price", "baths_min", "baths_max", "max_hoa"),
        "redfin_search": ("min_price", "max_price", "max_hoa"),
        "airbnb_search": ("min_price", "max_price"),
        "booking_search": ("min_price", "max_price"),
        "indeed_search": ("min_salary",),
        "home_depot_search": ("min_price", "max_price"),
    }.items():
        params = {p.name: p for p in ENDPOINTS[key].params}
        for name in names:
            assert params[name].annotation == "Optional[float]", (key, name)


def test_int_literal_unions_are_never_quoted():
    """A string '1' fails the route schema on every one of these."""
    for key, name in [
        ("yelp_reviews", "rating"),
        ("g2_search", "rating"),
        ("g2_reviews", "rating"),
        ("redfin_search", "region_type"),
        ("redfin_market", "region_type"),
        ("indeed_search", "radius"),
        ("indeed_search", "max_age_days"),
        ("ebay_search", "per_page"),
    ]:
        annotation = next(p for p in ENDPOINTS[key].params if p.name == name).annotation
        assert '"' not in annotation, (key, name, annotation)
        assert "Literal[" in annotation


def test_sec_list_fields_accept_a_scalar_a_list_or_a_joined_string(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.sec.filings(ticker="AAPL", form=["10-K", "10-Q"])
    assert captured["json"] == {"ticker": "AAPL", "form": ["10-K", "10-Q"]}
    annotation = next(p for p in ENDPOINTS["sec_filings"].params if p.name == "form").annotation
    assert annotation == "Optional[Union[str, list[str]]]"


def test_new_platform_endpoint_counts():
    """Guards against a fragment being half-merged."""
    expected = {
        "walmart": 8,
        "threads": 6,
        "kuaishou": 14,
        "ebay": 3,
        "target": 5,
        "home_depot": 11,
        "zillow": 3,
        "booking": 3,
        "tripadvisor": 4,
        "indeed": 4,
        "airbnb": 3,
        "glassdoor": 4,
        "yelp": 3,
        "app_store": 3,
        "google_play": 3,
        "sec": 6,
        "redfin": 3,
        "companies_house": 4,
        "g2": 3,
        "capterra": 3,
        "google_ads": 3,
        "meta_ads": 3,
        "costco": 13,
        "trustpilot": 6,
        "realtor": 6,
        "rightmove": 7,
        "mercadolibre": 5,
        # extract + extract_map / extract_crawl / extract_batch (0.23.0).
        "_core": 4,
    }
    counts: dict[str, int] = {}
    for ep in ENDPOINTS.values():
        if ep.namespace in expected:
            counts[ep.namespace] = counts.get(ep.namespace, 0) + 1
    assert counts == expected
    assert sum(expected.values()) == 143


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
@pytest.mark.parametrize("method", ["search", "product"])
def test_walmart_store_targeting_docstrings_state_the_2_credit_rule(module, method):
    """A store-targeted call costs 2; the docstring must not imply a flat 1."""
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_WalmartNamespace", None) or mod._AsyncWalmartNamespace
    doc = getattr(cls, method).__doc__ or ""
    assert "2 credits when store-targeted" in doc
    assert "delivery_zip" in doc and "store_id" in doc


def test_walmart_store_targeting_wire(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.walmart.search("milk", delivery_zip="50036", store_id=1389)
    assert captured["json"] == {"query": "milk", "delivery_zip": "50036", "store_id": 1389}
    client.walmart.product("10220526", domain="ca", delivery_zip="M5V 2T6", store_id="3106")
    assert captured["json"] == {
        "product_id": "10220526",
        "domain": "ca",
        "delivery_zip": "M5V 2T6",
        "store_id": "3106",
    }
    client.walmart.stores("M5V 2T6", domain="ca")
    assert captured["path"] == "/api/v1/walmart/stores"
    assert captured["json"] == {"zipcode": "M5V 2T6", "domain": "ca"}


# --- Social depth batch (TikTok, YouTube, Reddit, X; 0.22.0) ----------------

_SEC = "MS4wLjABAAAA"
_MUSIC = "7364498342501435408"
_PLAYLIST = "7596415294902389534"
_COMMUNITY = "1508567430188126209"

# key -> (positional args, the wire field each positional maps to)
SOCIAL_DEPTH = {
    "tiktok_trending_searches": ((), ()),
    "tiktok_trending_videos": ((), ()),
    "tiktok_search_suggestions": (("cooking",), ("keyword",)),
    "tiktok_music": ((_MUSIC,), ("music_id",)),
    "tiktok_music_videos": ((_MUSIC,), ("music_id",)),
    "tiktok_search_music": (("espresso",), ("keyword",)),
    "tiktok_music_chart": ((), ()),
    "tiktok_user_similar": ((_SEC,), ("sec_user_id",)),
    "tiktok_user_playlists": ((_SEC,), ("sec_user_id",)),
    "tiktok_playlist_videos": ((_PLAYLIST,), ("playlist_id",)),
    "tiktok_user_live": (("mrbeast",), ("username",)),
    "tiktok_user_region": (("mrbeast",), ("username",)),
    "youtube_community_post": (("Ugkx_post",), ("post_id",)),
    "youtube_community_post_comments": (("Ugkx_post",), ("post_id",)),
    "reddit_search_comments": (("web scraping api",), ("query",)),
    "reddit_search_subreddits": (("web scraping",), ("query",)),
    "x_search_communities": (("crypto",), ("keyword",)),
    "x_community": ((_COMMUNITY,), ("community_id",)),
    "x_community_tweets": ((_COMMUNITY,), ("community_id",)),
}


@pytest.mark.parametrize("key", sorted(SOCIAL_DEPTH))
def test_social_depth_positional_wire(monkeypatch, key):
    args, fields = SOCIAL_DEPTH[key]
    ep = ENDPOINTS[key]
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, ep.namespace), ep.method)(*args)
    assert captured["path"] == ep.path
    assert captured["json"] == dict(zip(fields, args))
    assert ep.credits == 1 and ep.http == "POST" and ep.credits_note is None


def test_social_depth_paths():
    assert ENDPOINTS["tiktok_user_region"].path == "/api/v1/tiktok/user/region"
    assert ENDPOINTS["tiktok_music_chart"].path == "/api/v1/tiktok/music/chart"
    assert ENDPOINTS["youtube_community_post_comments"].path == (
        "/api/v1/youtube/community/post/comments"
    )
    assert ENDPOINTS["reddit_search_comments"].path == "/api/v1/reddit/search/comments"
    assert ENDPOINTS["x_community_tweets"].path == "/api/v1/x/community/tweets"


async def test_social_depth_async_wire(monkeypatch):
    captured = patch_async(monkeypatch)
    client = AsyncScavioClient(api_key="sk_test")
    await client.x.community_tweets(_COMMUNITY, ranking="Recency", cursor="c2")
    assert captured["path"] == "/api/v1/x/community/tweets"
    assert captured["json"] == {"community_id": _COMMUNITY, "ranking": "Recency", "cursor": "c2"}
    await client.tiktok.music_chart(chart="viral", count=10)
    assert captured["json"] == {"chart": "viral", "count": 10}
    await client.reddit.search_comments("q", sort="NEW")
    assert captured["json"] == {"query": "q", "sort": "NEW"}


def test_youtube_transcript_costs_5_credits():
    assert ENDPOINTS["youtube_transcript"].credits == 5
    from scavio._namespaces_sync import _YouTubeNamespace

    assert "Costs 5 credits." in (_YouTubeNamespace.transcript.__doc__ or "")


def test_custom_search_wire_names(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.google.custom_search(
        "cold brew",
        num=5,
        start=11,
        site_search="example.com",
        site_search_filter="e",
        date_restrict="m6",
        exact_terms="ratio",
        exclude_terms="starbucks",
        or_terms="pdf guide",
        file_type="pdf",
        cx="abc",
    )
    assert captured["path"] == "/api/v1/google/customsearch"
    assert captured["json"] == {
        "q": "cold brew",
        "num": 5,
        "start": 11,
        "siteSearch": "example.com",
        "siteSearchFilter": "e",
        "dateRestrict": "m6",
        "exactTerms": "ratio",
        "excludeTerms": "starbucks",
        "orTerms": "pdf guide",
        "fileType": "pdf",
        "cx": "abc",
    }


def test_ai_chat_method_names_match_the_dashboard_playground():
    """The Playground advertises chatgpt.prompt() / gemini.prompt(); renaming breaks it."""
    for ns, credits in (("chatgpt", 2), ("gemini", 5)):
        eps = [ep for ep in ENDPOINTS.values() if ep.namespace == ns]
        assert [ep.method for ep in eps] == ["prompt"]
        assert eps[0].path == f"/api/v1/{ns}/prompt"
        assert eps[0].credits == credits
        assert eps[0].min_timeout == 120.0
    client = ScavioClient(api_key="sk_test")
    for ns in ("chatgpt", "gemini"):
        params = list(inspect.signature(getattr(client, ns).prompt).parameters.values())
        assert params[0].name == "prompt"
        assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD


def test_chatgpt_prompt(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.chatgpt.prompt("best crm", model="gpt-5", country="gb", include_html=True)
    assert captured["path"] == "/api/v1/chatgpt/prompt"
    assert captured["json"] == {
        "prompt": "best crm",
        "model": "gpt-5",
        "country": "gb",
        "include_html": True,
    }
    client.chatgpt.prompt("best crm")
    assert captured["json"] == {"prompt": "best crm"}


def test_gemini_prompt(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.gemini.prompt("best crm")
    assert captured["path"] == "/api/v1/gemini/prompt"
    assert captured["json"] == {"prompt": "best crm"}


def test_ai_chat_raises_the_timeout_but_never_lowers_it(monkeypatch):
    seen: list[float] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append(timeout)
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    ScavioClient(api_key="sk_test").chatgpt.prompt("hi")
    ScavioClient(api_key="sk_test", timeout=300).gemini.prompt("hi")
    ScavioClient(api_key="sk_test").trustpilot.search("vpn")
    assert seen == [120.0, 300, 30.0]


def test_ai_chat_async(monkeypatch):
    import asyncio

    from scavio import AsyncScavioClient

    seen: dict = {}

    async def fake_request(method, path, *, timeout, json=None, **_):
        seen.update(path=path, json=json, timeout=timeout)
        return {"ok": True}

    monkeypatch.setattr("scavio._async_client.async_request", fake_request)
    asyncio.run(AsyncScavioClient(api_key="sk_test").gemini.prompt("hi"))
    assert seen == {"path": "/api/v1/gemini/prompt", "json": {"prompt": "hi"}, "timeout": 120.0}


def test_us_retail_batch_1_credits_and_paths():
    """sephora/ulta/aldi/micro_center/walgreens/cvs (0.32.0): 20 endpoints, priced per method.

    0.93.0 adds the six Sephora Canada only endpoints (26 in all).
    """
    expected = {
        "sephora": {  # product 2 since 0.50.1
            "search": 1,
            "category": 1,
            "product": 2,
            "brand": 1,
            "brands": 1,
            "suggestions": 1,
            "offers": 2,
            "stores": 1,
            "store": 1,
        },
        "ulta": {"search": 1, "category": 1, "product": 1, "stores": 1},
        "aldi": {"search": 1, "product": 1, "stores": 1},
        "micro_center": {"search": 2, "product": 2, "stores": 1},
        "walgreens": {"search": 2, "product": 2, "stores": 2, "stock": 4},
        "cvs": {"search": 1, "product": 2, "stock": 1},  # product 2 since 0.95.1
    }
    for ns, methods in expected.items():
        eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == ns}
        assert {m: ep.credits for m, ep in eps.items()} == methods, ns
        wire_ns = ns.replace("_", "")
        for m, ep in eps.items():
            assert ep.path == f"/api/v1/{wire_ns}/{m}", ep.key
    assert sum(len(m) for m in expected.values()) == 26


def test_cvs_product_raises_the_timeout(monkeypatch):
    seen: list[float] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append(timeout)
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    client.cvs.product(product_id="789787")
    client.cvs.search("toothpaste")
    assert seen == [120.0, 30.0]
    with pytest.raises(ScavioError):
        client.cvs.product()


def test_us_retail_batch_2_credits_and_paths():
    """whole_foods/harbor_freight/petsmart/petco/iherb/chewy/menards (0.33.0): 33 endpoints,
    plus menards.search (0.34.0)."""
    one = dict.fromkeys
    expected = {
        "whole_foods": one(
            ("search", "category", "deals", "product", "stores", "store", "sales_flyer"), 1
        ),
        "harbor_freight": one(
            ("search", "clearance", "product", "prices", "stores", "availability", "reviews"), 1
        ),
        "petsmart": one(
            ("search", "product", "stores", "store_stock", "availability", "deals"), 1
        ),
        "petco": one(("search", "category", "product", "stores", "store_inventory"), 1),
        "iherb": one(("search", "product", "prices", "reviews"), 2),
        "chewy": one(("search", "product"), 10),
        "menards": {"search": 2, "product": 1, "stores": 1},
    }
    for ns, methods in expected.items():
        eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == ns}
        assert {m: ep.credits for m, ep in eps.items()} == methods, ns
        wire_ns = ns.replace("_", "")
        for m, ep in eps.items():
            assert ep.path == f"/api/v1/{wire_ns}/{m.replace('_', '-')}", ep.key
    assert sum(len(m) for m in expected.values()) == 34
    assert "store_id" in ENDPOINTS["menards_product"].credits_note


def test_slow_retail_endpoints_raise_the_timeout(monkeypatch):
    seen: list[float] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append(timeout)
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    client.petco.product(part_number="3748364")
    client.petco.category("dog/dog-food/dry-dog-food")
    client.menards.product(item_id="60893666613", store_id="3181")
    client.petco.search("dog food")
    client.iherb.search("vitamin d")
    client.iherb.product(product_id="62118")
    client.chewy.search(query="kong classic dog toy")
    assert seen == [120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 30.0]


def test_us_retail_batch_2_one_of_groups(monkeypatch):
    monkeypatch.setattr("scavio._client.sync_request", lambda *a, **k: {"ok": True})
    client = ScavioClient(api_key="sk_test")
    for call in (
        lambda: client.whole_foods.product(),
        lambda: client.harbor_freight.search(),
        lambda: client.harbor_freight.availability(["73216"]),
        lambda: client.petco.store_inventory(["6131012"]),
        lambda: client.iherb.reviews(),
        lambda: client.chewy.search(),
        lambda: client.menards.stores(),
    ):
        with pytest.raises(ScavioError):
            call()


def test_menards_search_wire_body(monkeypatch):
    """menards.search (0.34.0): query and store_id required, filters passed through as sent."""
    seen: list[tuple[str, dict]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json))
        timeouts.append(timeout)
        return {"ok": True}

    timeouts: list[float] = []
    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    client.menards.search("sledge hammer", "3181")
    client.menards.search(
        query="drill",
        store_id="3273",
        page=2,
        sort="price_asc",
        in_stock_today=True,
        min_price=0,
        max_price=60.0,
    )
    assert seen[0] == ("/api/v1/menards/search", {"query": "sledge hammer", "store_id": "3181"})
    assert seen[1][1] == {
        "query": "drill",
        "store_id": "3273",
        "page": 2,
        "sort": "price_asc",
        "in_stock_today": True,
        "min_price": 0,
        "max_price": 60.0,
    }
    assert ENDPOINTS["menards_search"].credits == 2
    # The default 30 s client timeout is raised for search's slow spells.
    assert timeouts[0] == 60.0


def test_nordstrom_credits_paths_and_wire(monkeypatch):
    """nordstrom (0.35.0): search + product, 5 credits each, 120 s timeout floor."""
    eps = {
        ep.method: ep
        for ep in ENDPOINTS.values()
        if ep.namespace == "nordstrom" and ep.method in ("search", "product")
    }
    assert {m: ep.credits for m, ep in eps.items()} == {"search": 5, "product": 5}
    for m, ep in eps.items():
        assert ep.path == f"/api/v1/nordstrom/{m}", ep.key
    sorts = ("relevance", "rating", "price_high", "price_low", "newest", "percent_off")
    sort_param = ENDPOINTS["nordstrom_search"].params[2]
    assert sort_param.name == "sort"
    assert sort_param.annotation == "Optional[Literal[" + ", ".join(f'"{c}"' for c in sorts) + "]]"

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    client.nordstrom.search("dress")
    client.nordstrom.search("dress", page=2, sort="percent_off")
    client.nordstrom.product(style_id="8098974")
    client.nordstrom.product(
        url="https://www.nordstrom.com/s/betsy-and-adam-strapless-mixed-media-gown/8098974"
    )
    assert seen == [
        ("/api/v1/nordstrom/search", {"query": "dress"}, 120.0),
        ("/api/v1/nordstrom/search", {"query": "dress", "page": 2, "sort": "percent_off"}, 120.0),
        ("/api/v1/nordstrom/product", {"style_id": "8098974"}, 120.0),
        (
            "/api/v1/nordstrom/product",
            {"url": "https://www.nordstrom.com/s/betsy-and-adam-strapless-mixed-media-gown/8098974"},
            120.0,
        ),
    ]
    with pytest.raises(ScavioError):
        client.nordstrom.product()


def test_nordstrom_listing_stores_availability_suggestions_wire(monkeypatch):
    """nordstrom (0.36.0): category, brand, stores, availability, suggestions.

    availability is 10 credits (product page + store lookup), the rest 5; all
    carry the same 120 s timeout floor as search/product.
    """
    eps = {
        ep.method: ep
        for ep in ENDPOINTS.values()
        if ep.namespace == "nordstrom" and ep.method != "reviews"
    }
    assert {m: ep.credits for m, ep in eps.items()} == {
        "search": 5,
        "product": 5,
        "category": 5,
        "brand": 5,
        "stores": 5,
        "availability": 10,
        "suggestions": 5,
    }
    for m, ep in eps.items():
        assert ep.path == f"/api/v1/nordstrom/{m}", ep.key
        assert ep.min_timeout == 120.0, ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    client.nordstrom.category("/browse/women/clothing/dresses", sort="price_low")
    client.nordstrom.brand("/brands/astr-the-label--53360", page=2)
    client.nordstrom.stores(zip="10001")
    client.nordstrom.stores(latitude=41.8781, longitude=-87.6298, distance_miles=25)
    client.nordstrom.stores(store_numbers=["210", 220])
    client.nordstrom.stores(store_numbers="210,220")
    client.nordstrom.availability(style_id="7737947")
    client.nordstrom.availability(
        url="https://www.nordstrom.com/s/maeve-midi-dress/7737947", sku_id="A7578713"
    )
    client.nordstrom.suggestions("nike air", limit=5)
    assert seen == [
        (
            "/api/v1/nordstrom/category",
            {"category": "/browse/women/clothing/dresses", "sort": "price_low"},
            120.0,
        ),
        ("/api/v1/nordstrom/brand", {"brand": "/brands/astr-the-label--53360", "page": 2}, 120.0),
        ("/api/v1/nordstrom/stores", {"zip": "10001"}, 120.0),
        (
            "/api/v1/nordstrom/stores",
            {"latitude": 41.8781, "longitude": -87.6298, "distance_miles": 25},
            120.0,
        ),
        ("/api/v1/nordstrom/stores", {"store_numbers": ["210", 220]}, 120.0),
        ("/api/v1/nordstrom/stores", {"store_numbers": "210,220"}, 120.0),
        ("/api/v1/nordstrom/availability", {"style_id": "7737947"}, 120.0),
        (
            "/api/v1/nordstrom/availability",
            {"url": "https://www.nordstrom.com/s/maeve-midi-dress/7737947", "sku_id": "A7578713"},
            120.0,
        ),
        ("/api/v1/nordstrom/suggestions", {"query": "nike air", "limit": 5}, 120.0),
    ]
    with pytest.raises(ScavioError):
        client.nordstrom.stores()
    with pytest.raises(ScavioError):
        client.nordstrom.availability(sku_id="A7578713")


def test_nordstrom_reviews_wire(monkeypatch):
    """nordstrom (0.37.0): reviews, 10 credits, 150 s timeout floor.

    A 200-review call takes up to ~100 s, so the floor is above the 120 s the
    rest of the namespace uses.
    """
    ep = ENDPOINTS["nordstrom_reviews"]
    assert (ep.namespace, ep.method, ep.http) == ("nordstrom", "reviews", "POST")
    assert ep.path == "/api/v1/nordstrom/reviews"
    assert ep.credits == 10
    assert ep.min_timeout == 150.0
    assert [p.name for p in ep.params] == [
        "url",
        "style_id",
        "sort",
        "stars",
        "verified_only",
        "with_photos",
        "search",
        "max_reviews",
    ]
    sort_param = ep.params[2]
    sorts = ("most_helpful", "most_recent", "highest_rated", "lowest_rated")
    assert sort_param.annotation == "Optional[Literal[" + ", ".join(f'"{c}"' for c in sorts) + "]]"

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    client.nordstrom.reviews(style_id="7737947")
    client.nordstrom.reviews(
        url="https://www.nordstrom.com/s/maeve-midi-dress/7737947",
        sort="lowest_rated",
        stars=[1, 2],
        verified_only=True,
        with_photos=False,
        max_reviews=200,
    )
    client.nordstrom.reviews(style_id="7737947", search="wedding")
    assert seen == [
        ("/api/v1/nordstrom/reviews", {"style_id": "7737947"}, 150.0),
        (
            "/api/v1/nordstrom/reviews",
            {
                "url": "https://www.nordstrom.com/s/maeve-midi-dress/7737947",
                "sort": "lowest_rated",
                "stars": [1, 2],
                "verified_only": True,
                "with_photos": False,
                "max_reviews": 200,
            },
            150.0,
        ),
        ("/api/v1/nordstrom/reviews", {"style_id": "7737947", "search": "wedding"}, 150.0),
    ]
    with pytest.raises(ScavioError):
        client.nordstrom.reviews(sort="most_recent")


def test_nordstrom_rack_credits_paths_and_wire(monkeypatch):
    """nordstrom_rack (0.38.0): 8 endpoints on /api/v1/nordstromrack.

    Same contract as nordstrom: availability and reviews 10 credits, the rest 5;
    120 s timeout floor, reviews 150 s.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "nordstrom_rack"}
    assert {m: ep.credits for m, ep in eps.items()} == {
        "search": 5,
        "product": 5,
        "category": 5,
        "brand": 5,
        "stores": 5,
        "availability": 10,
        "suggestions": 5,
        "reviews": 10,
    }
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/nordstromrack/{m}", ep.key
        assert ep.min_timeout == (150.0 if m == "reviews" else 120.0), ep.key
    # Same parameter names as nordstrom, endpoint for endpoint.
    for m, ep in eps.items():
        assert [p.name for p in ep.params] == [
            p.name for p in ENDPOINTS[f"nordstrom_{m}"].params
        ], ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    rack = client.nordstrom_rack
    rack.search("dress", sort="percent_off")
    rack.product(style_id="8816500")
    rack.category("/clearance/women", sort="percent_off", page=2)
    rack.brand("/brands/adidas")
    rack.stores(zip="10001", distance_miles=25)
    rack.stores(store_numbers=["229", 242])
    rack.availability(
        url="https://www.nordstromrack.com/s/maeve-midi-dress/7737947", sku_id="A5819201"
    )
    rack.suggestions("dre", limit=5)
    rack.reviews(style_id="7737947", stars=[1, 2], max_reviews=18)
    assert seen == [
        ("/api/v1/nordstromrack/search", {"query": "dress", "sort": "percent_off"}, 120.0),
        ("/api/v1/nordstromrack/product", {"style_id": "8816500"}, 120.0),
        (
            "/api/v1/nordstromrack/category",
            {"category": "/clearance/women", "sort": "percent_off", "page": 2},
            120.0,
        ),
        ("/api/v1/nordstromrack/brand", {"brand": "/brands/adidas"}, 120.0),
        ("/api/v1/nordstromrack/stores", {"zip": "10001", "distance_miles": 25}, 120.0),
        ("/api/v1/nordstromrack/stores", {"store_numbers": ["229", 242]}, 120.0),
        (
            "/api/v1/nordstromrack/availability",
            {
                "url": "https://www.nordstromrack.com/s/maeve-midi-dress/7737947",
                "sku_id": "A5819201",
            },
            120.0,
        ),
        ("/api/v1/nordstromrack/suggestions", {"query": "dre", "limit": 5}, 120.0),
        (
            "/api/v1/nordstromrack/reviews",
            {"style_id": "7737947", "stars": [1, 2], "max_reviews": 18},
            150.0,
        ),
    ]
    with pytest.raises(ScavioError):
        rack.product()
    with pytest.raises(ScavioError):
        rack.stores()
    with pytest.raises(ScavioError):
        rack.reviews(sort="most_recent")


def test_best_buy_credits_paths_and_wire(monkeypatch):
    """best_buy (0.39.0): 9 endpoints on /api/v1/bestbuy, 120 s timeout floor;
    0.92.0 adds the Best Buy Canada only questions endpoint.

    US: search, product, reviews and prices 2 credits; category 2 (3 on a
    pcmcat page, stated in credits_note); deals 3; stores and suggestions 1;
    availability 2 flat. questions 1.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "best_buy"}
    assert {m: ep.credits for m, ep in eps.items()} == {
        "search": 2,
        "product": 2,
        "reviews": 2,
        "category": 2,
        "deals": 3,
        "stores": 1,
        "availability": 2,
        "suggestions": 1,
        "prices": 2,
        "questions": 1,
    }
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/bestbuy/{m}", ep.key
        assert ep.min_timeout == 120.0, ep.key
    assert "3 for a pcmcat page" in (eps["category"].credits_note or "")

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    bb = client.best_buy
    bb.search(
        "tv",
        sort="best_selling",
        filters={"brand": "Samsung", "min_price": 300, "max_price": 500},
    )
    bb.product(sku="6607832")
    bb.reviews(sku="6607832", sort="newest", rating=1, page=2)
    bb.category(category_id="abcat0101001", filters={"on_sale": True}, include_sponsored=True)
    bb.deals()
    bb.stores("94103")
    bb.availability(sku="6607832", zip="94103", max_stores=3)
    bb.availability(sku="6607832", store_ids=["187", "873"])
    bb.suggestions("ps5 con")
    bb.prices(["6607832", "6673112", "6679316"])
    assert seen == [
        (
            "/api/v1/bestbuy/search",
            {
                "query": "tv",
                "sort": "best_selling",
                "filters": {"brand": "Samsung", "min_price": 300, "max_price": 500},
            },
            120.0,
        ),
        ("/api/v1/bestbuy/product", {"sku": "6607832"}, 120.0),
        (
            "/api/v1/bestbuy/reviews",
            {"sku": "6607832", "page": 2, "sort": "newest", "rating": 1},
            120.0,
        ),
        (
            "/api/v1/bestbuy/category",
            {
                "category_id": "abcat0101001",
                "filters": {"on_sale": True},
                "include_sponsored": True,
            },
            120.0,
        ),
        ("/api/v1/bestbuy/deals", {}, 120.0),
        ("/api/v1/bestbuy/stores", {"zip": "94103"}, 120.0),
        (
            "/api/v1/bestbuy/availability",
            {"sku": "6607832", "zip": "94103", "max_stores": 3},
            120.0,
        ),
        (
            "/api/v1/bestbuy/availability",
            {"sku": "6607832", "store_ids": ["187", "873"]},
            120.0,
        ),
        ("/api/v1/bestbuy/suggestions", {"query": "ps5 con"}, 120.0),
        ("/api/v1/bestbuy/prices", {"skus": ["6607832", "6673112", "6679316"]}, 120.0),
    ]
    with pytest.raises(ScavioError):
        bb.product()
    with pytest.raises(ScavioError):
        bb.category()
    with pytest.raises(ScavioError):
        bb.availability(sku="6607832")
    with pytest.raises(ScavioError):
        bb.availability(zip="94103")


def test_tcgplayer_credits_paths_and_wire(monkeypatch):
    """tcgplayer (0.40.0): 13 endpoints on /api/v1/tcgplayer, 1 credit each.

    Multi-word methods map to hyphenated paths (price_history ->
    price-history); 120 s timeout floor everywhere.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "tcgplayer"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "listings",
            "price_history",
            "sales",
            "games",
            "sets",
            "price_guide",
            "suggestions",
            "trending",
            "seller",
            "seller_feedback",
            "seller_products",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/tcgplayer/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    tcg = client.tcgplayer
    tcg.search("charizard", game="pokemon", sort="price_desc", limit=10)
    tcg.search(game="pokemon", set="base-set", product_type="cards")
    tcg.product(product_id=219058)
    tcg.listings(url="https://www.tcgplayer.com/product/219058/x", condition=["Near Mint"])
    tcg.price_history(product_id="219058", range="month")
    tcg.sales(product_id=219058, condition="NM,LP")
    tcg.games()
    tcg.sets("pokemon")
    tcg.price_guide(604, product_type="sealed", limit=500)
    tcg.suggestions("charizard")
    tcg.trending(game="yugioh")
    tcg.seller("58f7acae")
    tcg.seller_feedback("bf43b501", rating=1, with_comment=True, page=2)
    tcg.seller_products("58f7acae", game="pokemon", sort="price_asc")
    base = "/api/v1/tcgplayer/"
    assert seen == [
        (
            base + "search",
            {"query": "charizard", "game": "pokemon", "sort": "price_desc", "limit": 10},
            120.0,
        ),
        (
            base + "search",
            {"game": "pokemon", "set": "base-set", "product_type": "cards"},
            120.0,
        ),
        (base + "product", {"product_id": 219058}, 120.0),
        (
            base + "listings",
            {"url": "https://www.tcgplayer.com/product/219058/x", "condition": ["Near Mint"]},
            120.0,
        ),
        (base + "price-history", {"product_id": "219058", "range": "month"}, 120.0),
        (base + "sales", {"product_id": 219058, "condition": "NM,LP"}, 120.0),
        (base + "games", {}, 120.0),
        (base + "sets", {"game": "pokemon"}, 120.0),
        (base + "price-guide", {"set_id": 604, "product_type": "sealed", "limit": 500}, 120.0),
        (base + "suggestions", {"query": "charizard"}, 120.0),
        (base + "trending", {"game": "yugioh"}, 120.0),
        (base + "seller", {"seller_key": "58f7acae"}, 120.0),
        (
            base + "seller-feedback",
            {"seller_key": "bf43b501", "rating": 1, "with_comment": True, "page": 2},
            120.0,
        ),
        (
            base + "seller-products",
            {"seller_key": "58f7acae", "game": "pokemon", "sort": "price_asc"},
            120.0,
        ),
    ]
    with pytest.raises(ScavioError):
        tcg.product()
    with pytest.raises(ScavioError):
        tcg.listings()
    with pytest.raises(ScavioError):
        tcg.price_history()
    with pytest.raises(ScavioError):
        tcg.sales()


def test_vinted_credits_paths_and_wire(monkeypatch):
    """vinted (0.41.0): 9 endpoints on /api/v1/vinted, 1 credit each.

    Every method takes an optional country (27 sites, fr default on the
    server); multi-word methods map to hyphenated paths (seller_products ->
    seller-products); 120 s timeout floor everywhere.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "vinted"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "seller",
            "seller_products",
            "seller_feedback",
            "brands",
            "suggestions",
            "filters",
            "categories",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/vinted/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    v = client.vinted
    v.search("barbour jacket", country="uk", status_ids=[6, 1], price_to=80.0, sort="newest_first")
    v.search(country="pl", category_id=1907, brand_ids="46805,53", page=2)
    v.product(item_id=10671938315)
    v.product(url="https://www.vinted.co.uk/items/10671938315-x")
    v.seller(65958245, country="uk")
    v.seller_products("65958245", country="uk", sort="price_low_to_high", limit=96)
    v.seller_feedback(65958245, page=2, limit=50)
    v.brands("barbour", country="de")
    v.suggestions("barb")
    v.filters("size", country="fr", query="dress", category_id=1904)
    v.categories(country="uk", parent_id=1904)
    base = "/api/v1/vinted/"
    assert seen == [
        (
            base + "search",
            {
                "query": "barbour jacket",
                "country": "uk",
                "status_ids": [6, 1],
                "price_to": 80.0,
                "sort": "newest_first",
            },
            120.0,
        ),
        (
            base + "search",
            {"country": "pl", "category_id": 1907, "brand_ids": "46805,53", "page": 2},
            120.0,
        ),
        (base + "product", {"item_id": 10671938315}, 120.0),
        (base + "product", {"url": "https://www.vinted.co.uk/items/10671938315-x"}, 120.0),
        (base + "seller", {"user_id": 65958245, "country": "uk"}, 120.0),
        (
            base + "seller-products",
            {"user_id": "65958245", "country": "uk", "sort": "price_low_to_high", "limit": 96},
            120.0,
        ),
        (base + "seller-feedback", {"user_id": 65958245, "page": 2, "limit": 50}, 120.0),
        (base + "brands", {"query": "barbour", "country": "de"}, 120.0),
        (base + "suggestions", {"query": "barb"}, 120.0),
        (
            base + "filters",
            {"filter": "size", "country": "fr", "query": "dress", "category_id": 1904},
            120.0,
        ),
        (base + "categories", {"country": "uk", "parent_id": 1904}, 120.0),
    ]
    with pytest.raises(ScavioError):
        v.product()
    with pytest.raises(ScavioError):
        v.product(country="uk")


def test_macys_credits_paths_and_wire(monkeypatch):
    """macys (0.42.0): 9 endpoints on /api/v1/macys, 1 credit each.

    US only (no country). store_availability maps to the hyphenated
    /store-availability path; deals sends `type` as-is; 120 s timeout floor.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "macys"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "reviews",
            "category",
            "brand",
            "deals",
            "stores",
            "store_availability",
            "suggestions",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/macys/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert not any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    m = client.macys
    m.search(
        "jeans",
        brand=["Levi's", "Calvin Klein"],
        special_offer="clearance",
        min_price=50.0,
        max_price=100.0,
        sort="price_low_to_high",
        filters={"GENDER": "Women"},
    )
    m.product(product_id=25822310)
    m.product(product_ids=[25822310, 719388])
    m.reviews(product_id="25822310", sort="lowest_rated", rating=1, limit=100)
    m.category(category_id=3763, page=2, pickup_store_id=4592)
    m.brand(url="https://www.macys.com/shop/brands/calvin-klein?id=337747")
    m.deals(type="last_act", include_sponsored=True)
    m.stores(zip="10001", radius=25)
    m.store_availability(product_id=25822310, store_id=4592)
    m.store_availability(
        url="https://www.macys.com/shop/product/x?ID=25822310", city="Atlanta", state="GA"
    )
    m.suggestions("jea")
    base = "/api/v1/macys/"
    assert seen == [
        (
            base + "search",
            {
                "query": "jeans",
                "special_offer": "clearance",
                "sort": "price_low_to_high",
                "brand": ["Levi's", "Calvin Klein"],
                "min_price": 50.0,
                "max_price": 100.0,
                "filters": {"GENDER": "Women"},
            },
            120.0,
        ),
        (base + "product", {"product_id": 25822310}, 120.0),
        (base + "product", {"product_ids": [25822310, 719388]}, 120.0),
        (
            base + "reviews",
            {"product_id": "25822310", "sort": "lowest_rated", "limit": 100, "rating": 1},
            120.0,
        ),
        (base + "category", {"category_id": 3763, "page": 2, "pickup_store_id": 4592}, 120.0),
        (
            base + "brand",
            {"url": "https://www.macys.com/shop/brands/calvin-klein?id=337747"},
            120.0,
        ),
        (base + "deals", {"type": "last_act", "include_sponsored": True}, 120.0),
        (base + "stores", {"zip": "10001", "radius": 25}, 120.0),
        (base + "store-availability", {"product_id": 25822310, "store_id": 4592}, 120.0),
        (
            base + "store-availability",
            {
                "url": "https://www.macys.com/shop/product/x?ID=25822310",
                "city": "Atlanta",
                "state": "GA",
            },
            120.0,
        ),
        (base + "suggestions", {"query": "jea"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        m.product()
    with pytest.raises(ScavioError):
        m.reviews(rating=5)
    with pytest.raises(ScavioError):
        m.stores(radius=10)
    with pytest.raises(ScavioError):
        m.store_availability(product_id=25822310)


def test_saks_credits_paths_and_wire(monkeypatch):
    """saks (0.43.0): 9 endpoints on /api/v1/saks, 2 credits each.

    US only (no country). store_availability maps to the hyphenated
    /store-availability path and takes a required variant sku; radius is an
    int literal (15, 30, 50, 100, 300); 120 s timeout floor.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "saks"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "category",
            "brand",
            "deals",
            "stores",
            "store_availability",
            "suggestions",
            "designers",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 2, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/saks/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert not any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    s = client.saks
    s.search(
        "coat",
        brand=["Prada", "Moncler"],
        size="Medium",
        min_price=500.0,
        on_sale=True,
        sort="price_low_to_high",
        filters={"refGender": "Women's"},
    )
    s.product(product_id="0400019127312", color="BLUE OPAL", size="4")
    s.category(path="/c/women-s-apparel/dresses", start=22)
    s.brand(brand="gucci", new_arrivals=True, page=2)
    s.deals(type="womens_sale", color="Black")
    s.stores(zip="10022", radius=50)
    s.store_availability("10781654", lat=40.758, lng=-73.9855, radius=15)
    s.suggestions("gucci")
    s.designers(letter="G")
    base = "/api/v1/saks/"
    assert seen == [
        (
            base + "search",
            {
                "query": "coat",
                "brand": ["Prada", "Moncler"],
                "sort": "price_low_to_high",
                "size": "Medium",
                "min_price": 500.0,
                "on_sale": True,
                "filters": {"refGender": "Women's"},
            },
            120.0,
        ),
        (
            base + "product",
            {"product_id": "0400019127312", "color": "BLUE OPAL", "size": "4"},
            120.0,
        ),
        (base + "category", {"path": "/c/women-s-apparel/dresses", "start": 22}, 120.0),
        (base + "brand", {"brand": "gucci", "page": 2, "new_arrivals": True}, 120.0),
        (base + "deals", {"type": "womens_sale", "color": "Black"}, 120.0),
        (base + "stores", {"zip": "10022", "radius": 50}, 120.0),
        (
            base + "store-availability",
            {"sku": "10781654", "lat": 40.758, "lng": -73.9855, "radius": 15},
            120.0,
        ),
        (base + "suggestions", {"query": "gucci"}, 120.0),
        (base + "designers", {"letter": "G"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        s.product()
    with pytest.raises(ScavioError):
        s.category(sort="newest")
    with pytest.raises(ScavioError):
        s.stores(radius=25)
    with pytest.raises(ScavioError):
        s.store_availability("10781654")


def test_kohls_credits_paths_and_wire(monkeypatch):
    """kohls (0.44.0): 9 endpoints on /api/v1/kohls; stores 1 credit, the rest 2.

    US only (no country). store_availability maps to the hyphenated
    /store-availability path and takes a required sku and zip; filters is a
    facet value id or a list of them; 120 s timeout floor.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "kohls"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "category",
            "brand",
            "deals",
            "stores",
            "store_availability",
            "suggestions",
            "coupons",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == (1 if m == "stores" else 2), ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/kohls/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert not any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    k = client.kohls
    k.search(
        "jeans",
        brand="Levi's",
        size="M",
        clearance=True,
        sort="percent_off",
        filters=["Gender:Womens", "Price:$25 to $50"],
    )
    k.product(product_id="6251213", store_id=725)
    k.category(path="/catalog/womens-clothing.jsp?CN=Gender:Womens+Department:Clothing", page=2)
    k.brand(brand="Hamilton Beach", on_sale=True)
    k.deals(type="kohls_cash", color="Black")
    k.stores(city="Austin", state="TX", radius=50)
    k.store_availability("73519108", "10001", dept="063")
    k.suggestions("coff", type="products")
    k.coupons()
    base = "/api/v1/kohls/"
    assert seen == [
        (
            base + "search",
            {
                "query": "jeans",
                "brand": "Levi's",
                "sort": "percent_off",
                "size": "M",
                "clearance": True,
                "filters": ["Gender:Womens", "Price:$25 to $50"],
            },
            120.0,
        ),
        (base + "product", {"product_id": "6251213", "store_id": 725}, 120.0),
        (
            base + "category",
            {
                "path": "/catalog/womens-clothing.jsp?CN=Gender:Womens+Department:Clothing",
                "page": 2,
            },
            120.0,
        ),
        (base + "brand", {"brand": "Hamilton Beach", "on_sale": True}, 120.0),
        (base + "deals", {"type": "kohls_cash", "color": "Black"}, 120.0),
        (base + "stores", {"city": "Austin", "state": "TX", "radius": 50}, 120.0),
        (
            base + "store-availability",
            {"sku": "73519108", "zip": "10001", "dept": "063"},
            120.0,
        ),
        (base + "suggestions", {"query": "coff", "type": "products"}, 120.0),
        (base + "coupons", {}, 120.0),
    ]
    with pytest.raises(ScavioError):
        k.product(store_id=725)
    with pytest.raises(ScavioError):
        k.category(sort="best_sellers")
    with pytest.raises(ScavioError):
        k.brand(page=2)
    with pytest.raises(ScavioError):
        k.stores(radius=25)


def test_jcpenney_credits_paths_and_wire(monkeypatch):
    """jcpenney (0.45.0; reviews, questions 0.46.0): 11 endpoints, 1 credit each.

    US only (no country). store_availability maps to the hyphenated
    /store-availability path and takes a required sku plus zip or lat + lng;
    filters is a dict of facet id to value(s); product takes up to 20
    product_ids; reviews and questions take product_id or url; 120 s timeout
    floor, 240 s for the slow reviews and questions.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "jcpenney"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "category",
            "brand",
            "deals",
            "stores",
            "store_availability",
            "suggestions",
            "coupons",
            "reviews",
            "questions",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/jcpenney/" + m.replace("_", "-"), ep.key
        slow = m in ("reviews", "questions")
        assert ep.min_timeout == (240.0 if slow else 120.0), ep.key
        assert not any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    j = client.jcpenney
    j.search(
        "jeans",
        brand=["levi's", "lee"],
        deal="CLEARANCE",
        exact=True,
        sort="price_low_to_high",
        price_range="$20 - $24",
        filters={"gender": "women", "rise": ["mid rise", "high rise"]},
    )
    j.product(product_ids=["ppr5008604049", "ppr5008212471"])
    j.category(path="/g/women/dresses?id=cat100210008", page=2, color="black")
    j.brand(brand="Nike", size="m")
    j.deals(type="bogo", department="dept20000011")
    j.stores(city="Austin", state="TX", radius=50, page_size=20)
    j.store_availability("84630160042", zip="90012", in_stock_only=True)
    j.suggestions("jea")
    j.coupons()
    j.reviews(product_id="ppr5008604049", sort="most_helpful", rating=1, max_reviews=68)
    j.questions(url="https://www.jcpenney.com/p/x/ppr5008212471", max_questions=20)
    base = "/api/v1/jcpenney/"
    assert seen == [
        (
            base + "search",
            {
                "query": "jeans",
                "brand": ["levi's", "lee"],
                "deal": "CLEARANCE",
                "exact": True,
                "sort": "price_low_to_high",
                "price_range": "$20 - $24",
                "filters": {"gender": "women", "rise": ["mid rise", "high rise"]},
            },
            120.0,
        ),
        (base + "product", {"product_ids": ["ppr5008604049", "ppr5008212471"]}, 120.0),
        (
            base + "category",
            {"path": "/g/women/dresses?id=cat100210008", "page": 2, "color": "black"},
            120.0,
        ),
        (base + "brand", {"brand": "Nike", "size": "m"}, 120.0),
        (base + "deals", {"type": "bogo", "department": "dept20000011"}, 120.0),
        (
            base + "stores",
            {"city": "Austin", "state": "TX", "radius": 50, "page_size": 20},
            120.0,
        ),
        (
            base + "store-availability",
            {"sku": "84630160042", "zip": "90012", "in_stock_only": True},
            120.0,
        ),
        (base + "suggestions", {"query": "jea"}, 120.0),
        (base + "coupons", {}, 120.0),
        (
            base + "reviews",
            {"product_id": "ppr5008604049", "sort": "most_helpful", "rating": 1, "max_reviews": 68},
            240.0,
        ),
        (
            base + "questions",
            {"url": "https://www.jcpenney.com/p/x/ppr5008212471", "max_questions": 20},
            240.0,
        ),
    ]
    with pytest.raises(ScavioError):
        j.product()
    with pytest.raises(ScavioError):
        j.category(sort="best_sellers")
    with pytest.raises(ScavioError):
        j.brand(page=2)
    with pytest.raises(ScavioError):
        j.stores(radius=25)
    with pytest.raises(ScavioError):
        j.store_availability("84630160042")
    with pytest.raises(ScavioError):
        j.reviews(sort="most_recent")
    with pytest.raises(ScavioError):
        j.questions(max_questions=10)


def test_dicks_credits_paths_and_wire(monkeypatch):
    """dicks (0.47.0): 9 endpoints on /api/v1/dicks, 1 credit each except
    product and reviews (2).

    US only (no country). store_availability maps to the hyphenated
    /store-availability path and takes a required skus list plus zip or
    lat + lng; products takes a required product_ids list (up to 5); filters
    is a dict of facet id to value(s); 120 s timeout floor, 240 s for the slow
    product and reviews.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "dicks"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "products",
            "reviews",
            "category",
            "brand",
            "deals",
            "store_availability",
            "suggestions",
        ]
    )
    for m, ep in eps.items():
        slow = m in ("product", "reviews")
        assert ep.credits == (2 if slow else 1), ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/dicks/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == (240.0 if slow else 120.0), ep.key
        assert not any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    d = client.dicks
    d.search(
        "running shoes",
        brand=["Nike", "HOKA"],
        sort="savings",
        page_size=144,
        filters={"5495": "Men's", "rating": "4+"},
        min_price=60,
        max_price=80,
    )
    d.product(product_id="23FHQMCLFTN9GTXBLMNS")
    d.products(["23FHQMCLFTN9GTXBLMNS", "26UNDMFITN1HRI9WUAETC"])
    d.reviews(url="https://www.dickssportinggoods.com/p/x/26undmfitn1hri9wuaetc")
    d.category(path="/f/mens-running-shoes", page=2)
    d.category(category_id="202105", brand="Nike")
    d.brand("YETI", query="tumbler")
    d.deals(type="clearance", sort="savings")
    d.store_availability(["25535758", "26810079"], zip="60601", chain="golf_galaxy", radius=50)
    d.suggestions("yeti tum")
    base = "/api/v1/dicks/"
    assert seen == [
        (
            base + "search",
            {
                "query": "running shoes",
                "brand": ["Nike", "HOKA"],
                "sort": "savings",
                "page_size": 144,
                "filters": {"5495": "Men's", "rating": "4+"},
                "min_price": 60,
                "max_price": 80,
            },
            120.0,
        ),
        (base + "product", {"product_id": "23FHQMCLFTN9GTXBLMNS"}, 240.0),
        (
            base + "products",
            {"product_ids": ["23FHQMCLFTN9GTXBLMNS", "26UNDMFITN1HRI9WUAETC"]},
            120.0,
        ),
        (
            base + "reviews",
            {"url": "https://www.dickssportinggoods.com/p/x/26undmfitn1hri9wuaetc"},
            240.0,
        ),
        (base + "category", {"path": "/f/mens-running-shoes", "page": 2}, 120.0),
        (base + "category", {"category_id": "202105", "brand": "Nike"}, 120.0),
        (base + "brand", {"brand": "YETI", "query": "tumbler"}, 120.0),
        (base + "deals", {"type": "clearance", "sort": "savings"}, 120.0),
        (
            base + "store-availability",
            {
                "skus": ["25535758", "26810079"],
                "zip": "60601",
                "chain": "golf_galaxy",
                "radius": 50,
            },
            120.0,
        ),
        (base + "suggestions", {"query": "yeti tum"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        d.product()
    with pytest.raises(ScavioError):
        d.reviews()
    with pytest.raises(ScavioError):
        d.category(sort="featured")
    with pytest.raises(ScavioError):
        d.store_availability(["25535758"])


def test_footlocker_credits_paths_and_wire(monkeypatch):
    """footlocker (0.48.0): 10 endpoints on /api/v1/footlocker, 1 credit each.

    search, product, category, brand and deals take country (13 storefronts)
    and language; releases takes us / ca / gb and maps date_from / date_to to
    the wire's from / to; stores, store_availability, reviews and questions
    are US only. store_availability maps to the hyphenated /store-availability
    path; filters is a dict of facet id to value(s); 120 s timeout floor, 240 s
    for the slow reviews and questions.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "footlocker"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "category",
            "brand",
            "deals",
            "releases",
            "stores",
            "store_availability",
            "reviews",
            "questions",
        ]
    )
    for m, ep in eps.items():
        slow = m in ("reviews", "questions")
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/footlocker/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == (240.0 if slow else 120.0), ep.key
        assert any(p.name == "country" for p in ep.params), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    f = client.footlocker
    f.search(
        "nike dunk",
        country="be",
        language="fr",
        brand=["Nike", "Jordan"],
        sort="price_low_to_high",
        gender="Men's",
        on_sale=True,
        filters={"mensShoesSize": "10.0"},
    )
    f.product(product_id="Q5495005")
    f.product(url="https://www.footlocker.de/de/product/~/316707025504.html", country="de")
    f.category(path="/category/mens/shoes.html", page=2)
    f.category(collection_id="men-s-shoes", country="gb")
    f.brand(brand="New Balance", query="running shoes")
    f.deals(type="exclusives", country="ca", language="fr")
    f.releases(
        country="gb", status="upcoming", date_from="2026-11-01", date_to="2026-12-31", brand="Nike"
    )
    f.stores(city="Atlanta", state="GA", limit=5)
    f.store_availability(product_id="W2288111", size="10.0", zip="10001", radius=25)
    f.reviews(product_id="Q5495005", sort="lowest_rating", rating=1, limit=98)
    f.questions(url="https://www.footlocker.com/product/~/Q5495005.html", limit=50)
    base = "/api/v1/footlocker/"
    assert seen == [
        (
            base + "search",
            {
                "query": "nike dunk",
                "country": "be",
                "language": "fr",
                "brand": ["Nike", "Jordan"],
                "sort": "price_low_to_high",
                "gender": "Men's",
                "on_sale": True,
                "filters": {"mensShoesSize": "10.0"},
            },
            120.0,
        ),
        (base + "product", {"product_id": "Q5495005"}, 120.0),
        (
            base + "product",
            {"url": "https://www.footlocker.de/de/product/~/316707025504.html", "country": "de"},
            120.0,
        ),
        (base + "category", {"path": "/category/mens/shoes.html", "page": 2}, 120.0),
        (base + "category", {"collection_id": "men-s-shoes", "country": "gb"}, 120.0),
        (base + "brand", {"brand": "New Balance", "query": "running shoes"}, 120.0),
        (base + "deals", {"type": "exclusives", "country": "ca", "language": "fr"}, 120.0),
        (
            base + "releases",
            {
                "country": "gb",
                "status": "upcoming",
                "from": "2026-11-01",
                "to": "2026-12-31",
                "brand": "Nike",
            },
            120.0,
        ),
        (base + "stores", {"city": "Atlanta", "state": "GA", "limit": 5}, 120.0),
        (
            base + "store-availability",
            {"product_id": "W2288111", "size": "10.0", "zip": "10001", "radius": 25},
            120.0,
        ),
        (
            base + "reviews",
            {"product_id": "Q5495005", "sort": "lowest_rating", "rating": 1, "limit": 98},
            240.0,
        ),
        (
            base + "questions",
            {"url": "https://www.footlocker.com/product/~/Q5495005.html", "limit": 50},
            240.0,
        ),
    ]
    with pytest.raises(ScavioError):
        f.product(country="de")
    with pytest.raises(ScavioError):
        f.category(sort="top_rated")
    with pytest.raises(ScavioError):
        f.brand(query="running")
    with pytest.raises(ScavioError):
        f.stores(radius=10)
    with pytest.raises(ScavioError):
        f.store_availability(product_id="W2288111")
    with pytest.raises(ScavioError):
        f.reviews(sort="most_recent")
    with pytest.raises(ScavioError):
        f.questions(limit=10)


def test_fanatics_credits_paths_and_wire(monkeypatch):
    """fanatics (0.49.0): 5 endpoints on /api/v1/fanatics, 1 credit each.

    search, product, browse and deals take country (8 storefronts), language
    (ca) and site (US league stores); reviews is US only. filters is a dict of
    filter code to one value; ids take an int or a digit string; 120 s timeout
    floor, 300 s for the slow reviews.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "fanatics"}
    assert sorted(eps) == sorted(["search", "product", "browse", "deals", "reviews"])
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/fanatics/" + m, ep.key
        assert ep.min_timeout == (300.0 if m == "reviews" else 120.0), ep.key
        assert any(p.name == "country" for p in ep.params), ep.key
        assert any(p.name == "site" for p in ep.params) == (m != "reviews"), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    f = client.fanatics
    f.search(
        "chiefs jersey",
        site="nflshop",
        gender="women",
        league_id=25,
        department_id="8011",
        filters={"ks": "126"},
        page=2,
        page_size=24,
        sort="price_low_to_high",
    )
    f.search("trikot", country="de")
    f.product(product_id="3892922")
    f.product(url="https://www.fanatics.ca/fr/x/p-3892922", country="ca", language="fr")
    f.browse(team_id=3372, department_id="8008-8084", price_band="25_50", on_sale=True)
    f.browse(url="https://www.fanatics.com/nba/los-angeles-lakers/o-23+t-3372", site="fanatics")
    f.deals()
    f.deals(type="clearance", league_id=25, country="jp")
    f.reviews(product_id="3892922", sort="most_recent", rating=5, limit=50)
    base = "/api/v1/fanatics/"
    assert seen == [
        (
            base + "search",
            {
                "query": "chiefs jersey",
                "site": "nflshop",
                "gender": "women",
                "league_id": 25,
                "department_id": "8011",
                "filters": {"ks": "126"},
                "page": 2,
                "page_size": 24,
                "sort": "price_low_to_high",
            },
            120.0,
        ),
        (base + "search", {"query": "trikot", "country": "de"}, 120.0),
        (base + "product", {"product_id": "3892922"}, 120.0),
        (
            base + "product",
            {"url": "https://www.fanatics.ca/fr/x/p-3892922", "country": "ca", "language": "fr"},
            120.0,
        ),
        (
            base + "browse",
            {"team_id": 3372, "department_id": "8008-8084", "price_band": "25_50", "on_sale": True},
            120.0,
        ),
        (
            base + "browse",
            {
                "url": "https://www.fanatics.com/nba/los-angeles-lakers/o-23+t-3372",
                "site": "fanatics",
            },
            120.0,
        ),
        (base + "deals", {}, 120.0),
        (base + "deals", {"type": "clearance", "league_id": 25, "country": "jp"}, 120.0),
        (
            base + "reviews",
            {"product_id": "3892922", "sort": "most_recent", "rating": 5, "limit": 50},
            300.0,
        ),
    ]
    with pytest.raises(ScavioError):
        f.product(country="de")
    with pytest.raises(ScavioError):
        f.reviews(sort="most_recent")


def test_carrefour_credits_paths_and_wire(monkeypatch):
    """carrefour (0.50.0): 9 endpoints on /api/v1/carrefour, 1 credit each.

    search and product take country (fr, ar, ro, be; be costs 2), language
    (be) and store (fr); the other seven are carrefour.fr only. store takes a
    digit string or an int; 120 s timeout floor everywhere.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "carrefour"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "reviews",
            "category",
            "promotions",
            "suggestions",
            "stores",
            "store_availability",
            "store",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/carrefour/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert any(p.name == "country" for p in ep.params), ep.key
        assert (ep.credits_note is not None) == (m in ("search", "product")), ep.key
        assert any(p.name == "store" for p in ep.params) == (
            m in ("search", "product", "category", "promotions")
        ), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    c = client.carrefour
    c.search(
        "lait",
        brand="LACTEL",
        sort="price_low_to_high",
        store="840093",
        nutriscore="A",
        organic=True,
        min_price=1.5,
        page=2,
    )
    c.search("chocolat", country="be", language="nl")
    c.product(ean="3017620422003", store=281)
    c.product(url="https://carrefour.ro/x/p", country="ro")
    c.reviews("8006530256179", sort="lowest_rated", rating=1, limit=50, offset=10)
    c.category(path="/r/cremerie", sort="unit_price_low_to_high", carrefour_brands=True)
    c.promotions(type="loyalty", category="Boissons")
    c.suggestions("nutel")
    c.stores(postal_code="69003", service="station_service", limit=20)
    c.stores(lat=45.75, lng=4.85)
    c.store_availability("3017620422003", "69003")
    c.store(slug="venissieux")
    base = "/api/v1/carrefour/"
    assert seen == [
        (
            base + "search",
            {
                "query": "lait",
                "store": "840093",
                "page": 2,
                "sort": "price_low_to_high",
                "brand": "LACTEL",
                "nutriscore": "A",
                "organic": True,
                "min_price": 1.5,
            },
            120.0,
        ),
        (base + "search", {"query": "chocolat", "country": "be", "language": "nl"}, 120.0),
        (base + "product", {"ean": "3017620422003", "store": 281}, 120.0),
        (base + "product", {"url": "https://carrefour.ro/x/p", "country": "ro"}, 120.0),
        (
            base + "reviews",
            {
                "ean": "8006530256179",
                "sort": "lowest_rated",
                "rating": 1,
                "limit": 50,
                "offset": 10,
            },
            120.0,
        ),
        (
            base + "category",
            {"path": "/r/cremerie", "sort": "unit_price_low_to_high", "carrefour_brands": True},
            120.0,
        ),
        (base + "promotions", {"type": "loyalty", "category": "Boissons"}, 120.0),
        (base + "suggestions", {"query": "nutel"}, 120.0),
        (
            base + "stores",
            {"postal_code": "69003", "limit": 20, "service": "station_service"},
            120.0,
        ),
        (base + "stores", {"lat": 45.75, "lng": 4.85}, 120.0),
        (base + "store-availability", {"ean": "3017620422003", "postal_code": "69003"}, 120.0),
        (base + "store", {"slug": "venissieux"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        c.product(country="fr")
    with pytest.raises(ScavioError):
        c.category(sort="top_rated")
    with pytest.raises(ScavioError):
        c.stores(service="drive")
    with pytest.raises(ScavioError):
        c.store()


def test_allegro_credits_paths_and_wire(monkeypatch):
    """allegro (0.51.0): 7 endpoints on /api/v1/allegro, 2 credits each.

    Every endpoint takes country (pl, cz, sk, hu). buying_format and deals are
    pl-only filters on the grid endpoints (search, seller, category), absent on
    product_offers. offer_id and category_id take a digit string or an int;
    120 s timeout floor everywhere (sk / hu take up to ~60 s per attempt).
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "allegro"}
    assert sorted(eps) == sorted(
        [
            "search",
            "offer",
            "product",
            "product_offers",
            "seller",
            "seller_feedback",
            "category",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 2, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/allegro/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        country = next(p for p in ep.params if p.name == "country")
        assert country.annotation == 'Optional[Literal["pl", "cz", "sk", "hu"]]', ep.key
        names = {p.name for p in ep.params}
        assert ({"buying_format", "deals"} <= names) == (
            m in ("search", "seller", "category")
        ), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    a = client.allegro
    a.search(
        "laptop",
        sort="price_low_to_high",
        condition="new",
        buying_format="buy_now",
        deals=True,
        smart=True,
        min_price=500,
        category_id=491,
        page=2,
    )
    a.search("notebook", country="hu")
    a.offer(offer_id="18801787032")
    a.offer(url="https://allegro.cz/nabidka/18740738924")
    a.product(product_id="90d08230-e02a-4210-913d-d417453321b8", country="sk")
    a.product_offers(
        product_id="90d08230-e02a-4210-913d-d417453321b8",
        sort="price_with_delivery_low_to_high",
        condition="used",
        max_price=100.5,
    )
    a.seller("Yupilo_pl", query="lenovo", category="komputery", sort="newest")
    a.seller_feedback("Yupilo_pl", page=3)
    a.category(category_id="laptopy-491", query="dell", sort="popularity")
    a.category(url="https://allegro.pl/kategoria/laptopy-491")
    base = "/api/v1/allegro/"
    assert seen == [
        (
            base + "search",
            {
                "query": "laptop",
                "page": 2,
                "sort": "price_low_to_high",
                "category_id": 491,
                "min_price": 500,
                "condition": "new",
                "smart": True,
                "buying_format": "buy_now",
                "deals": True,
            },
            120.0,
        ),
        (base + "search", {"query": "notebook", "country": "hu"}, 120.0),
        (base + "offer", {"offer_id": "18801787032"}, 120.0),
        (base + "offer", {"url": "https://allegro.cz/nabidka/18740738924"}, 120.0),
        (
            base + "product",
            {"product_id": "90d08230-e02a-4210-913d-d417453321b8", "country": "sk"},
            120.0,
        ),
        (
            base + "product-offers",
            {
                "product_id": "90d08230-e02a-4210-913d-d417453321b8",
                "sort": "price_with_delivery_low_to_high",
                "max_price": 100.5,
                "condition": "used",
            },
            120.0,
        ),
        (
            base + "seller",
            {"login": "Yupilo_pl", "query": "lenovo", "category": "komputery", "sort": "newest"},
            120.0,
        ),
        (base + "seller-feedback", {"login": "Yupilo_pl", "page": 3}, 120.0),
        (
            base + "category",
            {"category_id": "laptopy-491", "query": "dell", "sort": "popularity"},
            120.0,
        ),
        (base + "category", {"url": "https://allegro.pl/kategoria/laptopy-491"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        a.offer(country="pl")
    with pytest.raises(ScavioError):
        a.product()
    with pytest.raises(ScavioError):
        a.product_offers(sort="price_low_to_high")
    with pytest.raises(ScavioError):
        a.category(query="dell")


def test_company_enrich_credits_paths_and_wire(monkeypatch):
    """company (0.52.0): enrich on /api/v1/company/enrich, body-priced.

    10 credits from a url, 20 from a place_id. url and place_id are both
    optional positionals; at least one is required (client-side one_of),
    both together are allowed (url is the site read). 180 s timeout floor:
    median ~23 s, place_id calls measured 78 s.
    """
    eps = [ep for ep in ENDPOINTS.values() if ep.namespace == "company"]
    assert [ep.method for ep in eps] == ["enrich"]
    ep = eps[0]
    assert ep.key == "company_enrich"
    assert ep.http == "POST"
    assert ep.path == "/api/v1/company/enrich"
    assert ep.credits == 10
    assert "20 from a place_id" in ep.credits_note
    assert ep.min_timeout == 180.0
    assert [p.name for p in ep.params] == ["url", "place_id"]
    assert all(not p.required and p.positional for p in ep.params)

    enrich = ScavioClient(api_key="sk_test").company.enrich
    params = list(inspect.signature(enrich).parameters.values())
    assert [p.name for p in params] == ["url", "place_id", "extra"]
    assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[0].default is None and params[1].default is None

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    c = ScavioClient(api_key="sk_test").company
    c.enrich("https://reliantplumbing.com")
    c.enrich(place_id="ChIJf--pagyMOIgRBVuxHteSRBo")
    c.enrich(url="reliantplumbing.com", place_id="ChIJf--pagyMOIgRBVuxHteSRBo")
    ScavioClient(api_key="sk_test", timeout=300).company.enrich("reliantplumbing.com")
    assert seen == [
        ("/api/v1/company/enrich", {"url": "https://reliantplumbing.com"}, 180.0),
        ("/api/v1/company/enrich", {"place_id": "ChIJf--pagyMOIgRBVuxHteSRBo"}, 180.0),
        (
            "/api/v1/company/enrich",
            {"url": "reliantplumbing.com", "place_id": "ChIJf--pagyMOIgRBVuxHteSRBo"},
            180.0,
        ),
        ("/api/v1/company/enrich", {"url": "reliantplumbing.com"}, 300),
    ]
    with pytest.raises(ScavioError):
        c.enrich()


def test_company_enrich_async(monkeypatch):
    import asyncio

    seen: dict = {}

    async def fake_request(method, path, *, timeout, json=None, **_):
        seen.update(path=path, json=json, timeout=timeout)
        return {"ok": True}

    monkeypatch.setattr("scavio._async_client.async_request", fake_request)
    client = AsyncScavioClient(api_key="sk_test")
    asyncio.run(client.company.enrich(place_id="ChIJf--pagyMOIgRBVuxHteSRBo"))
    assert seen == {
        "path": "/api/v1/company/enrich",
        "json": {"place_id": "ChIJf--pagyMOIgRBVuxHteSRBo"},
        "timeout": 180.0,
    }


def test_olx_credits_paths_and_wire(monkeypatch):
    """olx (0.53.0): 9 endpoints on /api/v1/olx, 1 credit each.

    Every endpoint takes country (pl, ro, pt, bg, ua, kz, uz) except filters and
    similar (pl, ro, pt, bg, ua). language (ru, kk, uz) is on search, seller_ads
    and offer only. search takes query, category_id or both; offer and similar
    take offer_id or url. 120 s timeout floor everywhere.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "olx"}
    assert sorted(eps) == sorted(
        [
            "search",
            "offer",
            "seller",
            "seller_ads",
            "filters",
            "categories",
            "locations",
            "suggestions",
            "similar",
        ]
    )
    all7 = 'Optional[Literal["pl", "ro", "pt", "bg", "ua", "kz", "uz"]]'
    eu5 = 'Optional[Literal["pl", "ro", "pt", "bg", "ua"]]'
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/olx/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        country = next(p for p in ep.params if p.name == "country")
        assert country.annotation == (eu5 if m in ("filters", "similar") else all7), ep.key
        names = {p.name for p in ep.params}
        assert ("language" in names) == (m in ("search", "seller_ads", "offer")), ep.key
        assert ("filters" in names) == (m in ("search", "seller_ads")), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    o = client.olx
    o.search(
        query="iphone",
        sort="newest",
        min_price=500,
        condition="used",
        seller_type="private",
        olx_delivery=True,
        city_id=17871,
        distance_km=30,
        page=2,
        page_size=50,
    )
    o.search(
        category_id="84",
        filters={"filter_float_year:from": 2018, "filter_enum_rooms": ["two", "three"]},
        include_promoted=False,
    )
    o.search(query="velosiped", country="uz", language="uz")
    o.offer(offer_id="1107557408")
    o.offer(offer_id=402863292, country="kz", language="kk")
    o.seller("2547532895")
    o.seller_ads(2547532895, sort="price_low_to_high", country="ro")
    o.filters(14, region_id=2, query="mieszkanie")
    o.categories(parent_id=5)
    o.locations("Warszawa")
    o.suggestions("rower", country="bg")
    o.similar(url="https://www.olx.pl/d/oferta/x-ID1cXcha.html")
    base = "/api/v1/olx/"
    assert seen == [
        (
            base + "search",
            {
                "query": "iphone",
                "page": 2,
                "page_size": 50,
                "sort": "newest",
                "min_price": 500,
                "condition": "used",
                "seller_type": "private",
                "olx_delivery": True,
                "city_id": 17871,
                "distance_km": 30,
            },
            120.0,
        ),
        (
            base + "search",
            {
                "category_id": "84",
                "filters": {"filter_float_year:from": 2018, "filter_enum_rooms": ["two", "three"]},
                "include_promoted": False,
            },
            120.0,
        ),
        (base + "search", {"query": "velosiped", "country": "uz", "language": "uz"}, 120.0),
        (base + "offer", {"offer_id": "1107557408"}, 120.0),
        (base + "offer", {"offer_id": 402863292, "country": "kz", "language": "kk"}, 120.0),
        (base + "seller", {"user_id": "2547532895"}, 120.0),
        (
            base + "seller-ads",
            {"user_id": 2547532895, "country": "ro", "sort": "price_low_to_high"},
            120.0,
        ),
        (base + "filters", {"category_id": 14, "query": "mieszkanie", "region_id": 2}, 120.0),
        (base + "categories", {"parent_id": 5}, 120.0),
        (base + "locations", {"query": "Warszawa"}, 120.0),
        (base + "suggestions", {"query": "rower", "country": "bg"}, 120.0),
        (base + "similar", {"url": "https://www.olx.pl/d/oferta/x-ID1cXcha.html"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        o.search(sort="newest")
    with pytest.raises(ScavioError):
        o.offer(country="pl")
    with pytest.raises(ScavioError):
        o.similar()


def test_kroger_banners_credits_paths_and_wire(monkeypatch):
    """kroger (0.54.0): 8 endpoints on /api/v1/kroger, banner on every one.

    banner is kroger (default), qfc or fred_meyer. search and product 2 credits,
    prices 3, the rest 1. prices needs store_id + upcs; stores takes zip, query
    or store_id; category url or taxonomy_id; coupons store_id or zip. 120 s
    timeout floor everywhere.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "kroger"}
    assert sorted(eps) == sorted(
        ["search", "product", "prices", "stores", "category", "deals", "coupons", "suggestions"]
    )
    credits = {"search": 2, "product": 2, "prices": 3}
    banners = 'Optional[Literal["kroger", "qfc", "fred_meyer"]]'
    for m, ep in eps.items():
        assert ep.credits == credits.get(m, 1), ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/kroger/" + m, ep.key
        assert ep.min_timeout == 120.0, ep.key
        banner = next(p for p in ep.params if p.name == "banner")
        assert banner.annotation == banners, ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    k = client.kroger
    k.search("coffee", banner="qfc")
    k.search("organic milk", page=1)
    k.product(upc="0001111050438", banner="fred_meyer")
    milk_url = "/p/simple-truth-organic-lactose-free-2-reduced-fat-milk-half-gallon/0001111050438"
    hp_url = "https://www.fredmeyer.com/pl/headphones-earbuds-headsets/2900300001"
    k.product(product_url=milk_url)
    k.prices("70500847", ["0001111050438", "0081006334306"], banner="qfc")
    k.stores(zip="97201", banner="fred_meyer", limit=5, include_other_banners=True)
    k.stores(store_id="70100011")
    k.category(taxonomy_id="08190", slug="Import-Beer", banner="qfc")
    k.category(url=hp_url)
    k.deals(banner="qfc")
    k.coupons(store_id="70100011", page=2, category="Dairy", query="milk")
    k.coupons(zip="98101", banner="qfc")
    k.suggestions("almond mi", banner="qfc", store_id="70500847")
    base = "/api/v1/kroger/"
    assert seen == [
        (base + "search", {"query": "coffee", "banner": "qfc"}, 120.0),
        (base + "search", {"query": "organic milk", "page": 1}, 120.0),
        (base + "product", {"upc": "0001111050438", "banner": "fred_meyer"}, 120.0),
        (
            base + "product",
            {"product_url": milk_url},
            120.0,
        ),
        (
            base + "prices",
            {"store_id": "70500847", "upcs": ["0001111050438", "0081006334306"], "banner": "qfc"},
            120.0,
        ),
        (
            base + "stores",
            {"zip": "97201", "banner": "fred_meyer", "limit": 5, "include_other_banners": True},
            120.0,
        ),
        (base + "stores", {"store_id": "70100011"}, 120.0),
        (
            base + "category",
            {"taxonomy_id": "08190", "slug": "Import-Beer", "banner": "qfc"},
            120.0,
        ),
        (base + "category", {"url": hp_url}, 120.0),
        (base + "deals", {"banner": "qfc"}, 120.0),
        (
            base + "coupons",
            {"store_id": "70100011", "page": 2, "category": "Dairy", "query": "milk"},
            120.0,
        ),
        (base + "coupons", {"zip": "98101", "banner": "qfc"}, 120.0),
        (
            base + "suggestions",
            {"query": "almond mi", "banner": "qfc", "store_id": "70500847"},
            120.0,
        ),
    ]
    with pytest.raises(ScavioError):
        k.product(banner="qfc")
    with pytest.raises(ScavioError):
        k.stores(banner="qfc")
    with pytest.raises(ScavioError):
        k.category(slug="Import-Beer")
    with pytest.raises(ScavioError):
        k.coupons(banner="fred_meyer")


def test_publix_credits_paths_and_wire(monkeypatch):
    """publix (0.55.0): 11 endpoints on /api/v1/publix, 1 credit each.

    store_id (a Publix store number, str or int) is required on every price
    endpoint and optional on categories, suggestions and stores. category takes
    category_url or category_id; stores takes zip, city (+ state) or store_id.
    120 s timeout floor everywhere.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "publix"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "category",
            "categories",
            "weekly_ad",
            "extra_savings",
            "coupons",
            "savings_search",
            "order_ahead",
            "stores",
            "suggestions",
        ]
    )
    optional_store = {"categories", "suggestions", "stores"}
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.credits_note is None, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/publix/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        store = next(p for p in ep.params if p.name == "store_id")
        assert store.required == (m not in optional_store), ep.key
        assert "Union[str, int]" in store.annotation, ep.key
    sort = next(p for p in eps["search"].params if p.name == "sort")
    assert sort.annotation == (
        'Optional[Literal["relevance", "featured", "name_asc", "name_desc", "popularity", '
        '"savings_amount", "most_viewed"]]'
    )

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    px = client.publix
    cat_id = "6772da29-55bf-4051-83d5-104d73ae9a96"
    px.search("chicken", "1614", sort="savings_amount", on_sale=True, page=2)
    px.search("chicken", 1453, bogo=True, brand="Tyson")
    px.product("90355", 1825)
    px.category("1825", category_id=cat_id, sort="name_asc")
    px.category(1614, category_url="https://www.publix.com/c/chicken/" + cat_id)
    px.categories()
    px.categories(store_id="1453", parent_id=cat_id)
    px.weekly_ad("1614", department="Produce", bogo_only=True, query="apple")
    px.extra_savings(1614)
    px.coupons("1453")
    px.savings_search("coffee", "1614")
    px.order_ahead("1825", section="all", page=2)
    px.stores(zip="33101", limit=5, radius_miles=100)
    px.stores(city="Nashville", state="TN")
    px.stores(store_id=1825)
    px.suggestions("chick", store_id="1614")
    base = "/api/v1/publix/"
    assert seen == [
        (
            base + "search",
            {
                "query": "chicken",
                "store_id": "1614",
                "page": 2,
                "sort": "savings_amount",
                "on_sale": True,
            },
            120.0,
        ),
        (
            base + "search",
            {"query": "chicken", "store_id": 1453, "bogo": True, "brand": "Tyson"},
            120.0,
        ),
        (base + "product", {"item_code": "90355", "store_id": 1825}, 120.0),
        (
            base + "category",
            {"store_id": "1825", "category_id": cat_id, "sort": "name_asc"},
            120.0,
        ),
        (
            base + "category",
            {"store_id": 1614, "category_url": "https://www.publix.com/c/chicken/" + cat_id},
            120.0,
        ),
        (base + "categories", {}, 120.0),
        (base + "categories", {"store_id": "1453", "parent_id": cat_id}, 120.0),
        (
            base + "weekly-ad",
            {"store_id": "1614", "department": "Produce", "bogo_only": True, "query": "apple"},
            120.0,
        ),
        (base + "extra-savings", {"store_id": 1614}, 120.0),
        (base + "coupons", {"store_id": "1453"}, 120.0),
        (base + "savings-search", {"query": "coffee", "store_id": "1614"}, 120.0),
        (base + "order-ahead", {"store_id": "1825", "section": "all", "page": 2}, 120.0),
        (base + "stores", {"zip": "33101", "limit": 5, "radius_miles": 100}, 120.0),
        (base + "stores", {"city": "Nashville", "state": "TN"}, 120.0),
        (base + "stores", {"store_id": 1825}, 120.0),
        (base + "suggestions", {"query": "chick", "store_id": "1614"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        px.category("1825", sort="name_asc")
    with pytest.raises(ScavioError):
        px.stores(limit=5)


def test_ikea_credits_paths_and_wire(monkeypatch):
    """ikea (0.56.0): 12 endpoints on /api/v1/ikea, 1 credit each; compare is priced per
    market that answered (credits_note).

    product and reviews take item_no or url (180 s timeout floor: a product page can take
    up to about 100 s); category takes category_id or url. country / language are plain
    strings (55 markets); island is a literal for country es_islands.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "ikea"}
    assert sorted(eps) == sorted(
        [
            "search",
            "product",
            "reviews",
            "category",
            "categories",
            "deals",
            "suggestions",
            "stores",
            "stock",
            "items",
            "compare",
            "as_is",
        ]
    )
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/ikea/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == (180.0 if m in ("product", "reviews") else 120.0), ep.key
        assert (ep.credits_note is not None) == (m == "compare"), ep.key
    assert "per market" in eps["compare"].credits_note
    sort = next(p for p in eps["search"].params if p.name == "sort")
    assert sort.annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc", "newest", "rating", '
        '"name_asc", "most_popular"]]'
    )

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ik = client.ikea
    ik.search("kallax", country="de", language="en", sort="price_asc", page=2, color="10156")
    ik.search("billy", country="es_islands", island="tenerife")
    ik.search("sofa", store_id="399", availability="in_store", filters={"f-materials": ["47350"]})
    ik.product(item_no="80275887", country="fr")
    ik.product(url="https://www.ikea.com/de/de/p/kallax-regal-weiss-80275887/")
    ik.reviews(item_no=80275887, country="de")
    ik.category(category_id="10382", new_only=True)
    ik.categories(country="ca", language="fr", parent_id="fu003")
    ik.deals("new_lower_price", country="gb", page_size=48)
    ik.suggestions("sof")
    ik.stores(country="se", lat=59.33, lng=18.06, limit=5)
    ik.stock(["20522046", "20631663"], "399", zip="91502")
    ik.items("80275887,00263850", country="de")
    ik.compare("80275887", ["de", "fr", "se"])
    ik.as_is(257, page=2, page_size=48)
    base = "/api/v1/ikea/"
    assert seen == [
        (
            base + "search",
            {
                "query": "kallax",
                "country": "de",
                "language": "en",
                "page": 2,
                "sort": "price_asc",
                "color": "10156",
            },
            120.0,
        ),
        (
            base + "search",
            {"query": "billy", "country": "es_islands", "island": "tenerife"},
            120.0,
        ),
        (
            base + "search",
            {
                "query": "sofa",
                "store_id": "399",
                "availability": "in_store",
                "filters": {"f-materials": ["47350"]},
            },
            120.0,
        ),
        (base + "product", {"item_no": "80275887", "country": "fr"}, 180.0),
        (
            base + "product",
            {"url": "https://www.ikea.com/de/de/p/kallax-regal-weiss-80275887/"},
            180.0,
        ),
        (base + "reviews", {"item_no": 80275887, "country": "de"}, 180.0),
        (base + "category", {"category_id": "10382", "new_only": True}, 120.0),
        (base + "categories", {"country": "ca", "language": "fr", "parent_id": "fu003"}, 120.0),
        (base + "deals", {"type": "new_lower_price", "country": "gb", "page_size": 48}, 120.0),
        (base + "suggestions", {"query": "sof"}, 120.0),
        (base + "stores", {"country": "se", "lat": 59.33, "lng": 18.06, "limit": 5}, 120.0),
        (
            base + "stock",
            {"item_nos": ["20522046", "20631663"], "store_id": "399", "zip": "91502"},
            120.0,
        ),
        (base + "items", {"item_nos": "80275887,00263850", "country": "de"}, 120.0),
        (base + "compare", {"item_no": "80275887", "countries": ["de", "fr", "se"]}, 120.0),
        (base + "as-is", {"store_id": 257, "page": 2, "page_size": 48}, 120.0),
    ]
    with pytest.raises(ScavioError):
        ik.product(country="de")
    with pytest.raises(ScavioError):
        ik.category(sort="newest")


def test_wayfair_credits_paths_and_wire(monkeypatch):
    """wayfair (0.57.0): 4 endpoints on /api/v1/wayfair, 1 credit each, 120 s timeout floor.

    product takes sku or url; category takes category_id or category_url. country is a
    literal (us, ca, gb, ie), language en / fr (ca), site the US banners; min_rating is an
    int literal (1, 3, 4, 5).
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "wayfair"}
    assert sorted(eps) == ["category", "deals", "product", "search"]
    for m, ep in eps.items():
        assert ep.credits == 1, ep.key
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/wayfair/" + m, ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits_note is None, ep.key
    params = {p.name: p for p in eps["search"].params}
    assert params["country"].annotation == 'Optional[Literal["us", "ca", "gb", "ie"]]'
    assert params["min_rating"].annotation == "Optional[Literal[1, 3, 4, 5]]"
    assert params["sort"].annotation == (
        'Optional[Literal["recommended", "price_asc", "price_desc", "rating"]]'
    )
    assert "site" not in {p.name for p in eps["deals"].params}

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    wf = client.wayfair
    wf.search("office chair", sort="price_asc", on_sale=True, brand=[44308], min_rating=4)
    wf.search("sofa", country="ca", language="fr", page=2, filters={"2471": ["274623"]})
    wf.search("velvet sofa", site="perigold", price_min=100, price_max=400.5)
    wf.product(sku="W005006988", zip="10001")
    wf.product(sku="W005006988", option_id="1820607042")
    wf.product(url="https://www.wayfair.ca/fr/mobilier/pdp/x-c115423787.html")
    wf.category(category_id=413892, sort="rating", in_stock=True)
    wf.category(category_url="https://www.wayfair.co.uk/furniture/sb0/sofas-c1772837.html")
    wf.deals(country="gb")
    base = "/api/v1/wayfair/"
    assert seen == [
        (
            base + "search",
            {
                "query": "office chair",
                "sort": "price_asc",
                "on_sale": True,
                "brand": [44308],
                "min_rating": 4,
            },
            120.0,
        ),
        (
            base + "search",
            {
                "query": "sofa",
                "country": "ca",
                "language": "fr",
                "page": 2,
                "filters": {"2471": ["274623"]},
            },
            120.0,
        ),
        (
            base + "search",
            {"query": "velvet sofa", "site": "perigold", "price_min": 100, "price_max": 400.5},
            120.0,
        ),
        (base + "product", {"sku": "W005006988", "zip": "10001"}, 120.0),
        (base + "product", {"sku": "W005006988", "option_id": "1820607042"}, 120.0),
        (
            base + "product",
            {"url": "https://www.wayfair.ca/fr/mobilier/pdp/x-c115423787.html"},
            120.0,
        ),
        (base + "category", {"category_id": 413892, "sort": "rating", "in_stock": True}, 120.0),
        (
            base + "category",
            {"category_url": "https://www.wayfair.co.uk/furniture/sb0/sofas-c1772837.html"},
            120.0,
        ),
        (base + "deals", {"country": "gb"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        wf.product(zip="10001")
    with pytest.raises(ScavioError):
        wf.category(sort="price_asc")


def test_ashley_credits_paths_and_wire(monkeypatch):
    """ashley (0.58.0): 6 endpoints on /api/v1/ashley, 120 s timeout floor.

    search and product serve us and the licensee storefronts (ca, mx, ph, sa, tr) and are
    market-priced (credits_note; floor 1); category, deals, stores and store are us only at
    2 credits and take no country. product takes sku, handle or url; category takes path or
    category_url; store takes store_id or url; stores takes lat and lng.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "ashley"}
    assert sorted(eps) == ["category", "deals", "product", "search", "store", "stores"]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/ashley/" + m, ep.key
        assert ep.min_timeout == 120.0, ep.key
    for m in ("search", "product"):
        assert eps[m].credits == 1, m
        assert eps[m].credits_note == (
            "Costs 2 credits on us (the default) and mx, 1 credit on ca, ph, sa and tr."
        )
        params = {p.name: p for p in eps[m].params}
        assert params["country"].annotation == (
            'Optional[Literal["us", "ca", "mx", "ph", "sa", "tr"]]'
        )
    for m in ("category", "deals", "stores", "store"):
        assert eps[m].credits == 2, m
        assert eps[m].credits_note is None, m
        assert "country" not in {p.name for p in eps[m].params}, m
    grid = {p.name: p for p in eps["category"].params}
    assert grid["sort"].annotation == (
        'Optional[Literal["best_sellers", "price_asc", "price_desc", "newest", "rating", "name"]]'
    )
    assert {p.name: p for p in eps["stores"].params}["radius"].annotation == (
        "Optional[Literal[10, 25, 50, 100]]"
    )
    assert {p.name: p for p in eps["deals"].params}["event"].annotation == (
        'Optional[Literal["black_friday", "clearance", "hot_buys"]]'
    )

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ash = client.ashley
    ash.search("sofa", sort="price_asc", page=2)
    ash.search("koltuk", country="tr")
    ash.product(sku="5950418")
    ash.product(handle="aviemore-sofa", country="ca")
    ash.product(url="https://store.ashleyfurniture.com.mx/products/cashton-sofa")
    ash.category(path="furniture/living-room/sofas", filters={"facetUpholsteryDesign": "Chaise"})
    ash.category(
        category_url="https://www.ashleyfurniture.com/c/furniture/living-room/sofas/",
        price_min=200,
        price_max=899.99,
    )
    ash.deals(event="clearance", sort="price_desc")
    ash.deals()
    ash.stores(40.7506, -73.9972, radius=25)
    ash.store(store_id="us/wisconsin/greenfield/4771-s-27th-st/luxe")
    base = "/api/v1/ashley/"
    assert seen == [
        (base + "search", {"query": "sofa", "sort": "price_asc", "page": 2}, 120.0),
        (base + "search", {"query": "koltuk", "country": "tr"}, 120.0),
        (base + "product", {"sku": "5950418"}, 120.0),
        (base + "product", {"handle": "aviemore-sofa", "country": "ca"}, 120.0),
        (
            base + "product",
            {"url": "https://store.ashleyfurniture.com.mx/products/cashton-sofa"},
            120.0,
        ),
        (
            base + "category",
            {
                "path": "furniture/living-room/sofas",
                "filters": {"facetUpholsteryDesign": "Chaise"},
            },
            120.0,
        ),
        (
            base + "category",
            {
                "category_url": "https://www.ashleyfurniture.com/c/furniture/living-room/sofas/",
                "price_min": 200,
                "price_max": 899.99,
            },
            120.0,
        ),
        (base + "deals", {"event": "clearance", "sort": "price_desc"}, 120.0),
        (base + "deals", {}, 120.0),
        (base + "stores", {"lat": 40.7506, "lng": -73.9972, "radius": 25}, 120.0),
        (base + "store", {"store_id": "us/wisconsin/greenfield/4771-s-27th-st/luxe"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        ash.product(country="mx")
    with pytest.raises(ScavioError):
        ash.category(sort="newest")
    with pytest.raises(ScavioError):
        ash.store()


def test_maisonsdumonde_credits_paths_and_wire(monkeypatch):
    """maisonsdumonde (0.59.0): 9 endpoints on /api/v1/maisonsdumonde, 1 credit each, 120 s floor.

    search, product, category, deals and reviews serve all 9 markets; stores, store and
    availability serve fr, be, de, es, it, pt, ch (no store finder on nl / lu); seller serves
    the marketplace markets fr, de, es, it. product takes id or url; category takes category
    or category_url; store takes store_id or url; seller takes seller_id or url.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "maisonsdumonde"}
    assert sorted(eps) == [
        "availability", "category", "deals", "product", "reviews", "search", "seller", "store",
        "stores",
    ]
    all_markets = 'Optional[Literal["fr", "be", "lu", "nl", "de", "es", "it", "pt", "ch"]]'
    store_markets = 'Optional[Literal["fr", "be", "de", "es", "it", "pt", "ch"]]'
    marketplace = 'Optional[Literal["fr", "de", "es", "it"]]'
    expected_country = {
        "search": all_markets, "product": all_markets, "category": all_markets,
        "deals": all_markets, "reviews": all_markets, "stores": store_markets,
        "store": store_markets, "availability": store_markets, "seller": marketplace,
    }
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/maisonsdumonde/" + m, ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        params = {p.name: p for p in ep.params}
        assert params["country"].annotation == expected_country[m], m
        assert params["language"].annotation == (
            'Optional[Literal["fr", "nl", "de", "es", "it", "pt"]]'
        ), m
    grid = {p.name: p for p in eps["search"].params}
    assert grid["sort"].annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc", "rating"]]'
    )
    assert grid["min_discount"].annotation == "Optional[Literal[20, 30, 40, 50]]"
    assert grid["min_rating"].annotation == "Optional[Literal[3, 4, 5]]"
    assert grid["sold_by"].annotation == 'Optional[Literal["mdm"]]'
    assert {p.name: p for p in eps["deals"].params}["event"].annotation == (
        'Optional[Literal["black_friday", "second_chance"]]'
    )
    assert {p.name: p for p in eps["reviews"].params}["sort"].annotation == (
        'Optional[Literal["newest", "rating_desc", "rating_asc"]]'
    )

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    mdm = client.maisonsdumonde
    mdm.search("table")
    mdm.search(
        "couchtisch",
        country="de",
        sort="price_asc",
        page=2,
        min_discount=30,
        color=["n9660c0e9e5310638a19012509703a483cebdb2b"],
        filters={"nbs": ["CAPACITY_2_places"]},
    )
    mdm.search("chaise", sold_by="mdm", on_sale=True, seller="BESTMOBILIER")
    mdm.product(id="204172", country="ch", language="de")
    mdm.product(url="https://www.maisonsdumonde.com/BE/nl/p/x-186339.htm")
    mdm.category(category="canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f", min_rating=4)
    mdm.deals()
    mdm.deals(event="second_chance", sort="price_desc")
    mdm.reviews("186339", sort="rating_asc", cursor="eyJzb3J0IjpbMV19", limit=30)
    mdm.stores("75011", limit=3)
    mdm.store(store_id="41")
    mdm.availability("204172", "125", country="fr")
    mdm.seller(seller_id="2066", page=2)
    base = "/api/v1/maisonsdumonde/"
    assert seen == [
        (base + "search", {"query": "table"}, 120.0),
        (
            base + "search",
            {
                "query": "couchtisch",
                "country": "de",
                "page": 2,
                "sort": "price_asc",
                "min_discount": 30,
                "color": ["n9660c0e9e5310638a19012509703a483cebdb2b"],
                "filters": {"nbs": ["CAPACITY_2_places"]},
            },
            120.0,
        ),
        (
            base + "search",
            {"query": "chaise", "on_sale": True, "seller": "BESTMOBILIER", "sold_by": "mdm"},
            120.0,
        ),
        (base + "product", {"id": "204172", "country": "ch", "language": "de"}, 120.0),
        (base + "product", {"url": "https://www.maisonsdumonde.com/BE/nl/p/x-186339.htm"}, 120.0),
        (
            base + "category",
            {"category": "canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f", "min_rating": 4},
            120.0,
        ),
        (base + "deals", {}, 120.0),
        (base + "deals", {"event": "second_chance", "sort": "price_desc"}, 120.0),
        (
            base + "reviews",
            {"id": "186339", "sort": "rating_asc", "cursor": "eyJzb3J0IjpbMV19", "limit": 30},
            120.0,
        ),
        (base + "stores", {"postcode": "75011", "limit": 3}, 120.0),
        (base + "store", {"store_id": "41"}, 120.0),
        (base + "availability", {"id": "204172", "store_id": "125", "country": "fr"}, 120.0),
        (base + "seller", {"seller_id": "2066", "page": 2}, 120.0),
    ]
    with pytest.raises(ScavioError):
        mdm.product(country="fr")
    with pytest.raises(ScavioError):
        mdm.category(sort="rating")
    with pytest.raises(ScavioError):
        mdm.store()
    with pytest.raises(ScavioError):
        mdm.seller(country="de")


def test_trendyol_credits_paths_and_wire(monkeypatch):
    """trendyol (0.60.0): 12 endpoints on /api/v1/trendyol, 1 credit each, 120 s floor.

    35 markets via country + language; deals and coupons serve tr only; rankings is not on the
    15 English-language EU storefronts. product, reviews, questions, coupons and delivery take
    content_id or url; category takes category_id or url; brand brand_id or url; seller
    seller_id or url.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "trendyol"}
    assert sorted(eps) == [
        "brand", "category", "coupons", "deals", "delivery", "product", "questions", "rankings",
        "reviews", "search", "seller", "suggestions",
    ]
    all_markets = (
        'Optional[Literal["tr", "de", "at", "fr", "be", "hr", "dk", "ee", "fi", "it", "lv", '
        '"lt", "nl", "pt", "si", "es", "se", "lu", "bg", "gr", "cz", "hu", "pl", "ro", "sk", '
        '"rs", "ua", "md", "ae", "sa", "qa", "kw", "om", "bh", "az"]]'
    )
    ranking_markets = (
        'Optional[Literal["tr", "de", "at", "bg", "gr", "cz", "hu", "pl", "ro", "sk", "rs", '
        '"ua", "md", "ae", "sa", "qa", "kw", "om", "bh", "az"]]'
    )
    tr_only = 'Optional[Literal["tr"]]'
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/trendyol/" + m, ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        params = {p.name: p for p in ep.params}
        expected = {"deals": tr_only, "coupons": tr_only, "rankings": ranking_markets}
        assert params["country"].annotation == expected.get(m, all_markets), m
        assert params["language"].annotation == (
            'Optional[Literal["tr", "en", "ar", "de", "bg", "el", "cs", "hu", "pl", "ro", "sk", '
            '"sr", "uk"]]'
        ), m
    grid = {p.name: p for p in eps["search"].params}
    assert grid["sort"].annotation == (
        'Optional[Literal["recommended", "price_asc", "price_desc", "newest", "best_seller", '
        '"most_favourited", "most_rated"]]'
    )
    assert grid["seller_type"].annotation == (
        'Optional[Literal["official", "authorized", "successful"]]'
    )
    assert grid["brand_id"].annotation == "Optional[Union[str, int, list[Union[str, int]]]]"
    assert not any(p.doc.startswith("1 to 10 category") for p in eps["category"].params)
    assert {p.name: p for p in eps["rankings"].params}["category_id"].required
    assert {p.name: p for p in eps["deals"].params}["type"].annotation == (
        'Optional[Literal["flash", "super_discounts"]]'
    )

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ty = client.trendyol
    ty.search("telefon")
    ty.search(
        "kulaklik",
        country="tr",
        language="en",
        page=2,
        sort="price_asc",
        brand_id=[794],
        price_max=5000,
        min_rating=4.5,
        lowest_price_days=30,
        seller_type="official",
        filters={"attr": ["348|1"]},
        include_facets=True,
    )
    ty.product(content_id=975557855, include_description=True)
    ty.product(url="https://www.trendyol.com/x/y-p-975557855", country="de")
    ty.category(category_id="103498", sort="price_desc")
    ty.brand(brand_id=794, country="ro")
    ty.reviews(
        content_id="975557855", page=2, page_size=50, sort="newest", rating=5, with_media=True
    )
    ty.questions(content_id="975557855", country="ae", language="ar")
    ty.seller(seller_id=4473, include_products=True, query="kilif")
    ty.deals(type="super_discounts", sort="price_asc")
    ty.coupons(content_id="780343279", seller_id="1188867")
    ty.rankings(56, ranking="most_favourited", page=2)
    ty.suggestions("iph", country="sa")
    ty.delivery(content_id="975557855", city_id=133, district_id=54)
    base = "/api/v1/trendyol/"
    assert seen == [
        (base + "search", {"query": "telefon"}, 120.0),
        (
            base + "search",
            {
                "query": "kulaklik",
                "country": "tr",
                "language": "en",
                "page": 2,
                "sort": "price_asc",
                "brand_id": [794],
                "price_max": 5000,
                "min_rating": 4.5,
                "lowest_price_days": 30,
                "seller_type": "official",
                "filters": {"attr": ["348|1"]},
                "include_facets": True,
            },
            120.0,
        ),
        (base + "product", {"content_id": 975557855, "include_description": True}, 120.0),
        (
            base + "product",
            {"url": "https://www.trendyol.com/x/y-p-975557855", "country": "de"},
            120.0,
        ),
        (base + "category", {"category_id": "103498", "sort": "price_desc"}, 120.0),
        (base + "brand", {"brand_id": 794, "country": "ro"}, 120.0),
        (
            base + "reviews",
            {
                "content_id": "975557855",
                "page": 2,
                "page_size": 50,
                "sort": "newest",
                "rating": 5,
                "with_media": True,
            },
            120.0,
        ),
        (
            base + "questions",
            {"content_id": "975557855", "country": "ae", "language": "ar"},
            120.0,
        ),
        (
            base + "seller",
            {"seller_id": 4473, "include_products": True, "query": "kilif"},
            120.0,
        ),
        (base + "deals", {"type": "super_discounts", "sort": "price_asc"}, 120.0),
        (base + "coupons", {"content_id": "780343279", "seller_id": "1188867"}, 120.0),
        (base + "rankings", {"category_id": 56, "ranking": "most_favourited", "page": 2}, 120.0),
        (base + "suggestions", {"query": "iph", "country": "sa"}, 120.0),
        (
            base + "delivery",
            {"content_id": "975557855", "city_id": 133, "district_id": 54},
            120.0,
        ),
    ]
    with pytest.raises(ScavioError):
        ty.product(country="tr")
    with pytest.raises(ScavioError):
        ty.category(sort="newest")
    with pytest.raises(ScavioError):
        ty.brand()
    with pytest.raises(ScavioError):
        ty.seller(include_products=True)
    with pytest.raises(ScavioError):
        ty.coupons(seller_id="1188867")
    with pytest.raises(ScavioError):
        ty.delivery(city_id=133)


def test_nintendo_credits_paths_and_wire(monkeypatch):
    """nintendo (0.61.0): 6 endpoints on /api/v1/nintendo, 1 credit each, 120 s floor.

    46 countries via country + language: search, product, deals, releases and dlc on the 42
    catalog markets; prices also on kr, hk, tw and il. product and dlc take nsuid, url or slug;
    prices takes 1 to 50 ids.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "nintendo"}
    assert sorted(eps) == ["deals", "dlc", "prices", "product", "releases", "search"]
    catalog = (
        '"us", "ca", "mx", "br", "ar", "cl", "co", "pe", "gb", "ie", "de", "at", "ch", "fr", '
        '"be", "nl", "lu", "it", "es", "pt", "au", "nz", "za", "pl", "cz", "se", "no", "dk", '
        '"fi", "sk", "hu", "ro", "bg", "gr", "hr", "si", "ee", "lv", "lt", "mt", "cy", "jp"'
    )
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/nintendo/" + m, ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        params = {p.name: p for p in ep.params}
        expected = (
            "Optional[Literal[" + catalog + ', "kr", "hk", "tw", "il"]]'
            if m == "prices"
            else "Optional[Literal[" + catalog + "]]"
        )
        assert params["country"].annotation == expected, m
        assert params["language"].annotation == (
            'Optional[Literal["en", "fr", "es", "pt", "de", "it", "nl", "ja", "ko", "zh"]]'
        ), m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "newest", "price_asc", "price_desc", "title", "discount"]]'
    )
    assert search["type"].annotation == 'Optional[Literal["game", "dlc", "bundle", "all"]]'
    assert search["price_min"].annotation == "Optional[float]"
    assert {p.name: p for p in eps["deals"].params}["sort"].annotation == (
        'Optional[Literal["featured", "discount", "price_asc", "newest", "ending_soon"]]'
    )
    assert {p.name: p for p in eps["releases"].params}["type"].annotation == (
        'Optional[Literal["new", "upcoming"]]'
    )
    assert {p.name: p for p in eps["prices"].params}["ids"].required
    assert eps["product"].one_of == (("nsuid", "url", "slug"),)
    assert eps["dlc"].one_of == (("nsuid", "url", "slug"),)

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    nd = client.nintendo
    nd.search("mario")
    nd.search(
        "zelda",
        country="de",
        language="de",
        page=2,
        page_size=50,
        sort="price_asc",
        platform="switch_2",
        on_sale=True,
        price_max=30,
        genre="RPG",
        players=2,
        has_demo=True,
        type="all",
    )
    nd.product(nsuid="70010000095431")
    nd.product(slug="mario-kart-world-switch-2", country="ca", language="fr")
    nd.prices("70010000095431,70010000063714,70010000094234")
    nd.prices(["70010000063716", 70010000084605], country="kr")
    nd.deals()
    nd.deals(country="us", sort="ending_soon", sale="square-enix")
    nd.releases(country="gb")
    nd.releases(country="jp", type="upcoming", platform="switch_2", page=2, page_size=10)
    nd.dlc(slug="super-smash-bros-ultimate-switch")
    nd.dlc(nsuid=70010000012332, country="mx")
    base = "/api/v1/nintendo/"
    assert seen == [
        (base + "search", {"query": "mario"}, 120.0),
        (
            base + "search",
            {
                "query": "zelda",
                "country": "de",
                "language": "de",
                "page": 2,
                "page_size": 50,
                "sort": "price_asc",
                "platform": "switch_2",
                "on_sale": True,
                "price_max": 30,
                "genre": "RPG",
                "players": 2,
                "has_demo": True,
                "type": "all",
            },
            120.0,
        ),
        (base + "product", {"nsuid": "70010000095431"}, 120.0),
        (
            base + "product",
            {"slug": "mario-kart-world-switch-2", "country": "ca", "language": "fr"},
            120.0,
        ),
        (base + "prices", {"ids": "70010000095431,70010000063714,70010000094234"}, 120.0),
        (
            base + "prices",
            {"ids": ["70010000063716", 70010000084605], "country": "kr"},
            120.0,
        ),
        (base + "deals", {}, 120.0),
        (
            base + "deals",
            {"country": "us", "sort": "ending_soon", "sale": "square-enix"},
            120.0,
        ),
        (base + "releases", {"country": "gb"}, 120.0),
        (
            base + "releases",
            {
                "country": "jp",
                "type": "upcoming",
                "platform": "switch_2",
                "page": 2,
                "page_size": 10,
            },
            120.0,
        ),
        (base + "dlc", {"slug": "super-smash-bros-ultimate-switch"}, 120.0),
        (base + "dlc", {"nsuid": 70010000012332, "country": "mx"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        nd.product(country="us")
    with pytest.raises(ScavioError):
        nd.dlc()


def test_hm_credits_paths_and_wire(monkeypatch):
    """hm (0.62.0): 9 endpoints on /api/v1/hm, product 2 credits, the rest 1, 120 s floor.

    47 countries via country + language: product not on mo, tw or the shared EU store
    countries; stores not on mo. product and production take article_code or url; stock takes
    article_code or product_code.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "hm"}
    assert sorted(eps) == [
        "category", "deals", "new_arrivals", "product", "production", "search", "stock",
        "stores", "suggestions",
    ]
    every = (
        '"us", "ca", "mx", "gb", "ie", "de", "at", "ch", "fr", "be", "nl", "it", "es", "pt", '
        '"se", "fi", "dk", "no", "pl", "cz", "sk", "hu", "ro", "bg", "gr", "rs", "tr", "ua", '
        '"il", "hk", "mo", "tw", "jp", "kr", "in", "my", "ph", "sg", "vn", "au", "hr", "cy", '
        '"ee", "lv", "lt", "lu", "si"'
    )
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/hm/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits == (2 if m == "product" else 1) and ep.credits_note is None, ep.key
        params = {p.name: p for p in ep.params}
        country = params["country"].annotation
        if m == "product":
            for cc in ("mo", "tw", "hr", "cy", "ee", "lv", "lt", "lu", "si"):
                assert f'"{cc}"' not in country, cc
            assert country.count('"') // 2 == 38
        elif m == "stores":
            assert '"mo"' not in country
            assert country.count('"') // 2 == 46
        else:
            assert country == "Optional[Literal[" + every + "]]", m
        if m not in ("stores", "production"):
            assert params["language"].annotation.count('"') // 2 == 26, m
    grid = {p.name: p for p in eps["category"].params}
    assert grid["category"].required
    assert grid["sort"].annotation == (
        'Optional[Literal["relevance", "newest", "price_asc", "price_desc"]]'
    )
    assert grid["color"].annotation == "Optional[Union[str, list[str]]]"
    assert {p.name: p for p in eps["deals"].params}["department"].annotation == (
        'Optional[Literal["women", "men", "kids", "baby", "home"]]'
    )
    assert "on_sale" not in {p.name for p in eps["deals"].params}
    assert eps["product"].one_of == (("article_code", "url"),)
    assert eps["production"].one_of == (("article_code", "url"),)
    assert eps["stock"].one_of == (("article_code", "product_code"),)
    assert {p.name: p for p in eps["stores"].params}["lat"].annotation == "Optional[float]"

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    hm = client.hm
    hm.search("jeans")
    hm.search(
        "jeans",
        country="de",
        language="de",
        department="women",
        page=2,
        page_size=72,
        sort="price_asc",
        color=["schwarz_000000", "blau_0000ff"],
        on_sale=True,
    )
    hm.product(article_code="1310382004")
    hm.product(article_code="1347936009", country="ca", language="fr")
    hm.stock(product_code="1310382", country="mo")
    hm.stores(city="New York")
    hm.stores(country="gb", lat=51.5, lng=-0.12, radius_km=5, page_size=50)
    hm.category("ladies_dresses", country="gb")
    hm.deals(country="gb", department="men")
    hm.new_arrivals(country="se", language="sv")
    hm.suggestions("hoodie")
    hm.production(article_code="1310382004")
    base = "/api/v1/hm/"
    assert seen == [
        (base + "search", {"query": "jeans"}, 120.0),
        (
            base + "search",
            {
                "query": "jeans",
                "country": "de",
                "language": "de",
                "department": "women",
                "page": 2,
                "page_size": 72,
                "sort": "price_asc",
                "color": ["schwarz_000000", "blau_0000ff"],
                "on_sale": True,
            },
            120.0,
        ),
        (base + "product", {"article_code": "1310382004"}, 120.0),
        (
            base + "product",
            {"article_code": "1347936009", "country": "ca", "language": "fr"},
            120.0,
        ),
        (base + "stock", {"product_code": "1310382", "country": "mo"}, 120.0),
        (base + "stores", {"city": "New York"}, 120.0),
        (
            base + "stores",
            {"country": "gb", "lat": 51.5, "lng": -0.12, "radius_km": 5, "page_size": 50},
            120.0,
        ),
        (base + "category", {"category": "ladies_dresses", "country": "gb"}, 120.0),
        (base + "deals", {"country": "gb", "department": "men"}, 120.0),
        (base + "new-arrivals", {"country": "se", "language": "sv"}, 120.0),
        (base + "suggestions", {"query": "hoodie"}, 120.0),
        (base + "production", {"article_code": "1310382004"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        hm.product(country="gb")
    with pytest.raises(ScavioError):
        hm.stock()
    with pytest.raises(ScavioError):
        hm.production()


def test_zara_credits_paths_and_wire(monkeypatch):
    """zara (0.63.0): 12 endpoints on /api/v1/zara, billed what each call spent, 120 s floor.

    102 storefronts via country + language: stores and store_stock not ao or iq; new_arrivals
    not dz; suggestions not ad al am az ba dz mk mo uz xk. search takes query or reference;
    product takes url, product_id (+ slug) or reference; store_stock takes store_ids or lat.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "zara"}
    assert sorted(eps) == [
        "categories", "category", "deals", "materials", "new_arrivals", "prices", "product",
        "search", "stock", "store_stock", "stores", "suggestions",
    ]
    credits = {"deals": 4, "new_arrivals": 4}
    drops = {
        "stores": ("ao", "iq"),
        "store_stock": ("ao", "iq"),
        "new_arrivals": ("dz",),
        "suggestions": ("ad", "al", "am", "az", "ba", "dz", "mk", "mo", "uz", "xk"),
    }
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/zara/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits == credits.get(m, 2), ep.key
        assert ep.credits_note and "cn" in ep.credits_note, ep.key
        params = {p.name: p for p in ep.params}
        if m == "prices":
            countries = params["countries"].annotation
            assert countries.startswith("Optional[list[Literal[")
            assert countries.count('"') // 2 == 102
            continue
        country = params["country"].annotation
        assert country.count('"') // 2 == 102 - len(drops.get(m, ())), m
        for cc in drops.get(m, ()):
            assert f'"{cc}"' not in country, (m, cc)
        assert '"uk"' not in country and '"by"' not in country, m
        if m != "stock":
            assert params["language"].annotation.count('"') // 2 == 45, m
            assert '"zh-Hant"' in params["language"].annotation, m
        else:
            assert "language" not in params
    assert eps["search"].one_of == (("query", "reference"),)
    assert eps["product"].one_of == (("url", "product_id", "reference"),)
    assert eps["store_stock"].one_of == (("store_ids", "lat"),)
    assert {p.name: p for p in eps["stores"].params}["lat"].annotation == "float"
    assert {p.name: p for p in eps["store_stock"].params}["store_ids"].annotation == (
        "Optional[list[str]]"
    )
    assert {p.name: p for p in eps["deals"].params}["section"].annotation == (
        'Optional[Literal["woman", "man", "girl", "boy"]]'
    )
    assert {p.name: p for p in eps["categories"].params}["section"].annotation == (
        'Optional[Literal["woman", "man", "kids", "home", "beauty"]]'
    )
    assert {p.name: p for p in eps["search"].params}["sort"].annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc"]]'
    )

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    zara = client.zara
    zara.search("blazer")
    zara.search(reference="4591/381", country="jp")
    zara.search(
        "jeans",
        country="es",
        language="es",
        section="woman",
        page=2,
        page_size=96,
        sort="price_asc",
        price_min=10,
        price_max=50.5,
    )
    zara.product(product_id="588478514", slug="trf-low-rise-wide-leg-jeans-p08727223")
    zara.product(reference="4591/381", country="hk", language="zh-Hant")
    zara.materials("588478514", country="fr")
    zara.stock("588478514")
    zara.stores(40.7128, -74.006)
    zara.store_stock("553306790", store_ids=["3904", "3862"])
    zara.store_stock("553306790", lat=35.6762, lng=139.6503, country="jp")
    zara.categories(section="woman")
    zara.category("2420896", on_sale=True)
    zara.deals(country="fr", section="man")
    zara.new_arrivals(country="gb", section="woman")
    zara.prices("4591/381", countries=["us", "gb", "cn"])
    zara.suggestions("jea")
    base = "/api/v1/zara/"
    assert seen == [
        (base + "search", {"query": "blazer"}, 120.0),
        (base + "search", {"reference": "4591/381", "country": "jp"}, 120.0),
        (
            base + "search",
            {
                "query": "jeans",
                "country": "es",
                "language": "es",
                "section": "woman",
                "page": 2,
                "page_size": 96,
                "sort": "price_asc",
                "price_min": 10,
                "price_max": 50.5,
            },
            120.0,
        ),
        (
            base + "product",
            {"product_id": "588478514", "slug": "trf-low-rise-wide-leg-jeans-p08727223"},
            120.0,
        ),
        (
            base + "product",
            {"reference": "4591/381", "country": "hk", "language": "zh-Hant"},
            120.0,
        ),
        (base + "materials", {"product_id": "588478514", "country": "fr"}, 120.0),
        (base + "stock", {"product_id": "588478514"}, 120.0),
        (base + "stores", {"lat": 40.7128, "lng": -74.006}, 120.0),
        (base + "store-stock", {"product_id": "553306790", "store_ids": ["3904", "3862"]}, 120.0),
        (
            base + "store-stock",
            {"product_id": "553306790", "lat": 35.6762, "lng": 139.6503, "country": "jp"},
            120.0,
        ),
        (base + "categories", {"section": "woman"}, 120.0),
        (base + "category", {"category_id": "2420896", "on_sale": True}, 120.0),
        (base + "deals", {"country": "fr", "section": "man"}, 120.0),
        (base + "new-arrivals", {"country": "gb", "section": "woman"}, 120.0),
        (base + "prices", {"reference": "4591/381", "countries": ["us", "gb", "cn"]}, 120.0),
        (base + "suggestions", {"query": "jea"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        zara.search()
    with pytest.raises(ScavioError):
        zara.product(country="gb")
    with pytest.raises(ScavioError):
        zara.store_stock("553306790")


def test_asos_credits_paths_and_wire(monkeypatch):
    """asos (0.64.0): 11 endpoints on /api/v1/asos, 1 credit each, 120 s floor.

    235 countries via country (default gb) + currency (245 combinations); suggestions not on
    pl; ru, by and uk are not in any country literal. product takes product_id, group_id or
    url; stock takes up to 100 product ids as a list or a comma-separated string.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "asos"}
    assert sorted(eps) == [
        "brands", "categories", "category", "deals", "markets", "new_arrivals", "product",
        "reviews", "search", "stock", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/asos/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 120.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        params = {p.name: p for p in ep.params}
        country = params["country"].annotation
        assert country.count('"') // 2 == (234 if m == "suggestions" else 235), m
        for cc in ("ru", "by", "uk"):
            assert f'"{cc}"' not in country, (m, cc)
        assert ('"pl"' in country) == (m != "suggestions"), m
        assert params["currency"].annotation.count('"') // 2 == 18, m
    assert eps["product"].one_of == (("product_id", "group_id", "url"),)
    assert {p.name: p for p in eps["stock"].params}["product_ids"].annotation == (
        "Union[str, list[str]]"
    )
    assert {p.name: p for p in eps["search"].params}["sort"].annotation == (
        'Optional[Literal["relevance", "newest", "price_asc", "price_desc"]]'
    )
    assert {p.name: p for p in eps["reviews"].params}["sort"].annotation == (
        'Optional[Literal["relevance", "newest", "oldest", "rating_desc", "rating_asc"]]'
    )
    for m in ("brands", "deals", "new_arrivals"):
        assert {p.name: p for p in eps[m].params}["gender"].annotation == (
            'Optional[Literal["women", "men"]]'
        ), m
    for m in ("search", "category"):
        assert {p.name: p for p in eps[m].params}["gender"].annotation == (
            'Optional[Literal["women", "men", "unisex"]]'
        ), m
        assert "on_sale" in {p.name for p in eps[m].params}, m
    for m in ("deals", "new_arrivals"):
        assert "on_sale" not in {p.name for p in eps[m].params}, m

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    asos = client.asos
    asos.search("jeans")
    asos.search(
        "kleid",
        country="de",
        page=2,
        page_size=200,
        sort="price_asc",
        gender="women",
        brand=["53", "401"],
        color="black",
        range="petite",
        price_min=10,
        price_max=49.5,
        facets={"discount_band": ["5", "6"]},
        on_sale=True,
    )
    asos.product(product_id="210309625")
    asos.product(group_id="210070576", country="nl")
    asos.product(product_id="211390171", country="jp", currency="USD")
    asos.stock(["205338218", "206956133", "209793673"], country="il", currency="USD")
    asos.stock("205338218,206956133")
    asos.reviews("210309625", sort="newest", page_size=50, rating=5)
    asos.suggestions("dre", country="us")
    asos.category("8799", country="fr", sort="price_asc")
    asos.categories(gender="men")
    asos.brands(country="es")
    asos.deals(country="us", gender="men")
    asos.new_arrivals(country="au")
    asos.markets(country="ae", currency="GBP")
    base = "/api/v1/asos/"
    assert seen == [
        (base + "search", {"query": "jeans"}, 120.0),
        (
            base + "search",
            {
                "query": "kleid",
                "country": "de",
                "page": 2,
                "page_size": 200,
                "sort": "price_asc",
                "gender": "women",
                "brand": ["53", "401"],
                "color": "black",
                "range": "petite",
                "price_min": 10,
                "price_max": 49.5,
                "facets": {"discount_band": ["5", "6"]},
                "on_sale": True,
            },
            120.0,
        ),
        (base + "product", {"product_id": "210309625"}, 120.0),
        (base + "product", {"group_id": "210070576", "country": "nl"}, 120.0),
        (
            base + "product",
            {"product_id": "211390171", "country": "jp", "currency": "USD"},
            120.0,
        ),
        (
            base + "stock",
            {
                "product_ids": ["205338218", "206956133", "209793673"],
                "country": "il",
                "currency": "USD",
            },
            120.0,
        ),
        (base + "stock", {"product_ids": "205338218,206956133"}, 120.0),
        (
            base + "reviews",
            {"product_id": "210309625", "sort": "newest", "page_size": 50, "rating": 5},
            120.0,
        ),
        (base + "suggestions", {"query": "dre", "country": "us"}, 120.0),
        (base + "category", {"category_id": "8799", "country": "fr", "sort": "price_asc"}, 120.0),
        (base + "categories", {"gender": "men"}, 120.0),
        (base + "brands", {"country": "es"}, 120.0),
        (base + "deals", {"country": "us", "gender": "men"}, 120.0),
        (base + "new-arrivals", {"country": "au"}, 120.0),
        (base + "markets", {"country": "ae", "currency": "GBP"}, 120.0),
    ]
    with pytest.raises(ScavioError):
        asos.product(country="gb")


def test_mercari_credits_paths_and_wire(monkeypatch):
    """mercari (0.65.0): 11 endpoints on /api/v1/mercari, 1 credit each, 240 s floor.

    country us (default) or jp: search, item, category, categories, brands, brand on both;
    deals and trending us only; seller, seller_reviews and shop jp only. gb / uk (Mercari UK
    closed) are not in any country literal.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "mercari"}
    assert sorted(eps) == [
        "brand", "brands", "categories", "category", "deals", "item", "search", "seller",
        "seller_reviews", "shop", "trending",
    ]
    markets = {
        "search": '"us", "jp"', "item": '"us", "jp"', "category": '"us", "jp"',
        "categories": '"us", "jp"', "brands": '"us", "jp"', "brand": '"us", "jp"',
        "deals": '"us"', "trending": '"us"', "seller": '"jp"', "seller_reviews": '"jp"',
        "shop": '"jp"',
    }
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/mercari/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        country = {p.name: p for p in ep.params}["country"].annotation
        assert country == "Optional[Literal[" + markets[m] + "]]", m
        for cc in ("gb", "uk"):
            assert f'"{cc}"' not in country, (m, cc)
    assert eps["search"].one_of == (("query", "category_id", "brand_id"),)
    assert eps["item"].one_of == (("item_id", "url"),)
    for m in ("seller", "seller_reviews"):
        assert eps[m].one_of == (("seller_id", "url"),), m
    assert eps["shop"].one_of == (("shop_id", "url"),)
    for m in ("search", "category", "brand", "deals"):
        params = {p.name: p for p in eps[m].params}
        assert params["status"].annotation == 'Optional[Literal["on_sale", "sold", "all"]]', m
        assert params["sort"].annotation == (
            'Optional[Literal["relevance", "newest", "price_asc", "price_desc", "likes", '
            '"recently_sold"]]'
        ), m
    for m in ("search", "category", "brand"):
        names = {p.name for p in eps[m].params}
        assert {"deals_only", "shops_only"} <= names, m
    assert not {"deals_only", "shops_only"} & {p.name for p in eps["deals"].params}

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    mercari = client.mercari
    mercari.search("nintendo switch")
    mercari.search("nintendo switch", status="sold", sort="recently_sold", page=2)
    mercari.search(
        "ポケモンカード",
        country="jp",
        price_min=1000,
        price_max=5000.5,
        condition=["new", "like_new"],
        shipping="free",
        shops_only=True,
    )
    mercari.search(category_id=797, brand_id="4591", deals_only=True, size_id=12)
    mercari.item("m38943035688")
    mercari.item(url="https://jp.mercari.com/item/m65962821601")
    mercari.category("797", status="sold")
    mercari.categories(parent_id="7")
    mercari.categories(country="jp")
    mercari.brands(query="nike", page=2)
    mercari.brand(4591, category_id="797", sort="price_asc")
    mercari.deals(query="jordan")
    mercari.trending()
    mercari.seller("477123966")
    mercari.seller_reviews(url="https://jp.mercari.com/user/profile/477123966")
    mercari.shop("LThudSk3aoGvKcW6R3sA6m")
    base = "/api/v1/mercari/"
    assert seen == [
        (base + "search", {"query": "nintendo switch"}, 240.0),
        (
            base + "search",
            {"query": "nintendo switch", "status": "sold", "page": 2, "sort": "recently_sold"},
            240.0,
        ),
        (
            base + "search",
            {
                "query": "ポケモンカード",
                "country": "jp",
                "price_min": 1000,
                "price_max": 5000.5,
                "condition": ["new", "like_new"],
                "shipping": "free",
                "shops_only": True,
            },
            240.0,
        ),
        (
            base + "search",
            {"category_id": 797, "brand_id": "4591", "size_id": 12, "deals_only": True},
            240.0,
        ),
        (base + "item", {"item_id": "m38943035688"}, 240.0),
        (base + "item", {"url": "https://jp.mercari.com/item/m65962821601"}, 240.0),
        (base + "category", {"category_id": "797", "status": "sold"}, 240.0),
        (base + "categories", {"parent_id": "7"}, 240.0),
        (base + "categories", {"country": "jp"}, 240.0),
        (base + "brands", {"query": "nike", "page": 2}, 240.0),
        (base + "brand", {"brand_id": 4591, "category_id": "797", "sort": "price_asc"}, 240.0),
        (base + "deals", {"query": "jordan"}, 240.0),
        (base + "trending", {}, 240.0),
        (base + "seller", {"seller_id": "477123966"}, 240.0),
        (
            base + "seller-reviews",
            {"url": "https://jp.mercari.com/user/profile/477123966"},
            240.0,
        ),
        (base + "shop", {"shop_id": "LThudSk3aoGvKcW6R3sA6m"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        mercari.search(country="us")
    with pytest.raises(ScavioError):
        mercari.item(country="jp")
    with pytest.raises(ScavioError):
        mercari.seller()
    with pytest.raises(ScavioError):
        mercari.shop()


def test_bolcom_credits_paths_and_wire(monkeypatch):
    """bolcom (0.66.0): 9 endpoints on /api/v1/bolcom, 2 credits each (product by ean 4).

    Storefronts nl-nl, be-nl, be-fr on every endpoint (country nl / be, language nl / fr).
    product_id is a string (16 digits). Listing endpoints sort by popularity, never relevance.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "bolcom"}
    assert sorted(eps) == [
        "brand", "campaign", "category", "deals", "offers", "product", "search", "seller",
        "seller_products",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/bolcom/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 2, ep.key
        params = {p.name: p for p in ep.params}
        assert params["country"].annotation == 'Optional[Literal["nl", "be"]]', m
        assert params["language"].annotation == 'Optional[Literal["nl", "fr"]]', m
    assert "4 by ean" in eps["product"].credits_note
    for m in ("product", "offers"):
        assert {p.name: p for p in eps[m].params}["product_id"].annotation == "Optional[str]", m
    assert eps["product"].one_of == (("product_id", "url", "ean"),)
    assert eps["offers"].one_of == (("product_id", "url"),)
    for m in ("seller", "seller_products"):
        assert eps[m].one_of == (("seller_id", "url"),), m
    assert eps["brand"].one_of == (("brand_id", "url"),)
    assert eps["campaign"].one_of == (("campaign_id", "url"),)
    search_sort = {p.name: p for p in eps["search"].params}["sort"].annotation
    assert '"relevance"' in search_sort and '"newest"' not in search_sort
    for m in ("seller_products", "category", "brand", "campaign"):
        sort = {p.name: p for p in eps[m].params}["sort"].annotation
        assert sort == (
            'Optional[Literal["popularity", "price_asc", "price_desc", "rating", "wishlist"]]'
        ), m
    for m in ("search", "category"):
        names = {p.name for p in eps[m].params}
        assert {"brand_facet_id", "facets", "delivery", "condition", "select_deals"} <= names, m
    assert "brand_facet_id" not in {p.name for p in eps["brand"].params}

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    bolcom = client.bolcom
    bolcom.search("airpods")
    bolcom.search(
        "aspirateur",
        country="be",
        language="fr",
        page=2,
        sort="price_asc",
        condition=["refurbished", "second_hand"],
        delivery="tomorrow",
        brand_facet_id="4294862300",
        facets=["58334"],
        price_min=10,
        price_max=99.5,
    )
    bolcom.product("9300000239314960")
    bolcom.product(ean="4242005483976", country="be", language="fr")
    bolcom.offers("9300000240171936", country="be")
    bolcom.seller("1770745")
    bolcom.seller_products("1767374", page=2, sort="rating")
    bolcom.category("8440", deals_only=True, select_deals=True)
    bolcom.brand("5070005", sort="price_desc")
    bolcom.deals()
    bolcom.campaign("555136", page=2)
    base = "/api/v1/bolcom/"
    assert seen == [
        (base + "search", {"query": "airpods"}, 240.0),
        (
            base + "search",
            {
                "query": "aspirateur",
                "country": "be",
                "language": "fr",
                "page": 2,
                "sort": "price_asc",
                "price_min": 10,
                "price_max": 99.5,
                "condition": ["refurbished", "second_hand"],
                "delivery": "tomorrow",
                "brand_facet_id": "4294862300",
                "facets": ["58334"],
            },
            240.0,
        ),
        (base + "product", {"product_id": "9300000239314960"}, 240.0),
        (
            base + "product",
            {"ean": "4242005483976", "country": "be", "language": "fr"},
            240.0,
        ),
        (base + "offers", {"product_id": "9300000240171936", "country": "be"}, 240.0),
        (base + "seller", {"seller_id": "1770745"}, 240.0),
        (base + "seller-products", {"seller_id": "1767374", "page": 2, "sort": "rating"}, 240.0),
        (
            base + "category",
            {"category_id": "8440", "deals_only": True, "select_deals": True},
            240.0,
        ),
        (base + "brand", {"brand_id": "5070005", "sort": "price_desc"}, 240.0),
        (base + "deals", {}, 240.0),
        (base + "campaign", {"campaign_id": "555136", "page": 2}, 240.0),
    ]
    with pytest.raises(ScavioError):
        bolcom.product()
    with pytest.raises(ScavioError):
        bolcom.offers(country="be")
    with pytest.raises(ScavioError):
        bolcom.seller_products()
    with pytest.raises(ScavioError):
        bolcom.campaign()


def test_uniqlo_credits_paths_and_wire(monkeypatch):
    """uniqlo (0.67.0): 12 endpoints on /api/v1/uniqlo, 1 credit each, 240 s floor.

    store_stock 2 when resolved from product_id + color + size; prices 1 per market that
    answered. us / jp / kr serve every endpoint; tw / hk / cn search + product; 35 more
    storefronts product + prices (38 prices markets, 41 product markets, uk alias of gb).
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "uniqlo"}
    assert sorted(eps) == [
        "categories", "category", "deals", "new_arrivals", "prices", "product", "reviews",
        "search", "stock", "store_stock", "stores", "suggestions",
    ]
    a_only = {"stock", "store_stock", "stores", "reviews", "suggestions", "category", "deals",
              "new_arrivals", "categories"}
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/uniqlo/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1, ep.key
        params = {p.name: p for p in ep.params}
        if m in a_only:
            assert params["country"].annotation == 'Optional[Literal["us", "jp", "kr"]]', m
    search_c = {p.name: p for p in eps["search"].params}["country"].annotation
    assert search_c == 'Optional[Literal["us", "jp", "kr", "tw", "hk", "cn"]]'
    product_c = {p.name: p for p in eps["product"].params}["country"].annotation
    assert product_c.count('"') // 2 == 42  # 41 markets + the uk alias
    assert '"ch"' not in product_c and '"mx"' not in product_c
    prices_c = {p.name: p for p in eps["prices"].params}["countries"].annotation
    assert prices_c.count('"') // 2 == 39  # 38 markets + the uk alias
    assert '"tw"' not in prices_c and '"cn"' not in prices_c and '"hk"' not in prices_c
    assert "2 with product_id" in eps["store_stock"].credits_note
    assert "per market" in eps["prices"].credits_note
    assert eps["product"].one_of == (("product_id", "url"),)
    assert eps["store_stock"].one_of == (("l2_id", "product_id"),)
    assert eps["stores"].one_of == (("lat", "store_id"),)
    search_sort = {p.name: p for p in eps["search"].params}["sort"].annotation
    assert '"best_selling"' in search_sort and '"top_rated"' in search_sort
    for m in ("category", "deals", "new_arrivals"):
        sort = {p.name: p for p in eps[m].params}["sort"].annotation
        assert '"best_selling"' not in sort, m

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    uniqlo = client.uniqlo
    uniqlo.search("heattech")
    uniqlo.search("牛仔褲", country="tw", sort="best_selling", page_size=48)
    uniqlo.product("E479000-000", country="de", language="de")
    uniqlo.product(url="https://www.uniqlo.com/us/en/products/E479000-000/00")
    uniqlo.stock("E479000-000")
    uniqlo.store_stock(40.758, -73.9855, l2_id="08665900")
    uniqlo.store_stock(40.758, -73.9855, l2_id="08665900", price_group="01")
    uniqlo.store_stock(35.6595, 139.7005, product_id="E479000-000", color="COL04",
                       size="INS022", country="jp")
    uniqlo.stores(lat=37.5636, lng=126.9826, country="kr", limit=5)
    uniqlo.reviews("E479000-000", sort="most_helpful", page_size=25)
    uniqlo.suggestions()
    uniqlo.category(["22210", "23296", "23339"], flag="sale")
    uniqlo.deals(type="limited_offer", gender="women")
    uniqlo.new_arrivals(country="jp")
    uniqlo.categories(include_subcategories=True)
    uniqlo.prices("E479000-000", countries=["jp", "us", "uk"])
    base = "/api/v1/uniqlo/"
    assert seen == [
        (base + "search", {"query": "heattech"}, 240.0),
        (base + "search", {"query": "牛仔褲", "country": "tw", "page_size": 48,
                           "sort": "best_selling"}, 240.0),
        (base + "product", {"product_id": "E479000-000", "country": "de", "language": "de"},
         240.0),
        (base + "product", {"url": "https://www.uniqlo.com/us/en/products/E479000-000/00"},
         240.0),
        (base + "stock", {"product_id": "E479000-000"}, 240.0),
        (base + "store-stock", {"lat": 40.758, "lng": -73.9855, "l2_id": "08665900"}, 240.0),
        (base + "store-stock", {"lat": 40.758, "lng": -73.9855, "l2_id": "08665900",
                                "price_group": "01"}, 240.0),
        (
            base + "store-stock",
            {"lat": 35.6595, "lng": 139.7005, "product_id": "E479000-000", "color": "COL04",
             "size": "INS022", "country": "jp"},
            240.0,
        ),
        (base + "stores", {"lat": 37.5636, "lng": 126.9826, "limit": 5, "country": "kr"}, 240.0),
        (base + "reviews", {"product_id": "E479000-000", "page_size": 25, "sort": "most_helpful"},
         240.0),
        (base + "suggestions", {}, 240.0),
        (base + "category", {"category_path": ["22210", "23296", "23339"], "flag": "sale"},
         240.0),
        (base + "deals", {"type": "limited_offer", "gender": "women"}, 240.0),
        (base + "new-arrivals", {"country": "jp"}, 240.0),
        (base + "categories", {"include_subcategories": True}, 240.0),
        (base + "prices", {"product_id": "E479000-000", "countries": ["jp", "us", "uk"]}, 240.0),
    ]
    with pytest.raises(ScavioError):
        uniqlo.product()
    with pytest.raises(ScavioError):
        uniqlo.store_stock(40.758, -73.9855)
    with pytest.raises(ScavioError):
        uniqlo.stores()


def test_depop_credits_paths_and_wire(monkeypatch):
    """depop (0.68.0): 14 endpoints on /api/v1/depop, 240 s floor.

    search / category / brand / explore 1 credit (nz 5); product us 1, gb au ie ca de fr it 2,
    nz 6; the rest 1. search, product, category, brand, explore and suggestions on 9 buyer
    markets (uk alias of gb); similar us only; shop data, categories and brands global.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "depop"}
    assert sorted(eps) == [
        "brand", "brands", "categories", "category", "explore", "product", "search", "shop",
        "shop_products", "shop_reviews", "shop_sold", "shops_search", "similar", "suggestions",
    ]
    markets = 'Optional[Literal["us", "gb", "uk", "au", "ie", "ca", "nz", "de", "fr", "it"]]'
    market_eps = {"search", "product", "category", "brand", "explore", "suggestions"}
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/depop/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1, ep.key
        params = {p.name: p for p in ep.params}
        if m in market_eps:
            assert params["country"].annotation == markets, m
        elif m == "similar":
            assert params["country"].annotation == 'Optional[Literal["us"]]'
        else:
            assert "country" not in params, m
    for m in ("search", "category", "brand", "explore"):
        assert "5 credits on nz" in eps[m].credits_note, m
    assert "2 credits on gb" in eps["product"].credits_note
    assert "6 credits on nz" in eps["product"].credits_note
    assert eps["suggestions"].credits_note is None
    sort = {p.name: p for p in eps["search"].params}["sort"].annotation
    assert sort == 'Optional[Literal["relevance", "price_asc", "price_desc"]]'
    assert eps["product"].one_of == (("slug", "url", "product_id"),)
    for m in ("shop", "shop_products", "shop_sold", "shop_reviews"):
        assert eps[m].one_of == (("username", "shop_id"),), m
    assert eps["brands"].one_of == (("letter", "slug"),)

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    depop = client.depop
    depop.search("levis 501")
    depop.search("levis 501", country="gb", sort="price_asc", brand_ids=[31],
                 conditions=["used_excellent"], price_max=40, on_sale=True)
    depop.product("f0omem-levis-550-38x36-blue-jeans-662f")
    depop.product(product_id=1002884801, country="nz")
    depop.category("mens/bottoms/jeans", country="de")
    depop.brand("carhartt")
    depop.explore("90s-menswear")
    depop.suggestions("carh", country="au")
    depop.shop("flomem")
    depop.shop_products(shop_id=46847613, limit=10)
    depop.shop_sold("flomem", cursor="abc")
    depop.shop_reviews("flomem", role="buyer", page=2)
    depop.shops_search("y2k")
    depop.categories(language="de", include_sizes=True)
    depop.brands("c")
    depop.brands(slug="carhartt")
    depop.similar(1002884801)
    base = "/api/v1/depop/"
    assert seen == [
        (base + "search", {"query": "levis 501"}, 240.0),
        (base + "search", {"query": "levis 501", "country": "gb", "sort": "price_asc",
                           "brand_ids": [31], "conditions": ["used_excellent"], "price_max": 40,
                           "on_sale": True}, 240.0),
        (base + "product", {"slug": "f0omem-levis-550-38x36-blue-jeans-662f"}, 240.0),
        (base + "product", {"product_id": 1002884801, "country": "nz"}, 240.0),
        (base + "category", {"category": "mens/bottoms/jeans", "country": "de"}, 240.0),
        (base + "brand", {"slug": "carhartt"}, 240.0),
        (base + "explore", {"slug": "90s-menswear"}, 240.0),
        (base + "suggestions", {"query": "carh", "country": "au"}, 240.0),
        (base + "shop", {"username": "flomem"}, 240.0),
        (base + "shop-products", {"shop_id": 46847613, "limit": 10}, 240.0),
        (base + "shop-sold", {"username": "flomem", "cursor": "abc"}, 240.0),
        (base + "shop-reviews", {"username": "flomem", "role": "buyer", "page": 2}, 240.0),
        (base + "shops-search", {"query": "y2k"}, 240.0),
        (base + "categories", {"language": "de", "include_sizes": True}, 240.0),
        (base + "brands", {"letter": "c"}, 240.0),
        (base + "brands", {"slug": "carhartt"}, 240.0),
        (base + "similar", {"product_id": 1002884801}, 240.0),
    ]
    with pytest.raises(ScavioError):
        depop.product()
    with pytest.raises(ScavioError):
        depop.shop()
    with pytest.raises(ScavioError):
        depop.brands()


def test_poshmark_credits_paths_and_wire(monkeypatch):
    """poshmark (0.69.0): 15 endpoints on /api/v1/poshmark, 1 credit each, 240 s floor.

    Every endpoint accepts us and ca. product, closet, closet_listings, love_notes, closets_search
    and categories are global (country only picks the domain asked). category needs department;
    product takes one of listing_id or url.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "poshmark"}
    assert sorted(eps) == [
        "brand", "brands", "categories", "category", "closet", "closet_listings",
        "closets_search", "love_notes", "parties", "party_listings", "product", "search",
        "similar", "sold", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/poshmark/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        params = {p.name: p for p in ep.params}
        assert params["country"].annotation == 'Optional[Literal["us", "ca"]]', m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "just_shared", "just_in", "price_asc", "price_desc", '
        '"price_drop", "most_liked"]]'
    )
    assert search["condition"].annotation == (
        'Optional[Literal["new_with_tags", "new_with_tags_or_boutique", "boutique", "like_new", '
        '"good", "fair"]]'
    )
    assert "availability" not in {p.name for p in eps["sold"].params}
    assert "480 per query" in eps["search"].summary and "480 per query" in eps["sold"].summary
    dept = {p.name: p for p in eps["category"].params}["department"]
    assert dept.required
    assert eps["product"].one_of == (("listing_id", "url"),)

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    posh = client.poshmark
    posh.search("lululemon align")
    posh.search("lululemon align", country="ca", availability="all", brand=["lululemon athletica"],
                department="Women", condition="like_new", sort="price_drop", size="10",
                color=["Black"], price_min=20, price_max=60, page=2)
    posh.sold("coach bag", page=10, category="Bags", department="Women")
    posh.product("6ad80f0dce5b0ace7ee9abd7")
    posh.product(url="https://poshmark.ca/listing/x-6af9e2547049a1ea8b9d2617", country="ca")
    posh.category("Women", category="Bags", subcategory="Totes", availability="sold")
    posh.brand("Coach", department="Women")
    posh.closet("thriftedbyher")
    posh.closet_listings("thriftedbyher", availability="sold", page=2)
    posh.love_notes("thriftedbyher")
    posh.closets_search("vintage", page=2)
    posh.categories()
    posh.brands(country="ca")
    posh.suggestions("lulu")
    posh.parties(status="scheduled")
    posh.party_listings("6af437b4ccaeb9c6a30f84a3", cursor="abc")
    posh.similar("6ad80f0dce5b0ace7ee9abd7")
    base = "/api/v1/poshmark/"
    assert seen == [
        (base + "search", {"query": "lululemon align"}, 240.0),
        (base + "search", {"query": "lululemon align", "country": "ca", "page": 2,
                           "availability": "all", "brand": ["lululemon athletica"],
                           "department": "Women", "sort": "price_drop", "size": "10",
                           "condition": "like_new", "color": ["Black"], "price_min": 20,
                           "price_max": 60}, 240.0),
        (base + "sold", {"query": "coach bag", "page": 10, "department": "Women",
                         "category": "Bags"}, 240.0),
        (base + "product", {"listing_id": "6ad80f0dce5b0ace7ee9abd7"}, 240.0),
        (base + "product", {"url": "https://poshmark.ca/listing/x-6af9e2547049a1ea8b9d2617",
                            "country": "ca"}, 240.0),
        (base + "category", {"department": "Women", "category": "Bags", "subcategory": "Totes",
                             "availability": "sold"}, 240.0),
        (base + "brand", {"brand": "Coach", "department": "Women"}, 240.0),
        (base + "closet", {"username": "thriftedbyher"}, 240.0),
        (base + "closet-listings", {"username": "thriftedbyher", "availability": "sold",
                                    "page": 2}, 240.0),
        (base + "love-notes", {"username": "thriftedbyher"}, 240.0),
        (base + "closets-search", {"query": "vintage", "page": 2}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "brands", {"country": "ca"}, 240.0),
        (base + "suggestions", {"query": "lulu"}, 240.0),
        (base + "parties", {"status": "scheduled"}, 240.0),
        (base + "party-listings", {"party_id": "6af437b4ccaeb9c6a30f84a3", "cursor": "abc"}, 240.0),
        (base + "similar", {"listing_id": "6ad80f0dce5b0ace7ee9abd7"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        posh.product()


def test_thredup_credits_paths_and_wire(monkeypatch):
    """thredup (0.70.0): 12 endpoints on /api/v1/thredup, 1 credit each, 240 s floor.

    One US store, so no endpoint takes country. sold takes no query and needs brand or
    category; product and similar take one of item_number or url; category needs department and
    category; deals needs collection.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "thredup"}
    assert sorted(eps) == [
        "brand", "brands", "categories", "category", "deals", "product", "rescue_boxes",
        "search", "similar", "sold", "suggestions", "trending",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/thredup/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        assert "country" not in {p.name for p in ep.params}, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["default", "recommended", "relevance", "newest", "price_high", '
        '"price_low", "price_drop"]]'
    )
    assert "Literal[\"women\", \"girls\"" in search["department"].annotation
    assert "men\"" not in search["department"].annotation.replace("women\"", "")
    assert "query" not in {p.name for p in eps["sold"].params}
    assert eps["sold"].one_of == (("brand", "category"),)
    assert eps["product"].one_of == (("item_number", "url"),)
    assert eps["similar"].one_of == (("item_number", "url"),)
    cat = {p.name: p for p in eps["category"].params}
    assert cat["department"].required and cat["category"].required
    assert {p.name: p for p in eps["deals"].params}["collection"].required
    assert eps["rescue_boxes"].params == ()
    assert "no sold date" in eps["sold"].summary
    assert "estimated original retail" in eps["search"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    tu = client.thredup
    tu.search("denim jacket")
    tu.search("denim jacket", brand="Levi's", department="women", size=[20778, 795],
              condition=["excellent", "new_with_tags"], color="blue", material=["cotton"],
              pattern="solid", price_min=10, price_max=40, clearance=True,
              seller_type=["thredup", "direct_listing"], sort="price_low", page=21)
    tu.sold(brand="Coach", department="handbags")
    tu.sold(category="dresses", page=2)
    tu.product(241601590)
    tu.product(url="https://www.thredup.com/product/women-zenim-denim-jacket/241601590")
    tu.category("women", "dresses", brand="Madewell", sort="newest")
    tu.brand("Madewell", category="jeans")
    tu.deals("clearance", department="women", sort="price_low")
    tu.deals("price_drops", brand="Madewell")
    tu.rescue_boxes()
    tu.categories()
    tu.categories(department="girls")
    tu.brands(query="coach")
    tu.brands(letter="M", page=2, limit=500)
    tu.suggestions("made")
    tu.suggestions("made", department="boys")
    tu.trending()
    tu.similar(241601590)
    base = "/api/v1/thredup/"
    assert seen == [
        (base + "search", {"query": "denim jacket"}, 240.0),
        (base + "search", {"query": "denim jacket", "brand": "Levi's", "department": "women",
                           "sort": "price_low", "size": [20778, 795],
                           "condition": ["excellent", "new_with_tags"], "color": "blue",
                           "material": ["cotton"], "pattern": "solid", "price_min": 10,
                           "price_max": 40, "clearance": True,
                           "seller_type": ["thredup", "direct_listing"], "page": 21}, 240.0),
        (base + "sold", {"brand": "Coach", "department": "handbags"}, 240.0),
        (base + "sold", {"category": "dresses", "page": 2}, 240.0),
        (base + "product", {"item_number": 241601590}, 240.0),
        (base + "product",
         {"url": "https://www.thredup.com/product/women-zenim-denim-jacket/241601590"}, 240.0),
        (base + "category", {"department": "women", "category": "dresses", "brand": "Madewell",
                             "sort": "newest"}, 240.0),
        (base + "brand", {"brand": "Madewell", "category": "jeans"}, 240.0),
        (base + "deals", {"collection": "clearance", "department": "women",
                          "sort": "price_low"}, 240.0),
        (base + "deals", {"collection": "price_drops", "brand": "Madewell"}, 240.0),
        (base + "rescue-boxes", {}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"department": "girls"}, 240.0),
        (base + "brands", {"query": "coach"}, 240.0),
        (base + "brands", {"letter": "M", "page": 2, "limit": 500}, 240.0),
        (base + "suggestions", {"query": "made"}, 240.0),
        (base + "suggestions", {"query": "made", "department": "boys"}, 240.0),
        (base + "trending", {}, 240.0),
        (base + "similar", {"item_number": 241601590}, 240.0),
    ]
    with pytest.raises(ScavioError):
        tu.product()
    with pytest.raises(ScavioError):
        tu.similar()
    with pytest.raises(ScavioError):
        tu.sold()


def test_fashionnova_credits_paths_and_wire(monkeypatch):
    """fashionnova (0.71.0, 0.71.1): 7 endpoints on /api/v1/fashionnova, 1 credit each, 240 s floor.

    search, product and collection take country (104 storefronts) and language (en, es);
    categories, suggestions and reviews are the same for every storefront and similar answers
    from the US store, so none of those takes country. product, reviews and similar take one of
    handle or url; collection takes one of handle or url.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "fashionnova"}
    assert sorted(eps) == [
        "categories", "collection", "product", "reviews", "search", "similar", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/fashionnova/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        names = {p.name for p in ep.params}
        if m in ("search", "product", "collection"):
            assert {"country", "language"} <= names, m
        else:
            assert "country" not in names and "language" not in names, m
    search = {p.name: p for p in eps["search"].params}
    country = search["country"].annotation
    assert country.count('"') == 2 * 104
    assert '"zz"' in country and '"us"' in country and '"uk"' not in country
    assert search["language"].annotation == 'Optional[Literal["en", "es"]]'
    assert search["sort"].annotation == (
        'Optional[Literal["featured", "best_selling", "price_low", "price_high", "newest"]]'
    )
    for m in ("product", "collection", "reviews", "similar"):
        assert eps[m].one_of == (("handle", "url"),), m
    reviews = {p.name: p for p in eps["reviews"].params}
    assert reviews["sort"].annotation == (
        'Optional[Literal["highest_rated", "most_recent", "most_helpful", "lowest_rated"]]'
    )
    assert reviews["star"].annotation == "Optional[Literal[1, 2, 3, 4, 5]]"
    assert "per style, not per colour" in eps["reviews"].summary
    assert "mostly English" in eps["reviews"].summary
    # 0.71.1: collections list up to about 10,000 products (page 166), code price flag.
    coll = {p.name: p for p in eps["collection"].params}
    assert "1 to 166" in coll["page"].doc and "1 to 166" in eps["collection"].summary
    assert "dedupe by product_id + color" in eps["collection"].summary
    for m in ("search", "collection", "product", "similar"):
        assert "code_lowers_price" in eps[m].summary, m
    assert "27 EEA" in eps["search"].summary and "no compare-at" in eps["search"].summary
    assert "Fashion Nova's own AI summary" in eps["product"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    fn = client.fashionnova
    fn.search("bodycon dress")
    fn.search("bodycon dress", country="mx", language="es", sort="price_low", size=["M", "L"],
              color="black", price_min=10, price_max=40, division=["women", "curve"],
              category="Dresses", filters={"occasion": "Club"}, page=6)
    fn.product("san-diego-sculpting-stretch-flare-jeans", color="black-wash", country="fr")
    fn.product(url="https://www.fashionnova.com/products/san-diego-sculpting-stretch-flare-jeans")
    fn.collection("sale")
    fn.collection("sale", country="gb", sort="best_selling", page=200)
    fn.categories()
    fn.categories(division="men")
    fn.suggestions("dress")
    fn.suggestions("dress", division="curve")
    fn.reviews("san-diego-sculpting-stretch-flare-jeans", color="black-wash", sort="most_recent",
               star=5, page=8)
    fn.similar("san-diego-sculpting-stretch-flare-jeans", limit=24)
    base = "/api/v1/fashionnova/"
    assert seen == [
        (base + "search", {"query": "bodycon dress"}, 240.0),
        (base + "search", {"query": "bodycon dress", "country": "mx", "language": "es",
                           "sort": "price_low", "size": ["M", "L"], "color": "black",
                           "price_min": 10, "price_max": 40, "division": ["women", "curve"],
                           "category": "Dresses", "filters": {"occasion": "Club"},
                           "page": 6}, 240.0),
        (base + "product", {"handle": "san-diego-sculpting-stretch-flare-jeans",
                            "color": "black-wash", "country": "fr"}, 240.0),
        (base + "product",
         {"url": "https://www.fashionnova.com/products/san-diego-sculpting-stretch-flare-jeans"},
         240.0),
        (base + "collection", {"handle": "sale"}, 240.0),
        (base + "collection", {"handle": "sale", "country": "gb", "sort": "best_selling",
                               "page": 200}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"division": "men"}, 240.0),
        (base + "suggestions", {"query": "dress"}, 240.0),
        (base + "suggestions", {"query": "dress", "division": "curve"}, 240.0),
        (base + "reviews", {"handle": "san-diego-sculpting-stretch-flare-jeans",
                            "color": "black-wash", "sort": "most_recent", "star": 5,
                            "page": 8}, 240.0),
        (base + "similar", {"handle": "san-diego-sculpting-stretch-flare-jeans",
                            "limit": 24}, 240.0),
    ]
    for call in (fn.product, fn.collection, fn.reviews, fn.similar):
        with pytest.raises(ScavioError):
            call()


def test_argos_credits_paths_and_wire(monkeypatch):
    """argos (0.72.0): 10 endpoints on /api/v1/argos, 2 credits each, 240 s floor.

    One UK store (argos.co.uk, GBP), so no endpoint takes country. product, reviews and
    questions take one of product_id or url; stores takes one of postcode or store.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "argos"}
    assert sorted(eps) == [
        "categories", "category", "deals", "product", "questions", "reviews", "search",
        "store_stock", "stores", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/argos/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 2 and ep.credits_note is None, ep.key
        assert "country" not in {p.name for p in ep.params}, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_low", "price_high", "rating"]]'
    )
    assert search["seller"].annotation == 'Optional[Literal["argos", "trusted_seller"]]'
    assert search["rating_min"].annotation == "Optional[Literal[1, 2, 3, 4, 5]]"
    for m in ("product", "reviews", "questions"):
        assert eps[m].one_of == (("product_id", "url"),), m
    assert eps["stores"].one_of == (("postcode", "store"),)
    stock = {p.name: p for p in eps["store_stock"].params}
    assert stock["product_ids"].required and stock["postcode"].required
    assert "no unit counts" in eps["store_stock"].summary
    deals = {p.name: p for p in eps["deals"].params}
    assert deals["collection"].annotation == (
        'Literal["black_friday", "clearance", "special_offers", "top_100"]'
    )
    reviews = {p.name: p for p in eps["reviews"].params}
    assert reviews["sort"].annotation == (
        'Optional[Literal["newest", "oldest", "most_helpful", "highest_rating", '
        '"lowest_rating"]]'
    )
    assert "Argos's own AI-generated summary" in eps["reviews"].summary
    assert "No reviewer name" in eps["reviews"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ar = client.argos
    ar.search("air fryer")
    ar.search("air fryer", brand=["ninja", "tower"], seller="argos", offers="clearance",
              price_min=40, price_max=150, rating_min=4, sort="price_low", page=2,
              filters={"capacity": "5l - 6.9l"})
    ar.product("8377058")
    ar.product(url="https://www.argos.co.uk/product/8377058/")
    ar.store_stock(["8377058", "7163184"], "SW1A 1AA")
    ar.store_stock("8377058,7163184", "SW1A 1AA", delivery_postcode="M1 1AE", max_distance=20,
                   max_results=5)
    ar.stores("M1 1AE")
    ar.stores(store="661-manchester-arndale-argos")
    ar.reviews("7163184", sort="most_helpful", rating=[1, 2], page=2, limit=100)
    ar.questions("8377058", sort="oldest", limit=50)
    ar.categories()
    ar.category("29560", sort="rating", new_in=True)
    ar.deals("black_friday", query="lego", page=3)
    ar.deals("top_100", page=2)
    ar.suggestions("lego", limit=5)
    base = "/api/v1/argos/"
    assert seen == [
        (base + "search", {"query": "air fryer"}, 240.0),
        (base + "search", {"query": "air fryer", "offers": "clearance",
                           "brand": ["ninja", "tower"], "seller": "argos", "price_min": 40,
                           "price_max": 150, "rating_min": 4,
                           "filters": {"capacity": "5l - 6.9l"}, "sort": "price_low",
                           "page": 2}, 240.0),
        (base + "product", {"product_id": "8377058"}, 240.0),
        (base + "product", {"url": "https://www.argos.co.uk/product/8377058/"}, 240.0),
        (base + "store-stock", {"product_ids": ["8377058", "7163184"], "postcode": "SW1A 1AA"},
         240.0),
        (base + "store-stock", {"product_ids": "8377058,7163184", "postcode": "SW1A 1AA",
                                "delivery_postcode": "M1 1AE", "max_distance": 20,
                                "max_results": 5}, 240.0),
        (base + "stores", {"postcode": "M1 1AE"}, 240.0),
        (base + "stores", {"store": "661-manchester-arndale-argos"}, 240.0),
        (base + "reviews", {"product_id": "7163184", "sort": "most_helpful", "rating": [1, 2],
                            "page": 2, "limit": 100}, 240.0),
        (base + "questions", {"product_id": "8377058", "sort": "oldest", "limit": 50}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "category", {"category_id": "29560", "new_in": True, "sort": "rating"}, 240.0),
        (base + "deals", {"collection": "black_friday", "query": "lego", "page": 3}, 240.0),
        (base + "deals", {"collection": "top_100", "page": 2}, 240.0),
        (base + "suggestions", {"query": "lego", "limit": 5}, 240.0),
    ]
    for call in (ar.product, ar.reviews, ar.questions, ar.stores):
        with pytest.raises(ScavioError):
            call()


def test_mediaexpert_credits_paths_and_wire(monkeypatch):
    """mediaexpert (0.73.0): 13 endpoints on /api/v1/mediaexpert, actual cost 1 to 3 credits.

    One Polish store (mediaexpert.pl, PLN), so no endpoint takes country. product takes one of
    product_id or url; reviews one of sku, product_id or url. Variable-cost endpoints state
    their range in credits_note; flat ones keep credits.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "mediaexpert"}
    assert sorted(eps) == [
        "brand", "brands", "categories", "category", "outlet", "product", "promotions",
        "reviews", "search", "seller", "store_stock", "stores", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/mediaexpert/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "country" not in {p.name for p in ep.params}, m
    flat = {m: ep.credits for m, ep in eps.items() if ep.credits_note is None}
    assert flat == {
        "product": 1, "store_stock": 2, "stores": 1, "reviews": 1, "categories": 2,
        "brands": 1, "suggestions": 1,
    }
    for m in ("search", "category", "brand", "promotions", "outlet", "seller"):
        assert eps[m].credits == 1 and "3 credits" in eps[m].credits_note, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc", "rating", "newest", '
        '"name_asc", "name_desc", "brand_asc", "brand_desc", "discount"]]'
    )
    assert search["limit"].annotation == "Optional[Literal[5, 10, 15, 20, 30, 50]]"
    assert eps["product"].one_of == (("product_id", "url"),)
    assert eps["reviews"].one_of == (("sku", "product_id", "url"),)
    stock = {p.name: p for p in eps["store_stock"].params}
    assert stock["product_id"].required and stock["location"].required
    assert "not a unit count" in eps["store_stock"].summary
    assert "omnibus_lowest_30d" in eps["product"].summary
    assert "No reviewer name" in eps["reviews"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    me = client.mediaexpert
    me.search("telewizor")
    me.search("iphone 17", category_id="12900", sort="price_asc", page=2, limit=50)
    me.product("8128227")
    me.product(url="https://www.mediaexpert.pl/telewizory-i-rtv/telewizory/x")
    me.store_stock("8128227", "Warszawa")
    me.store_stock(8128227, "00-950", limit=10)
    me.stores()
    me.stores("Krakow")
    me.stores(store="warszawa/al-jerozolimskie-148")
    me.reviews("709727")
    me.reviews(product_id="8128227", sort="newest", rating_min=1, rating_max=2, verified=True,
               page=2, limit=100)
    me.category("agd/pralki-i-suszarki/pralki", filters=["bosch", "pojemnosc-kg_od-10-kg"],
                sort="price_asc")
    me.categories(category="agd", depth=2)
    me.brands("sams", limit=50)
    me.brand("samsung", category="telewizory-i-rtv/telewizory", sort="price_desc")
    me.promotions(black_weeks=True)
    me.promotions("32975-logitech-black-weeks-czas-na-nowy-poziom-sprzetu", page=2)
    me.outlet()
    me.outlet("outlet/outlet-agd/outlet-lodowki-wolnostojace", limit=20)
    me.seller("autobi", page=2)
    me.suggestions("pral", limit=5)
    base = "/api/v1/mediaexpert/"
    assert seen == [
        (base + "search", {"query": "telewizor"}, 240.0),
        (base + "search", {"query": "iphone 17", "category_id": "12900", "sort": "price_asc",
                           "page": 2, "limit": 50}, 240.0),
        (base + "product", {"product_id": "8128227"}, 240.0),
        (base + "product", {"url": "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory/x"},
         240.0),
        (base + "store-stock", {"product_id": "8128227", "location": "Warszawa"}, 240.0),
        (base + "store-stock", {"product_id": 8128227, "location": "00-950", "limit": 10}, 240.0),
        (base + "stores", {}, 240.0),
        (base + "stores", {"city": "Krakow"}, 240.0),
        (base + "stores", {"store": "warszawa/al-jerozolimskie-148"}, 240.0),
        (base + "reviews", {"sku": "709727"}, 240.0),
        (base + "reviews", {"product_id": "8128227", "sort": "newest", "rating_min": 1,
                            "rating_max": 2, "verified": True, "page": 2, "limit": 100}, 240.0),
        (base + "category", {"category": "agd/pralki-i-suszarki/pralki",
                             "filters": ["bosch", "pojemnosc-kg_od-10-kg"], "sort": "price_asc"},
         240.0),
        (base + "categories", {"category": "agd", "depth": 2}, 240.0),
        (base + "brands", {"query": "sams", "limit": 50}, 240.0),
        (base + "brand", {"brand": "samsung", "category": "telewizory-i-rtv/telewizory",
                          "sort": "price_desc"}, 240.0),
        (base + "promotions", {"black_weeks": True}, 240.0),
        (base + "promotions", {"list": "32975-logitech-black-weeks-czas-na-nowy-poziom-sprzetu",
                               "page": 2}, 240.0),
        (base + "outlet", {}, 240.0),
        (base + "outlet", {"category": "outlet/outlet-agd/outlet-lodowki-wolnostojace",
                           "limit": 20}, 240.0),
        (base + "seller", {"seller": "autobi", "page": 2}, 240.0),
        (base + "suggestions", {"query": "pral", "limit": 5}, 240.0),
    ]
    for call in (me.product, me.reviews):
        with pytest.raises(ScavioError):
            call()


def test_action_credits_paths_and_wire(monkeypatch):
    """action (0.74.0): 16 endpoints on /api/v1/action, 1 credit each.

    19 storefronts (country + language for be and ch). product takes one of product_code or
    url; store one of store or store_id; webshop_search one of query or category;
    webshop_product one of ean or url. reviews serve nl, de, fr and pl; the webshop nl and be.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "action"}
    assert sorted(eps) == [
        "brand", "brands", "categories", "category", "collection", "new_arrivals", "product",
        "products", "reviews", "search", "store", "stores", "suggestions", "webshop_product",
        "webshop_search", "weekly_deals",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/action/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        assert "action.com, the European non-food discount store" in ep.summary, ep.key
    countries = {m: {p.name: p for p in ep.params}["country"].annotation for m, ep in eps.items()}
    assert countries["search"] == (
        'Optional[Literal["nl", "be", "fr", "lu", "de", "at", "ch", "it", "es", "pt", "pl", "cz", '
        '"sk", "ro", "hr", "si"]]'
    )
    assert countries["reviews"] == 'Optional[Literal["nl", "de", "fr", "pl"]]'
    assert countries["webshop_search"] == countries["webshop_product"] == (
        'Optional[Literal["nl", "be"]]'
    )
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc", "newest"]]'
    )
    assert "brand_filter" not in {p.name for p in eps["brand"].params}
    assert "new_only" not in {p.name for p in eps["new_arrivals"].params}
    assert eps["product"].one_of == (("product_code", "url"),)
    assert eps["store"].one_of == (("store", "store_id"),)
    assert eps["webshop_search"].one_of == (("query", "category"),)
    assert eps["webshop_product"].one_of == (("ean", "url"),)
    assert {p.name: p for p in eps["products"].params}["product_codes"].required
    assert {p.name: p for p in eps["reviews"].params}["product_code"].required
    assert "Promo2026Week47" in eps["weekly_deals"].summary
    assert "Wednesday to Tuesday" in eps["weekly_deals"].summary
    assert "does not publish store stock" in eps["stores"].summary
    assert "No reviewer name" in eps["reviews"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ac = client.action
    ac.search("kerst")
    ac.search("weihnachten", country="de", sort="price_asc", page=2, price_range="2-5",
              new_only=True)
    ac.product("3225277")
    ac.product("3225277", country="ch", language="fr")
    ac.product(url="https://www.action.com/nl-nl/p/3225277/dennenslinger-met-led/")
    ac.products(["3225277", "3011615", "3225488"], country="pl")
    ac.category("wonen/woonaccessoires", brand_filter="Disney")
    ac.categories(country="ro", depth=2)
    ac.brand("max-more", sort="newest")
    ac.brands()
    ac.brands(query="max")
    ac.new_arrivals(country="de")
    ac.weekly_deals()
    ac.weekly_deals(country="be", language="fr", page=2)
    ac.collection("black-friday")
    ac.suggestions("opberg")
    ac.stores("Amsterdam")
    ac.stores(lat=52.37, lng=4.89, country="nl")
    ac.store("/nl-nl/winkels/amsterdam-kinkerstraat/")
    ac.store(store_id="1260")
    ac.reviews("3224838", scope="all", sort="newest")
    ac.reviews("3224838", country="de", rating=[1, 2], query="kapot", limit=100, offset=20)
    ac.webshop_search("stofzuiger")
    ac.webshop_search(category="alle-tijdelijke-deals", country="be", language="fr", page=2)
    ac.webshop_product("8718969571098")
    base = "/api/v1/action/"
    assert seen == [
        (base + "search", {"query": "kerst"}, 240.0),
        (base + "search", {"query": "weihnachten", "country": "de", "sort": "price_asc",
                           "page": 2, "price_range": "2-5", "new_only": True}, 240.0),
        (base + "product", {"product_code": "3225277"}, 240.0),
        (base + "product", {"product_code": "3225277", "country": "ch", "language": "fr"},
         240.0),
        (base + "product", {"url": "https://www.action.com/nl-nl/p/3225277/dennenslinger-met-led/"},
         240.0),
        (base + "products", {"product_codes": ["3225277", "3011615", "3225488"],
                             "country": "pl"}, 240.0),
        (base + "category", {"category": "wonen/woonaccessoires", "brand_filter": "Disney"},
         240.0),
        (base + "categories", {"country": "ro", "depth": 2}, 240.0),
        (base + "brand", {"brand": "max-more", "sort": "newest"}, 240.0),
        (base + "brands", {}, 240.0),
        (base + "brands", {"query": "max"}, 240.0),
        (base + "new-arrivals", {"country": "de"}, 240.0),
        (base + "weekly-deals", {}, 240.0),
        (base + "weekly-deals", {"country": "be", "language": "fr", "page": 2}, 240.0),
        (base + "collection", {"collection": "black-friday"}, 240.0),
        (base + "suggestions", {"query": "opberg"}, 240.0),
        (base + "stores", {"query": "Amsterdam"}, 240.0),
        (base + "stores", {"lat": 52.37, "lng": 4.89, "country": "nl"}, 240.0),
        (base + "store", {"store": "/nl-nl/winkels/amsterdam-kinkerstraat/"}, 240.0),
        (base + "store", {"store_id": "1260"}, 240.0),
        (base + "reviews", {"product_code": "3224838", "scope": "all", "sort": "newest"}, 240.0),
        (base + "reviews", {"product_code": "3224838", "country": "de", "rating": [1, 2],
                            "query": "kapot", "limit": 100, "offset": 20}, 240.0),
        (base + "webshop-search", {"query": "stofzuiger"}, 240.0),
        (base + "webshop-search", {"category": "alle-tijdelijke-deals", "country": "be",
                                   "language": "fr", "page": 2}, 240.0),
        (base + "webshop-product", {"ean": "8718969571098"}, 240.0),
    ]
    for call in (ac.product, ac.store, ac.webshop_search, ac.webshop_product):
        with pytest.raises(ScavioError):
            call()


def test_hema_credits_paths_and_wire(monkeypatch):
    """hema (0.75.0): 13 endpoints on /api/v1/hema, 1 credit each.

    Webshops nl, be (nl or fr), fr, de; store_stock and stores also lu and at; sale nl, be,
    de; offers nl, be. product takes one of sku or url; store takes a store id (no country).
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "hema"}
    assert sorted(eps) == [
        "campaign", "categories", "category", "new_arrivals", "offers", "product", "reviews",
        "sale", "search", "store", "store_stock", "stores", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/hema/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1 and ep.credits_note is None, ep.key
        assert "hema.com, the Dutch variety store" in ep.summary, ep.key
    countries = {
        m: {p.name: p for p in ep.params}["country"].annotation
        for m, ep in eps.items()
        if m != "store"
    }
    shop = 'Optional[Literal["nl", "be", "fr", "de"]]'
    stores = 'Optional[Literal["nl", "be", "fr", "de", "lu", "at"]]'
    for m in ("search", "product", "category", "categories", "new_arrivals", "campaign",
              "suggestions", "reviews"):
        assert countries[m] == shop, m
    assert countries["store_stock"] == countries["stores"] == stores
    assert countries["sale"] == 'Optional[Literal["nl", "be", "de"]]'
    assert countries["offers"] == 'Optional[Literal["nl", "be"]]'
    assert "country" not in {p.name for p in eps["store"].params}
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc", "newest", "best_selling"]]'
    )
    assert search["filters"].annotation == "Optional[dict[str, Union[str, list[str]]]]"
    assert search["price_min"].annotation == "Optional[float]"
    assert "new_only" not in {p.name for p in eps["new_arrivals"].params}
    assert eps["product"].one_of == (("sku", "url"),)
    assert {p.name: p for p in eps["store_stock"].params}["skus"].required
    assert {p.name: p for p in eps["store"].params}["store_id"].required
    assert {p.name: p for p in eps["reviews"].params}["sku"].required
    assert "sellable units HEMA's store service reports" in eps["store_stock"].summary
    assert "not a promise that the shelf has it" in eps["store_stock"].summary
    assert "upcoming promotions included" in eps["product"].summary
    assert "No reviewer name" in eps["reviews"].summary
    assert "brands (HEMA sells its own brand)" in eps["search"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    hm = client.hema
    hm.search("sokken")
    hm.search("bougie", country="be", language="fr", sort="price_asc", page=2,
              filters={"maincolour": ["zwart", "wit"]}, price_min=1.5, price_max=10)
    hm.product("15300147")
    hm.product("15300147", country="de")
    hm.product(url="https://www.hema.nl/speelgoed-hobby/babyspeelgoed/knuffeldoekje-konijn-15300147.html")
    hm.category("baby/babykleding", new_only=True)
    hm.categories(depth=1)
    hm.new_arrivals(country="fr", sort="newest")
    hm.sale(country="de")
    hm.offers()
    hm.offers(country="be", language="fr")
    hm.campaign("sinterklaas", country="be")
    hm.suggestions("kerst")
    hm.store_stock(["15300147", "10860090"], query="Utrecht")
    hm.store_stock(["15300147"], lat=48.85, lng=2.35, country="fr", in_stock_only=True, limit=5)
    hm.store_stock(["15300147"], country="lu")
    hm.stores("Utrecht")
    hm.stores(country="at")
    hm.store("0013")
    hm.store("0013", sku="15300147")
    hm.reviews("10860090")
    hm.reviews("10860090", country="be", sort="highest", page=2)
    base = "/api/v1/hema/"
    assert seen == [
        (base + "search", {"query": "sokken"}, 240.0),
        (base + "search", {"query": "bougie", "country": "be", "language": "fr",
                           "sort": "price_asc", "page": 2,
                           "filters": {"maincolour": ["zwart", "wit"]}, "price_min": 1.5,
                           "price_max": 10}, 240.0),
        (base + "product", {"sku": "15300147"}, 240.0),
        (base + "product", {"sku": "15300147", "country": "de"}, 240.0),
        (base + "product", {"url": "https://www.hema.nl/speelgoed-hobby/babyspeelgoed/"
                                   "knuffeldoekje-konijn-15300147.html"}, 240.0),
        (base + "category", {"category": "baby/babykleding", "new_only": True}, 240.0),
        (base + "categories", {"depth": 1}, 240.0),
        (base + "new-arrivals", {"country": "fr", "sort": "newest"}, 240.0),
        (base + "sale", {"country": "de"}, 240.0),
        (base + "offers", {}, 240.0),
        (base + "offers", {"country": "be", "language": "fr"}, 240.0),
        (base + "campaign", {"campaign": "sinterklaas", "country": "be"}, 240.0),
        (base + "suggestions", {"query": "kerst"}, 240.0),
        (base + "store-stock", {"skus": ["15300147", "10860090"], "query": "Utrecht"}, 240.0),
        (base + "store-stock", {"skus": ["15300147"], "lat": 48.85, "lng": 2.35,
                                "country": "fr", "limit": 5, "in_stock_only": True}, 240.0),
        (base + "store-stock", {"skus": ["15300147"], "country": "lu"}, 240.0),
        (base + "stores", {"query": "Utrecht"}, 240.0),
        (base + "stores", {"country": "at"}, 240.0),
        (base + "store", {"store_id": "0013"}, 240.0),
        (base + "store", {"store_id": "0013", "sku": "15300147"}, 240.0),
        (base + "reviews", {"sku": "10860090"}, 240.0),
        (base + "reviews", {"sku": "10860090", "country": "be", "sort": "highest", "page": 2},
         240.0),
    ]
    with pytest.raises(ScavioError):
        hm.product()


def test_autozone_credits_paths_and_wire(monkeypatch):
    """autozone (0.76.0): 12 endpoints on /api/v1/autozone.

    1 credit each; br search and br product 2 (credits_note), store_stock (Brazil only) 2.
    search and product serve us and br; vehicles, stores, store and categories us, br, mx;
    category, brand, reviews, clearance and rebates are us only and take no country. Lists are
    the first 24 results only: no page param.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "autozone"}
    assert sorted(eps) == [
        "brand", "categories", "category", "clearance", "product", "rebates", "reviews",
        "search", "store", "store_stock", "stores", "vehicles",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/autozone/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "AutoZone" in ep.summary, ep.key
        names = {p.name for p in ep.params}
        if m in ("search", "category", "brand", "clearance"):
            assert "page" not in names, ep.key
    for m in ("search", "product"):
        assert eps[m].credits == 1, m
        assert eps[m].credits_note == "Costs 1 credit on us (the default), 2 credits on br.", m
    assert eps["store_stock"].credits == 2 and eps["store_stock"].credits_note is None
    for m in ("category", "brand", "vehicles", "reviews", "stores", "store", "categories",
              "clearance", "rebates"):
        assert eps[m].credits == 1 and eps[m].credits_note is None, m
    countries = {
        m: {p.name: p for p in ep.params}.get("country")
        for m, ep in eps.items()
    }
    for m in ("search", "product"):
        assert countries[m].annotation == 'Optional[Literal["us", "br"]]', m
    for m in ("vehicles", "stores", "store", "categories"):
        assert countries[m].annotation == 'Optional[Literal["us", "br", "mx"]]', m
    for m in ("category", "brand", "reviews", "clearance", "rebates", "store_stock"):
        assert countries[m] is None, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == 'Optional[Literal["relevance", "price_asc", "price_desc"]]'
    assert search["min_price"].annotation == "Optional[float]"
    assert eps["product"].one_of == eps["reviews"].one_of == eps["store_stock"].one_of == (
        ("id", "url"),
    )
    assert eps["store"].one_of == (("slug", "url"),)
    assert {p.name: p for p in eps["store_stock"].params}["store_number"].required
    assert {p.name: p for p in eps["category"].params}["category"].required
    for m in ("search", "product", "category", "brand", "clearance"):
        assert "priced_for" in eps[m].summary, m
        assert "never report a price as national" in eps[m].summary, m
    assert "NEEDS_BASE_VEHICLE" in eps["category"].summary
    assert "cross-reference" in eps["search"].summary
    assert "No reviewer name" in eps["reviews"].summary
    assert "Brazil only" in eps["store_stock"].summary
    assert "stores-near-a-ZIP" in eps["stores"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    az = client.autozone
    az.search("brake pads")
    az.search("5w-30", sort="price_asc", min_price=20, max_price=40,
              filters={"position_name_s": "Front"})
    az.search("spark plugs", brand="NGK")
    az.search("pastilha de freio", country="br")
    az.product("1399158")
    az.product("100123563", country="br")
    az.product(url="https://www.autozone.com/p/duralast-floor-jack-d3thj/1399158")
    az.category("/brakes-and-traction-control/brake-pads",
                vehicle={"year": 2018, "make": "Ford", "model": "F-150"})
    az.category("/batteries-starting-and-charging/battery", sort="price_desc")
    az.brand("duralast")
    az.brand("duralast-gold", category="/brakes-and-traction-control/brake-rotor")
    az.vehicles()
    az.vehicles(level="models", year=2018, make_id=54)
    az.vehicles(level="makes", year=2020, country="mx")
    az.reviews("1399158")
    az.reviews("906340", page=2, sort="most_helpful", stars=[1, 2])
    az.stores()
    az.stores(state="tx", city="houston")
    az.stores(country="br", state="sao-paulo")
    az.store("vt/barre/18-overlook-dr.html")
    az.store(url="https://www.autozone.com.mx/ubicaciones/nl/monterrey/x.html")
    az.categories(country="br")
    az.clearance()
    az.rebates()
    az.store_stock("7602", id="100123563")
    base = "/api/v1/autozone/"
    assert seen == [
        (base + "search", {"query": "brake pads"}, 240.0),
        (base + "search", {"query": "5w-30", "sort": "price_asc",
                           "filters": {"position_name_s": "Front"}, "min_price": 20,
                           "max_price": 40}, 240.0),
        (base + "search", {"query": "spark plugs", "brand": "NGK"}, 240.0),
        (base + "search", {"query": "pastilha de freio", "country": "br"}, 240.0),
        (base + "product", {"id": "1399158"}, 240.0),
        (base + "product", {"id": "100123563", "country": "br"}, 240.0),
        (base + "product", {"url": "https://www.autozone.com/p/duralast-floor-jack-d3thj/1399158"},
         240.0),
        (base + "category", {"category": "/brakes-and-traction-control/brake-pads",
                             "vehicle": {"year": 2018, "make": "Ford", "model": "F-150"}}, 240.0),
        (base + "category", {"category": "/batteries-starting-and-charging/battery",
                             "sort": "price_desc"}, 240.0),
        (base + "brand", {"brand": "duralast"}, 240.0),
        (base + "brand", {"brand": "duralast-gold",
                          "category": "/brakes-and-traction-control/brake-rotor"}, 240.0),
        (base + "vehicles", {}, 240.0),
        (base + "vehicles", {"level": "models", "year": 2018, "make_id": 54}, 240.0),
        (base + "vehicles", {"level": "makes", "year": 2020, "country": "mx"}, 240.0),
        (base + "reviews", {"id": "1399158"}, 240.0),
        (base + "reviews", {"id": "906340", "page": 2, "sort": "most_helpful", "stars": [1, 2]},
         240.0),
        (base + "stores", {}, 240.0),
        (base + "stores", {"state": "tx", "city": "houston"}, 240.0),
        (base + "stores", {"country": "br", "state": "sao-paulo"}, 240.0),
        (base + "store", {"slug": "vt/barre/18-overlook-dr.html"}, 240.0),
        (base + "store", {"url": "https://www.autozone.com.mx/ubicaciones/nl/monterrey/x.html"},
         240.0),
        (base + "categories", {"country": "br"}, 240.0),
        (base + "clearance", {}, 240.0),
        (base + "rebates", {}, 240.0),
        (base + "store-stock", {"store_number": "7602", "id": "100123563"}, 240.0),
    ]
    for call in (az.product, az.reviews, az.store):
        with pytest.raises(ScavioError):
            call()
    with pytest.raises(ScavioError):
        az.store_stock("7602")


def test_instacart_credits_paths_and_wire(monkeypatch):
    """instacart (0.77.0): 11 endpoints on /api/v1/instacart.

    1 credit each; search 3 (2 when the page fits in Instacart's first answer) and cross_search
    3 for up to 5 stores, 4 for 6 to 10 (credits_note; credits is the floor). Every endpoint
    takes a zip except reviews; us everywhere, ca everywhere except cross_search and reviews
    (those take no country). language fr is Canada only and not offered on suggestions.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "instacart"}
    assert sorted(eps) == [
        "categories", "category", "cross_search", "deals", "price_compare", "product",
        "retailers", "reviews", "search", "stores", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/instacart/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "Instacart (instacart.com, the US and Canada grocery delivery and pickup " \
            "marketplace)" in ep.summary, ep.key
        names = {p.name: p for p in ep.params}
        if m == "reviews":
            assert "zip" not in names
        else:
            assert names["zip"].required and names["zip"].annotation == "Union[str, int]", m
        if m in ("cross_search", "reviews"):
            assert "country" not in names and "language" not in names, m
        else:
            assert names["country"].annotation == 'Optional[Literal["us", "ca"]]', m
        if m == "suggestions":
            assert "language" not in names
        elif m not in ("cross_search", "reviews"):
            assert names["language"].annotation == 'Optional[Literal["en", "fr"]]', m
        if m in ("search", "categories", "category", "deals", "stores"):
            assert names["retailer"].required, m
        if m in ("product", "suggestions"):
            assert not names["retailer"].required, m
        if m in ("search", "product", "category", "deals"):
            assert names["service_type"].annotation == (
                'Optional[Literal["delivery", "pickup", "instore"]]'
            ), m
            assert "priced_for" in ep.summary and "shelf price" in ep.summary, m
    assert eps["search"].credits == 2
    assert eps["search"].credits_note == (
        "Costs 3 credits (2 when the page fits in Instacart's first answer)."
    )
    assert eps["cross_search"].credits == 3
    assert eps["cross_search"].credits_note == (
        "Costs 3 credits for up to 5 stores (max_retailers), 4 for 6 to 10."
    )
    for m in ("retailers", "product", "price_compare", "categories", "category", "deals",
              "stores", "suggestions", "reviews"):
        assert eps[m].credits == 1 and eps[m].credits_note is None, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == 'Optional[Literal["best_match", "price_asc", "price_desc"]]'
    assert search["on_sale"].annotation == "Optional[bool]"
    assert "service_type" not in {p.name for p in eps["price_compare"].params}
    assert "No reviewer name" in eps["reviews"].summary
    assert "us only" in eps["cross_search"].summary and "us only" in eps["reviews"].summary
    assert "coupons" in eps["search"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ic = client.instacart
    ic.retailers("10001")
    ic.retailers("M5V 2T6", country="ca", language="fr")
    ic.search("yogurt", "jewel-osco", "60540", limit=10)
    ic.search("milk", "costco", 10001, service_type="instore", sort="price_asc", on_sale=True,
              brand_id="18514", page=2)
    ic.search("lait", "metro", "H2X1Y4", country="ca", language="fr", limit=10)
    ic.cross_search("milk", "10001", max_retailers=3)
    ic.cross_search("eggs", "10001", max_retailers=10, items_per_retailer=20)
    ic.product("16408559", "10001", retailer="wegmans")
    ic.product("16408559", "60540", retailer="jewel-osco", service_type="pickup")
    ic.price_compare("16408559", "10001")
    ic.categories("wegmans", "10001")
    ic.category("produce", "wegmans", "10001", limit=10)
    ic.deals("jewel-osco", "60540", limit=10)
    ic.stores("jewel-osco", "60540", limit=5)
    ic.suggestions("eg", "60540", retailer="jewel-osco")
    ic.suggestions("eg", "60540")
    ic.reviews("16408559")
    ic.reviews("16408559", page=2)
    base = "/api/v1/instacart/"
    assert seen == [
        (base + "retailers", {"zip": "10001"}, 240.0),
        (base + "retailers", {"zip": "M5V 2T6", "country": "ca", "language": "fr"}, 240.0),
        (base + "search", {"query": "yogurt", "retailer": "jewel-osco", "zip": "60540",
                           "limit": 10}, 240.0),
        (base + "search", {"query": "milk", "retailer": "costco", "zip": 10001,
                           "service_type": "instore", "sort": "price_asc", "on_sale": True,
                           "brand_id": "18514", "page": 2}, 240.0),
        (base + "search", {"query": "lait", "retailer": "metro", "zip": "H2X1Y4",
                           "country": "ca", "language": "fr", "limit": 10}, 240.0),
        (base + "cross-search", {"query": "milk", "zip": "10001", "max_retailers": 3}, 240.0),
        (base + "cross-search", {"query": "eggs", "zip": "10001", "max_retailers": 10,
                                 "items_per_retailer": 20}, 240.0),
        (base + "product", {"product_id": "16408559", "zip": "10001", "retailer": "wegmans"},
         240.0),
        (base + "product", {"product_id": "16408559", "zip": "60540", "retailer": "jewel-osco",
                            "service_type": "pickup"}, 240.0),
        (base + "price-compare", {"product_id": "16408559", "zip": "10001"}, 240.0),
        (base + "categories", {"retailer": "wegmans", "zip": "10001"}, 240.0),
        (base + "category", {"category": "produce", "retailer": "wegmans", "zip": "10001",
                             "limit": 10}, 240.0),
        (base + "deals", {"retailer": "jewel-osco", "zip": "60540", "limit": 10}, 240.0),
        (base + "stores", {"retailer": "jewel-osco", "zip": "60540", "limit": 5}, 240.0),
        (base + "suggestions", {"query": "eg", "zip": "60540", "retailer": "jewel-osco"}, 240.0),
        (base + "suggestions", {"query": "eg", "zip": "60540"}, 240.0),
        (base + "reviews", {"product_id": "16408559"}, 240.0),
        (base + "reviews", {"product_id": "16408559", "page": 2}, 240.0),
    ]


def test_oreilly_credits_paths_and_wire(monkeypatch):
    """oreilly (0.78.0): 14 endpoints on /api/v1/oreilly.

    2 credits each; product by line_code + part_number 4, cross_reference 2 / 4 / 6 by inputs,
    brand index 4, store_stock and stores by zip 4 (credits_note; credits is the floor); deals 4.
    Only stores and store take country (us | mx); the rest are us only and take no country.
    Lists are 24 a page, pages 1-20.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "oreilly"}
    assert sorted(eps) == [
        "brand", "categories", "category", "compatibility", "cross_reference", "deals",
        "product", "rebates", "search", "store", "store_stock", "stores", "suggestions",
        "vehicles",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/oreilly/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "O'Reilly" in ep.summary, ep.key
        country = {p.name: p for p in ep.params}.get("country")
        if m in ("stores", "store"):
            assert country.annotation == 'Optional[Literal["us", "mx"]]', m
        else:
            assert country is None, m
    for m in ("search", "category", "brand", "cross_reference"):
        page = {p.name: p for p in eps[m].params}["page"]
        assert page.annotation == "Optional[int]", m
        assert "1-20" in page.doc, m
    for m in ("search", "category"):
        names = [p.name for p in eps[m].params]
        assert names[1:] == ["page", "sort", "brand", "availability", "filters", "vehicle"], m
    sort = {p.name: p for p in eps["search"].params}["sort"]
    assert sort.annotation == (
        'Optional[Literal["relevance", "price_desc", "price_asc", "best_selling", "brand"]]'
    )
    for m in ("search", "vehicles", "compatibility", "category", "categories", "store",
              "suggestions", "rebates"):
        assert eps[m].credits == 2 and eps[m].credits_note is None, m
    assert eps["deals"].credits == 4 and eps["deals"].credits_note is None
    assert eps["product"].credits_note == "Costs 2 credits by url, 4 by line_code + part_number."
    assert eps["cross_reference"].credits_note == (
        "Costs 2 credits with part_type_id and manufacturer, 4 with one of them or when "
        "several manufacturers use the number, 6 with neither when one manufacturer matches."
    )
    assert eps["brand"].credits_note == (
        "Costs 2 credits for one brand, 4 for the brand index (no brand)."
    )
    assert eps["store_stock"].credits_note == (
        "Costs 4 credits with zip, 2 with latitude + longitude."
    )
    assert eps["stores"].credits_note == (
        "Costs 4 credits near a zip, 2 near latitude + longitude or by state (+ city)."
    )
    assert eps["product"].one_of == (("url", "part_number"),)
    assert eps["store_stock"].one_of == (("zip", "latitude"),)
    assert eps["stores"].one_of == (("zip", "latitude", "state"),)
    assert eps["store"].one_of == (("store_id", "url", "store_number"),)
    for m in ("compatibility", "store_stock"):
        req = [p.name for p in eps[m].params if p.required]
        assert req == ["line_code", "part_number"], m
    assert {p.name: p for p in eps["stores"].params}["latitude"].annotation == "Optional[float]"
    for m in ("search", "cross_reference", "product", "category", "brand"):
        assert "priced_for" in eps[m].summary, m
        assert "never report a price as national" in eps[m].summary, m
    assert "never False" in eps["product"].summary
    assert "10 most recent" in eps["product"].summary
    assert "not unit counts" in eps["store_stock"].summary
    assert "Spanish" in eps["stores"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    o = client.oreilly
    o.search("brake pads")
    o.search("brake pads", vehicle={"base_vehicle_id": 129927}, sort="price_asc", page=2,
             availability="store_pickup", brand="Wagner_OEX",
             filters={"/attributes/prodAttr_32769": "104088"})
    o.cross_reference("PH3614")
    o.cross_reference("PH3614", part_type_id="02269", manufacturer="FRAM")
    o.product("https://www.oreillyauto.com/detail/c/brakebest-select-brake-pads/"
              "brakebest-select-ceramic-brake-pads/bsg0/sc1001")
    o.product(line_code="BB", part_number="SC1001", vehicle={"base_vehicle_id": 129927})
    o.vehicles()
    o.vehicles(level="resolve", year=2015, make_id=23076, model_id=31549)
    o.vehicles(level="vin", vin="1HGCM82633A004352")
    o.compatibility("BB", "SC1001")
    o.compatibility("BB", "SC1001", make="Ford")
    o.category("/shop/b/brakes/brake-pads---shoes/brake-pads/a99314144bb6",
               vehicle={"base_vehicle_id": 129927})
    o.categories()
    o.categories(root="95397663b44a")
    o.brand()
    o.brand("https://www.oreillyauto.com/shop/brands/a/3m/mmm", sort="best_selling")
    o.store_stock("BB", "SC1001", zip="77002")
    o.store_stock("BB", "SC1001", latitude=29.75, longitude=-95.36, quantity=2)
    o.stores(zip="77002")
    o.stores(state="mo", city="springfield")
    o.stores(state="jal", country="mx")
    o.store("4973")
    o.store(store_number="7601", state="jal", city="guadalajara", country="mx")
    o.suggestions("brake")
    o.rebates()
    o.deals()
    base = "/api/v1/oreilly/"
    assert seen == [
        (base + "search", {"query": "brake pads"}, 240.0),
        (base + "search", {"query": "brake pads", "page": 2, "sort": "price_asc",
                           "brand": "Wagner_OEX", "availability": "store_pickup",
                           "filters": {"/attributes/prodAttr_32769": "104088"},
                           "vehicle": {"base_vehicle_id": 129927}}, 240.0),
        (base + "cross-reference", {"part_number": "PH3614"}, 240.0),
        (base + "cross-reference", {"part_number": "PH3614", "part_type_id": "02269",
                                    "manufacturer": "FRAM"}, 240.0),
        (base + "product", {"url": "https://www.oreillyauto.com/detail/c/brakebest-select-brake-"
                                   "pads/brakebest-select-ceramic-brake-pads/bsg0/sc1001"}, 240.0),
        (base + "product", {"line_code": "BB", "part_number": "SC1001",
                            "vehicle": {"base_vehicle_id": 129927}}, 240.0),
        (base + "vehicles", {}, 240.0),
        (base + "vehicles", {"level": "resolve", "year": 2015, "make_id": 23076,
                             "model_id": 31549}, 240.0),
        (base + "vehicles", {"level": "vin", "vin": "1HGCM82633A004352"}, 240.0),
        (base + "compatibility", {"line_code": "BB", "part_number": "SC1001"}, 240.0),
        (base + "compatibility", {"line_code": "BB", "part_number": "SC1001", "make": "Ford"},
         240.0),
        (base + "category", {"category": "/shop/b/brakes/brake-pads---shoes/brake-pads/"
                                         "a99314144bb6",
                             "vehicle": {"base_vehicle_id": 129927}}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"root": "95397663b44a"}, 240.0),
        (base + "brand", {}, 240.0),
        (base + "brand", {"brand": "https://www.oreillyauto.com/shop/brands/a/3m/mmm",
                          "sort": "best_selling"}, 240.0),
        (base + "store-stock", {"line_code": "BB", "part_number": "SC1001", "zip": "77002"},
         240.0),
        (base + "store-stock", {"line_code": "BB", "part_number": "SC1001", "latitude": 29.75,
                                "longitude": -95.36, "quantity": 2}, 240.0),
        (base + "stores", {"zip": "77002"}, 240.0),
        (base + "stores", {"state": "mo", "city": "springfield"}, 240.0),
        (base + "stores", {"state": "jal", "country": "mx"}, 240.0),
        (base + "store", {"store_id": "4973"}, 240.0),
        (base + "store", {"store_number": "7601", "state": "jal", "city": "guadalajara",
                          "country": "mx"}, 240.0),
        (base + "suggestions", {"query": "brake"}, 240.0),
        (base + "rebates", {}, 240.0),
        (base + "deals", {}, 240.0),
    ]
    with pytest.raises(ScavioError):
        o.product()
    with pytest.raises(ScavioError):
        o.store_stock("BB", "SC1001")
    with pytest.raises(ScavioError):
        o.stores()
    with pytest.raises(ScavioError):
        o.store()


def test_acehardware_credits_paths_and_wire(monkeypatch):
    """acehardware (0.79.0): 11 endpoints on /api/v1/acehardware, US only (no country).

    search 2 (3 on a category redirect), product 2, store_stock 1 per 5 stores (nearby 6),
    stores 1 (details 1 lookup per store) (credits_note; credits is the floor); the rest 1.
    Store numbers are 5-digit strings with leading zeros kept.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "acehardware"}
    assert sorted(eps) == [
        "brand", "categories", "category", "deals", "paint_colors", "product", "search",
        "store", "store_stock", "stores", "weekly_ad",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/acehardware/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "Ace" in ep.summary, ep.key
        assert "country" not in {p.name for p in ep.params}, m
    for m in ("search", "category"):
        names = [p.name for p in eps[m].params]
        assert names[1:] == ["page", "page_size", "sort", "brand", "offer", "on_sale", "filters"], m
    assert [p.name for p in eps["deals"].params] == [
        "page", "page_size", "sort", "brand", "offer", "on_sale", "filters",
    ]
    assert "brand" not in [p.name for p in eps["brand"].params][1:]
    sort = {p.name: p for p in eps["search"].params}["sort"]
    assert sort.annotation == (
        'Optional[Literal["relevance", "price_asc", "price_desc", "name_asc", "name_desc", '
        '"newest", "oldest"]]'
    )
    size = {p.name: p for p in eps["search"].params}["page_size"]
    assert size.annotation == "Optional[Literal[15, 30, 50, 100, 200]]"
    assert eps["search"].credits == 2
    assert eps["search"].credits_note == (
        "Costs 2 credits (3 when Ace redirects the search to a category and the list options "
        "are applied to it)."
    )
    assert eps["product"].credits == 2 and eps["product"].credits_note is None
    assert eps["store_stock"].credits_note == (
        "Costs 1 credit per 5 stores (1 store 1, 5 stores 1, 25 stores 5; nearby 6)."
    )
    assert eps["stores"].credits_note == (
        "Costs 1 credit without details; with details 1 lookup per store (25 stores 6 credits)."
    )
    for m in ("store", "category", "categories", "brand", "deals", "weekly_ad", "paint_colors"):
        assert eps[m].credits == 1 and eps[m].credits_note is None, m
        assert "occasional call costs 2" in eps[m].summary, m
    assert eps["product"].one_of == (("product_code", "url"),)
    assert eps["store_stock"].one_of == (("store", "stores"),)
    for m in ("store", "stores", "weekly_ad"):
        store = {p.name: p for p in eps[m].params}["store"]
        assert store.required and store.annotation == "Union[str, int]", m
        assert "leading zeros" in store.doc, m
    for m in ("search", "category", "brand", "deals"):
        assert "not a store's price" in eps[m].summary, m
    assert "priced_for" in eps["product"].summary
    assert "exactly as for one out of stock" in eps["store_stock"].summary
    assert "no public store search by ZIP" in eps["stores"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    a = client.acehardware
    a.search("brass hose nozzle")
    a.search("cordless drill", page=2, page_size=50, sort="price_asc", brand="dewalt",
             offer="sale", filters=["tenant~A00317:lithium-ion"])
    a.product("72779")
    a.product("72779", store="03085")
    a.product(url="https://www.acehardware.com/p/72779", store="10665")
    a.store_stock("72779", stores=["18250", "17309"])
    a.store_stock("72779", store="18250", nearby=True)
    a.store("18250")
    a.stores("03085", details=True, limit=4)
    a.category("/departments/tools/power-tools/cordless-drills", sort="newest")
    a.categories()
    a.categories("/departments/tools")
    a.brand()
    a.brand(query="web")
    a.brand("weber", on_sale=True)
    a.deals(offer="ace_rewards")
    a.weekly_ad("18250")
    a.weekly_ad("18250", page=2, ad_group="261101_WCAS")
    a.paint_colors(query="pink")
    a.paint_colors(brand="Benjamin Moore", page=2, page_size=500)
    base = "/api/v1/acehardware/"
    assert seen == [
        (base + "search", {"query": "brass hose nozzle"}, 240.0),
        (base + "search", {"query": "cordless drill", "page": 2, "page_size": 50,
                           "sort": "price_asc", "brand": "dewalt", "offer": "sale",
                           "filters": ["tenant~A00317:lithium-ion"]}, 240.0),
        (base + "product", {"product_code": "72779"}, 240.0),
        (base + "product", {"product_code": "72779", "store": "03085"}, 240.0),
        (base + "product", {"url": "https://www.acehardware.com/p/72779", "store": "10665"},
         240.0),
        (base + "store-stock", {"product_code": "72779", "stores": ["18250", "17309"]}, 240.0),
        (base + "store-stock", {"product_code": "72779", "store": "18250", "nearby": True},
         240.0),
        (base + "store", {"store": "18250"}, 240.0),
        (base + "stores", {"store": "03085", "details": True, "limit": 4}, 240.0),
        (base + "category", {"category": "/departments/tools/power-tools/cordless-drills",
                             "sort": "newest"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"category": "/departments/tools"}, 240.0),
        (base + "brand", {}, 240.0),
        (base + "brand", {"query": "web"}, 240.0),
        (base + "brand", {"brand": "weber", "on_sale": True}, 240.0),
        (base + "deals", {"offer": "ace_rewards"}, 240.0),
        (base + "weekly-ad", {"store": "18250"}, 240.0),
        (base + "weekly-ad", {"store": "18250", "page": 2, "ad_group": "261101_WCAS"}, 240.0),
        (base + "paint-colors", {"query": "pink"}, 240.0),
        (base + "paint-colors", {"brand": "Benjamin Moore", "page": 2, "page_size": 500},
         240.0),
    ]
    with pytest.raises(ScavioError):
        a.product()
    with pytest.raises(ScavioError):
        a.store_stock("72779")


def test_tractorsupply_credits_paths_and_wire(monkeypatch):
    """tractorsupply (0.80.0): 12 endpoints on /api/v1/tractorsupply, US only (no country).

    1 credit each; product 2 on the first call for a store not yet looked up, store_prices 1 per
    5 lookups (credits_note; credits is the floor). Search, product, category, brand and deals
    need store or zip; store_prices and store_stock need stores, store or zip.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "tractorsupply"}
    assert sorted(eps) == [
        "brand", "categories", "category", "deals", "fulfillment", "product", "promotions",
        "search", "store", "store_prices", "store_stock", "stores",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/tractorsupply/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "Tractor Supply" in ep.summary, ep.key
        assert "country" not in {p.name for p in ep.params}, m
        assert ep.credits == 1, m
    list_tail = ["page", "page_size", "sort", "brand", "on_sale", "new", "pickup", "rating",
                 "filters", "store", "zip"]
    for m in ("search", "category"):
        assert [p.name for p in eps[m].params][1:] == list_tail, m
    assert [p.name for p in eps["brand"].params] == ["brand", "query"] + [
        n for n in list_tail if n != "brand"
    ]
    assert [p.name for p in eps["deals"].params] == ["type", "query"] + [
        n for n in list_tail if n not in ("on_sale", "new")
    ]
    sort = {p.name: p for p in eps["search"].params}["sort"]
    assert sort.annotation == (
        'Optional[Literal["popular", "rating", "name_asc", "name_desc", "price_asc", '
        '"price_desc", "recent", "new_arrivals"]]'
    )
    size = {p.name: p for p in eps["search"].params}["page_size"]
    assert size.annotation == "Optional[Literal[24, 48, 96, 200]]"
    deal_type = {p.name: p for p in eps["deals"].params}["type"]
    assert deal_type.annotation == 'Optional[Literal["sale", "new"]]'
    assert eps["product"].credits_note == (
        "Costs 1 credit (2 on the first call for a store not yet looked up; credits_used is what "
        "was charged)."
    )
    assert eps["store_prices"].credits_note == (
        "Costs 1 credit per 5 lookups (each store's price, a store's details when not yet "
        "known, the item): 25 new stores cost 11."
    )
    for m in eps:
        if m not in ("product", "store_prices"):
            assert eps[m].credits_note is None, m
    for m in ("search", "category", "brand", "deals"):
        assert eps[m].one_of == (("store", "zip"),), m
        assert "priced_for" in eps[m].summary, m
    assert eps["product"].one_of == (("item_number", "url"), ("store", "zip"))
    for m in ("store_prices", "store_stock"):
        assert eps[m].one_of == (("stores", "store", "zip"),), m
        assert [p.name for p in eps[m].params] == ["item_number", "stores", "store", "zip",
                                                   "limit"], m
    fp = {p.name: p for p in eps["fulfillment"].params}
    assert fp["item_number"].required and fp["store"].required and fp["zip"].required
    assert "mapp" in eps["product"].summary
    assert "in_transit" in eps["store_stock"].summary
    assert "not a promise" in eps["store_stock"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    t = client.tractorsupply
    t.search("layer pellets", store="1933")
    t.search("dog food", zip="59330", page=2, page_size=48, sort="price_asc", brand="Purina",
             on_sale=True, pickup=True, rating=4, filters=["2bb%3A%2250%20lb%22"])
    t.product("2340147", store="1933")
    t.product(url="https://www.tractorsupply.com/tsc/product/x-2340147", zip="59330")
    t.store_prices("2340147", stores=["1933", "1923"])
    t.store_prices("2340147", zip="59301", limit=10)
    t.store_stock("2340147", store="1933")
    t.store_stock("2340147", zip="59301")
    t.fulfillment("2340147", "1933", "59330", quantity=2)
    t.stores("59301", limit=3)
    t.store("1933")
    t.category("/tsc/catalog/poultry-feed", store="1933", sort="new_arrivals")
    t.categories()
    t.categories("1004851")
    t.brand("Producer's Pride", store="1933", query="feed")
    t.deals(store="1933")
    t.deals(type="new", zip="59330", query="boots")
    t.promotions("3609112")
    base = "/api/v1/tractorsupply/"
    assert seen == [
        (base + "search", {"query": "layer pellets", "store": "1933"}, 240.0),
        (base + "search", {"query": "dog food", "page": 2, "page_size": 48, "sort": "price_asc",
                           "brand": "Purina", "on_sale": True, "pickup": True, "rating": 4,
                           "filters": ["2bb%3A%2250%20lb%22"], "zip": "59330"}, 240.0),
        (base + "product", {"item_number": "2340147", "store": "1933"}, 240.0),
        (base + "product", {"url": "https://www.tractorsupply.com/tsc/product/x-2340147",
                            "zip": "59330"}, 240.0),
        (base + "store-prices", {"item_number": "2340147", "stores": ["1933", "1923"]}, 240.0),
        (base + "store-prices", {"item_number": "2340147", "zip": "59301", "limit": 10}, 240.0),
        (base + "store-stock", {"item_number": "2340147", "store": "1933"}, 240.0),
        (base + "store-stock", {"item_number": "2340147", "zip": "59301"}, 240.0),
        (base + "fulfillment", {"item_number": "2340147", "store": "1933", "zip": "59330",
                                "quantity": 2}, 240.0),
        (base + "stores", {"zip": "59301", "limit": 3}, 240.0),
        (base + "store", {"store": "1933"}, 240.0),
        (base + "category", {"category": "/tsc/catalog/poultry-feed", "sort": "new_arrivals",
                             "store": "1933"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"parent_id": "1004851"}, 240.0),
        (base + "brand", {"brand": "Producer's Pride", "query": "feed", "store": "1933"}, 240.0),
        (base + "deals", {"store": "1933"}, 240.0),
        (base + "deals", {"type": "new", "query": "boots", "zip": "59330"}, 240.0),
        (base + "promotions", {"item_number": "3609112"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        t.search("layer pellets")
    with pytest.raises(ScavioError):
        t.product("2340147")
    with pytest.raises(ScavioError):
        t.product(store="1933")
    with pytest.raises(ScavioError):
        t.store_prices("2340147")
    with pytest.raises(ScavioError):
        t.store_stock("2340147")
    with pytest.raises(ScavioError):
        t.deals()


def test_michaels_credits_paths_and_wire(monkeypatch):
    """michaels (0.81.0): 11 endpoints on /api/v1/michaels.

    2 credits each; category and deals 4 with a /shop/ category (credits_note; credits is the
    floor). country us | ca and language en | fr everywhere except stores, categories and
    suggestions (us only: no country there). query is sent as q.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "michaels"}
    assert sorted(eps) == [
        "brand", "categories", "category", "deals", "product", "search", "store",
        "store_inventory", "store_stock", "stores", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/michaels/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "Michaels (michaels.com, the US and Canada arts and crafts retailer)" in ep.summary
        assert ep.credits == 2, m
        names = {p.name: p for p in ep.params}
        if m in ("stores", "categories", "suggestions"):
            assert "country" not in names and "language" not in names, m
            assert "us only" in ep.summary, m
        else:
            assert names["country"].annotation == 'Optional[Literal["us", "ca"]]', m
            assert names["language"].annotation == 'Optional[Literal["en", "fr"]]', m
        if "query" in names:
            assert names["query"].wire_field == "q", m
    for m in ("category", "deals"):
        assert eps[m].credits_note == (
            "Costs 2 credits with a category code path, 4 with a /shop/ link or path (one more "
            "call finds its code path; credits_used is what was charged)."
        ), m
    for m in eps:
        if m not in ("category", "deals"):
            assert eps[m].credits_note is None, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["best_match", "best_sellers", "new_arrivals", "price_asc", '
        '"price_desc", "rating"]]'
    )
    assert search["seller"].annotation == (
        'Optional[Literal["michaels", "marketplace", "michaels_pro"]]'
    )
    assert search["filters"].annotation == "Optional[dict[str, Union[str, list[str]]]]"
    assert search["min_price"].annotation == "Optional[float]"
    deals = {p.name for p in eps["deals"].params}
    assert not deals & {"on_sale", "new", "clearance", "great_buy"}
    deal_type = {p.name: p for p in eps["deals"].params}["type"]
    assert deal_type.annotation == 'Optional[Literal["sale", "new", "clearance", "great_buy"]]'
    assert eps["product"].one_of == (("sku", "url"),)
    assert eps["deals"].one_of == (("query", "category"),)
    assert eps["stores"].one_of == (("zip", "city", "latitude"),)
    inv = {p.name: p for p in eps["store_inventory"].params}
    assert inv["store"].required and inv["skus"].required
    assert inv["skus"].annotation == "list[Union[str, int]]"
    assert "online stock, not a store's" in eps["product"].summary
    assert "virtual" in eps["store_stock"].summary
    assert "national per country" in eps["search"].summary
    for word in ("collect", "scrape", "proxy"):
        assert all(word not in ep.summary.lower() for ep in eps.values()), word

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    mi = client.michaels
    mi.search("yarn")
    mi.search("laine", country="ca", language="fr", page=2, page_size=24, sort="price_asc",
              brand="Bernat", on_sale=True, min_price=5.0, filters={"material": ["Acrylic"]})
    mi.product("10228177")
    mi.product(url="https://canada.michaels.com/en/product/x-10816737", country="ca")
    mi.store_stock("10228177", "10001", radius=10)
    mi.store_stock("10519836", "M5V 2T6", country="ca")
    mi.store_inventory("1191", ["10228177", "10816737"])
    mi.stores("60657")
    mi.stores(city="San Francisco, CA", radius=30)
    mi.store("4936", country="ca")
    mi.category("/shop/art-supplies/artist-canvas", sort="best_sellers")
    mi.category("root//Categories//809187838", country="ca", query="acrylic")
    mi.categories()
    mi.categories("/shop/art-supplies")
    mi.brand("Cricut", query="explore")
    mi.deals(query="christmas")
    mi.deals(type="clearance", category="root//Categories//809187838", country="ca")
    mi.suggestions("yarn")
    base = "/api/v1/michaels/"
    assert seen == [
        (base + "search", {"q": "yarn"}, 240.0),
        (base + "search", {"q": "laine", "brand": "Bernat", "page": 2, "page_size": 24,
                           "sort": "price_asc", "min_price": 5.0, "on_sale": True,
                           "filters": {"material": ["Acrylic"]}, "country": "ca",
                           "language": "fr"}, 240.0),
        (base + "product", {"sku": "10228177"}, 240.0),
        (base + "product", {"url": "https://canada.michaels.com/en/product/x-10816737",
                            "country": "ca"}, 240.0),
        (base + "store-stock", {"sku": "10228177", "zip": "10001", "radius": 10}, 240.0),
        (base + "store-stock", {"sku": "10519836", "zip": "M5V 2T6", "country": "ca"}, 240.0),
        (base + "store-inventory", {"store": "1191", "skus": ["10228177", "10816737"]}, 240.0),
        (base + "stores", {"zip": "60657"}, 240.0),
        (base + "stores", {"city": "San Francisco, CA", "radius": 30}, 240.0),
        (base + "store", {"store": "4936", "country": "ca"}, 240.0),
        (base + "category", {"category": "/shop/art-supplies/artist-canvas",
                             "sort": "best_sellers"}, 240.0),
        (base + "category", {"category": "root//Categories//809187838", "q": "acrylic",
                             "country": "ca"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"path": "/shop/art-supplies"}, 240.0),
        (base + "brand", {"brand": "Cricut", "q": "explore"}, 240.0),
        (base + "deals", {"q": "christmas"}, 240.0),
        (base + "deals", {"type": "clearance", "category": "root//Categories//809187838",
                          "country": "ca"}, 240.0),
        (base + "suggestions", {"q": "yarn"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        mi.product()
    with pytest.raises(ScavioError):
        mi.deals()
    with pytest.raises(ScavioError):
        mi.stores()


def test_nike_credits_paths_and_wire(monkeypatch):
    """nike (0.82.0): 8 endpoints on /api/v1/nike.

    1 credit each. country (42 countries, 62 storefronts) + language everywhere; releases /
    release not on vn or cn, reviews not on cn. query is sent as q.
    """
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "nike"}
    assert sorted(eps) == [
        "brand", "category", "deals", "product", "release", "releases", "reviews", "search",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/nike/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert "Nike (nike.com, including Jordan Brand)" in ep.summary, m
        assert ep.credits == 1, m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        assert "country" in names and "language" in names, m
        assert '"zh-Hans"' in names["language"].annotation, m
        if "query" in names:
            assert names["query"].wire_field == "q", m
    countries = {m: {p.name: p for p in ep.params}["country"].annotation for m, ep in eps.items()}
    for m in ("search", "product", "category", "brand", "deals"):
        assert '"cn"' in countries[m] and '"vn"' in countries[m] and '"gb"' in countries[m], m
        assert '"uk"' not in countries[m] and '"br"' not in countries[m], m
    for m in ("releases", "release"):
        assert '"cn"' not in countries[m] and '"vn"' not in countries[m] and '"jp"' in countries[m]
    assert '"cn"' not in countries["reviews"] and '"vn"' in countries["reviews"]
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["featured", "newest", "price_high", "price_low"]]'
    )
    assert search["filter"].annotation == "Optional[Union[str, list[str]]]"
    brand = {p.name: p for p in eps["brand"].params}["brand"]
    assert brand.required and brand.annotation == 'Literal["jordan", "acg", "sb"]'
    view = {p.name: p for p in eps["releases"].params}["view"]
    assert view.annotation == 'Optional[Literal["upcoming", "feed", "in_stock"]]'
    assert eps["product"].one_of == (("style_color", "url"),)
    assert eps["reviews"].one_of == (("style_color", "url"),)
    assert eps["release"].one_of == (("style_color", "url", "slug"),)
    assert eps["category"].one_of == (("path", "url"),)
    for m in ("search", "category", "brand", "deals"):
        assert "First page only" in eps[m].summary, m
    assert "sizes, not stock levels" in eps["product"].summary
    assert "LINE or DRAW" in eps["releases"].summary
    assert "3 newest reviews" in eps["reviews"].summary
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"checkout api|stock checker)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    nk = client.nike
    nk.search("dunk low")
    nk.search("dunk low", country="gb", sort="price_low", filter="black-90poy")
    nk.product("DD1503-103", country="fr")
    nk.product(url="https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/IM6572-104")
    nk.category("mens-shoes-nik1zy7ok", filter=["black-90poy", "mens-nik1"], sort="newest")
    nk.category(url="https://www.nike.com/w/mens-shoes-nik1zy7ok")
    nk.brand("jordan", country="ch", language="fr")
    nk.deals()
    nk.deals(gender="women", category="shoes-y7ok", country="jp", language="en")
    nk.releases()
    nk.releases(view="feed", country="gb")
    nk.release("IX8180-001")
    nk.release(slug="air-jordan-4-bred", country="gb")
    nk.reviews("CW2288-111")
    base = "/api/v1/nike/"
    assert seen == [
        (base + "search", {"q": "dunk low"}, 240.0),
        (base + "search", {"q": "dunk low", "sort": "price_low", "filter": "black-90poy",
                           "country": "gb"}, 240.0),
        (base + "product", {"style_color": "DD1503-103", "country": "fr"}, 240.0),
        (base + "product", {"url": "https://www.nike.com/t/dunk-low-womens-shoes-ppQwKZ/"
                                   "IM6572-104"}, 240.0),
        (base + "category", {"path": "mens-shoes-nik1zy7ok", "sort": "newest",
                             "filter": ["black-90poy", "mens-nik1"]}, 240.0),
        (base + "category", {"url": "https://www.nike.com/w/mens-shoes-nik1zy7ok"}, 240.0),
        (base + "brand", {"brand": "jordan", "country": "ch", "language": "fr"}, 240.0),
        (base + "deals", {}, 240.0),
        (base + "deals", {"gender": "women", "category": "shoes-y7ok", "country": "jp",
                          "language": "en"}, 240.0),
        (base + "releases", {}, 240.0),
        (base + "releases", {"view": "feed", "country": "gb"}, 240.0),
        (base + "release", {"style_color": "IX8180-001"}, 240.0),
        (base + "release", {"slug": "air-jordan-4-bred", "country": "gb"}, 240.0),
        (base + "reviews", {"style_color": "CW2288-111"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        nk.product()
    with pytest.raises(ScavioError):
        nk.release()
    with pytest.raises(ScavioError):
        nk.reviews()
    with pytest.raises(ScavioError):
        nk.category()


def test_staples_credits_paths_and_wire(monkeypatch):
    """staples (0.83.0): 12 endpoints on /api/v1/staples.

    1 credit each. country us | ca + language en | fr on search and product only; the rest are
    US only (no country there). query is sent as q.
    """
    _STP_NAME = "Staples (staples.com, the US office supply retailer; Staples Canada at staples.ca)"
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "staples"}
    assert sorted(eps) == [
        "categories", "category", "coupons", "deals", "product", "questions", "reviews", "search",
        "store", "store_stock", "stores", "trending",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/staples/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert _STP_NAME in ep.summary, m
        assert ep.credits == 1, m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        if m in ("search", "product"):
            assert names["country"].annotation == 'Optional[Literal["us", "ca"]]', m
            assert names["language"].annotation == 'Optional[Literal["en", "fr"]]', m
        else:
            assert "country" not in names and "language" not in names, m
        if "query" in names:
            assert names["query"].wire_field == "q", m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["best_match", "price_low", "price_high", "rating", "newest"]]'
    )
    assert search["brand"].annotation == "Optional[Union[str, list[str]]]"
    assert search["filters"].annotation == "Optional[list[str]]"
    assert search["deal"].annotation == 'Optional[Literal["on_promotion", "clearance"]]'
    reviews = {p.name: p for p in eps["reviews"].params}
    assert reviews["sort"].annotation == (
        'Optional[Literal["most_relevant", "newest", "oldest", "highest_rating", "lowest_rating", '
        '"most_helpful"]]'
    )
    assert eps["product"].one_of == (("item_id", "url", "handle"),)
    assert eps["deals"].one_of == (("query", "category"),)
    assert eps["stores"].one_of == (("zip", "city"),)
    assert "ZIP and store change availability, not price" in eps["search"].summary
    assert "staples.com publishes no UPC" in eps["product"].summary
    assert "only stores that have the item" in eps["store_stock"].summary
    assert "threshold" in eps["store_stock"].summary
    assert "No reviewer names" in eps["reviews"].summary
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"checkout api|stock checker|overpriced|inflated)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    st = client.staples
    st.search("copy paper")
    st.search("copy paper", page=2, sort="price_low", brand=["Hammermill"],
              filters=["Number of Reams_3A_2210-Ream_22"], deal="on_promotion")
    st.search("hp 67", country="ca")
    st.search("papier", country="ca", language="fr")
    st.product("122374")
    st.product(2724258, zip="60540", store="1633")
    st.product(handle="24430098-en-hp-67-black-original-ink-cartridge", country="ca")
    st.product("15332", country="ca", language="fr")
    st.category("CL140691", sort="rating")
    st.categories()
    st.categories(category="SC1676")
    st.deals(query="laptop")
    st.deals(type="clearance", category="CL140691")
    st.coupons(category="Printers")
    st.store_stock("2724258", "60540", radius=50)
    st.stores("10001")
    st.stores(city="Chicago, IL", radius=10)
    st.store("1574")
    st.reviews("24430099", limit=100, sort="newest", rating=5, photos_only=True)
    st.questions("990119", page=2, sort="most_answered")
    st.trending()
    base = "/api/v1/staples/"
    assert seen == [
        (base + "search", {"q": "copy paper"}, 240.0),
        (base + "search", {"q": "copy paper", "page": 2, "sort": "price_low",
                           "brand": ["Hammermill"], "filters": ["Number of Reams_3A_2210-Ream_22"],
                           "deal": "on_promotion"}, 240.0),
        (base + "search", {"q": "hp 67", "country": "ca"}, 240.0),
        (base + "search", {"q": "papier", "country": "ca", "language": "fr"}, 240.0),
        (base + "product", {"item_id": "122374"}, 240.0),
        (base + "product", {"item_id": 2724258, "zip": "60540", "store": "1633"}, 240.0),
        (base + "product", {"handle": "24430098-en-hp-67-black-original-ink-cartridge",
                            "country": "ca"}, 240.0),
        (base + "product", {"item_id": "15332", "country": "ca", "language": "fr"}, 240.0),
        (base + "category", {"category": "CL140691", "sort": "rating"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"category": "SC1676"}, 240.0),
        (base + "deals", {"q": "laptop"}, 240.0),
        (base + "deals", {"type": "clearance", "category": "CL140691"}, 240.0),
        (base + "coupons", {"category": "Printers"}, 240.0),
        (base + "store-stock", {"item_id": "2724258", "zip": "60540", "radius": 50}, 240.0),
        (base + "stores", {"zip": "10001"}, 240.0),
        (base + "stores", {"city": "Chicago, IL", "radius": 10}, 240.0),
        (base + "store", {"store": "1574"}, 240.0),
        (base + "reviews", {"item_id": "24430099", "limit": 100, "sort": "newest", "rating": 5,
                            "photos_only": True}, 240.0),
        (base + "questions", {"item_id": "990119", "page": 2, "sort": "most_answered"}, 240.0),
        (base + "trending", {}, 240.0),
    ]
    with pytest.raises(ScavioError):
        st.product()
    with pytest.raises(ScavioError):
        st.deals()
    with pytest.raises(ScavioError):
        st.stores()


def test_dollartree_credits_paths_and_wire(monkeypatch):
    """dollartree (0.84.0): 10 endpoints on /api/v1/dollartree.

    1 credit each, stores 5. us only (no country) on every method except store, which takes
    country us | ca. query is sent as q. store_stock, stores and reviews get a 300 s floor, the
    rest 240 s.
    """
    _DT_NAME = "Dollar Tree (dollartree.com, the US and Canada discount variety store chain)"
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "dollartree"}
    assert sorted(eps) == [
        "brand", "categories", "category", "deals", "product", "reviews", "search", "store",
        "store_stock", "stores",
    ]
    slow = {"store_stock", "stores", "reviews"}
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/dollartree/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == (300.0 if m in slow else 240.0), ep.key
        assert _DT_NAME in ep.summary, m
        assert ep.credits == (5 if m == "stores" else 1), m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        if m == "store":
            assert names["country"].annotation == 'Optional[Literal["us", "ca"]]', m
        else:
            assert "country" not in names and "language" not in names, m
        if "query" in names:
            assert names["query"].wire_field == "q", m
        if m in slow:
            assert "Slow:" in ep.summary, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_low", "price_high", "newest", "rating"]]'
    )
    assert search["filters"].annotation == "Optional[list[str]]"
    assert search["price_point"].annotation == "Optional[Union[float, str]]"
    assert search["rating"].annotation == "Optional[Literal[1, 2, 3, 4, 5]]"
    deals = {p.name: p for p in eps["deals"].params}
    assert deals["type"].annotation == (
        'Optional[Literal["sale", "clearance", "new", "more_choices"]]'
    )
    assert eps["product"].one_of == (("item_id", "url"),)
    assert eps["reviews"].one_of == (("item_id", "url"),)
    assert eps["store_stock"].one_of == (("item_id", "url"), ("store",))
    assert eps["stores"].one_of == (("zip", "city"),)
    assert eps["store"].one_of == (("url", "slug"),)
    assert "one national online price list" in eps["search"].summary
    assert "in-store shelf prices are not published online" in eps["product"].summary
    assert "case_price is the price of case_pack units" in eps["product"].summary
    assert "does not match UPCs" in eps["search"].summary
    assert "a ZIP alone does not pick a store" in eps["store_stock"].summary
    assert "no reviewer names" in eps["reviews"].summary
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|stock checker)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    dt = client.dollartree
    dt.search("paper plates")
    dt.search("paper plates", category="4070223595", brand="Dixie", page=2, page_size=96,
              sort="price_low", filters=["3543933063"], price_point=1.25, rating=4,
              in_store_only=True, min_price=1, max_price=5)
    dt.product("221159")
    dt.product(url="https://www.dollartree.com/x/221159")
    dt.category("3804024826", query="ornaments", sort="newest")
    dt.categories()
    dt.categories(category=2264625405)
    dt.brand("Dixie", category="4070223595")
    dt.deals()
    dt.deals(type="more_choices", query="mugs")
    dt.store_stock("221159", "5126")
    dt.store_stock("221159", 5126, zip="10035", state="NY")
    dt.stores("60540")
    dt.stores(city="Naperville, IL")
    dt.store("https://locations.dollartree.com/ny/new-york/2182-3rd-avenue")
    dt.store(slug="on/toronto/2340-eglinton-ave-west", country="ca")
    dt.reviews("206652")
    base = "/api/v1/dollartree/"
    assert seen == [
        (base + "search", {"q": "paper plates"}, 240.0),
        (base + "search", {"q": "paper plates", "category": "4070223595", "brand": "Dixie",
                           "page": 2, "page_size": 96, "sort": "price_low",
                           "filters": ["3543933063"], "price_point": 1.25, "rating": 4,
                           "in_store_only": True, "min_price": 1, "max_price": 5}, 240.0),
        (base + "product", {"item_id": "221159"}, 240.0),
        (base + "product", {"url": "https://www.dollartree.com/x/221159"}, 240.0),
        (base + "category", {"category": "3804024826", "q": "ornaments", "sort": "newest"},
         240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"category": 2264625405}, 240.0),
        (base + "brand", {"brand": "Dixie", "category": "4070223595"}, 240.0),
        (base + "deals", {}, 240.0),
        (base + "deals", {"type": "more_choices", "q": "mugs"}, 240.0),
        (base + "store-stock", {"item_id": "221159", "store": "5126"}, 300.0),
        (base + "store-stock", {"item_id": "221159", "store": 5126, "zip": "10035",
                                "state": "NY"}, 300.0),
        (base + "stores", {"zip": "60540"}, 300.0),
        (base + "stores", {"city": "Naperville, IL"}, 300.0),
        (base + "store", {"url": "https://locations.dollartree.com/ny/new-york/2182-3rd-avenue"},
         240.0),
        (base + "store", {"slug": "on/toronto/2340-eglinton-ave-west", "country": "ca"}, 240.0),
        (base + "reviews", {"item_id": "206652"}, 300.0),
    ]
    with pytest.raises(ScavioError):
        dt.product()
    with pytest.raises(ScavioError):
        dt.store_stock("221159")
    with pytest.raises(ScavioError):
        dt.store_stock(store="5126")
    with pytest.raises(ScavioError):
        dt.stores()
    with pytest.raises(ScavioError):
        dt.store()
    with pytest.raises(ScavioError):
        dt.reviews()


def test_discounttire_credits_paths_and_wire(monkeypatch):
    """discounttire (0.85.0): 15 endpoints on /api/v1/discounttire.

    1 credit each, US only (no country on any method). query is sent as q. Every method gets a
    240 s floor. Price methods need store or zip.
    """
    _DTR_NAME = (
        "Discount Tire (discounttire.com, the US tire and wheel retailer, America's Tire in parts "
        "of CA, PA, NJ and NY)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "discounttire"}
    assert sorted(eps) == [
        "appointments", "browse", "categories", "model", "product", "reviews", "search", "store",
        "store_reviews", "store_stock", "stores", "suggestions", "vehicle", "vehicle_tires",
        "wheels",
    ]
    priced = {"search", "vehicle_tires", "product", "model", "wheels", "browse"}
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/discounttire/" + m.replace("_", "-"), ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert _DTR_NAME in ep.summary, m
        assert ep.credits == 1, m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        assert "country" not in names and "language" not in names, m
        if "query" in names:
            assert names["query"].wire_field == "q", m
        if m in priced:
            assert ("store", "zip") in [tuple(g) for g in ep.one_of], m
            assert "Prices, stock and promotions are per store" in ep.summary, m
            assert "$205 at an America's Tire store in New Jersey" in ep.summary, m
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["best_seller", "price_low", "price_high", "rating"]]'
    )
    assert search["brand"].annotation == "Optional[Union[str, list[str]]]"
    assert search["filters"].annotation == "Optional[list[str]]"
    vt = {p.name: p for p in eps["vehicle_tires"].params}
    assert [p.name for p in eps["vehicle_tires"].required_params] == [
        "vehicle_id", "trim_id", "assembly_id",
    ]
    assert vt["sort"].annotation == (
        'Optional[Literal["best_seller", "price_low", "price_high", "rating", "treadwell"]]'
    )
    assert vt["position"].annotation == 'Optional[Literal["set", "front", "rear"]]'
    stock = {p.name: p for p in eps["store_stock"].params}
    assert stock["radius"].annotation == "Optional[Literal[10, 25, 50, 75, 150]]"
    assert eps["store_stock"].one_of == (("item_number", "item_numbers"), ("zip",))
    assert eps["stores"].one_of == (("zip", "city", "latitude"),)
    assert eps["search"].one_of == (("size", "width"), ("store", "zip"))
    assert eps["wheels"].one_of == (("diameter", "vehicle_id"), ("store", "zip"))
    assert eps["browse"].one_of == (("category", "brand", "query"), ("store", "zip"))
    assert "no set-of-four price" in eps["search"].summary
    assert "4 x price is arithmetic" in eps["product"].summary
    assert "Discount Tire's own estimates" in eps["vehicle_tires"].summary
    assert "Available as soon as <date>" in eps["store_stock"].summary
    assert "Scavio never books" in eps["appointments"].summary
    assert "the store's local time" in eps["appointments"].summary
    assert "UTC" not in eps["appointments"].summary
    assert "No reviewer names" in eps["reviews"].summary
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|graphql|robots?|hurry|"
                        r"ends soon|last day|mavis)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    dt = client.discounttire
    dt.search("225/65R17", store="1009")
    dt.search(width=225, aspect_ratio=65, diameter=17, zip="85251", sort="price_low",
              brand=["Michelin"], filters=["brands:brand-MCH"], page=2, page_size=50,
              min_price=100, max_price=300, instant_savings=True, in_stock=True,
              category="All-Season Tires", speed_rating="H", load_range="XL",
              three_peak=True, run_flat=False, rebates=True, mileage_warranty="60,000-70,000")
    dt.search("245/35R19", rear_size="305/30R20", store=1009)
    dt.vehicle()
    dt.vehicle(year=2022, make="Ford")
    dt.vehicle(vehicle_id="17361", trim_id="52455", assembly_id="0000E28B")
    dt.vehicle_tires("17361", "52455", "0000E28B", store="1009")
    dt.vehicle_tires("16990", "51166", "0000DI40", zip="85251", position="front",
                     ranking="treadwell", sort="treadwell")
    dt.product("108547", store="1009")
    dt.product(108547, zip="85251", nearby_stores=["1022", 1003])
    dt.model("michelin-defender-2", store="1009", type="tires")
    dt.store_stock("108547", "85251")
    dt.store_stock(item_numbers=["102019", "102020"], zip=85251, radius=50,
                   sort="availability", page=2, quantity=2, store="1009")
    dt.stores("85251")
    dt.stores(city="Phoenix, AZ", radius=25, page=2)
    dt.stores(latitude=33.47, longitude=-111.92)
    dt.store("1009")
    dt.reviews("108547", scope="size", sort="most_helpful", rating=5, page=3, page_size=50)
    dt.store_reviews(1009, sort="lowest", rating=1, page=2)
    dt.wheels(diameter=20, width=9, bolt_pattern="6-135", store="1009")
    dt.wheels(vehicle_id="17361", trim_id="52455", assembly_id="0000E28B", zip="85251",
              color="Black", special_offers=True)
    dt.browse(category="all-season-tires", store="1009")
    dt.browse(query="michelin defender", zip="85251", sort="relevance")
    dt.categories()
    dt.categories(type="wheels")
    dt.suggestions("michelin")
    dt.appointments("1009", month=12)
    base = "/api/v1/discounttire/"
    assert seen == [
        (base + "search", {"size": "225/65R17", "store": "1009"}, 240.0),
        (base + "search", {"width": 225, "aspect_ratio": 65, "diameter": 17, "zip": "85251",
                           "page": 2, "page_size": 50, "filters": ["brands:brand-MCH"],
                           "brand": ["Michelin"], "min_price": 100, "max_price": 300,
                           "instant_savings": True, "in_stock": True, "sort": "price_low",
                           "category": "All-Season Tires", "speed_rating": "H",
                           "mileage_warranty": "60,000-70,000", "load_range": "XL",
                           "three_peak": True, "run_flat": False, "rebates": True}, 240.0),
        (base + "search", {"size": "245/35R19", "rear_size": "305/30R20", "store": 1009}, 240.0),
        (base + "vehicle", {}, 240.0),
        (base + "vehicle", {"year": 2022, "make": "Ford"}, 240.0),
        (base + "vehicle", {"vehicle_id": "17361", "trim_id": "52455",
                            "assembly_id": "0000E28B"}, 240.0),
        (base + "vehicle-tires", {"vehicle_id": "17361", "trim_id": "52455",
                                  "assembly_id": "0000E28B", "store": "1009"}, 240.0),
        (base + "vehicle-tires", {"vehicle_id": "16990", "trim_id": "51166",
                                  "assembly_id": "0000DI40", "position": "front",
                                  "ranking": "treadwell", "zip": "85251",
                                  "sort": "treadwell"}, 240.0),
        (base + "product", {"item_number": "108547", "store": "1009"}, 240.0),
        (base + "product", {"item_number": 108547, "nearby_stores": ["1022", 1003],
                            "zip": "85251"}, 240.0),
        (base + "model", {"model_id": "michelin-defender-2", "type": "tires", "store": "1009"},
         240.0),
        (base + "store-stock", {"item_number": "108547", "zip": "85251"}, 240.0),
        (base + "store-stock", {"zip": 85251, "item_numbers": ["102019", "102020"],
                                "radius": 50, "sort": "availability", "page": 2,
                                "quantity": 2, "store": "1009"}, 240.0),
        (base + "stores", {"zip": "85251"}, 240.0),
        (base + "stores", {"city": "Phoenix, AZ", "radius": 25, "page": 2}, 240.0),
        (base + "stores", {"latitude": 33.47, "longitude": -111.92}, 240.0),
        (base + "store", {"store_code": "1009"}, 240.0),
        (base + "reviews", {"item_number": "108547", "scope": "size", "sort": "most_helpful",
                            "rating": 5, "page": 3, "page_size": 50}, 240.0),
        (base + "store-reviews", {"store_code": 1009, "sort": "lowest", "rating": 1,
                                  "page": 2}, 240.0),
        (base + "wheels", {"diameter": 20, "width": 9, "bolt_pattern": "6-135",
                           "store": "1009"}, 240.0),
        (base + "wheels", {"vehicle_id": "17361", "trim_id": "52455",
                           "assembly_id": "0000E28B", "color": "Black",
                           "special_offers": True, "zip": "85251"}, 240.0),
        (base + "browse", {"category": "all-season-tires", "store": "1009"}, 240.0),
        (base + "browse", {"q": "michelin defender", "sort": "relevance", "zip": "85251"},
         240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"type": "wheels"}, 240.0),
        (base + "suggestions", {"q": "michelin"}, 240.0),
        (base + "appointments", {"store_code": "1009", "month": 12}, 240.0),
    ]
    with pytest.raises(ScavioError):
        dt.search("225/65R17")
    with pytest.raises(ScavioError):
        dt.search(store="1009")
    with pytest.raises(ScavioError):
        dt.product("108547")
    with pytest.raises(ScavioError):
        dt.vehicle_tires("17361", "52455", "0000E28B")
    with pytest.raises(ScavioError):
        dt.store_stock("108547")
    with pytest.raises(ScavioError):
        dt.store_stock(zip="85251")
    with pytest.raises(ScavioError):
        dt.stores()
    with pytest.raises(ScavioError):
        dt.wheels(store="1009")
    with pytest.raises(ScavioError):
        dt.browse(store="1009")


def test_vevor_credits_paths_and_wire(monkeypatch):
    """vevor (0.86.0): 11 endpoints on /api/v1/vevor.

    1 credit each, prices 3. country + language on every method except prices (sku only).
    query is sent as q. Every method gets a 240 s floor.
    """
    _VEV_FIRST = (
        "VEVOR (vevor.com, the tools and equipment seller with storefronts in 13 countries)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "vevor"}
    assert sorted(eps) == [
        "categories", "category", "collections", "deals", "prices", "product", "questions",
        "reviews", "search", "shipping", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/vevor/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == (3 if m == "prices" else 1), m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        if m == "prices":
            assert list(names) == ["sku"], m
        else:
            assert names["country"].annotation == (
                'Optional[Literal["us", "ca", "gb", "au", "de", "fr", "es", "it", "nl", "pl", '
                '"mx", "no", "eu"]]'
            ), m
            assert "language" in names, m
        if "query" in names:
            assert names["query"].wire_field == "q", m
    assert _VEV_FIRST in eps["search"].summary
    for m in ("search", "product", "category", "collections", "deals"):
        assert "was_price is given only while a VEVOR deal is active" in eps[m].summary, m
        assert "price and stock do not change by ZIP or state" in eps[m].summary, m
    assert "Coupon codes" not in eps["search"].summary
    assert "coupon codes (VEVOR shows them only after a claim)" in eps["search"].summary
    assert "coupon codes are not included" in eps["deals"].summary
    assert "Country us needs state" in eps["shipping"].summary
    assert "$130 fee" in eps["shipping"].summary
    assert "No reviewer names" in eps["reviews"].summary
    assert "many languages" in eps["reviews"].summary
    assert "195.01 USD on us" in eps["prices"].summary
    assert "721.90 PLN on pl" in eps["prices"].summary
    assert eps["product"].one_of == (("sku", "url"),)
    assert [p.name for p in eps["category"].required_params] == ["category"]
    search = {p.name: p for p in eps["search"].params}
    assert search["sort"].annotation == (
        'Optional[Literal["popular", "price_low", "price_high", "hot", "new"]]'
    )
    assert search["rating"].annotation == 'Optional[Literal["highly_rated", "best_rated"]]'
    assert search["min_price"].annotation == "Optional[float]"
    reviews = {p.name: p for p in eps["reviews"].params}
    assert reviews["rating"].annotation == "Optional[Literal[1, 2, 3, 4, 5]]"
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|robots?|hurry|geocode|pool of "
                        r"proxies|ends soon|last day|recalls?|cpsc|tariffs?|legit|scam)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    vv = client.vevor
    vv.search("welder")
    vv.search("schweissgeraet", country="de", language="de", category=40339, page=2,
              sort="price_low", in_stock=True, on_sale=True, black_friday=False,
              bulk_savings=True, min_price=50, max_price=300.5, rating="highly_rated")
    vv.search("welder", pickup=True)
    vv.product("DHJMIGMMAMIGLL6WNV5")
    vv.product(url="https://www.vevor.ca/x-c_1/y-p_010752182768", country="ca", language="fr")
    vv.shipping("DHJMIGMMAMIGLL6WNV5", state="AK", zip="99501")
    vv.shipping("DHJMIGMMAMIGLL6WNV5", province="ON", zip="M5V 2T6", city="Toronto",
                country="ca")
    vv.reviews("CKKMJ3300LBSAPPKZV1", page=2, page_size=100, sort="newest", rating=5,
               photos_only=True, this_variant_only=True)
    vv.questions("DHJMIGMMAMIGLL6WNV5", page=3, country="gb")
    vv.suggestions("ice")
    vv.categories()
    vv.categories(category="40339", country="eu", language="sv")
    vv.category("40035")
    vv.category(40035, page=2, sort="new", in_stock=True)
    vv.collections()
    vv.collections(type="promotion",
                   url="https://www.vevor.com/promotion/commercial-kitchen-equipment-special-10018.html")
    vv.collections(type="best_sellers", category="40035", page=2, sort="hot")
    vv.deals()
    vv.deals(type="clearance", category=40035, page=3, sort="price_high", country="pl")
    vv.prices("GYQXJBMQJQYPKEO1LV0")
    base = "/api/v1/vevor/"
    assert seen == [
        (base + "search", {"q": "welder"}, 240.0),
        (base + "search", {"q": "schweissgeraet", "category": 40339, "page": 2,
                           "sort": "price_low", "in_stock": True, "on_sale": True,
                           "black_friday": False, "bulk_savings": True, "min_price": 50,
                           "max_price": 300.5, "rating": "highly_rated", "country": "de",
                           "language": "de"}, 240.0),
        (base + "search", {"q": "welder", "pickup": True}, 240.0),
        (base + "product", {"sku": "DHJMIGMMAMIGLL6WNV5"}, 240.0),
        (base + "product", {"url": "https://www.vevor.ca/x-c_1/y-p_010752182768",
                            "country": "ca", "language": "fr"}, 240.0),
        (base + "shipping", {"sku": "DHJMIGMMAMIGLL6WNV5", "state": "AK", "zip": "99501"},
         240.0),
        (base + "shipping", {"sku": "DHJMIGMMAMIGLL6WNV5", "province": "ON", "zip": "M5V 2T6",
                             "city": "Toronto", "country": "ca"}, 240.0),
        (base + "reviews", {"sku": "CKKMJ3300LBSAPPKZV1", "page": 2, "page_size": 100,
                            "sort": "newest", "rating": 5, "photos_only": True,
                            "this_variant_only": True}, 240.0),
        (base + "questions", {"sku": "DHJMIGMMAMIGLL6WNV5", "page": 3, "country": "gb"}, 240.0),
        (base + "suggestions", {"q": "ice"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"category": "40339", "country": "eu", "language": "sv"}, 240.0),
        (base + "category", {"category": "40035"}, 240.0),
        (base + "category", {"category": 40035, "page": 2, "sort": "new", "in_stock": True},
         240.0),
        (base + "collections", {}, 240.0),
        (base + "collections", {"type": "promotion", "url": "https://www.vevor.com/promotion/"
                                "commercial-kitchen-equipment-special-10018.html"}, 240.0),
        (base + "collections", {"type": "best_sellers", "category": "40035", "page": 2,
                                "sort": "hot"}, 240.0),
        (base + "deals", {}, 240.0),
        (base + "deals", {"type": "clearance", "category": 40035, "page": 3,
                          "sort": "price_high", "country": "pl"}, 240.0),
        (base + "prices", {"sku": "GYQXJBMQJQYPKEO1LV0"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        vv.product()


def test_nellis_credits_paths_and_wire(monkeypatch):
    """nellis (0.87.0): 4 endpoints on /api/v1/nellis.

    1 credit each. location (6 shopping locations) on search, locations and categories; item
    takes id or url. query is sent as q and is optional. Every method gets a 240 s floor.
    """
    _NEL_FIRST = (
        "Nellis Auction (nellisauction.com, the liquidation auction marketplace with pickup "
        "warehouses in Las Vegas, Phoenix, Houston, Philadelphia, Denver and Dallas)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "nellis"}
    assert sorted(eps) == ["categories", "item", "locations", "search"]
    loc = 'Optional[Literal["las-vegas", "phoenix", "houston", "philadelphia", "denver", "dallas"]]'
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/nellis/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1, m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        if m == "item":
            assert list(names) == ["id", "url"], m
        else:
            assert names["location"].annotation == loc, m
    assert _NEL_FIRST in eps["search"].summary
    assert _NEL_FIRST in eps["locations"].summary
    for m in ("search", "item"):
        s = eps[m].summary
        assert '"Estimated Retail Price", as Nellis labels it' in s, m
        assert "not an MSRP" in s, m
        assert '"typically 15% but may vary based on the auction event"' in s, m
    assert "Open auctions only" in eps["search"].summary
    assert "search suggestions" in eps["search"].summary
    assert "no bidder names or ids" in eps["item"].summary
    assert "before Nellis's buyer's premium and tax" in eps["item"].summary
    assert "final_price 6 after 5 bids" in eps["item"].summary
    assert eps["item"].one_of == (("id", "url"),)
    search = {p.name: p for p in eps["search"].params}
    assert search["query"].wire_field == "q"
    assert search["query"].required is False
    assert search["page_size"].annotation == "Optional[Literal[48, 120, 240]]"
    assert search["sort"].annotation == (
        'Optional[Literal["featured", "price_low", "price_high", "ending_soon", "ending_last", '
        '"retail_low", "retail_high", "bids_low", "bids_high"]]'
    )
    assert search["brand"].annotation == "Optional[Union[str, list[str]]]"
    assert search["retail_min"].annotation == "Optional[float]"
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|robots?|shill\w*|rigged|"
                        r"worth it|deals?|scam|only api|legit)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    nl = client.nellis
    nl.search("robot vacuum")
    nl.search()
    nl.search("vacuum", location="phoenix", page=2, page_size=48, sort="bids_high",
              category="Electronics", subcategory=["TVs", "Soundbars"], brand="Samsung",
              pickup_location="Mesa", condition_rating=[4, 5], retail_min=50,
              retail_max=999.99, auction_event_type="Retail Returns",
              auction_event_name="Daily Auction - North Las Vegas - Nov 24th", color="Black",
              size="Large")
    nl.item("141281552")
    nl.item(141100004)
    nl.item(url="https://www.nellisauction.com/p/LG-65-OLED-evo-C6-4K-Smart-TV/141281552")
    nl.locations()
    nl.locations(location="dallas")
    nl.categories()
    nl.categories(location="houston", category="Electronics")
    base = "/api/v1/nellis/"
    assert seen == [
        (base + "search", {"q": "robot vacuum"}, 240.0),
        (base + "search", {}, 240.0),
        (base + "search", {"q": "vacuum", "location": "phoenix", "page": 2, "page_size": 48,
                           "sort": "bids_high", "category": "Electronics",
                           "subcategory": ["TVs", "Soundbars"], "brand": "Samsung",
                           "pickup_location": "Mesa", "condition_rating": [4, 5],
                           "retail_min": 50, "retail_max": 999.99,
                           "auction_event_type": "Retail Returns",
                           "auction_event_name": "Daily Auction - North Las Vegas - Nov 24th",
                           "color": "Black", "size": "Large"}, 240.0),
        (base + "item", {"id": "141281552"}, 240.0),
        (base + "item", {"id": 141100004}, 240.0),
        (base + "item", {"url": "https://www.nellisauction.com/p/LG-65-OLED-evo-C6-4K-Smart-TV/"
                         "141281552"}, 240.0),
        (base + "locations", {}, 240.0),
        (base + "locations", {"location": "dallas"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "categories", {"location": "houston", "category": "Electronics"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        nl.item()


def test_dermstore_credits_paths_and_wire(monkeypatch):
    """dermstore (0.88.0): 7 endpoints on /api/v1/dermstore.

    1 credit each. country (us or ca) on every method; list takes path or url, product takes sku
    or url. query is sent as q. Every method gets a 240 s floor.
    """
    _DRM_FIRST = (
        "Dermstore (dermstore.com, the US skincare and beauty retailer, shipping to the US and "
        "Canada)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "dermstore"}
    assert sorted(eps) == [
        "brands", "categories", "list", "offers", "product", "search", "suggestions",
    ]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/dermstore/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1, m
        assert ep.credits_note is None, m
        names = {p.name: p for p in ep.params}
        assert names["country"].annotation == 'Optional[Literal["us", "ca"]]', m
    for m in ("search", "suggestions", "offers", "brands", "categories"):
        assert _DRM_FIRST in eps[m].summary, m
    for m in ("search", "list", "product"):
        s = eps[m].summary
        assert "rrp is Dermstore's RRP as given" in s, m
        assert "discount_percent is computed by Scavio" in s, m
    assert "resolved_from" in eps["search"].summary
    assert "10 latest reviews" in eps["search"].summary
    assert "no reviewer names" in eps["product"].summary
    assert "Dermstore gives no start date" in eps["offers"].summary
    assert "46 USD (us) and 65.78 CAD (ca)" in eps["search"].summary
    assert eps["list"].one_of == (("path", "url"),)
    assert eps["product"].one_of == (("sku", "url"),)
    search = {p.name: p for p in eps["search"].params}
    assert search["query"].wire_field == "q"
    assert search["query"].required is True
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "popularity", "price_low", "price_high", "name", '
        '"newest", "discount"]]'
    )
    assert search["brand"].annotation == "Optional[Union[str, list[str]]]"
    assert search["min_price"].annotation == "Optional[float]"
    assert search["include_facets"].annotation == "Optional[bool]"
    sugg = {p.name: p for p in eps["suggestions"].params}
    assert sugg["query"].wire_field == "q"
    assert sugg["query"].required is True
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|"
                        r"counterfeit|authentic\w*|authori[sz]ed|legit|scam|fake|only api|"
                        r"only at)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    dm = client.dermstore
    dm.search("uv clear spf 46")
    dm.search("sunscreen", country="ca", page=2, page_size=200, sort="discount",
              brand=["EltaMD", "SkinCeuticals"], skin_type="Dry Skin", concern="Aging",
              spf="SPF 30+", key_ingredient="Retinol", preference="Clean", gender="Female",
              min_price=10, max_price=99.5, min_rating=4, min_discount=20, max_discount=50,
              include_facets=True)
    dm.list("/brands/eltamd")
    dm.list(url="https://www.dermstore.com/c/sale/", sort="price_low", country="ca")
    dm.product("11289609")
    dm.product(13806521, country="ca")
    dm.product(url="https://www.dermstore.com/p/medik8-crystal-retinal-20-30ml/13806521/")
    dm.suggestions("eltamd")
    dm.offers()
    dm.offers(country="ca")
    dm.brands()
    dm.brands(letter="E", country="ca")
    dm.categories()
    base = "/api/v1/dermstore/"
    assert seen == [
        (base + "search", {"q": "uv clear spf 46"}, 240.0),
        (base + "search", {"q": "sunscreen", "page": 2, "page_size": 200, "sort": "discount",
                           "brand": ["EltaMD", "SkinCeuticals"], "skin_type": "Dry Skin",
                           "concern": "Aging", "spf": "SPF 30+", "key_ingredient": "Retinol",
                           "preference": "Clean", "gender": "Female", "min_price": 10,
                           "max_price": 99.5, "min_rating": 4, "min_discount": 20,
                           "max_discount": 50, "include_facets": True, "country": "ca"}, 240.0),
        (base + "list", {"path": "/brands/eltamd"}, 240.0),
        (base + "list", {"url": "https://www.dermstore.com/c/sale/", "sort": "price_low",
                         "country": "ca"}, 240.0),
        (base + "product", {"sku": "11289609"}, 240.0),
        (base + "product", {"sku": 13806521, "country": "ca"}, 240.0),
        (base + "product", {"url": "https://www.dermstore.com/p/medik8-crystal-retinal-20-30ml/"
                            "13806521/"}, 240.0),
        (base + "suggestions", {"q": "eltamd"}, 240.0),
        (base + "offers", {}, 240.0),
        (base + "offers", {"country": "ca"}, 240.0),
        (base + "brands", {}, 240.0),
        (base + "brands", {"letter": "E", "country": "ca"}, 240.0),
        (base + "categories", {}, 240.0),
    ]
    with pytest.raises(ScavioError):
        dm.product()
    with pytest.raises(ScavioError):
        dm.list()


def test_offerup_credits_paths_and_wire(monkeypatch):
    """offerup (0.89.0): 5 endpoints on /api/v1/offerup.

    1 credit each; listing is 1, or 2 when it needs a second, costlier fetch (credits_note). US
    only (no country). search and category need zip; listing takes listing_id or url; query is
    sent as q. Every method gets a 240 s floor.
    """
    _OFU_FIRST = (
        "OfferUp (offerup.com, the US local marketplace for buying and selling used items, cars "
        "and trucks)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "offerup"}
    assert sorted(eps) == ["categories", "category", "listing", "search", "seller"]
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/offerup/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == 1, m
        assert "country" not in {p.name for p in ep.params}, m
        if m == "listing":
            assert ep.credits_note is not None and "or 2 when" in ep.credits_note
        else:
            assert ep.credits_note is None, m
    for m in ("search", "category", "categories", "seller"):
        assert _OFU_FIRST in eps[m].summary, m
    for m in ("search", "listing", "category", "seller"):
        s = eps[m].summary
        assert "no seller names" in s, m
        assert "asking prices" in s, m
    assert "sold listings or sold prices" in eps["search"].summary
    assert "ended nationwide shipping in 2025" in eps["search"].summary
    assert "no total count" in eps["search"].summary
    assert "filters_not_applied" in eps["category"].summary
    assert "no VIN" in eps["listing"].summary
    assert "first 20" in eps["seller"].summary
    assert eps["listing"].one_of == (("listing_id", "url"),)
    search = {p.name: p for p in eps["search"].params}
    assert search["query"].wire_field == "q"
    assert search["query"].required is True
    assert search["zip"].required is True
    assert search["zip"].annotation == "Union[str, int]"
    assert search["sort"].annotation == (
        'Optional[Literal["best_match", "newest", "distance", "price_low", "price_high", '
        '"newest_year", "lowest_mileage"]]'
    )
    assert search["radius"].annotation == (
        "Optional[Literal[5, 10, 20, 25, 30, 50, 80, 100, 200, 1500]]"
    )
    assert search["condition"].annotation == "Optional[Union[str, list[str]]]"
    assert search["seller_type"].annotation == 'Optional[Literal["dealer", "private"]]'
    category = {p.name: p for p in eps["category"].params}
    assert category["category"].required is True
    assert category["zip"].required is True
    assert "category_id" not in category
    assert '"best_match"' not in category["sort"].annotation
    seller = {p.name: p for p in eps["seller"].params}
    assert seller["seller_id"].required is True
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|"
                        r"cloudflare|firewall|pool|deals?|underpriced|worth it|market value|"
                        r"scam|fraud|fake|only api|only at)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key
        assert not banned.search((ep.credits_note or "").lower()), ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    ou = client.offerup
    ou.search("iphone 15", "98101")
    ou.search("toyota tacoma", 75201, radius=80, page=2, sort="lowest_mileage",
              category_id="5.1", min_price=5000, max_price=60000, condition=["used"],
              seller_type="dealer", make="Toyota", year_min=2018, year_max=2026,
              max_mileage=100000)
    ou.listing("7a392126-fb9d-34c2-a6d8-1b94698428df")
    ou.listing(url="https://offerup.com/item/detail/7a392126-fb9d-34c2-a6d8-1b94698428df")
    ou.category("furniture", "90012")
    ou.category("cars-and-trucks", "75201", sort="newest_year", condition="used,refurbished",
                radius=100)
    ou.categories()
    ou.seller("8668343")
    ou.seller(8668343)
    base = "/api/v1/offerup/"
    assert seen == [
        (base + "search", {"q": "iphone 15", "zip": "98101"}, 240.0),
        (base + "search", {"q": "toyota tacoma", "zip": 75201, "radius": 80, "page": 2,
                           "min_price": 5000, "max_price": 60000, "condition": ["used"],
                           "seller_type": "dealer", "make": "Toyota", "year_min": 2018,
                           "year_max": 2026, "max_mileage": 100000, "sort": "lowest_mileage",
                           "category_id": "5.1"}, 240.0),
        (base + "listing", {"listing_id": "7a392126-fb9d-34c2-a6d8-1b94698428df"}, 240.0),
        (base + "listing", {"url": "https://offerup.com/item/detail/"
                            "7a392126-fb9d-34c2-a6d8-1b94698428df"}, 240.0),
        (base + "category", {"category": "furniture", "zip": "90012"}, 240.0),
        (base + "category", {"category": "cars-and-trucks", "zip": "75201", "radius": 100,
                             "condition": "used,refurbished", "sort": "newest_year"}, 240.0),
        (base + "categories", {}, 240.0),
        (base + "seller", {"seller_id": "8668343"}, 240.0),
        (base + "seller", {"seller_id": 8668343}, 240.0),
    ]
    with pytest.raises(ScavioError):
        ou.listing()


def test_sportchek_and_marks_credits_paths_and_wire(monkeypatch):
    """sportchek + marks (0.90.0): 8 endpoints each on /api/v1/sportchek and /api/v1/marks.

    1 credit per call on every endpoint. SportChek has reviews (English only, no language);
    Mark's has questions and language en | fr (L'Equipeur) on search, list, product, brands and
    categories. query is sent as q; product, reviews and questions take code or url; list takes
    path or url. Every method gets a 240 s floor (answers take about 10-90 s).
    """
    firsts = {
        "sportchek": "SportChek (sportchek.ca, Canada's sporting goods retailer, a Canadian Tire "
        "Corporation banner)",
        "marks": "Mark's (marks.com, the Canadian workwear, casual clothing and footwear "
        "retailer, a Canadian Tire Corporation banner; L'Equipeur in French)",
    }
    methods = {
        "sportchek": ["brands", "categories", "list", "product", "reviews", "search", "store",
                      "suggestions"],
        "marks": ["brands", "categories", "list", "product", "questions", "search", "store",
                  "suggestions"],
    }
    french = {"search", "list", "product", "brands", "categories"}
    _CTC_FOOT = "Was price reflects the last national regular price this product was sold for."
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|headless|browser|retr(y|ies|ied)|cheapest|robots?|graphql|"
                        r"cookies?|bazaarvoice|sitemaps?|msrp|real discount|fake|price.match|"
                        r"ct money value|only api|only at)\b")
    for ns in ("sportchek", "marks"):
        eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == ns}
        assert sorted(eps) == methods[ns], ns
        for m, ep in eps.items():
            assert ep.http == "POST", ep.key
            assert ep.path == "/api/v1/" + ns + "/" + m, ep.key
            assert ep.key == ns + "_" + m
            assert ep.min_timeout == 240.0, ep.key
            assert ep.credits == 1 and ep.credits_note is None, ep.key
            assert "not-found is charged" in ep.summary, ep.key
            names = {p.name for p in ep.params}
            if ns == "marks" and m in french:
                assert "language" in names, ep.key
                lang = {p.name: p for p in ep.params}["language"]
                assert lang.annotation == 'Optional[Literal["en", "fr"]]'
            else:
                assert "language" not in names, ep.key
            assert not banned.search(ep.summary.lower()), ep.key
            assert "http" not in ep.summary.lower(), ep.key
        for m in ("search", "list", "product", "reviews", "questions", "suggestions", "store"):
            if m in eps:
                assert "allow up to 2 minutes" in eps[m].summary, (ns, m)
        assert firsts[ns] in eps["search"].summary
        for m in ("search", "list", "product"):
            s = eps[m].summary
            assert _CTC_FOOT in s, (ns, m)
            assert "label it computed" in s, (ns, m)
            assert "sale_ends" in s, (ns, m)
        assert "a caller cannot choose a store" in eps["product"].summary
        assert "assigned_store" in eps["product"].summary
        assert "no UPC or barcode" in eps["product"].summary
        assert "near a postal code is not supported" in eps["store"].summary
        assert "price history" in eps["search"].summary
        for m in ("product", "reviews", "questions"):
            if m in eps:
                assert eps[m].one_of == (("code", "url"),), (ns, m)
        assert eps["list"].one_of == (("path", "url"),)
        search = {p.name: p for p in eps["search"].params}
        assert search["query"].wire_field == "q" and search["query"].required is True
        assert search["sort"].annotation == (
            'Optional[Literal["relevance", "price_high", "price_low", "rating"]]'
        )
        assert search["deals"].annotation == "Optional[Union[str, list[str]]]"
        assert search["filters"].annotation == "Optional[list[dict[str, Union[str, list[str]]]]]"
        store = {p.name: p for p in eps["store"].params}
        assert store["store_id"].required is True
        assert store["store_id"].annotation == "Union[str, int]"
    sc = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "sportchek"}
    reviews = {p.name: p for p in sc["reviews"].params}
    assert reviews["sort"].annotation == (
        'Optional[Literal["newest", "relevance", "helpful", "rating_high", "rating_low"]]'
    )
    assert "first 8" in sc["reviews"].summary and "No reviewer names" in sc["reviews"].summary
    mk = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "marks"}
    assert "No asker or answerer names" in mk["questions"].summary
    assert "L'Equipeur" in mk["product"].summary

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    s = client.sportchek
    s.search("winter jacket")
    s.search("winter jacket", page=2, sort="price_low", brand=["COLUMBIA", "NIKE"],
             deals="sale", filters=[{"facet": "sku_gender_attr", "value": "Female"}],
             include_facets=True)
    s.list("/en/sale-clearance/clearance.html", sort="price_low")
    s.list(url="https://www.sportchek.ca/en/cat/accessories-DC2000012.html", deals="both")
    s.product("84166659F")
    s.product(url="https://www.sportchek.ca/en/pdp/x-84166659f.html")
    s.reviews("84166659F", page=2, sort="rating_low", rating=1)
    s.suggestions("bauer")
    s.store("272")
    s.store(272)
    s.brands()
    s.brands(letter="B")
    s.categories()
    k = client.marks
    k.search("bottes de travail", language="fr")
    k.list("/en/cat/work-boots-shoes-DC3000008.html", brand="Dakota Workpro Series")
    k.product("75983776F", language="fr")
    k.questions("75984589F")
    k.suggestions("dakota")
    k.store("589")
    k.brands(language="fr")
    k.categories(language="en")
    sb, mb = "/api/v1/sportchek/", "/api/v1/marks/"
    assert seen == [
        (sb + "search", {"q": "winter jacket"}, 240.0),
        (sb + "search", {"q": "winter jacket", "page": 2, "sort": "price_low",
                         "brand": ["COLUMBIA", "NIKE"], "deals": "sale",
                         "filters": [{"facet": "sku_gender_attr", "value": "Female"}],
                         "include_facets": True}, 240.0),
        (sb + "list", {"path": "/en/sale-clearance/clearance.html", "sort": "price_low"}, 240.0),
        (sb + "list", {"url": "https://www.sportchek.ca/en/cat/accessories-DC2000012.html",
                       "deals": "both"}, 240.0),
        (sb + "product", {"code": "84166659F"}, 240.0),
        (sb + "product", {"url": "https://www.sportchek.ca/en/pdp/x-84166659f.html"}, 240.0),
        (sb + "reviews", {"code": "84166659F", "page": 2, "sort": "rating_low", "rating": 1},
         240.0),
        (sb + "suggestions", {"q": "bauer"}, 240.0),
        (sb + "store", {"store_id": "272"}, 240.0),
        (sb + "store", {"store_id": 272}, 240.0),
        (sb + "brands", {}, 240.0),
        (sb + "brands", {"letter": "B"}, 240.0),
        (sb + "categories", {}, 240.0),
        (mb + "search", {"q": "bottes de travail", "language": "fr"}, 240.0),
        (mb + "list", {"path": "/en/cat/work-boots-shoes-DC3000008.html",
                       "brand": "Dakota Workpro Series"}, 240.0),
        (mb + "product", {"code": "75983776F", "language": "fr"}, 240.0),
        (mb + "questions", {"code": "75984589F"}, 240.0),
        (mb + "suggestions", {"q": "dakota"}, 240.0),
        (mb + "store", {"store_id": "589"}, 240.0),
        (mb + "brands", {"language": "fr"}, 240.0),
        (mb + "categories", {"language": "en"}, 240.0),
    ]
    # A client timeout above the floor is kept, never lowered.
    seen.clear()
    ScavioClient(api_key="sk_test", timeout=400.0).marks.store("589")
    assert seen == [(mb + "store", {"store_id": "589"}, 400.0)]
    with pytest.raises(ScavioError):
        s.product()
    with pytest.raises(ScavioError):
        s.reviews()
    with pytest.raises(ScavioError):
        k.questions()
    with pytest.raises(ScavioError):
        k.list()


# --- Home Depot Canada --------------------------------------------------------


def test_home_depot_us_calls_post_exactly_what_they_did(monkeypatch):
    """country is absent by default: a US call's body is unchanged by Home Depot Canada."""
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.home_depot.search("cordless drill", page=2, sort_by="top_sellers")
    assert captured["path"] == "/api/v1/homedepot/search"
    assert captured["json"] == {"query": "cordless drill", "page": 2, "sort_by": "top_sellers"}
    client.home_depot.product("325479354")
    assert captured["json"] == {"item_id": "325479354"}
    client.home_depot.reviews("325479354", page=3)
    assert captured["json"] == {"item_id": "325479354", "page": 3}


def test_home_depot_ca_search_takes_store_filters_and_deals(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.home_depot.search(
        "cordless drill",
        country="ca",
        store_id="7080",
        page_size=40,
        filters=[{"facet": "manufacturerName", "value": "9wh"}],
        deals=["special_buy", "savings"],
        include_facets=True,
        language="fr",
    )
    assert captured["json"] == {
        "query": "cordless drill",
        "country": "ca",
        "store_id": "7080",
        "page_size": 40,
        "filters": [{"facet": "manufacturerName", "value": "9wh"}],
        "deals": ["special_buy", "savings"],
        "include_facets": True,
        "language": "fr",
    }
    client.home_depot.search(country="ca", deals="new_lower_price")
    assert captured["json"] == {"country": "ca", "deals": "new_lower_price"}
    with pytest.raises(ScavioError):
        client.home_depot.search(country="ca")


def test_home_depot_ca_product_at_a_store(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.home_depot.product("1000112108", country="ca", store_id=7128)
    assert captured["path"] == "/api/v1/homedepot/product"
    assert captured["json"] == {"item_id": "1000112108", "country": "ca", "store_id": 7128}


def test_home_depot_ca_only_endpoints(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.home_depot.category("661103", store_id="7128", sort_by="price_low")
    assert captured["path"] == "/api/v1/homedepot/category"
    assert captured["json"] == {"category_id": "661103", "store_id": "7128", "sort_by": "price_low"}
    client.home_depot.categories(depth=2)
    assert captured["path"] == "/api/v1/homedepot/categories"
    assert captured["json"] == {"depth": 2}
    client.home_depot.stock("1001769719", "H3B 1A1", limit=15)
    assert captured["path"] == "/api/v1/homedepot/stock"
    assert captured["json"] == {"item_id": "1001769719", "location": "H3B 1A1", "limit": 15}
    client.home_depot.store("7076")
    assert captured["path"] == "/api/v1/homedepot/store"
    assert captured["json"] == {"store_id": "7076"}
    client.home_depot.suggestions("christ", language="en")
    assert captured["path"] == "/api/v1/homedepot/suggestions"
    assert captured["json"] == {"query": "christ", "language": "en"}
    for key in ("category", "categories", "stock", "store", "suggestions"):
        ep = ENDPOINTS[f"home_depot_{key}"]
        assert ep.credits == 1 and ep.credits_note is None
        assert all(p.name != "country" for p in ep.params), key


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_home_depot_shared_docstrings_state_both_rates(module):
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_HomeDepotNamespace", None) or mod._AsyncHomeDepotNamespace
    for method in ("search", "product", "reviews", "stores", "availability"):
        doc = getattr(cls, method).__doc__ or ""
        assert "Costs 2 credits." not in doc, method
        assert "2 credits in the US" in doc and "1 credit with country='ca'" in doc, method


def test_home_depot_stores_availability_shipping(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.home_depot.stores("98101", limit=5)
    assert captured["path"] == "/api/v1/homedepot/stores"
    assert captured["json"] == {"query": "98101", "limit": 5}
    client.home_depot.stores(country="ca", latitude=45.5, longitude=-73.6)
    assert captured["json"] == {"country": "ca", "latitude": 45.5, "longitude": -73.6}
    with pytest.raises(ScavioError):
        client.home_depot.stores()
    client.home_depot.availability("325479354", store_id="4702", zip="98101")
    assert captured["path"] == "/api/v1/homedepot/availability"
    assert captured["json"] == {"item_id": "325479354", "store_id": "4702", "zip": "98101"}
    client.home_depot.availability("1001769719", store_id="7076", country="ca")
    assert captured["json"] == {"item_id": "1001769719", "store_id": "7076", "country": "ca"}
    with pytest.raises(ScavioError):
        client.home_depot.availability("325479354")
    client.home_depot.shipping("325479354", "98101", quantity=2)
    assert captured["path"] == "/api/v1/homedepot/shipping"
    assert captured["json"] == {"item_id": "325479354", "zip": "98101", "quantity": 2}
    ship = ENDPOINTS["home_depot_shipping"]
    assert ship.credits == 4 and ship.credits_note is None
    assert all(p.name != "country" for p in ship.params)


# --- Best Buy Canada ----------------------------------------------------------


def test_best_buy_ca_calls_send_country_and_ca_params(monkeypatch):
    """country is absent by default (US bodies are pinned above); 'ca' adds the Canada fields."""
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    bb = client.best_buy
    bb.search(
        "4k tv",
        country="ca",
        page_size=48,
        sort="price_low",
        filters={"sold_by": "best_buy", "rating": 4},
        province="QC",
        language="fr",
    )
    assert captured["path"] == "/api/v1/bestbuy/search"
    assert captured["json"] == {
        "query": "4k tv",
        "sort": "price_low",
        "filters": {"sold_by": "best_buy", "rating": 4},
        "country": "ca",
        "page_size": 48,
        "province": "QC",
        "language": "fr",
    }
    bb.product(sku="19791103", country="ca", province="BC")
    assert captured["json"] == {"sku": "19791103", "country": "ca", "province": "BC"}
    bb.reviews(sku="19296507", country="ca", page_size=50, verified_only=True)
    assert captured["json"] == {
        "sku": "19296507",
        "country": "ca",
        "page_size": 50,
        "verified_only": True,
    }
    bb.category(category_id="21344", country="ca", sort="best_match")
    assert captured["json"] == {"category_id": "21344", "sort": "best_match", "country": "ca"}
    bb.deals(country="ca", collection="black_friday", page=2)
    assert captured["path"] == "/api/v1/bestbuy/deals"
    assert captured["json"] == {"country": "ca", "collection": "black_friday", "page": 2}
    bb.stores(country="ca", postal_code="M5V 3L9", radius_km=10)
    assert captured["path"] == "/api/v1/bestbuy/stores"
    assert captured["json"] == {"country": "ca", "postal_code": "M5V 3L9", "radius_km": 10}
    bb.stores(country="ca", city="Winnipeg")
    assert captured["json"] == {"country": "ca", "city": "Winnipeg"}
    bb.availability(
        skus=["19791103", "19296507"], country="ca", postal_code="H3B 4W8", max_stores=5
    )
    assert captured["path"] == "/api/v1/bestbuy/availability"
    assert captured["json"] == {
        "max_stores": 5,
        "country": "ca",
        "postal_code": "H3B 4W8",
        "skus": ["19791103", "19296507"],
    }
    bb.availability(sku="19791103", country="ca", store_ids=["651", "705"])
    assert captured["json"] == {"sku": "19791103", "store_ids": ["651", "705"], "country": "ca"}
    bb.suggestions("nintendo sw", country="ca", language="en")
    assert captured["json"] == {"query": "nintendo sw", "country": "ca", "language": "en"}
    bb.prices(["19791103", "19296507"], country="ca", province="ON")
    assert captured["path"] == "/api/v1/bestbuy/prices"
    assert captured["json"] == {"skus": ["19791103", "19296507"], "country": "ca", "province": "ON"}
    with pytest.raises(ScavioError):
        bb.stores(country="ca")
    with pytest.raises(ScavioError):
        bb.availability(skus=["19791103"], country="ca")


def test_best_buy_questions_is_canada_only(monkeypatch):
    captured = patch_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.best_buy.questions(sku="19296507", sort="newest", page_size=20)
    assert captured["path"] == "/api/v1/bestbuy/questions"
    assert captured["json"] == {"sku": "19296507", "page_size": 20, "sort": "newest"}
    ep = ENDPOINTS["best_buy_questions"]
    assert ep.credits == 1 and ep.credits_note is None and ep.min_timeout == 120.0
    assert all(p.name != "country" for p in ep.params)
    with pytest.raises(ScavioError):
        client.best_buy.questions()


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_best_buy_shared_docstrings_state_both_rates(module):
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_BestBuyNamespace", None) or mod._AsyncBestBuyNamespace
    for method in ("search", "product", "reviews", "category", "deals", "availability", "prices"):
        doc = " ".join((getattr(cls, method).__doc__ or "").split())
        assert "in the US" in doc and "1 credit with country='ca'" in doc, method
    for method in ("stores", "suggestions", "questions"):
        assert "Costs 1 credit." in " ".join((getattr(cls, method).__doc__ or "").split()), method


# --- Sephora Canada -----------------------------------------------------------


def test_sephora_us_calls_send_no_country(monkeypatch):
    """A US call posts exactly the body it did before Sephora Canada existed."""
    captured = patch_sync(monkeypatch)
    sephora = ScavioClient(api_key="sk_test").sephora
    sephora.search("lipstick", sort="best_selling", zip="10001")
    assert captured["json"] == {"query": "lipstick", "sort": "best_selling", "zip": "10001"}
    sephora.category("lipstick", page=2)
    assert captured["json"] == {"category": "lipstick", "page": 2}
    sephora.product(product_id="P510799")
    assert captured["json"] == {"product_id": "P510799"}


def test_sephora_ca_calls_send_country_and_ca_params(monkeypatch):
    captured = patch_sync(monkeypatch)
    sephora = ScavioClient(api_key="sk_test").sephora
    sephora.search(
        "lip oil",
        country="ca",
        sort="price_low",
        filters={"brand": "The Ordinary", "on_sale": True, "rating": 4},
        include_facets=True,
        language="fr",
    )
    assert captured["path"] == "/api/v1/sephora/search"
    assert captured["json"] == {
        "query": "lip oil",
        "sort": "price_low",
        "country": "ca",
        "filters": {"brand": "The Ordinary", "on_sale": True, "rating": 4},
        "include_facets": True,
        "language": "fr",
    }
    sephora.category("lipstick", country="ca", sort="newest", filters=[{"value": "x"}])
    assert captured["path"] == "/api/v1/sephora/category"
    assert captured["json"] == {
        "category": "lipstick",
        "country": "ca",
        "sort": "newest",
        "filters": [{"value": "x"}],
    }
    sephora.product(product_id="P428500", country="ca", language="en")
    assert captured["path"] == "/api/v1/sephora/product"
    assert captured["json"] == {"product_id": "P428500", "country": "ca", "language": "en"}


def test_sephora_ca_only_endpoints(monkeypatch):
    captured = patch_sync(monkeypatch)
    sephora = ScavioClient(api_key="sk_test").sephora
    sephora.brand("the-ordinary", page=2, sort="rating", filters={"new": True})
    assert captured["path"] == "/api/v1/sephora/brand"
    assert captured["json"] == {
        "brand": "the-ordinary",
        "page": 2,
        "sort": "rating",
        "filters": {"new": True},
    }
    sephora.brands(language="fr")
    assert captured["path"] == "/api/v1/sephora/brands"
    assert captured["json"] == {"language": "fr"}
    sephora.suggestions("lip")
    assert captured["path"] == "/api/v1/sephora/suggestions"
    assert captured["json"] == {"query": "lip"}
    sephora.offers()
    assert captured["path"] == "/api/v1/sephora/offers"
    assert captured["json"] == {}
    sephora.stores(province="QC")
    assert captured["path"] == "/api/v1/sephora/stores"
    assert captured["json"] == {"province": "QC"}
    sephora.store("toronto-eaton-centre")
    assert captured["path"] == "/api/v1/sephora/store"
    assert captured["json"] == {"store": "toronto-eaton-centre"}
    for m in ("brand", "brands", "suggestions", "offers", "stores", "store"):
        ep = ENDPOINTS[f"sephora_{m}"]
        assert all(p.name != "country" for p in ep.params), m
        assert ep.credits_note is None and ep.min_timeout == 120.0, m
    for m in ("search", "category", "product"):
        ep = ENDPOINTS[f"sephora_{m}"]
        assert any(p.name == "country" for p in ep.params), m
        assert ep.credits_note is None and ep.min_timeout == 120.0, m


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_sephora_docstrings_state_credits(module):
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_SephoraNamespace", None) or mod._AsyncSephoraNamespace
    for method in ("search", "category", "brand", "brands", "suggestions", "stores", "store"):
        assert "Costs 1 credit." in " ".join((getattr(cls, method).__doc__ or "").split()), method
    for method in ("product", "offers"):
        assert "Costs 2 credits." in " ".join((getattr(cls, method).__doc__ or "").split()), method


def test_rona_credits_paths_and_wire(monkeypatch):
    """rona (0.94.0): 9 endpoints on /api/v1/rona.

    prices, categories, stores and store 1 credit; product and stock 3; search and deals 2 (3
    with store_id; search 2 more on a redirect); category 2 (3 with store_id) or 1 with
    family_id and store_id. Canada only, language en | fr on every endpoint. Every method gets
    a 240 s floor.
    """
    first = (
        "RONA (rona.ca, the Canadian home improvement retailer: RONA+ and RONA stores, about 425 "
        "corporate and affiliated dealer stores per RONA inc.)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "rona"}
    assert sorted(eps) == [
        "categories", "category", "deals", "prices", "product", "search", "stock", "store",
        "stores",
    ]
    credits = {"search": 2, "product": 3, "prices": 1, "category": 1, "categories": 1,
               "stores": 1, "store": 1, "stock": 3, "deals": 2}
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/rona/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == credits[m], m
        assert first in ep.summary, m
        names = {p.name for p in ep.params}
        assert "language" in names, m
        assert "country" not in names, m
        assert "postal_code" not in names, m
        if m in ("search", "category", "deals"):
            assert ep.credits_note is not None and "3 with store_id" in ep.credits_note, m
        else:
            assert ep.credits_note is None, m
    assert "2 more when RONA redirects" in eps["search"].credits_note
    assert "1 credit with family_id and store_id" in eps["category"].credits_note
    for m in ("search", "product", "category", "deals"):
        assert "store.requested false" in eps[m].summary, m
    for m in ("search", "product", "prices", "category", "deals"):
        assert "null means RONA showed no count, not zero" in eps[m].summary, m
    assert "4.35 CAD at store '41460' (Quebec), 4.22 at '55130' (Ontario)" in eps[
        "prices"].summary
    assert "until Dec 10th, 2026" in eps["product"].summary
    assert "Postal code lookup is not supported" in eps["stores"].summary
    assert "Postal code lookup is not supported" in eps["stock"].summary
    assert "no sort" in eps["deals"].summary
    assert "sort" not in {p.name for p in eps["deals"].params}
    assert "review text" in eps["search"].summary
    assert eps["product"].one_of == (("sku", "url"),)
    assert eps["category"].one_of == (("category", "family_id"),)
    assert eps["store"].one_of == (("store_id", "url"),)
    assert eps["stock"].one_of == (("store_id", "latitude"),)
    prices = {p.name: p for p in eps["prices"].params}
    assert prices["skus"].required is True
    assert prices["skus"].annotation == "Union[list[str], str]"
    assert prices["store_id"].required is True
    search = {p.name: p for p in eps["search"].params}
    assert search["query"].required is True
    assert search["query"].wire_field == "query"
    assert search["page_size"].annotation == "Optional[Literal[24, 48, 96]]"
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_low_to_high", "price_high_to_low", '
        '"highest_rated", "newest", "best_sellers"]]'
    )
    assert search["language"].annotation == 'Optional[Literal["en", "fr"]]'
    stock = {p.name: p for p in eps["stock"].params}
    assert stock["sku"].required is True
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|"
                        r"cloudflare|firewall|pool|affiliates?|class action|only api|"
                        r"only at|first api)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key
        assert not banned.search((ep.credits_note or "").lower()), ep.key
        assert "https://www.rona.ca" not in ep.summary, ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    rn = client.rona
    rn.search("2x4")
    rn.search("perceuse", page=2, page_size=24, sort="price_low_to_high",
              filters=["1000337236"], on_sale=True, include_facets=True, store_id="41460",
              language="fr")
    rn.product("00277649", store_id="55130")
    rn.product(url="https://www.rona.ca/en/product/x-00277649")
    rn.prices(["0971073", "0938002", "00277649"], "55130")
    rn.prices("0971073,00277649", 41460, language="fr")
    rn.category("/en/tools/power-tools-158001/cordless-drills-and-drivers-158003",
                store_id="55130", clearance=True)
    rn.category(family_id="318485", store_id="55130", page_size=100)
    rn.categories(depth=2)
    rn.stores(latitude=43.6426, longitude=-79.3871, limit=10)
    rn.stores(province="qc", banner="rona_plus")
    rn.store("55130")
    rn.stock("00277649", "62860")
    rn.stock("00277649", latitude=51.0774, longitude=-113.99011)
    rn.deals()
    rn.deals(type="clearance", store_id="55130", page=3)
    base = "/api/v1/rona/"
    assert seen == [
        (base + "search", {"query": "2x4"}, 240.0),
        (base + "search", {"query": "perceuse", "page": 2, "page_size": 24,
                           "sort": "price_low_to_high", "filters": ["1000337236"],
                           "on_sale": True, "include_facets": True, "store_id": "41460",
                           "language": "fr"}, 240.0),
        (base + "product", {"sku": "00277649", "store_id": "55130"}, 240.0),
        (base + "product", {"url": "https://www.rona.ca/en/product/x-00277649"}, 240.0),
        (base + "prices", {"skus": ["0971073", "0938002", "00277649"], "store_id": "55130"},
         240.0),
        (base + "prices", {"skus": "0971073,00277649", "store_id": 41460, "language": "fr"},
         240.0),
        (base + "category", {"category": "/en/tools/power-tools-158001/"
                             "cordless-drills-and-drivers-158003", "clearance": True,
                             "store_id": "55130"}, 240.0),
        (base + "category", {"family_id": "318485", "page_size": 100, "store_id": "55130"},
         240.0),
        (base + "categories", {"depth": 2}, 240.0),
        (base + "stores", {"latitude": 43.6426, "longitude": -79.3871, "limit": 10}, 240.0),
        (base + "stores", {"province": "qc", "banner": "rona_plus"}, 240.0),
        (base + "store", {"store_id": "55130"}, 240.0),
        (base + "stock", {"sku": "00277649", "store_id": "62860"}, 240.0),
        (base + "stock", {"sku": "00277649", "latitude": 51.0774, "longitude": -113.99011},
         240.0),
        (base + "deals", {}, 240.0),
        (base + "deals", {"type": "clearance", "page": 3, "store_id": "55130"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        rn.product()
    with pytest.raises(ScavioError):
        rn.category()
    with pytest.raises(ScavioError):
        rn.store()
    with pytest.raises(ScavioError):
        rn.stock("00277649")


def test_pcexpress_credits_paths_and_wire(monkeypatch):
    """pcexpress (0.95.0): 7 endpoints on /api/v1/pcexpress.

    search, category, collection, stores and suggestions 1 credit; product 5 (1 when it answers
    from the search listing); store 5. Canada only, banner (10) and language en | fr. Prices are
    each banner's default store's (no store_id on priced endpoints). Every method gets a 240 s
    floor.
    """
    first = (
        "PC Express (Loblaw's online grocery for Real Canadian Superstore, No Frills, Loblaws, "
        "Zehrs, Fortinos, Valu-mart, Your Independent Grocer, Wholesale Club, Provigo and Maxi; "
        "Loblaw operates 2,504 stores per its 2025 annual report)"
    )
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == "pcexpress"}
    assert sorted(eps) == [
        "category", "collection", "product", "search", "store", "stores", "suggestions",
    ]
    credits = {"search": 1, "category": 1, "collection": 1, "product": 5, "stores": 1,
               "store": 5, "suggestions": 1}
    banners = (
        'Optional[Literal["superstore", "nofrills", "loblaw", "zehrs", "fortinos", "valumart", '
        '"independent", "wholesaleclub", "provigo", "maxi"]]'
    )
    for m, ep in eps.items():
        assert ep.http == "POST", ep.key
        assert ep.path == "/api/v1/pcexpress/" + m, ep.key
        assert ep.min_timeout == 240.0, ep.key
        assert ep.credits == credits[m], m
        assert first in ep.summary, m
        params = {p.name: p for p in ep.params}
        assert params["banner"].annotation == banners, m
        assert params["language"].annotation == 'Optional[Literal["en", "fr"]]', m
        assert "country" not in params, m
        if m == "product":
            assert ep.credits_note is not None
            assert "1 when it answers from the search listing" in ep.credits_note
        else:
            assert ep.credits_note is None, m
        if m != "store":
            assert "store_id" not in params, m
    for m in ("search", "category", "collection", "product"):
        assert "default online store" in eps[m].summary, m
        assert "requested false" in eps[m].summary, m
        assert "no start date" in eps[m].summary, m
        assert "not a price behind a login" in eps[m].summary, m
        assert "3.93 CAD at Real Canadian Superstore's default store '1033'" in eps[m].summary
        assert "4.17 at Maxi's default store '8976'" in eps[m].summary
    for m in ("product", "store", "stores", "suggestions"):
        assert "allow up to 2 minutes" in eps[m].summary, m
    assert "expiry_date 2026-12-02" in eps["collection"].summary
    assert "gtin 00060383664145" in eps["product"].summary
    assert "Shoppers Drug Mart" in eps["search"].summary
    assert "review text" in eps["search"].summary
    assert eps["product"].one_of == (("code", "url"),)
    search = {p.name: p for p in eps["search"].params}
    assert search["query"].required is True
    assert search["sort"].annotation == (
        'Optional[Literal["relevance", "price_low_to_high", "price_high_to_low", '
        '"name_a_to_z", "newest"]]'
    )
    assert search["brand"].annotation == "Optional[Union[str, list[str]]]"
    assert {p.name: p for p in eps["category"].params}["category"].required is True
    assert {p.name: p for p in eps["collection"].params}["collection"].required is True
    store = {p.name: p for p in eps["store"].params}
    assert store["store_id"].required is True
    assert store["store_id"].annotation == "Union[str, int]"
    banned = re.compile(r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|"
                        r"render\w*|retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|"
                        r"cloudflare|firewall|pool|affiliates?|class action|only api|"
                        r"only at|first api|akamai|next\.js|settlement|boycott)\b")
    for ep in eps.values():
        assert not banned.search(ep.summary.lower()), ep.key
        assert not banned.search((ep.credits_note or "").lower()), ep.key
        assert "https://" not in ep.summary, ep.key

    seen: list[tuple[str, dict, float]] = []

    def fake_request(method, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    pcx = client.pcexpress
    pcx.search("eggs")
    pcx.search("oeufs", banner="maxi", language="fr", page=2, sort="price_low_to_high",
               brand=["N", "P"], deals="pc_points", prepared_in_canada=True,
               filters=[{"facet": "dietaryCallouts", "value": "organic"}], include_facets=True)
    pcx.category("28224")
    pcx.category(28224, banner="nofrills", deals=["price_reduction", "multi_buy"])
    pcx.collection("deals-centre", banner="nofrills")
    pcx.product("20812144001_EA")
    pcx.product(url="https://example.com/p/20812144001_EA", banner="maxi")
    pcx.stores(city="Winnipeg")
    pcx.stores(latitude=49.2827, longitude=-123.1207, limit=5, shoppable_only=True)
    pcx.store("1517")
    pcx.store("0559", banner="zehrs")
    pcx.suggestions("egg")
    base = "/api/v1/pcexpress/"
    assert seen == [
        (base + "search", {"query": "eggs"}, 240.0),
        (base + "search", {"query": "oeufs", "page": 2, "sort": "price_low_to_high",
                           "brand": ["N", "P"], "deals": "pc_points",
                           "prepared_in_canada": True,
                           "filters": [{"facet": "dietaryCallouts", "value": "organic"}],
                           "include_facets": True, "banner": "maxi", "language": "fr"}, 240.0),
        (base + "category", {"category": "28224"}, 240.0),
        (base + "category", {"category": 28224, "deals": ["price_reduction", "multi_buy"],
                             "banner": "nofrills"}, 240.0),
        (base + "collection", {"collection": "deals-centre", "banner": "nofrills"}, 240.0),
        (base + "product", {"code": "20812144001_EA"}, 240.0),
        (base + "product", {"url": "https://example.com/p/20812144001_EA", "banner": "maxi"},
         240.0),
        (base + "stores", {"city": "Winnipeg"}, 240.0),
        (base + "stores", {"latitude": 49.2827, "longitude": -123.1207,
                           "shoppable_only": True, "limit": 5}, 240.0),
        (base + "store", {"store_id": "1517"}, 240.0),
        (base + "store", {"store_id": "0559", "banner": "zehrs"}, 240.0),
        (base + "suggestions", {"query": "egg"}, 240.0),
    ]
    with pytest.raises(ScavioError):
        pcx.product()


@pytest.mark.parametrize("module", ["scavio._namespaces_sync", "scavio._namespaces_async"])
def test_pcexpress_docstrings_state_credits(module):
    import importlib

    mod = importlib.import_module(module)
    cls = getattr(mod, "_PcexpressNamespace", None) or mod._AsyncPcexpressNamespace
    for method in ("search", "category", "collection", "stores", "suggestions"):
        assert "Costs 1 credit." in " ".join((getattr(cls, method).__doc__ or "").split()), method
    assert "Costs 5 credits." in " ".join((cls.store.__doc__ or "").split())
    doc = " ".join((cls.product.__doc__ or "").split())
    assert "Costs 5 credits; 1 when it answers from the search listing" in doc


# --- batch 2026-11-26: 14 namespaces (beauty + cars), generated from the backend routes ---

BATCH_1126 = {
    "spacenk": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "brands": ("brands", 1, 240.0),
        "product": ("product", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "offers": ("offers", 1, 240.0),
    },
    "lookfantastic": {
        "search": ("search", 1, 240.0),
        "list": ("list", 1, 240.0),
        "product": ("product", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "offers": ("offers", 1, 240.0),
        "brands": ("brands", 1, 240.0),
        "categories": ("categories", 1, 240.0),
    },
    "cultbeauty": {
        "search": ("search", 1, 240.0),
        "list": ("list", 1, 240.0),
        "product": ("product", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "offers": ("offers", 1, 240.0),
        "brands": ("brands", 1, 240.0),
        "categories": ("categories", 1, 240.0),
    },
    "yesstyle": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "brand": ("brand", 2, 240.0),
        "brands": ("brands", 1, 240.0),
        "deals": ("deals", 2, 240.0),
        "product": ("product", 2, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "markets": ("markets", 1, 240.0),
    },
    "notino": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "reviews": ("reviews", 1, 250.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "promo": ("promo", 1, 240.0),
        "brands": ("brands", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
    },
    "douglas": {
        "search": ("search", 1, 250.0),
        "category": ("category", 1, 250.0),
        "brand": ("brand", 1, 250.0),
        "deals": ("deals", 1, 250.0),
        "product": ("product", 1, 250.0),
        "stores": ("stores", 1, 250.0),
        "store": ("store", 1, 250.0),
        "review_summary": ("review-summary", 1, 250.0),
        "suggestions": ("suggestions", 1, 250.0),
        "brands": ("brands", 1, 250.0),
    },
    "boots": {
        "product": ("product", 1, 240.0),
        "store_stock": ("store-stock", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
    },
    "rockauto": {
        "vehicles": ("vehicles", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "parts": ("parts", 1, 240.0),
        "search": ("search", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "brands": ("brands", 1, 240.0),
        "part": ("part", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "resolve": ("resolve", 1, 240.0),
        "tools": ("tools", 1, 240.0),
        "promotions": ("promotions", 1, 240.0),
    },
    "carscom": {
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "dealer": ("dealer", 1, 240.0),
        "dealer_inventory": ("dealer-inventory", 1, 240.0),
        "dealer_reviews": ("dealer-reviews", 1, 240.0),
        "model_reviews": ("model-reviews", 1, 240.0),
        "dealers": ("dealers", 1, 240.0),
        "research": ("research", 1, 240.0),
    },
    "autotrader": {
        "search": ("search", 2, 240.0),
        "listing": ("listing", 2, 240.0),
        "dealers": ("dealers", 2, 240.0),
        "dealer": ("dealer", 2, 240.0),
        "makes": ("makes", 2, 240.0),
    },
    "cargurus": {
        "search": ("search", 1, 240.0),
        "dealer": ("dealer", 1, 240.0),
        "dealers": ("dealers", 1, 240.0),
        "price_trends": ("price-trends", 1, 240.0),
        "research": ("research", 1, 240.0),
        "expert_reviews": ("expert-reviews", 1, 240.0),
        "makes": ("makes", 1, 240.0),
        "models": ("models", 1, 240.0),
    },
    "carmax": {
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "photos": ("photos", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "store_inventory": ("store-inventory", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "review_summary": ("review-summary", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "makes": ("makes", 1, 240.0),
        "models": ("models", 1, 240.0),
        "car_value": ("car-value", 1, 240.0),
    },
    "carvana": {
        "search": ("search", 1, 240.0),
        "vehicle": ("vehicle", 1, 240.0),
        "model_guide": ("model-guide", 1, 240.0),
        "trims": ("trims", 1, 240.0),
        "make": ("make", 1, 240.0),
        "makes": ("makes", 1, 240.0),
    },
    "bringatrailer": {
        "results": ("results", 1, 240.0),
        "price_history": ("price-history", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "live": ("live", 1, 240.0),
        "make": ("make", 1, 240.0),
        "model": ("model", 1, 240.0),
        "location": ("location", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
}
BATCH_1126_ONE_OF = {
    "spacenk_stores": ("postcode", "latitude"),
    "lookfantastic_list": ("path", "url"),
    "lookfantastic_product": ("sku", "url"),
    "cultbeauty_list": ("path", "url"),
    "cultbeauty_product": ("sku", "url"),
    "yesstyle_product": ("product_id", "url"),
    "yesstyle_reviews": ("product_id", "url"),
    "notino_product": ("url", "order_code"),
    "notino_reviews": ("url", "order_code"),
    "douglas_product": ("code", "url"),
    "boots_product": ("url", "product_id"),
    "boots_store_stock": ("postcode", "latitude"),
    "boots_stores": ("postcode", "city"),
    "boots_store": ("store", "store_number", "name"),
    "carscom_listing": ("listing_id", "url"),
    "carscom_dealer": ("dealer_id", "url"),
    "carscom_dealer_inventory": ("dealer_id", "url"),
    "carscom_dealer_reviews": ("dealer_id", "url"),
    "autotrader_listing": ("listing_id", "url"),
    "autotrader_dealer": ("dealer_id", "url"),
    "cargurus_dealer": ("dealer_id", "url"),
    "cargurus_research": ("research_id", "url", "year"),
    "carmax_listing": ("stock_number", "url"),
    "carmax_photos": ("stock_number", "url"),
    "carmax_stores": ("zip", "state", "city"),
    "carvana_vehicle": ("vehicle_id", "url"),
    "bringatrailer_listing": ("slug", "url"),
    "bringatrailer_price_history": ("model_id", "make"),
}
BATCH_1126_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|pool|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super pool|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH_1126))
def test_batch_1126_credits_paths_timeouts(namespace):
    """Every endpoint of the 14 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH_1126[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(ep.one_of) == ((BATCH_1126_ONE_OF[ep.key],) if ep.key in
                                    BATCH_1126_ONE_OF else ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        # "Click & Collect" is the retailer's own service name, not a description of Scavio.
        text = text.lower().replace("click & collect", "click-and-pickup")
        assert not BATCH_1126_BANNED.search(text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH_1126_WIRE = [
    ("spacenk", "search", {"query": "vitamin c serum"}, "search"),
    ("spacenk", "category", {"category_id": "black-friday"}, "category"),
    ("spacenk", "brand", {"brand_id": "medik8"}, "brand"),
    ("spacenk", "brands", {}, "brands"),
    ("spacenk", "product", {"product_id": "MUK200057800"}, "product"),
    ("spacenk", "reviews", {"product_id": "MUK200057800"}, "reviews"),
    ("spacenk", "suggestions", {"query": "charlotte"}, "suggestions"),
    ("spacenk", "stores", {"product_id": "MUK200057800", "postcode": "W1D 1BS"}, "stores"),
    ("spacenk", "offers", {}, "offers"),
    ("lookfantastic", "search", {"query": "glow tonic"}, "search"),
    ("lookfantastic", "list", {"path": "/black-friday"}, "list"),
    ("lookfantastic", "product", {"sku": "11200055"}, "product"),
    ("lookfantastic", "suggestions", {"query": "cerave"}, "suggestions"),
    ("lookfantastic", "offers", {}, "offers"),
    ("lookfantastic", "brands", {}, "brands"),
    ("lookfantastic", "categories", {}, "categories"),
    ("cultbeauty", "search", {"query": "glow tonic"}, "search"),
    ("cultbeauty", "list", {"path": "/black-friday-cyber-monday"}, "list"),
    ("cultbeauty", "product", {"sku": "11200055"}, "product"),
    ("cultbeauty", "suggestions", {"query": "olaplex"}, "suggestions"),
    ("cultbeauty", "offers", {}, "offers"),
    ("cultbeauty", "brands", {}, "brands"),
    ("cultbeauty", "categories", {}, "categories"),
    ("yesstyle", "search", {"query": "snail mucin"}, "search"),
    ("yesstyle", "category", {"category": "15556"}, "category"),
    ("yesstyle", "brand", {"brand": "317041"}, "brand"),
    ("yesstyle", "brands", {}, "brands"),
    ("yesstyle", "deals", {}, "deals"),
    ("yesstyle", "product", {"product_id": "1052684695"}, "product"),
    ("yesstyle", "reviews", {"product_id": "1052684695"}, "reviews"),
    ("yesstyle", "suggestions", {"query": "cosrx"}, "suggestions"),
    ("yesstyle", "markets", {}, "markets"),
    ("notino", "search", {"query": "vitamin c serum"}, "search"),
    (
        "notino", "product",
        {
            "url": "https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/",
        },
        "product",
    ),
    (
        "notino", "reviews",
        {
            "url": "https://www.notino.de/dior/sauvage-eau-de-parfum-fuer-herren/",
        },
        "reviews",
    ),
    ("notino", "category", {"category": "/hautseren/"}, "category"),
    ("notino", "brand", {"brand": "cerave"}, "brand"),
    ("notino", "promo", {}, "promo"),
    ("notino", "brands", {}, "brands"),
    ("notino", "suggestions", {"query": "dior sa"}, "suggestions"),
    ("notino", "stores", {}, "stores"),
    ("notino", "store", {"store": "florentinum-praha"}, "store"),
    ("douglas", "search", {"query": "mascara"}, "search"),
    ("douglas", "category", {"category": "parfum/01"}, "category"),
    ("douglas", "brand", {"brand": "dior/b0690"}, "brand"),
    ("douglas", "deals", {}, "deals"),
    ("douglas", "product", {"code": "5000005003"}, "product"),
    ("douglas", "stores", {"query": "Berlin"}, "stores"),
    ("douglas", "store", {"store_id": "00020475"}, "store"),
    ("douglas", "review_summary", {"code": "5000005003"}, "review-summary"),
    ("douglas", "suggestions", {"query": "dior"}, "suggestions"),
    ("douglas", "brands", {}, "brands"),
    (
        "boots", "product",
        {
            "url": ("https://www.boots.com/no7-protect-and-per"
                "fect-intense-advanced-serum-30ml-10288490"),
        },
        "product",
    ),
    (
        "boots", "store_stock",
        {
            "item_code": "10213975001",
            "catentry_id": "1838584",
            "postcode": "NG2 3AA",
        },
        "store-stock",
    ),
    ("boots", "stores", {"postcode": "M1 1AE"}, "stores"),
    ("boots", "store", {"store": "868-london-battersea-sw11-1qn"}, "store"),
    ("rockauto", "vehicles", {}, "vehicles"),
    (
        "rockauto", "categories",
        {
            "make": "HONDA",
            "year": 2010,
            "model": "ACCORD",
            "engine": "2.4L L4",
            "carcode": "1444945",
        },
        "categories",
    ),
    (
        "rockauto", "parts",
        {
            "make": "HONDA",
            "year": 2010,
            "model": "ACCORD",
            "engine": "2.4L L4",
            "carcode": "1444945",
            "category": "Brake & Wheel Hub",
            "part_type_id": "1684",
        },
        "parts",
    ),
    ("rockauto", "search", {"part_number": "BP1084"}, "search"),
    ("rockauto", "brand", {"brand": "BOSCH", "part_type_id": "1684"}, "brand"),
    ("rockauto", "brands", {}, "brands"),
    ("rockauto", "part", {"part_key": "6129207", "part_type_id": "1684"}, "part"),
    ("rockauto", "suggestions", {"query": "2015 ford f-150"}, "suggestions"),
    ("rockauto", "resolve", {"query": "2010 honda accord brake pads"}, "resolve"),
    ("rockauto", "tools", {}, "tools"),
    ("rockauto", "promotions", {}, "promotions"),
    ("carscom", "search", {"zip": "10001"}, "search"),
    ("carscom", "listing", {"listing_id": "90e3df05-5f5e-4f4d-a474-79eb2077c99a"}, "listing"),
    ("carscom", "dealer", {"dealer_id": "97701"}, "dealer"),
    ("carscom", "dealer_inventory", {"dealer_id": "97701"}, "dealer-inventory"),
    ("carscom", "dealer_reviews", {"dealer_id": "97701"}, "dealer-reviews"),
    (
        "carscom", "model_reviews",
        {
            "make": "Toyota",
            "model": "RAV4",
            "year": 2019,
        },
        "model-reviews",
    ),
    ("carscom", "dealers", {"zip": "10001"}, "dealers"),
    ("carscom", "research", {"make": "Toyota"}, "research"),
    ("autotrader", "search", {"zip": "90012"}, "search"),
    ("autotrader", "listing", {"listing_id": "795241382"}, "listing"),
    ("autotrader", "dealers", {"zip": "90012"}, "dealers"),
    ("autotrader", "dealer", {"dealer_id": "87788"}, "dealer"),
    ("autotrader", "makes", {"make": "Honda"}, "makes"),
    ("cargurus", "search", {"zip": "10001"}, "search"),
    ("cargurus", "dealer", {"dealer_id": "440818"}, "dealer"),
    ("cargurus", "dealers", {"zip": "10001"}, "dealers"),
    ("cargurus", "price_trends", {}, "price-trends"),
    ("cargurus", "research", {"research_id": "c31935"}, "research"),
    ("cargurus", "expert_reviews", {}, "expert-reviews"),
    ("cargurus", "makes", {}, "makes"),
    ("cargurus", "models", {"make": "Toyota"}, "models"),
    ("carmax", "search", {"zip": "75201"}, "search"),
    ("carmax", "listing", {"stock_number": "28466923"}, "listing"),
    ("carmax", "photos", {"stock_number": "28466923"}, "photos"),
    ("carmax", "stores", {"zip": "75201"}, "stores"),
    ("carmax", "store", {"store_id": "7115"}, "store"),
    ("carmax", "store_inventory", {"store_id": "7115", "zip": "75201"}, "store-inventory"),
    ("carmax", "reviews", {"make": "Toyota", "model": "RAV4", "year": 2022}, "reviews"),
    (
        "carmax", "review_summary",
        {
            "make": "Toyota",
            "model": "RAV4",
            "year": 2022,
        },
        "review-summary",
    ),
    ("carmax", "suggestions", {"query": "rav"}, "suggestions"),
    ("carmax", "makes", {}, "makes"),
    ("carmax", "models", {"make": "toyota"}, "models"),
    ("carmax", "car_value", {"make": "Ford", "model": "F-150", "year": 2019}, "car-value"),
    ("carvana", "search", {}, "search"),
    ("carvana", "vehicle", {"vehicle_id": "4850967"}, "vehicle"),
    ("carvana", "model_guide", {"year": 2021, "make": "Toyota", "model": "RAV4"}, "model-guide"),
    ("carvana", "trims", {"make": "Toyota", "model": "RAV4"}, "trims"),
    ("carvana", "make", {"make": "Toyota"}, "make"),
    ("carvana", "makes", {}, "makes"),
    ("bringatrailer", "results", {}, "results"),
    ("bringatrailer", "price_history", {"model_id": 1833018}, "price-history"),
    ("bringatrailer", "listing", {"slug": "1988-bmw-m3-272-2"}, "listing"),
    ("bringatrailer", "live", {}, "live"),
    ("bringatrailer", "make", {"make": "bmw"}, "make"),
    ("bringatrailer", "model", {"model": "bmw/e30-m3"}, "model"),
    ("bringatrailer", "location", {"country": "germany"}, "location"),
    ("bringatrailer", "suggestions", {"query": "land cruiser"}, "suggestions"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH_1126_WIRE)
def test_batch_1126_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH_1126[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH_1126_ONE_OF))
def test_batch_1126_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch_1126_boots_has_no_search_and_carvana_no_zip():
    names = {ep.method for ep in ENDPOINTS.values() if ep.namespace == "boots"}
    assert "search" not in names
    carvana = {p.name for p in ENDPOINTS["carvana_search"].params}
    assert not {"zip", "postal_code", "query"} & carvana
    assert {p.wire_field for p in ENDPOINTS["lookfantastic_search"].params} >= {"q"}
    assert ENDPOINTS["notino_reviews"].min_timeout == 250.0
    assert ENDPOINTS["douglas_search"].min_timeout == 250.0


# --- batch 2 2026-11-26: 8 namespaces (real estate, travel, cars), from the backend routes ---

BATCH2_1126 = {
    "rentcom": {
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "building": ("building", 1, 240.0),
        "rent_trends": ("rent-trends", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "cities": ("cities", 1, 240.0),
    },
    "trulia": {
        "neighborhood": ("neighborhood", 1, 240.0),
        "search": ("search", 1, 240.0),
        "property": ("property", 1, 240.0),
        "school": ("school", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "streeteasy": {
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "building": ("building", 1, 240.0),
        "buildings": ("buildings", 1, 240.0),
        "market": ("market", 1, 240.0),
    },
    "rentcafe": {
        "search": ("search", 1, 240.0),
        "property": ("property", 1, 240.0),
        "floorplan_units": ("floorplan-units", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "rent_trends": ("rent-trends", 1, 240.0),
    },
    "vrbo": {
        "search": ("search", 2, 250.0),
        "property": ("property", 2, 250.0),
        "suggestions": ("suggestions", 2, 250.0),
    },
    "truecar": {
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "model": ("model", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "dealer": ("dealer", 1, 240.0),
        "dealer_inventory": ("dealer-inventory", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "makes": ("makes", 1, 240.0),
        "models": ("models", 1, 240.0),
    },
    "edmunds": {
        "search": ("search", 2, 250.0),
        "listing": ("listing", 2, 250.0),
        "reviews": ("reviews", 2, 250.0),
        "dealer": ("dealer", 2, 250.0),
        "model": ("model", 2, 250.0),
        "price": ("price", 2, 250.0),
        "appraisal": ("appraisal", 2, 250.0),
        "makes": ("makes", 2, 250.0),
    },
    "kbb": {
        "car_value": ("car-value", 1, 250.0),
        "model": ("model", 1, 250.0),
        "search": ("search", 1, 250.0),
        "listing": ("listing", 1, 250.0),
        "reviews": ("reviews", 1, 250.0),
        "dealers": ("dealers", 1, 250.0),
        "dealer": ("dealer", 1, 250.0),
        "makes_models": ("makes-models", 1, 250.0),
    },
}
BATCH2_1126_ONE_OF = {
    "rentcom_search": ("city", "zip"),
    "rentcom_listing": ("id", "url"),
    "rentcom_building": ("building_id", "url"),
    "trulia_neighborhood": ("location_id", "url"),
    "trulia_property": ("zpid", "building_id", "url"),
    "trulia_school": ("url", "school_id"),
    "streeteasy_listing": ("url", "id"),
    "streeteasy_building": ("slug", "url"),
    "rentcafe_search": ("location", "city", "zip"),
    "rentcafe_property": ("url", "slug"),
    "vrbo_search": ("destination", "region_id"),
    "vrbo_property": ("id", "url"),
    "truecar_listing": ("vin", "url"),
    "truecar_dealer": ("dealer_id", "url"),
    "truecar_dealer_inventory": ("dealer_id", "url"),
    "edmunds_listing": ("vin", "url"),
    "edmunds_dealer": ("dealer_id", "url"),
    "kbb_listing": ("listing_id", "url"),
    "kbb_dealer": ("dealer_id", "url"),
}
BATCH2_1126_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|fallback|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super|plain pool|residential|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH2_1126))
def test_batch2_1126_credits_paths_timeouts(namespace):
    """Every endpoint of the 8 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH2_1126[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(ep.one_of) == ((BATCH2_1126_ONE_OF[ep.key],) if ep.key in
                                    BATCH2_1126_ONE_OF else ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        text = text.lower().replace("is_fallback", "").replace("unrelated fallback", "")
        assert not BATCH2_1126_BANNED.search(text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH2_1126_WIRE = [
    ("rentcom", "search", {"city": "Austin"}, "search"),
    ("rentcom", "listing", {"id": "lc5898701"}, "listing"),
    ("rentcom", "building", {"building_id": "b147857"}, "building"),
    ("rentcom", "rent_trends", {"city": "Austin", "state": "TX"}, "rent-trends"),
    ("rentcom", "suggestions", {"query": "Austin"}, "suggestions"),
    ("rentcom", "cities", {"state": "TX"}, "cities"),
    ("trulia", "neighborhood", {"location_id": "85381"}, "neighborhood"),
    ("trulia", "search", {"location": "Austin, TX"}, "search"),
    ("trulia", "property", {"zpid": "339349810"}, "property"),
    ("trulia", "school", {"url": "x-url"}, "school"),
    ("trulia", "suggestions", {"query": "Austin"}, "suggestions"),
    ("streeteasy", "search", {"area": "Brooklyn"}, "search"),
    ("streeteasy", "listing", {"url": "https://streeteasy.com/building/the-pilot/3e"}, "listing"),
    ("streeteasy", "building", {"slug": "eastlight-condominium"}, "building"),
    ("streeteasy", "buildings", {"area": "Williamsburg"}, "buildings"),
    ("streeteasy", "market", {}, "market"),
    ("rentcafe", "search", {"location": "austin-tx"}, "search"),
    ("rentcafe", "property", {"url": "x-url"}, "property"),
    (
        "rentcafe", "floorplan_units",
        {
            "property_id": "1651075",
            "floorplan_id": "4746456",
        },
        "floorplan-units",
    ),
    ("rentcafe", "reviews", {"property_id": "1651075"}, "reviews"),
    ("rentcafe", "suggestions", {"query": "Austin"}, "suggestions"),
    ("rentcafe", "rent_trends", {"city": "Austin", "state": "TX"}, "rent-trends"),
    (
        "vrbo", "search",
        {
            "check_in": "2027-01-15",
            "check_out": "2027-01-18",
            "destination": "Destin, Florida",
        },
        "search",
    ),
    ("vrbo", "property", {"id": "1046285"}, "property"),
    ("vrbo", "suggestions", {"query": "destin"}, "suggestions"),
    ("truecar", "search", {"zip": "10001"}, "search"),
    ("truecar", "listing", {"vin": "x-vin"}, "listing"),
    ("truecar", "model", {"make": "Toyota", "model": "RAV4"}, "model"),
    ("truecar", "reviews", {"make": "Toyota", "model": "RAV4"}, "reviews"),
    ("truecar", "dealer", {"dealer_id": "414984"}, "dealer"),
    ("truecar", "dealer_inventory", {"dealer_id": "414984"}, "dealer-inventory"),
    ("truecar", "suggestions", {"query": "rav4"}, "suggestions"),
    ("truecar", "makes", {}, "makes"),
    ("truecar", "models", {"make": "Toyota"}, "models"),
    ("edmunds", "search", {"city": "New York", "state": "NY"}, "search"),
    ("edmunds", "listing", {"vin": "x-vin"}, "listing"),
    ("edmunds", "reviews", {"make": "Toyota", "model": "RAV4", "year": 2022}, "reviews"),
    ("edmunds", "dealer", {"dealer_id": "JakeSweeneyMitsubishi_891713"}, "dealer"),
    ("edmunds", "model", {"make": "Toyota", "model": "RAV4"}, "model"),
    ("edmunds", "price", {"make": "Toyota", "model": "RAV4", "year": 2022}, "price"),
    ("edmunds", "appraisal", {"make": "Toyota", "model": "RAV4", "year": 2022}, "appraisal"),
    ("edmunds", "makes", {"make": "Toyota"}, "makes"),
    (
        "kbb", "car_value",
        {
            "make": "Toyota",
            "model": "rav4",
            "year": 2021,
            "trim": "le-sport-utility-4d",
        },
        "car-value",
    ),
    ("kbb", "model", {"make": "Toyota", "model": "rav4", "year": 2021}, "model"),
    ("kbb", "search", {"zip": "10001"}, "search"),
    ("kbb", "listing", {"listing_id": "796688649"}, "listing"),
    ("kbb", "reviews", {"make": "Toyota", "model": "rav4", "year": 2021}, "reviews"),
    ("kbb", "dealers", {"zip": "10001"}, "dealers"),
    ("kbb", "dealer", {"dealer_id": "68613"}, "dealer"),
    ("kbb", "makes_models", {}, "makes-models"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH2_1126_WIRE)
def test_batch2_1126_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH2_1126[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH2_1126_ONE_OF))
def test_batch2_1126_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch2_1126_vin_is_input_only_and_skipped_params_absent():
    """VINs go in (truecar / edmunds listing) and the refused TrueCar inputs are not offered."""
    assert "vin" in {p.name for p in ENDPOINTS["truecar_listing"].params}
    assert "vin" in {p.name for p in ENDPOINTS["edmunds_listing"].params}
    truecar = {p.name for p in ENDPOINTS["truecar_search"].params}
    assert not {"query", "keyword", "mileage_min", "seller_type"} & truecar
    assert "sort" not in {p.name for p in ENDPOINTS["truecar_reviews"].params}
    assert ENDPOINTS["truecar_makes"].params == ()
    assert ENDPOINTS["vrbo_search"].credits == 2
    assert ENDPOINTS["edmunds_makes"].credits == 2
    assert ENDPOINTS["kbb_car_value"].min_timeout == 250.0
    assert ENDPOINTS["rentcom_search"].min_timeout == 240.0


# --- batch 3 2026-11-26: 11 namespaces (real estate, storage, estate sales, books, travel) ---

BATCH3_1126 = {
    "movoto": {
        "search": ("search", 1, 240.0),
        "property": ("property", 1, 240.0),
        "market_trends": ("market-trends", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "school": ("school", 1, 240.0),
    },
    "hotpads": {
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "price_history": ("price-history", 1, 240.0),
        "fees": ("fees", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "apartmentlist": {
        "suggestions": ("suggestions", 1, 240.0),
        "search": ("search", 1, 240.0),
        "listing": ("listing", 1, 240.0),
        "rent_report": ("rent-report", 1, 240.0),
        "market_summary": ("market-summary", 1, 240.0),
        "review_summaries": ("review-summaries", 1, 240.0),
    },
    "compass": {
        "search": ("search", 2, 240.0),
        "listing": ("listing", 2, 240.0),
        "suggestions": ("suggestions", 2, 240.0),
    },
    "affordablehousing": {
        "search": ("search", 2, 240.0),
        "listing": ("listing", 1, 240.0),
        "suggestions": ("suggestions", 2, 240.0),
        "waiting_lists": ("waiting-lists", 1, 240.0),
        "housing_authority": ("housing-authority", 1, 240.0),
        "housing_authorities": ("housing-authorities", 1, 240.0),
    },
    "lennar": {
        "search": ("search", 1, 240.0),
        "community": ("community", 1, 240.0),
        "plan": ("plan", 1, 240.0),
        "home": ("home", 1, 240.0),
        "master_planned": ("master-planned", 1, 240.0),
        "markets": ("markets", 1, 240.0),
        "market": ("market", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "resolve": ("resolve", 1, 240.0),
        "promotions": ("promotions", 1, 240.0),
        "payment": ("payment", 1, 240.0),
    },
    "extraspace": {
        "search": ("search", 1, 240.0),
        "facility": ("facility", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "city_prices": ("city-prices", 1, 240.0),
        "locations": ("locations", 1, 240.0),
    },
    "publicstorage": {
        "search": ("search", 1, 240.0),
        "facility": ("facility", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
    },
    "estatesales": {
        "sales": ("sales", 1, 240.0),
        "sale": ("sale", 1, 240.0),
        "companies": ("companies", 1, 240.0),
        "company": ("company", 1, 240.0),
        "search": ("search", 1, 240.0),
        "item": ("item", 1, 240.0),
    },
    "goodreads": {
        "search": ("search", 1, 240.0),
        "book": ("book", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "author": ("author", 1, 240.0),
        "author_books": ("author-books", 1, 240.0),
        "series": ("series", 1, 240.0),
        "editions": ("editions", 1, 240.0),
        "list": ("list", 1, 240.0),
        "book_lists": ("book-lists", 1, 240.0),
        "list_search": ("list-search", 1, 240.0),
        "quotes": ("quotes", 1, 240.0),
        "genre": ("genre", 1, 240.0),
        "new_releases": ("new-releases", 1, 240.0),
    },
    "expedia": {
        "search": ("search", 2, 250.0),
        "property": ("property", 2, 250.0),
        "price_calendar": ("price-calendar", 2, 250.0),
        "suggestions": ("suggestions", 2, 250.0),
    },
}
BATCH3_1126_ONE_OF = {
    "movoto_search": ("city", "zip", "county"),
    "movoto_property": ("url", "path"),
    "movoto_market_trends": ("city", "zip"),
    "movoto_school": ("url", "path"),
    "hotpads_listing": ("url", "id"),
    "apartmentlist_search": ("location", "city", "zip"),
    "apartmentlist_listing": ("url", "slug"),
    "apartmentlist_rent_report": ("city_slug", "city"),
    "apartmentlist_market_summary": ("location", "city", "zip"),
    "apartmentlist_review_summaries": ("city_slug", "city"),
    "compass_listing": ("url", "id"),
    "affordablehousing_listing": ("url", "id"),
    "affordablehousing_housing_authority": ("url", "id"),
    "lennar_search": ("market", "state", "city", "text", "latitude", "bounds"),
    "lennar_resolve": ("url", "path"),
    "extraspace_search": ("term", "latitude"),
    "extraspace_facility": ("store_id", "url"),
    "extraspace_reviews": ("store_id", "url"),
    "publicstorage_search": ("location", "slug"),
    "publicstorage_facility": ("store_id", "url"),
    "estatesales_sales": ("zip", "city"),
    "estatesales_companies": ("metro", "city"),
    "estatesales_sale": ("sale_id", "url"),
    "estatesales_company": ("org_id", "url"),
    "estatesales_item": ("item_id", "url"),
    "goodreads_book": ("book_id", "url", "isbn"),
    "goodreads_reviews": ("book_id", "url"),
    "goodreads_author": ("author_id", "url"),
    "goodreads_author_books": ("author_id", "url"),
    "goodreads_series": ("series_id", "url"),
    "goodreads_editions": ("work_id", "url"),
    "goodreads_list": ("list_id", "url"),
    "goodreads_book_lists": ("book_id", "url"),
    "goodreads_quotes": ("query", "tag", "work_id"),
    "goodreads_new_releases": ("genre", "month"),
    "expedia_search": ("destination", "region_id"),
    "expedia_property": ("id", "path"),
    "expedia_price_calendar": ("id", "path"),
    "expedia_suggestions": ("query", "text"),
}
BATCH3_1126_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|fallback|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super|plain pool|residential|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH3_1126))
def test_batch3_1126_credits_paths_timeouts(namespace):
    """Every endpoint of the 11 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH3_1126[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(ep.one_of) == ((BATCH3_1126_ONE_OF[ep.key],) if ep.key in
                                    BATCH3_1126_ONE_OF else ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        text = text.lower().replace("is_fallback", "").replace("unrelated fallback", "")
        assert not BATCH3_1126_BANNED.search(text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH3_1126_WIRE = [
    ("movoto", "search", {"city": "Austin"}, "search"),
    (
        "movoto", "property",
        {
            "url": ("https://www.movoto.com/austin-tx/6001-sier"
                "ra-arbor-ct-austin-tx-78759/pid_lgzxbh54nh/"),
        },
        "property",
    ),
    ("movoto", "market_trends", {"city": "Austin"}, "market-trends"),
    ("movoto", "suggestions", {"query": "Austin"}, "suggestions"),
    (
        "movoto", "school",
        {
            "url": ("https://www.movoto.com/schools/austin-t"
                "x/davis-elementary-school-480894022775/"),
        },
        "school",
    ),
    ("hotpads", "search", {"area": "brooklyn-new-york-ny"}, "search"),
    (
        "hotpads", "listing",
        {
            "url": "https://hotpads.com/11227-drummond-dr-dallas-tx-75228-skrzz0/pad",
        },
        "listing",
    ),
    (
        "hotpads", "price_history",
        {
            "listing_alias": "5759ydyqtn49h",
            "model_id": "738529",
        },
        "price-history",
    ),
    ("hotpads", "fees", {"listing_alias": "5759ydyqtn49h"}, "fees"),
    ("hotpads", "suggestions", {"text": "brooklyn"}, "suggestions"),
    ("apartmentlist", "suggestions", {"query": "Austin"}, "suggestions"),
    ("apartmentlist", "search", {"location": "/tx/austin"}, "search"),
    (
        "apartmentlist", "listing",
        {
            "url": "https://www.apartmentlist.com/tx/austin/riata--4",
        },
        "listing",
    ),
    ("apartmentlist", "rent_report", {"city_slug": "/tx/austin"}, "rent-report"),
    ("apartmentlist", "market_summary", {"location": "/tx/austin"}, "market-summary"),
    ("apartmentlist", "review_summaries", {"city_slug": "/tx/austin"}, "review-summaries"),
    ("compass", "search", {"area": "austin-tx"}, "search"),
    (
        "compass", "listing",
        {
            "url": ("https://www.compass.com/homedetails/214"
                "1-Norlock-Ln-Dallas-TX-75201/19YYG3_pid/"),
        },
        "listing",
    ),
    ("compass", "suggestions", {"query": "Austin, TX"}, "suggestions"),
    ("affordablehousing", "search", {"state": "TX"}, "search"),
    (
        "affordablehousing", "listing",
        {
            "url": ("https://www.affordablehousing.com/hous"
                "ton-tx/the-reserve-at-westwood--766073/"),
        },
        "listing",
    ),
    ("affordablehousing", "suggestions", {"text": "Houston"}, "suggestions"),
    ("affordablehousing", "waiting_lists", {}, "waiting-lists"),
    (
        "affordablehousing", "housing_authority",
        {
            "url": ("https://www.affordablehousing.com/housing-au"
                "thority-ma/somerville-housing-authority-674/"),
        },
        "housing-authority",
    ),
    ("affordablehousing", "housing_authorities", {"state": "TX"}, "housing-authorities"),
    ("lennar", "search", {"market": "DAL"}, "search"),
    ("lennar", "community", {"comnum": "22704"}, "community"),
    ("lennar", "plan", {"comnum": "22704", "plan_number": "4504"}, "plan"),
    ("lennar", "home", {"lot_id": "22704535134"}, "home"),
    ("lennar", "master_planned", {"mpc_id": 1916}, "master-planned"),
    ("lennar", "markets", {}, "markets"),
    ("lennar", "market", {"market": "PHO"}, "market"),
    ("lennar", "suggestions", {"query": "Katy"}, "suggestions"),
    (
        "lennar", "resolve",
        {
            "path": "/new-homes/texas/houston/montgomery/kresston/melrose-ii",
        },
        "resolve",
    ),
    ("lennar", "promotions", {"market": "DAL"}, "promotions"),
    (
        "lennar", "payment",
        {
            "lot_id": "22704535134",
            "comnum": "22704",
            "down_payment": 40000,
            "interest_rate": 0.065,
        },
        "payment",
    ),
    ("extraspace", "search", {"term": "90012"}, "search"),
    ("extraspace", "facility", {"store_id": "1934"}, "facility"),
    ("extraspace", "reviews", {"store_id": "1934"}, "reviews"),
    ("extraspace", "city_prices", {"city": "Dallas", "state": "TX"}, "city-prices"),
    ("extraspace", "locations", {}, "locations"),
    ("publicstorage", "search", {"location": "75201"}, "search"),
    ("publicstorage", "facility", {"store_id": "2044"}, "facility"),
    ("publicstorage", "reviews", {"store_id": "2044"}, "reviews"),
    ("estatesales", "sales", {"zip": "75201"}, "sales"),
    ("estatesales", "sale", {"sale_id": "5114622"}, "sale"),
    (
        "estatesales", "companies",
        {
            "state": "TX",
            "metro": "Dallas-Fort-Worth-Arlington",
        },
        "companies",
    ),
    ("estatesales", "company", {"org_id": "14402"}, "company"),
    ("estatesales", "search", {"query": "rolex"}, "search"),
    ("estatesales", "item", {"item_id": "2038603"}, "item"),
    ("goodreads", "search", {"query": "dune"}, "search"),
    ("goodreads", "book", {"book_id": "44767458"}, "book"),
    ("goodreads", "reviews", {"book_id": "44767458"}, "reviews"),
    ("goodreads", "suggestions", {"query": "sanderson"}, "suggestions"),
    ("goodreads", "author", {"author_id": "38550"}, "author"),
    ("goodreads", "author_books", {"author_id": "38550"}, "author-books"),
    ("goodreads", "series", {"series_id": "49075"}, "series"),
    ("goodreads", "editions", {"work_id": "3634639"}, "editions"),
    ("goodreads", "list", {"list_id": "1"}, "list"),
    ("goodreads", "book_lists", {"book_id": "44767458"}, "book-lists"),
    ("goodreads", "list_search", {"query": "fantasy"}, "list-search"),
    ("goodreads", "quotes", {"query": "hope"}, "quotes"),
    ("goodreads", "genre", {"genre": "fantasy"}, "genre"),
    ("goodreads", "new_releases", {"genre": "fantasy"}, "new-releases"),
    (
        "expedia", "search",
        {
            "check_in": "2027-03-12",
            "check_out": "2027-03-15",
            "destination": "Las Vegas, NV",
        },
        "search",
    ),
    ("expedia", "property", {"id": "17117062"}, "property"),
    (
        "expedia", "price_calendar",
        {
            "check_in": "2027-03-12",
            "check_out": "2027-03-15",
            "id": "17117062",
        },
        "price-calendar",
    ),
    ("expedia", "suggestions", {"query": "new yo"}, "suggestions"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH3_1126_WIRE)
def test_batch3_1126_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH3_1126[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH3_1126_ONE_OF))
def test_batch3_1126_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch3_1126_credits_wire_and_timeouts():
    """Compass 2 credits, AffordableHousing.com 2 on search and suggestions, Expedia actual cost."""
    assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == "compass"} == {2}
    assert ENDPOINTS["affordablehousing_search"].credits == 2
    assert ENDPOINTS["affordablehousing_suggestions"].credits == 2
    assert ENDPOINTS["affordablehousing_listing"].credits == 1
    assert ENDPOINTS["affordablehousing_waiting_lists"].credits == 1
    for m in ("search", "property", "price_calendar", "suggestions"):
        ep = ENDPOINTS[f"expedia_{m}"]
        assert ep.credits == 2 and ep.min_timeout == 250.0, ep.key
        assert "actual cost" in (ep.credits_note or ""), ep.key
    q = {p.name: p.wire_field for p in ENDPOINTS["compass_suggestions"].params}
    assert q == {"query": "q"}
    assert ENDPOINTS["lennar_markets"].params == ()
    assert "pages" in {p.name for p in ENDPOINTS["goodreads_reviews"].params}
    assert ENDPOINTS["movoto_search"].min_timeout == 240.0
    assert all(p.doc for ep in ENDPOINTS.values() if ep.namespace in BATCH3_1126 for p in ep.params)


# --- batch 4 2026-11-26: 8 namespaces (US retailers) ---

BATCH4_1126 = {
    "academy": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "store_availability": ("store-availability", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "bathandbodyworks": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "promotions": ("promotions", 1, 240.0),
        "offers": ("offers", 1, 240.0),
        "store_availability": ("store-availability", 1, 240.0),
        "store": ("store", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "reviews_summary": ("reviews-summary", 1, 240.0),
    },
    "gap": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "prices": ("prices", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "store_stock": ("store-stock", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "trending": ("trending", 1, 240.0),
        "deals": ("deals", 1, 240.0),
    },
    "rakuten": {
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "store_coupons": ("store-coupons", 1, 240.0),
        "rates": ("rates", 1, 240.0),
        "search": ("search", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "category": ("category", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "in_store": ("in-store", 1, 240.0),
    },
    "bjs": {
        "product": ("product", 1, 240.0),
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "coupons": ("coupons", 1, 240.0),
        "clubs": ("clubs", 1, 240.0),
    },
    "zappos": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "questions": ("questions", 1, 240.0),
        "lowest_prices": ("lowest-prices", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "newegg": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "categories": ("categories", 2, 240.0),
        "product": ("product", 2, 240.0),
        "offers": ("offers", 2, 240.0),
        "reviews": ("reviews", 2, 240.0),
        "deals": ("deals", 2, 240.0),
        "seller": ("seller", 2, 240.0),
        "seller_products": ("seller-products", 2, 240.0),
        "suggestions": ("suggestions", 2, 240.0),
    },
    "rei": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "deals": ("deals", 2, 240.0),
        "product": ("product", 2, 240.0),
        "reviews": ("reviews", 2, 240.0),
        "store_stock": ("store-stock", 2, 240.0),
        "stores": ("stores", 2, 240.0),
        "store": ("store", 2, 240.0),
        "suggestions": ("suggestions", 2, 240.0),
    },
}
BATCH4_1126_ONE_OF = {
    "academy_product": ("url", "slug"),
    "academy_stores": ("zip", "latitude"),
    "academy_category": ("path", "url"),
    "bathandbodyworks_product": ("product_id", "url"),
    "bathandbodyworks_promotions": ("product_id", "url"),
    "bathandbodyworks_store_availability": ("product_id", "url"),
    "bathandbodyworks_reviews_summary": ("product_id", "url"),
    "gap_category": ("cid", "url"),
    "gap_product": ("pid", "url"),
    "gap_stores": ("zip", "latitude"),
    "gap_store_stock": ("sku_ids", "style_id"),
    "bjs_product": ("product_id", "url"),
    "bjs_reviews": ("product_id", "url"),
    "zappos_product": ("product_id", "style_id", "stock_id", "asin"),
    "rei_category": ("slug", "url"),
    "rei_product": ("product_id", "url"),
    "rei_reviews": ("product_id", "url"),
    "rei_store_stock": ("zip", "city", "latitude"),
    "rei_stores": ("zip", "latitude"),
}
BATCH4_1126_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|fallback|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super|plain pool|residential|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH4_1126))
def test_batch4_1126_credits_paths_timeouts(namespace):
    """Every endpoint of the 8 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH4_1126[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(ep.one_of) == ((BATCH4_1126_ONE_OF[ep.key],) if ep.key in
                                    BATCH4_1126_ONE_OF else ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        text = text.lower().replace("is_fallback", "").replace("unrelated fallback", "")
        assert not BATCH4_1126_BANNED.search(text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH4_1126_WIRE = [
    ("academy", "search", {"query": "yeti tumbler"}, "search"),
    (
        "academy", "product",
        {
            "url": "https://www.academy.com/p/yeti-duracoat-rambler-20-oz-tumbler",
        },
        "product",
    ),
    (
        "academy", "store_availability",
        {
            "part_number": "111805768",
            "store_id": "19",
            "state": "TX",
        },
        "store-availability",
    ),
    ("academy", "stores", {"zip": "77098"}, "stores"),
    ("academy", "store", {"store_ids": ["19", "327", "256"]}, "store"),
    ("academy", "category", {"path": "/c/outdoors/coolers"}, "category"),
    ("academy", "categories", {}, "categories"),
    ("academy", "deals", {}, "deals"),
    ("academy", "suggestions", {"query": "yeti"}, "suggestions"),
    ("bathandbodyworks", "search", {"query": "candle"}, "search"),
    ("bathandbodyworks", "category", {"path": "/c/all-candles/3-wick-candles"}, "category"),
    ("bathandbodyworks", "categories", {}, "categories"),
    ("bathandbodyworks", "product", {"product_id": "028029548"}, "product"),
    ("bathandbodyworks", "promotions", {"product_id": "028029548"}, "promotions"),
    ("bathandbodyworks", "offers", {}, "offers"),
    (
        "bathandbodyworks", "store_availability",
        {
            "store_id": "BBW00010",
            "product_id": "028029548",
        },
        "store-availability",
    ),
    ("bathandbodyworks", "store", {"store_id": "BBW00010"}, "store"),
    ("bathandbodyworks", "stores", {}, "stores"),
    ("bathandbodyworks", "reviews_summary", {"product_id": "028029548"}, "reviews-summary"),
    ("gap", "search", {"query": "jeans"}, "search"),
    ("gap", "category", {"cid": "3033077"}, "category"),
    ("gap", "categories", {}, "categories"),
    ("gap", "product", {"pid": "403540002"}, "product"),
    (
        "gap", "prices",
        {
            "items": [{"brand": "old_navy", "pid": "903453022"}, "athleta:1177198082"],
        },
        "prices",
    ),
    ("gap", "stores", {"zip": "10001"}, "stores"),
    ("gap", "store", {"store_id": "4132"}, "store"),
    (
        "gap", "store_stock",
        {
            "store_ids": ["220", "1519", "1456"],
            "sku_ids": ["4035400023503"],
        },
        "store-stock",
    ),
    ("gap", "suggestions", {"query": "jea"}, "suggestions"),
    ("gap", "trending", {}, "trending"),
    ("gap", "deals", {}, "deals"),
    ("rakuten", "stores", {}, "stores"),
    ("rakuten", "store", {"store": "macys"}, "store"),
    ("rakuten", "store_coupons", {"store": "macys"}, "store-coupons"),
    ("rakuten", "rates", {"store_ids": ["8333", "7206", "3930"]}, "rates"),
    ("rakuten", "search", {"query": "nike"}, "search"),
    ("rakuten", "suggestions", {"query": "target"}, "suggestions"),
    ("rakuten", "category", {"category": "electronics"}, "category"),
    ("rakuten", "deals", {}, "deals"),
    ("rakuten", "in_store", {}, "in-store"),
    ("bjs", "product", {"product_id": "3000000000005430255"}, "product"),
    ("bjs", "search", {"query": "coffee"}, "search"),
    ("bjs", "category", {"category": "tvs-and-electronics>tvs"}, "category"),
    ("bjs", "categories", {}, "categories"),
    ("bjs", "reviews", {"product_id": "3000000000005430255"}, "reviews"),
    ("bjs", "coupons", {}, "coupons"),
    ("bjs", "clubs", {}, "clubs"),
    ("zappos", "search", {}, "search"),
    ("zappos", "product", {"product_id": "10002909"}, "product"),
    ("zappos", "reviews", {"product_id": "10002909"}, "reviews"),
    ("zappos", "questions", {"product_id": "10002909"}, "questions"),
    ("zappos", "lowest_prices", {"product_id": "10002909"}, "lowest-prices"),
    ("zappos", "categories", {}, "categories"),
    ("zappos", "suggestions", {"query": "hoka bon"}, "suggestions"),
    ("newegg", "search", {"query": "rtx 5070"}, "search"),
    ("newegg", "category", {"category_id": "100007709"}, "category"),
    ("newegg", "categories", {}, "categories"),
    ("newegg", "product", {"item_number": "N82E16819113877"}, "product"),
    ("newegg", "offers", {"item_number": "N82E16819113877"}, "offers"),
    (
        "newegg", "reviews",
        {
            "item_number": "N82E16819113877",
            "group_id": 196668433,
            "subcategory_id": 343,
        },
        "reviews",
    ),
    ("newegg", "deals", {}, "deals"),
    ("newegg", "seller", {"seller": "TECH-EDGE"}, "seller"),
    ("newegg", "seller_products", {"seller_id": "1066805289"}, "seller-products"),
    ("newegg", "suggestions", {"query": "rtx 5"}, "suggestions"),
    ("rei", "search", {"query": "rain jacket"}, "search"),
    ("rei", "category", {"slug": "tents"}, "category"),
    ("rei", "deals", {}, "deals"),
    ("rei", "product", {"product_id": "243702"}, "product"),
    ("rei", "reviews", {"product_id": "228617"}, "reviews"),
    ("rei", "store_stock", {"sku": "2437020001", "zip": "98101"}, "store-stock"),
    ("rei", "stores", {"zip": "80202"}, "stores"),
    ("rei", "store", {"store_number": "18"}, "store"),
    ("rei", "suggestions", {"query": "tent"}, "suggestions"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH4_1126_WIRE)
def test_batch4_1126_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH4_1126[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH4_1126_ONE_OF))
def test_batch4_1126_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch4_1126_credits_wire_and_timeouts():
    """Newegg and REI 2 credits, the other six 1; 240 s floor everywhere."""
    for ns in ("newegg", "rei"):
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {2}, ns
    for ns in ("academy", "bathandbodyworks", "gap", "rakuten", "bjs", "zappos"):
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    assert {ep.min_timeout for ep in ENDPOINTS.values() if ep.namespace in BATCH4_1126} == {240.0}
    assert not [
        ep.key for ep in ENDPOINTS.values() if ep.namespace in BATCH4_1126 and ep.credits_note
    ]
    assert ENDPOINTS["academy_categories"].params == ()
    assert ENDPOINTS["bjs_coupons"].params == ()
    assert [p.name for p in ENDPOINTS["academy_store_availability"].required_params] == [
        "part_number", "store_id", "state"]
    assert ENDPOINTS["zappos_product"].one_of == (("product_id", "style_id", "stock_id", "asin"),)
    assert ENDPOINTS["gap_store_stock"].one_of == (("sku_ids", "style_id"),)
    assert "items" in {p.name for p in ENDPOINTS["gap_prices"].required_params}
    assert all(p.doc for ep in ENDPOINTS.values() if ep.namespace in BATCH4_1126 for p in ep.params)


# --- batch 5 2026-11-27: 5 namespaces (QVC + HSN, B&N, ThriftBooks, U-Haul, Williams-Sonoma) ---

BATCH5_1127 = {
    "qvc": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "products": ("products", 1, 240.0),
        "todays_special": ("todays-special", 1, 240.0),
        "on_air": ("on-air", 1, 240.0),
        "program_guide": ("program-guide", 1, 240.0),
        "recently_aired": ("recently-aired", 1, 240.0),
        "category": ("category", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
    },
    "barnesandnoble": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "store_availability": ("store-availability", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "bestsellers": ("bestsellers", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "deals": ("deals", 1, 240.0),
    },
    "thriftbooks": {
        "search": ("search", 1, 240.0),
        "isbn": ("isbn", 1, 240.0),
        "work": ("work", 1, 240.0),
        "edition": ("edition", 1, 240.0),
        "copies": ("copies", 1, 240.0),
        "editions": ("editions", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "uhaul": {
        "truck_quote": ("truck-quote", 1, 240.0),
        "locations": ("locations", 1, 240.0),
        "location": ("location", 1, 240.0),
        "storage_search": ("storage-search", 1, 240.0),
        "storage_facility": ("storage-facility", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "supplies": ("supplies", 1, 240.0),
    },
    "williamssonoma": {
        "product": ("product", 1, 240.0),
        "configurator": ("configurator", 1, 240.0),
        "delivery_estimate": ("delivery-estimate", 1, 240.0),
        "stock": ("stock", 1, 240.0),
        "store_pickup": ("store-pickup", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "floor_samples": ("floor-samples", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "category": ("category", 5, 240.0),
        "search": ("search", 5, 240.0),
        "popular_searches": ("popular-searches", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
    },
}
BATCH5_1127_ONE_OF = {
    "qvc_product": (("item_number", "url"),),
    "qvc_category": (("url", "path"),),
    "qvc_reviews": (("item_number", "url"),),
    "barnesandnoble_product": (("ean", "isbn"),),
    "barnesandnoble_store_availability": (("ean", "isbn"),),
    "barnesandnoble_stores": (("near", "latitude"),),
    "barnesandnoble_category": (("path", "url"),),
    "uhaul_location": (("location_id", "url"),),
    "uhaul_storage_facility": (("facility_id", "url"),),
    "uhaul_reviews": (("location_id", "url"),),
    "uhaul_supplies": (("category", "url"),),
    "williamssonoma_product": (("product", "url"), ("brand", "url")),
    "williamssonoma_configurator": (("base_sku", "product", "url"), ("brand", "url")),
    "williamssonoma_delivery_estimate": (("product", "url", "skus"), ("brand", "url")),
    "williamssonoma_stock": (("product", "url"), ("brand", "url")),
    "williamssonoma_stores": (("zip", "latitude"),),
    "williamssonoma_floor_samples": (
        ("product", "url", "sku"), ("brand", "url"), ("zip", "latitude"),
    ),
    "williamssonoma_category": (("path", "url"),),
    "williamssonoma_reviews": (("product", "url"), ("brand", "url")),
}
BATCH5_1127_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|fallback|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super|plain pool|residential|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH5_1127))
def test_batch5_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 5 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH5_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH5_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        text = text.lower().replace("is_fallback", "").replace("unrelated fallback", "")
        assert not BATCH5_1127_BANNED.search(text), ep.key
        if namespace == "williamssonoma":
            assert not re.search(r"\b(ai|agents?|agentic|mcp|llms?|chatbots?)\b", text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH5_1127_WIRE = [
    ("qvc", "search", {"query": "blender"}, "search"),
    ("qvc", "product", {"item_number": "K341654"}, "product"),
    ("qvc", "products", {"item_numbers": ["K341654", "K82223", "A700206"]}, "products"),
    ("qvc", "todays_special", {}, "todays-special"),
    ("qvc", "on_air", {}, "on-air"),
    ("qvc", "program_guide", {}, "program-guide"),
    ("qvc", "recently_aired", {"site": "hsn"}, "recently-aired"),
    (
        "qvc", "category",
        {
            "url": "https://www.qvc.com/c/beauty/hair-care/hair-styling-tools/-/1ajqy/c.html",
        },
        "category",
    ),
    ("qvc", "suggestions", {"query": "blen"}, "suggestions"),
    ("qvc", "reviews", {"item_number": "K341654"}, "reviews"),
    ("barnesandnoble", "search", {"query": "project hail mary"}, "search"),
    ("barnesandnoble", "product", {"ean": "9780593135204"}, "product"),
    (
        "barnesandnoble", "store_availability",
        {
            "near": "60611",
            "ean": "9780593135204",
        },
        "store-availability",
    ),
    ("barnesandnoble", "stores", {"near": "10001"}, "stores"),
    ("barnesandnoble", "store", {"store_id": "2234"}, "store"),
    ("barnesandnoble", "suggestions", {"query": "hunger"}, "suggestions"),
    ("barnesandnoble", "bestsellers", {}, "bestsellers"),
    ("barnesandnoble", "category", {"path": "books/mystery-thrillers"}, "category"),
    ("barnesandnoble", "categories", {}, "categories"),
    ("barnesandnoble", "deals", {}, "deals"),
    ("thriftbooks", "search", {}, "search"),
    ("thriftbooks", "isbn", {"isbn": "9780593135204"}, "isbn"),
    ("thriftbooks", "work", {"work_id": "26830049"}, "work"),
    ("thriftbooks", "edition", {"edition_id": "49364660"}, "edition"),
    ("thriftbooks", "copies", {"edition_id": "49364660"}, "copies"),
    ("thriftbooks", "editions", {"work_id": "26830049"}, "editions"),
    ("thriftbooks", "reviews", {"work_id": "26830049"}, "reviews"),
    ("thriftbooks", "suggestions", {"query": "hunger"}, "suggestions"),
    ("uhaul", "truck_quote", {"pickup": "Dallas, TX", "date": "2026-12-10"}, "truck-quote"),
    ("uhaul", "locations", {"near": "75201"}, "locations"),
    ("uhaul", "location", {"location_id": "741028"}, "location"),
    ("uhaul", "storage_search", {"near": "Dallas, TX 75201"}, "storage-search"),
    ("uhaul", "storage_facility", {"facility_id": "741065"}, "storage-facility"),
    ("uhaul", "reviews", {"location_id": "741028"}, "reviews"),
    ("uhaul", "suggestions", {"term": "dall"}, "suggestions"),
    ("uhaul", "supplies", {"category": "Boxes"}, "supplies"),
    (
        "williamssonoma", "product",
        {
            "product": "gabrielle-upholstered-sofa",
            "brand": "pottery_barn",
        },
        "product",
    ),
    (
        "williamssonoma", "configurator",
        {
            "base_sku": "4889446",
            "brand": "pottery_barn",
        },
        "configurator",
    ),
    (
        "williamssonoma", "delivery_estimate",
        {
            "zip": "94103",
            "brand": "pottery_barn",
            "product": "gabrielle-upholstered-sofa",
        },
        "delivery-estimate",
    ),
    (
        "williamssonoma", "stock",
        {
            "product": "wusthof-classic-chefs-knife",
            "brand": "pottery_barn",
        },
        "stock",
    ),
    (
        "williamssonoma", "store_pickup",
        {
            "brand": "williams_sonoma",
            "skus": ["1468824", "2600435"],
            "stores": ["ST:0859", "ST:6016"],
        },
        "store-pickup",
    ),
    ("williamssonoma", "stores", {"zip": "60611"}, "stores"),
    (
        "williamssonoma", "floor_samples",
        {
            "product": "gabrielle-upholstered-sofa",
            "brand": "pottery_barn",
            "zip": "94103",
        },
        "floor-samples",
    ),
    ("williamssonoma", "categories", {"brand": "pottery_barn"}, "categories"),
    (
        "williamssonoma", "category",
        {
            "brand": "pottery_barn",
            "path": "furniture/sofas",
        },
        "category",
    ),
    ("williamssonoma", "search", {"brand": "williams_sonoma", "query": "chef knife"}, "search"),
    ("williamssonoma", "popular_searches", {"brand": "williams_sonoma"}, "popular-searches"),
    (
        "williamssonoma", "reviews",
        {
            "product": "shun-classic-chefs-knife",
            "brand": "williams_sonoma",
        },
        "reviews",
    ),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH5_1127_WIRE)
def test_batch5_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH5_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH5_1127_ONE_OF))
def test_batch5_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch5_1127_credits_wire_and_timeouts():
    """1 credit per call except Williams-Sonoma search and category (5); 240 s floor everywhere."""
    for ns in ("qvc", "barnesandnoble", "thriftbooks", "uhaul"):
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    ws = {ep.method: ep.credits for ep in ENDPOINTS.values() if ep.namespace == "williamssonoma"}
    assert {m for m, c in ws.items() if c == 5} == {"search", "category"}
    assert {c for m, c in ws.items() if m not in ("search", "category")} == {1}
    assert {ep.min_timeout for ep in ENDPOINTS.values() if ep.namespace in BATCH5_1127} == {240.0}
    assert not [
        ep.key for ep in ENDPOINTS.values() if ep.namespace in BATCH5_1127 and ep.credits_note
    ]
    assert ENDPOINTS["barnesandnoble_categories"].params[0].name == "country"
    assert [p.name for p in ENDPOINTS["uhaul_truck_quote"].required_params] == ["pickup", "date"]
    assert [p.name for p in ENDPOINTS["williamssonoma_store_pickup"].required_params] == [
        "brand", "skus", "stores"]
    assert ENDPOINTS["williamssonoma_floor_samples"].one_of == (
        ("product", "url", "sku"), ("brand", "url"), ("zip", "latitude"))
    reviews = {p.name for p in ENDPOINTS["williamssonoma_reviews"].params}
    assert "sort" not in reviews and "rating" not in reviews
    assert "item_numbers" in {p.name for p in ENDPOINTS["qvc_products"].required_params}
    assert all(p.doc for ep in ENDPOINTS.values() if ep.namespace in BATCH5_1127 for p in ep.params)


# --- batch 6 2026-11-27: 5 namespaces (Belk, A&F + Hollister, L.L.Bean, Sweetwater, BB&B) ---

BATCH6_1127 = {
    "belk": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "deals": ("deals", 2, 240.0),
        "categories": ("categories", 2, 240.0),
        "product": ("product", 2, 240.0),
        "variant": ("variant", 2, 240.0),
        "store_availability": ("store-availability", 1, 240.0),
        "stores": ("stores", 2, 240.0),
        "store": ("store", 2, 240.0),
        "reviews": ("reviews", 2, 240.0),
    },
    "abercrombie": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "store_stock": ("store-stock", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "promotions": ("promotions", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "llbean": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "store_stock": ("store-stock", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "review_summary": ("review-summary", 1, 240.0),
        "delivery_estimate": ("delivery-estimate", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "deals": ("deals", 1, 240.0),
    },
    "sweetwater": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "product": ("product", 1, 240.0),
        "serial_units": ("serial-units", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "deals": ("deals", 1, 240.0),
    },
    "bedbathbeyond": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "delivery_estimate": ("delivery-estimate", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "questions": ("questions", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "deals": ("deals", 1, 240.0),
    },
}
BATCH6_1127_ONE_OF = {
    "belk_product": (("product_id", "url"),),
    "belk_store_availability": (("variant_id", "items"),),
    "belk_reviews": (("product_id", "url"),),
    "abercrombie_store_stock": (("zip", "latitude"),),
    "abercrombie_stores": (("zip", "latitude"),),
    "llbean_store_stock": (("store_ids", "all_stores"),),
    "llbean_stores": (("zip", "latitude", "city", "store_ids", "all_stores"),),
    "sweetwater_product": (("item_id", "url"),),
    "sweetwater_serial_units": (("item_id", "url"),),
    "sweetwater_reviews": (("item_id", "url"),),
    "bedbathbeyond_search": (("query", "facet_url"),),
    "bedbathbeyond_category": (("slug", "url"), ("category_id", "url")),
    "bedbathbeyond_product": (("product_id", "url"),),
    "bedbathbeyond_reviews": (("product_id", "url"),),
    "bedbathbeyond_questions": (("product_id", "url"),),
}
BATCH6_1127_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|fallback|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super|plain pool|residential|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH6_1127))
def test_batch6_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 5 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH6_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH6_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        text = text.lower().replace("super buys", "").replace("super_buys", "")
        assert not BATCH6_1127_BANNED.search(text), ep.key
        assert not re.search(r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b", text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH6_1127_WIRE = [
    ("belk", "search", {"query": "sweater"}, "search"),
    ("belk", "category", {"category": "women/womens-clothing/sweaters"}, "category"),
    ("belk", "deals", {}, "deals"),
    ("belk", "categories", {}, "categories"),
    ("belk", "product", {"product_id": "18000269151219"}, "product"),
    ("belk", "variant", {"variant_id": "0480046046048"}, "variant"),
    (
        "belk", "store_availability",
        {
            "store_ids": ["452", "329", "270"],
            "variant_id": "0480046046048",
        },
        "store-availability",
    ),
    ("belk", "stores", {"zip": "28202"}, "stores"),
    ("belk", "store", {"store_id": "452"}, "store"),
    ("belk", "reviews", {"product_id": "18000269151219"}, "reviews"),
    ("abercrombie", "search", {"query": "baggy jeans"}, "search"),
    ("abercrombie", "product", {"product_id": "59359439"}, "product"),
    ("abercrombie", "store_stock", {"skus": ["662258406"], "zip": "10001"}, "store-stock"),
    ("abercrombie", "stores", {"zip": "10001"}, "stores"),
    ("abercrombie", "store", {"store_number": "11958"}, "store"),
    ("abercrombie", "category", {"category_id": "12236"}, "category"),
    ("abercrombie", "categories", {}, "categories"),
    ("abercrombie", "promotions", {}, "promotions"),
    ("abercrombie", "reviews", {"product_id": "59359439"}, "reviews"),
    ("abercrombie", "suggestions", {"query": "hoo"}, "suggestions"),
    ("llbean", "search", {"query": "fleece jacket"}, "search"),
    ("llbean", "category", {"category_id": "474"}, "category"),
    ("llbean", "categories", {}, "categories"),
    ("llbean", "product", {"product_id": "37037"}, "product"),
    (
        "llbean", "store_stock",
        {
            "item_id": "112644",
            "store_ids": ["0040", "1350", "2140"],
        },
        "store-stock",
    ),
    ("llbean", "stores", {"zip": "04032"}, "stores"),
    ("llbean", "reviews", {"product_id": "120785"}, "reviews"),
    ("llbean", "review_summary", {"product_id": "37037"}, "review-summary"),
    ("llbean", "delivery_estimate", {"item_id": "112644", "zip": "10001"}, "delivery-estimate"),
    ("llbean", "suggestions", {"query": "fle"}, "suggestions"),
    ("llbean", "deals", {}, "deals"),
    ("sweetwater", "search", {"query": "boss delay pedal"}, "search"),
    ("sweetwater", "category", {"category": "c590--Solid_Body_Guitars"}, "category"),
    ("sweetwater", "product", {"item_id": "DD8"}, "product"),
    ("sweetwater", "serial_units", {"item_id": "DD8"}, "serial-units"),
    ("sweetwater", "reviews", {"item_id": "DD8"}, "reviews"),
    ("sweetwater", "deals", {}, "deals"),
    ("bedbathbeyond", "search", {"query": "bath towels"}, "search"),
    (
        "bedbathbeyond", "category",
        {
            "slug": "bedding/bedding-sets",
            "category_id": "276",
        },
        "category",
    ),
    ("bedbathbeyond", "categories", {}, "categories"),
    ("bedbathbeyond", "product", {"product_id": "5296998"}, "product"),
    (
        "bedbathbeyond", "delivery_estimate",
        {
            "option_id": "94445783",
            "zip": "10001",
        },
        "delivery-estimate",
    ),
    ("bedbathbeyond", "reviews", {"product_id": "5296998"}, "reviews"),
    ("bedbathbeyond", "questions", {"product_id": "5296998"}, "questions"),
    ("bedbathbeyond", "stores", {}, "stores"),
    ("bedbathbeyond", "deals", {}, "deals"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH6_1127_WIRE)
def test_batch6_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH6_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH6_1127_ONE_OF))
def test_batch6_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch6_1127_credits_wire_and_timeouts():
    """Belk 2 (store_availability 1); BB&B search and category 2; the rest 1; 240 s floor."""
    for ns in ("abercrombie", "llbean", "sweetwater"):
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    belk = {ep.method: ep.credits for ep in ENDPOINTS.values() if ep.namespace == "belk"}
    assert {m for m, c in belk.items() if c != 2} == {"store_availability"}
    assert belk["store_availability"] == 1
    bbb = {ep.method: ep.credits for ep in ENDPOINTS.values() if ep.namespace == "bedbathbeyond"}
    assert {m for m, c in bbb.items() if c == 2} == {"search", "category"}
    assert {c for m, c in bbb.items() if m not in ("search", "category")} == {1}
    assert {ep.min_timeout for ep in ENDPOINTS.values() if ep.namespace in BATCH6_1127} == {240.0}
    noted = {ep.key for ep in ENDPOINTS.values() if ep.namespace in BATCH6_1127 and ep.credits_note}
    assert noted == {
        "belk_product", "belk_variant", "belk_store_availability", "abercrombie_reviews",
        "bedbathbeyond_deals", "bedbathbeyond_product",
    }
    assert "include_color_prices" in ENDPOINTS["belk_variant"].credits_note
    assert [p.name for p in ENDPOINTS["belk_store_availability"].required_params] == ["store_ids"]
    assert "radius" not in {p.name for p in ENDPOINTS["belk_stores"].params}
    reviews = {p.name for p in ENDPOINTS["belk_reviews"].params}
    assert not reviews & {"page", "sort", "rating"}
    assert [p.name for p in ENDPOINTS["abercrombie_store_stock"].required_params] == ["skus"]
    assert [p.name for p in ENDPOINTS["llbean_delivery_estimate"].required_params] == [
        "item_id", "zip"]
    assert ENDPOINTS["llbean_stores"].one_of == (
        ("zip", "latitude", "city", "store_ids", "all_stores"),)
    assert ENDPOINTS["bedbathbeyond_category"].one_of == (("slug", "url"), ("category_id", "url"))
    assert ENDPOINTS["bedbathbeyond_search"].params[0].name == "query"
    assert ENDPOINTS["bedbathbeyond_search"].params[0].wire_field == "query"
    assert all(p.doc for ep in ENDPOINTS.values() if ep.namespace in BATCH6_1127 for p in ep.params)


# --- batch 7 2026-11-27: 7 Brazil namespaces (KaBuM!, Magalu, Casas Bahia, Buscape, RD Saude,
# Reclame Aqui, Leroy Merlin) ---

BATCH7_1127 = {
    "kabum": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "shipping": ("shipping", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "offers": ("offers", 1, 240.0),
    },
    "magalu": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "deals": ("deals", 2, 240.0),
        "product": ("product", 2, 240.0),
        "reviews": ("reviews", 2, 240.0),
        "suggestions": ("suggestions", 2, 240.0),
        "stores": ("stores", 2, 240.0),
        "store": ("store", 2, 240.0),
    },
    "casasbahia": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "product": ("product", 2, 240.0),
        "categories": ("categories", 2, 240.0),
    },
    "buscape": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "offers": ("offers", 1, 240.0),
        "price_history": ("price-history", 1, 240.0),
        "lowest_price": ("lowest-price", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "deal_landing": ("deal-landing", 1, 240.0),
        "store": ("store", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "shipping": ("shipping", 1, 240.0),
    },
    "rdsaude": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "prices": ("prices", 1, 240.0),
        "store_availability": ("store-availability", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "stores_search": ("stores/search", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "reclameaqui": {
        "company_search": ("company-search", 1, 240.0),
        "company": ("company", 1, 240.0),
        "complaints": ("complaints", 1, 240.0),
        "complaint": ("complaint", 1, 240.0),
        "complaint_search": ("complaint-search", 1, 240.0),
        "rankings": ("rankings", 1, 240.0),
        "segments": ("segments", 1, 240.0),
        "segment_ranking": ("segment-ranking", 1, 240.0),
    },
    "leroymerlin": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "product": ("product", 1, 240.0),
        "store_stock": ("store-stock", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "shipping": ("shipping", 1, 240.0),
        "cep": ("cep", 1, 240.0),
        "regions": ("regions", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "offers": ("offers", 1, 240.0),
    },
}
BATCH7_1127_ONE_OF = {
    "kabum_product": (("product_id", "url"),),
    "kabum_shipping": (("product_id", "url"),),
    "kabum_reviews": (("product_id", "url"),),
    "magalu_product": (("product_id", "url"),),
    "magalu_reviews": (("product_id", "url"),),
    "magalu_store": (("store_id", "url"),),
    "casasbahia_product": (("sku", "url"),),
    "buscape_category": (("category_id", "category"),),
    "buscape_product": (("product_id", "url"),),
    "buscape_store": (("store_id", "store"),),
    "rdsaude_category": (("category_id", "url"),),
    "rdsaude_product": (("sku", "url"),),
    "reclameaqui_company": (("shortname", "url"),),
    "reclameaqui_complaints": (("company_id", "shortname"),),
    "reclameaqui_complaint": (("url", "company"), ("url", "complaint_id")),
    "reclameaqui_segment_ranking": (("main_segment", "url"), ("segment", "url")),
    "leroymerlin_product": (("id", "url"),),
    "leroymerlin_store_stock": (("id", "url"),),
    "leroymerlin_reviews": (("id", "url"),),
    "leroymerlin_shipping": (("id", "url"),),
    "leroymerlin_store": (("store", "url"),),
}
BATCH7_1127_BANNED = re.compile(
    r"\b(collect(s|ed|ing)?|data collection|scrap\w*|prox(y|ies)|bots?|render\w*|"
    r"retr(y|ies|ied)|cheapest|robots?|graphql|cookies?|cloudflare|firewall|fallback|"
    r"harvest\w*|crawl\w*|akamai|datadome|bazaarvoice|algolia|hybris|demandware|"
    r"wordpress|geocode|super|plain pool|residential|only api|first api)\b"
)


@pytest.mark.parametrize("namespace", sorted(BATCH7_1127))
def test_batch7_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 7 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH7_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH7_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        text = text.lower().replace("super buys", "").replace("super_buys", "")
        assert not BATCH7_1127_BANNED.search(text), ep.key
        assert not re.search(r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b", text), ep.key
        assert not [p.name for p in ep.params if p.doc.startswith(("Not offered", "Not supp"))]


BATCH7_1127_WIRE = [
    ("kabum", "search", {"query": "cadeira gamer"}, "search"),
    ("kabum", "category", {"category": "hardware/placa-de-video-vga"}, "category"),
    ("kabum", "categories", {}, "categories"),
    ("kabum", "product", {"product_id": "311424"}, "product"),
    ("kabum", "shipping", {"cep": "01310-100", "product_id": "311424"}, "shipping"),
    ("kabum", "reviews", {"product_id": "311424"}, "reviews"),
    ("kabum", "offers", {}, "offers"),
    ("magalu", "search", {"query": "geladeira frost free"}, "search"),
    (
        "magalu", "category",
        {
            "path": "/geladeira-refrigerador/eletrodomesticos/s/ed/refr/",
        },
        "category",
    ),
    ("magalu", "deals", {}, "deals"),
    ("magalu", "product", {"product_id": "238058800"}, "product"),
    ("magalu", "reviews", {"product_id": "238058800"}, "reviews"),
    ("magalu", "suggestions", {"query": "geladeira"}, "suggestions"),
    ("magalu", "stores", {"state": "sp"}, "stores"),
    ("magalu", "store", {"store_id": "1000"}, "store"),
    ("casasbahia", "search", {"query": "geladeira frost free"}, "search"),
    ("casasbahia", "category", {"path": "/c/eletroportateis?filtro=categoria-c73"}, "category"),
    ("casasbahia", "product", {"sku": "55066339"}, "product"),
    ("casasbahia", "categories", {}, "categories"),
    ("buscape", "search", {"query": "geladeira"}, "search"),
    ("buscape", "category", {"category_id": "8"}, "category"),
    ("buscape", "categories", {}, "categories"),
    ("buscape", "product", {"product_id": "12755140"}, "product"),
    ("buscape", "offers", {"product_id": "12755140"}, "offers"),
    ("buscape", "price_history", {"product_id": "12755140"}, "price-history"),
    ("buscape", "lowest_price", {"product_id": "12755140"}, "lowest-price"),
    ("buscape", "deals", {}, "deals"),
    ("buscape", "deal_landing", {"slug": "black-friday"}, "deal-landing"),
    ("buscape", "store", {"store_id": "21"}, "store"),
    ("buscape", "suggestions", {"query": "geladeira"}, "suggestions"),
    (
        "buscape", "shipping",
        {
            "product_id": "12755140",
            "cep": "01310-100",
            "state": "SP",
            "city": "São Paulo",
        },
        "shipping",
    ),
    ("rdsaude", "search", {"query": "protetor solar"}, "search"),
    ("rdsaude", "category", {"category_id": "515"}, "category"),
    ("rdsaude", "categories", {}, "categories"),
    ("rdsaude", "product", {"sku": "331137"}, "product"),
    ("rdsaude", "prices", {"skus": ["331137", "38155", "24216"]}, "prices"),
    (
        "rdsaude", "store_availability",
        {
            "skus": ["331137"],
            "store_ids": ["1156", "200"],
        },
        "store-availability",
    ),
    ("rdsaude", "stores", {"cep": "01310-100"}, "stores"),
    ("rdsaude", "stores_search", {}, "stores/search"),
    ("rdsaude", "reviews", {"sku": "38155"}, "reviews"),
    ("rdsaude", "deals", {}, "deals"),
    ("rdsaude", "suggestions", {"query": "shamp"}, "suggestions"),
    ("reclameaqui", "company_search", {"query": "nubank"}, "company-search"),
    ("reclameaqui", "company", {"shortname": "nubank"}, "company"),
    ("reclameaqui", "complaints", {"company_id": "88850"}, "complaints"),
    (
        "reclameaqui", "complaint",
        {
            "url": ("https://www.reclameaqui.com.br/nubank/quero-aumentar-meu-li"
                "mite-no-cartao-pois-o-atual-e-insuficiente_NhIy-6O6osFhQdJ-/"),
        },
        "complaint",
    ),
    ("reclameaqui", "complaint_search", {"query": "iphone quebrado"}, "complaint-search"),
    ("reclameaqui", "rankings", {}, "rankings"),
    ("reclameaqui", "segments", {}, "segments"),
    (
        "reclameaqui", "segment_ranking",
        {
            "main_segment": "bancos-e-financeiras",
            "segment": "bancos-digitais",
        },
        "segment-ranking",
    ),
    ("leroymerlin", "search", {"country": "br", "query": "furadeira"}, "search"),
    ("leroymerlin", "category", {"country": "br", "category": "furadeiras"}, "category"),
    ("leroymerlin", "product", {"country": "br", "id": "92450351"}, "product"),
    ("leroymerlin", "store_stock", {"country": "br", "id": "92450351"}, "store-stock"),
    ("leroymerlin", "stores", {"country": "br"}, "stores"),
    ("leroymerlin", "store", {"country": "br", "store": "raposo_tav"}, "store"),
    ("leroymerlin", "reviews", {"country": "br", "id": "92450351"}, "reviews"),
    ("leroymerlin", "shipping", {"cep": "01310-100", "id": "92450351"}, "shipping"),
    ("leroymerlin", "cep", {"cep": "01310-100"}, "cep"),
    ("leroymerlin", "regions", {}, "regions"),
    ("leroymerlin", "categories", {}, "categories"),
    ("leroymerlin", "suggestions", {"country": "it", "query": "trapano"}, "suggestions"),
    ("leroymerlin", "offers", {"country": "it"}, "offers"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH7_1127_WIRE)
def test_batch7_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH7_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH7_1127_ONE_OF))
def test_batch7_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch7_1127_credits_wire_and_timeouts():
    """KaBuM!, Buscape, RD Saude, Reclame Aqui 1; Magalu, Casas Bahia 2; Leroy Merlin per market."""
    for ns, credits in (("kabum", 1), ("buscape", 1), ("rdsaude", 1), ("reclameaqui", 1),
                        ("magalu", 2), ("casasbahia", 2), ("leroymerlin", 1)):
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {credits}, ns
    assert {ep.min_timeout for ep in ENDPOINTS.values() if ep.namespace in BATCH7_1127} == {240.0}
    noted = {ep.key for ep in ENDPOINTS.values() if ep.namespace in BATCH7_1127 and ep.credits_note}
    assert noted == {
        "reclameaqui_complaints", "leroymerlin_search", "leroymerlin_category",
        "leroymerlin_product", "leroymerlin_stores", "leroymerlin_store", "leroymerlin_reviews",
        "leroymerlin_suggestions",
    }
    assert "France 5" not in ENDPOINTS["leroymerlin_search"].credits_note
    assert "5 in France" in ENDPOINTS["leroymerlin_product"].credits_note
    assert "2 by shortname" in ENDPOINTS["reclameaqui_complaints"].credits_note
    rd = ENDPOINTS["rdsaude_stores_search"]
    assert rd.path == "/api/v1/rdsaude/stores/search" and rd.method == "stores_search"
    assert [p.name for p in ENDPOINTS["rdsaude_store_availability"].required_params] == [
        "skus", "store_ids"]
    assert [p.name for p in ENDPOINTS["buscape_shipping"].required_params] == [
        "product_id", "cep", "state", "city"]
    assert [p.name for p in ENDPOINTS["leroymerlin_search"].required_params] == ["country", "query"]
    assert [p.name for p in ENDPOINTS["kabum_shipping"].required_params] == ["cep"]
    assert ENDPOINTS["reclameaqui_complaint"].one_of == (
        ("url", "company"), ("url", "complaint_id"))
    assert not ENDPOINTS["reclameaqui_segments"].params
    assert {p.name for p in ENDPOINTS["casasbahia_search"].params} >= {"site", "own_store"}
    assert "carry no prices" in ENDPOINTS["casasbahia_search"].summary
    for ep in ENDPOINTS.values():
        if ep.namespace in BATCH7_1127:
            assert "keyed price service" not in ep.summary, ep.key
            assert "upstream / 5" not in ep.summary, ep.key
    assert all(p.doc for ep in ENDPOINTS.values() if ep.namespace in BATCH7_1127 for p in ep.params)


# --- batch 7 wave 2 2026-11-27: 3 Brazil namespaces (Natura, O Boticario + Eudora, Centauro) ---

BATCH7W2_1127 = {
    "natura": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "deals": ("deals", 1, 240.0),
    },
    "boticario": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "promotions": ("promotions", 1, 240.0),
        "product": ("product", 1, 240.0),
        "prices": ("prices", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "pickup": ("pickup", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "centauro": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "product": ("product", 1, 240.0),
        "freight": ("freight", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
}
BATCH7W2_1127_ONE_OF = {
    "natura_product": (("product_id", "url"),),
    "boticario_product": (("slug", "url", "sku"),),
    "boticario_pickup": (("slug", "url", "sku"),),
    "centauro_product": (("product_id", "model", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH7W2_1127))
def test_batch7w2_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 3 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH7W2_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH7W2_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b"
        assert not re.search(ai, text.lower()), ep.key


BATCH7W2_1127_WIRE = [
    ("natura", "search", {"query": "perfume"}, "search"),
    (
        "natura", "search",
        {"query": "perfume", "country": "mx", "filters": {"brand": "Kaiak"}},
        "search",
    ),
    ("natura", "category", {"category_id": "maquiagem"}, "category"),
    ("natura", "categories", {}, "categories"),
    ("natura", "product", {"product_id": "NATBRA-194225"}, "product"),
    ("natura", "suggestions", {"query": "kaiak"}, "suggestions"),
    ("natura", "stores", {"state": "sp", "type": "franchise"}, "stores"),
    ("natura", "deals", {}, "deals"),
    ("boticario", "search", {"query": "perfume"}, "search"),
    (
        "boticario", "search",
        {"query": "perfume", "brand": "eudora", "product_brand": ["egeo", "lily"]},
        "search",
    ),
    ("boticario", "category", {"path": "/perfumaria/"}, "category"),
    ("boticario", "categories", {}, "categories"),
    ("boticario", "deals", {"type": "promotions", "section": "cashback"}, "deals"),
    ("boticario", "promotions", {}, "promotions"),
    ("boticario", "product", {"slug": "base-liquida-cor-330-make-b-mate-salicylic-30g"}, "product"),
    ("boticario", "prices", {"skus": ["B01863", "B48734", "B2022081233"]}, "prices"),
    ("boticario", "reviews", {"product_id": "B2022081233"}, "reviews"),
    ("boticario", "stores", {"cep": "01310-100"}, "stores"),
    ("boticario", "pickup", {"cep": "01310-100", "sku": "B01863"}, "pickup"),
    ("boticario", "suggestions", {"query": "perfume"}, "suggestions"),
    ("centauro", "search", {"query": "tenis corrida"}, "search"),
    (
        "centauro", "search",
        {"query": "tenis corrida", "filters": ["marca:nike", "genero:masculino"]},
        "search",
    ),
    ("centauro", "category", {"path": "/nav/categorias/calcados/produto/tenis"}, "category"),
    ("centauro", "deals", {}, "deals"),
    ("centauro", "product", {"product_id": "9976EA51"}, "product"),
    ("centauro", "product", {"model": "9976EA", "color": "51"}, "product"),
    ("centauro", "freight", {"sku": "9976EA510375", "cep": "01310-100"}, "freight"),
    ("centauro", "stores", {"cep": "01310-100"}, "stores"),
    ("centauro", "suggestions", {"query": "tenis"}, "suggestions"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH7W2_1127_WIRE)
def test_batch7w2_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH7W2_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH7W2_1127_ONE_OF))
def test_batch7w2_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch7w2_1127_credits_wire_and_timeouts():
    """Natura, Centauro 1 flat; O Boticario 1, 2 when a page needs a second route, prices per 5."""
    for ns in BATCH7W2_1127:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    assert {ep.min_timeout for ep in ENDPOINTS.values() if ep.namespace in BATCH7W2_1127} == {240.0}
    w2 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH7W2_1127]
    noted = {ep.key for ep in w2 if ep.credits_note}
    assert noted == {
        "boticario_search", "boticario_category", "boticario_categories", "boticario_deals",
        "boticario_promotions", "boticario_product", "boticario_prices",
    }
    assert "second route" in ENDPOINTS["boticario_product"].credits_note
    assert "per 5 SKUs" in ENDPOINTS["boticario_prices"].credits_note
    assert [p.name for p in ENDPOINTS["boticario_pickup"].required_params] == ["cep"]
    assert [p.name for p in ENDPOINTS["boticario_prices"].required_params] == ["skus"]
    assert [p.name for p in ENDPOINTS["centauro_freight"].required_params] == ["sku", "cep"]
    assert [p.name for p in ENDPOINTS["natura_search"].required_params] == ["query"]
    assert not ENDPOINTS["natura_stores"].required_params
    assert ENDPOINTS["natura_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["centauro_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["boticario_product"].positional_optional_params[0].name == "slug"
    assert "AI summary" not in ENDPOINTS["boticario_product"].summary
    assert all(p.doc for ep in w2 for p in ep.params)


# --- batch 7 wave 3 2026-11-27: 3 Brazil namespaces (Enjoei, Atacadao, Carrefour Brasil) ---

BATCH7W3_1127 = {
    "enjoei": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "shop": ("shop", 1, 240.0),
        "shop_listings": ("shop-listings", 1, 240.0),
        "shop_sold": ("shop-sold", 1, 240.0),
        "shop_reviews": ("shop-reviews", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "atacadao": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "product": ("product", 1, 240.0),
        "stores_near": ("stores-near", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
        "flyers": ("flyers", 1, 240.0),
        "facets": ("facets", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "categories": ("categories", 1, 240.0),
    },
    "carrefourbr": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "collection": ("collection", 1, 240.0),
        "product": ("product", 1, 240.0),
        "delivery": ("delivery", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "coupons": ("coupons", 1, 240.0),
        "categories": ("categories", 1, 240.0),
    },
}
BATCH7W3_1127_ONE_OF = {
    "enjoei_product": (("product_id", "url"),),
    "enjoei_shop_reviews": (("handle", "shop_id"),),
    "atacadao_category": (("category", "category_id"),),
    "atacadao_product": (("sku", "ean", "product_id", "slug", "url"),),
    "atacadao_stores_near": (("cep", "latitude"),),
    "carrefourbr_product": (("item_id", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH7W3_1127))
def test_batch7w3_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 3 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH7W3_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH7W3_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b"
        assert not re.search(ai, text.lower()), ep.key


BATCH7W3_1127_WIRE = [
    ("enjoei", "search", {"query": "vestido farm"}, "search"),
    (
        "enjoei", "search",
        {"query": "vestido farm", "brand": ["farm"], "condition": "used", "sort": "price_asc"},
        "search",
    ),
    (
        "enjoei", "category",
        {"department": "feminino", "category": "feminino-roupas",
         "subcategory": "feminino-roupas-vestidos"},
        "category",
    ),
    ("enjoei", "categories", {}, "categories"),
    ("enjoei", "product", {"product_id": "153252795"}, "product"),
    ("enjoei", "shop", {"handle": "utstore"}, "shop"),
    ("enjoei", "shop_listings", {"handle": "utstore"}, "shop-listings"),
    ("enjoei", "shop_sold", {"handle": "utstore", "page": 2}, "shop-sold"),
    ("enjoei", "shop_reviews", {"handle": "utstore", "filter": "negative"}, "shop-reviews"),
    ("enjoei", "suggestions", {"query": "vestido"}, "suggestions"),
    ("atacadao", "search", {"query": "arroz"}, "search"),
    (
        "atacadao", "search",
        {"query": "arroz", "store_id": "atacadaobr340", "brand": ["Camil"], "page_size": 50},
        "search",
    ),
    (
        "atacadao", "category",
        {"category": "mercearia/graos", "store_id": "atacadaobr340"},
        "category",
    ),
    ("atacadao", "product", {"ean": "7896079431158"}, "product"),
    ("atacadao", "product", {"sku": "14443", "store_id": 340}, "product"),
    ("atacadao", "stores_near", {"cep": "01310-100"}, "stores-near"),
    ("atacadao", "stores_near", {"latitude": -23.56, "longitude": -46.65}, "stores-near"),
    ("atacadao", "stores", {"state": "SP", "city": "Sao Paulo"}, "stores"),
    ("atacadao", "store", {"store_id": "atacadaobr340"}, "store"),
    ("atacadao", "flyers", {"store_id": 340}, "flyers"),
    ("atacadao", "facets", {"query": "arroz"}, "facets"),
    ("atacadao", "suggestions", {"query": "arroz"}, "suggestions"),
    ("atacadao", "categories", {}, "categories"),
    ("carrefourbr", "search", {"query": "arroz", "cep": "01310-100"}, "search"),
    (
        "carrefourbr", "search",
        {"query": "geladeira", "site": "www", "filters": {"brand": "consul"}, "sort": "price_asc"},
        "search",
    ),
    (
        "carrefourbr", "category",
        {"path": "/categoria/mercearia/alimentos-basicos/arroz"},
        "category",
    ),
    ("carrefourbr", "collection", {"collection_id": 29861}, "collection"),
    ("carrefourbr", "product", {"item_id": "1972"}, "product"),
    ("carrefourbr", "delivery", {"item_id": "1972", "cep": "01310-100"}, "delivery"),
    ("carrefourbr", "stores", {"state": "SP"}, "stores"),
    ("carrefourbr", "suggestions", {"query": "arroz"}, "suggestions"),
    ("carrefourbr", "coupons", {}, "coupons"),
    ("carrefourbr", "categories", {"site": "www"}, "categories"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH7W3_1127_WIRE)
def test_batch7w3_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH7W3_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH7W3_1127_ONE_OF))
def test_batch7w3_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch7w3_1127_credits_wire_and_timeouts():
    """Enjoei, Atacadao, Carrefour Brasil: 1 credit flat, 240 s floor, no credits note."""
    for ns in BATCH7W3_1127:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    w3 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH7W3_1127]
    assert len(w3) == 28
    assert {ep.min_timeout for ep in w3} == {240.0}
    assert not [ep.key for ep in w3 if ep.credits_note]
    assert [p.name for p in ENDPOINTS["carrefourbr_delivery"].required_params] == ["item_id", "cep"]
    assert [p.name for p in ENDPOINTS["enjoei_shop"].required_params] == ["handle"]
    assert [p.name for p in ENDPOINTS["atacadao_stores"].required_params] == ["state"]
    assert [p.name for p in ENDPOINTS["atacadao_flyers"].required_params] == ["store_id"]
    assert not ENDPOINTS["atacadao_suggestions"].required_params
    assert not ENDPOINTS["carrefourbr_coupons"].required_params
    assert ENDPOINTS["enjoei_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["atacadao_product"].positional_optional_params[0].name == "sku"
    assert ENDPOINTS["carrefourbr_product"].positional_optional_params[0].name == "item_id"
    # Carrefour Brasil is its own namespace, never merged with Carrefour France.
    brasil = [ep for ep in w3 if ep.namespace == "carrefourbr"]
    assert all(ep.path.startswith("/api/v1/carrefourbr/") for ep in brasil)
    assert all(p.doc for ep in w3 for p in ep.params)


# --- batch 7 wave 4 2026-11-27: 4 Brazil namespaces ---
# (Terabyteshop, Cobasi, Netshoes, Estante Virtual)

BATCH7W4_1127 = {
    "terabyte": {
        "search": ("search", 1, 240.0),
        "product": ("product", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "coupons": ("coupons", 1, 240.0),
        "trending_searches": ("trending-searches", 1, 240.0),
        "pc_builder": ("pc-builder", 1, 240.0),
    },
    "cobasi": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "product": ("product", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "questions": ("questions", 1, 240.0),
        "availability": ("availability", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "store": ("store", 1, 240.0),
    },
    "netshoes": {
        "search": ("search", 1, 240.0),
        "list": ("list", 1, 240.0),
        "product": ("product", 1, 240.0),
        "offers": ("offers", 1, 240.0),
        "inventory": ("inventory", 1, 240.0),
        "shipping": ("shipping", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "questions": ("questions", 1, 240.0),
        "daily_deal": ("daily-deal", 1, 240.0),
        "seller": ("seller", 1, 240.0),
        "popular_searches": ("popular-searches", 1, 240.0),
    },
    "estantevirtual": {
        "search": ("search", 1, 240.0),
        "isbn": ("isbn", 1, 240.0),
        "book": ("book", 1, 240.0),
        "copies": ("copies", 1, 240.0),
        "copy": ("copy", 1, 240.0),
        "shipping": ("shipping", 1, 240.0),
        "seller": ("seller", 1, 240.0),
        "seller_books": ("seller-books", 1, 240.0),
        "seller_reviews": ("seller-reviews", 1, 240.0),
        "sellers": ("sellers", 1, 240.0),
        "category": ("category", 1, 240.0),
        "list": ("list", 1, 240.0),
    },
}
BATCH7W4_1127_ONE_OF = {
    "terabyte_product": (("product_id", "url"),),
    "terabyte_reviews": (("product_id", "url"),),
    "terabyte_brand": (("brand", "brand_id"),),
    "cobasi_product": (("product_id", "url"),),
    "cobasi_reviews": (("product_id", "url"),),
    "cobasi_questions": (("product_id", "url"),),
    "cobasi_store": (("slug", "url"),),
    "netshoes_product": (("product_id", "url"),),
    "netshoes_reviews": (("product_id", "url"),),
    "netshoes_questions": (("product_id", "url"),),
    "estantevirtual_book": (("book_id", "url"),),
    "estantevirtual_copies": (("book_id", "url"),),
    "estantevirtual_copy": (("copy_id", "url"),),
    "estantevirtual_shipping": (("copy_id", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH7W4_1127))
def test_batch7w4_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 4 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH7W4_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH7W4_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b"
        assert not re.search(ai, text.lower()), ep.key


BATCH7W4_1127_WIRE = [
    ("terabyte", "search", {"query": "rtx 5060"}, "search"),
    (
        "terabyte", "search",
        {"query": "rtx 5060", "sort": "price_asc", "page": 2, "page_size": 50},
        "search",
    ),
    ("terabyte", "product", {"product_id": "41251"}, "product"),
    ("terabyte", "reviews", {"product_id": 20782, "page": 2}, "reviews"),
    (
        "terabyte", "category",
        {
            "category": "hardware/placas-de-video",
            "sort": "price_asc",
            "filters": {"modelo": "RTX 5070"},
        },
        "category",
    ),
    ("terabyte", "brand", {"category": "perifericos/mouse", "brand": "Logitech"}, "brand"),
    ("terabyte", "brand", {"category": "perifericos/mouse", "brand_id": "39"}, "brand"),
    ("terabyte", "deals", {}, "deals"),
    ("terabyte", "deals", {"deal": "open_box", "sort": "price_desc"}, "deals"),
    ("terabyte", "coupons", {"code": "BLACKDT3"}, "coupons"),
    ("terabyte", "trending_searches", {"limit": 10}, "trending-searches"),
    ("terabyte", "pc_builder", {"platform_id": "18613", "group_id": "21065"}, "pc-builder"),
    ("cobasi", "search", {"query": "ração golden", "filters": ["brand/golden"]}, "search"),
    ("cobasi", "category", {"category": "cachorro/racao", "sort": "price_asc"}, "category"),
    ("cobasi", "brand", {"brand": "golden"}, "brand"),
    ("cobasi", "deals", {"sort": "discount_desc"}, "deals"),
    ("cobasi", "product", {"product_id": "3934097"}, "product"),
    ("cobasi", "reviews", {"product_id": "3767590", "page": 2}, "reviews"),
    ("cobasi", "questions", {"product_id": "3767590"}, "questions"),
    (
        "cobasi", "availability",
        {"sku_id": "934097", "cep": "01310-100", "quantity": 2},
        "availability",
    ),
    ("cobasi", "suggestions", {"query": "areia gato"}, "suggestions"),
    ("cobasi", "stores", {"state": "SP"}, "stores"),
    ("cobasi", "store", {"slug": "cobasi-americana"}, "store"),
    ("netshoes", "search", {"query": "tenis corrida"}, "search"),
    (
        "netshoes", "search",
        {
            "query": "tenis corrida", "brand": ["nike"], "size": "40",
            "price_min": 100, "sort": "price_asc",
        },
        "search",
    ),
    ("netshoes", "list", {}, "list"),
    ("netshoes", "list", {"slug": "tenis-black-friday", "page": 2}, "list"),
    ("netshoes", "product", {"product_id": "FBA-82XQ-006"}, "product"),
    ("netshoes", "offers", {"sku": "I0Y-0011-289-01"}, "offers"),
    ("netshoes", "inventory", {"sku": "FBA-82XQ-006-38", "seller_id": 0}, "inventory"),
    ("netshoes", "shipping", {"sku": "FBA-82XQ-006-38", "cep": "01310-100"}, "shipping"),
    ("netshoes", "reviews", {"product_id": "FBA-82XQ", "rating": "negative"}, "reviews"),
    (
        "netshoes", "reviews",
        {"product_id": "FBA-82XQ", "rating": [3], "with_photos": True},
        "reviews",
    ),
    ("netshoes", "questions", {"product_id": "I0Y-0011"}, "questions"),
    ("netshoes", "daily_deal", {}, "daily-deal"),
    ("netshoes", "seller", {"seller_id": "21072"}, "seller"),
    ("netshoes", "popular_searches", {}, "popular-searches"),
    ("estantevirtual", "search", {"query": "dom casmurro"}, "search"),
    (
        "estantevirtual", "search",
        {"query": "dom casmurro", "condition": "used", "sort": "price_asc", "price_max": 30},
        "search",
    ),
    ("estantevirtual", "isbn", {"isbn": "9788535914849"}, "isbn"),
    ("estantevirtual", "book", {"book_id": "017-4778-000-BK"}, "book"),
    ("estantevirtual", "copies", {"book_id": "017-4778-000-BK"}, "copies"),
    (
        "estantevirtual", "copies",
        {"book_id": "017-4778-000-BK", "condition": "new", "page_size": 10, "sellers": True},
        "copies",
    ),
    ("estantevirtual", "copy", {"copy_id": "GME-2437-000"}, "copy"),
    ("estantevirtual", "shipping", {"copy_id": "GME-2437-000", "cep": "01310-100"}, "shipping"),
    ("estantevirtual", "seller", {"seller_id": "1002276"}, "seller"),
    ("estantevirtual", "seller_books", {"seller_id": 1002276, "query": "orwell"}, "seller-books"),
    (
        "estantevirtual", "seller_reviews",
        {"seller_id": "1002276", "rating": "negative"},
        "seller-reviews",
    ),
    ("estantevirtual", "sellers", {"state": "SP", "city": "São Paulo"}, "sellers"),
    ("estantevirtual", "category", {"category_slug": "literatura-brasileira"}, "category"),
    ("estantevirtual", "list", {"slug": "black-friday"}, "list"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH7W4_1127_WIRE)
def test_batch7w4_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH7W4_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH7W4_1127_ONE_OF))
def test_batch7w4_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch7w4_1127_credits_wire_and_timeouts():
    """Terabyteshop, Cobasi, Netshoes, Estante Virtual: 1 credit floor, 240 s floor; copies note."""
    for ns in BATCH7W4_1127:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    w4 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH7W4_1127]
    assert len(w4) == 43
    assert {ep.min_timeout for ep in w4} == {240.0}
    assert [ep.key for ep in w4 if ep.credits_note] == ["estantevirtual_copies"]
    assert "ceil((1 + copies) / 5)" in ENDPOINTS["estantevirtual_copies"].credits_note
    assert [p.name for p in ENDPOINTS["cobasi_availability"].required_params] == ["sku_id", "cep"]
    assert [p.name for p in ENDPOINTS["netshoes_shipping"].required_params] == ["sku", "cep"]
    assert [p.name for p in ENDPOINTS["estantevirtual_shipping"].required_params] == ["cep"]
    assert [p.name for p in ENDPOINTS["terabyte_brand"].required_params] == ["category"]
    category = ENDPOINTS["estantevirtual_category"]
    assert [p.name for p in category.required_params] == ["category_slug"]
    assert not ENDPOINTS["netshoes_daily_deal"].params
    assert not ENDPOINTS["netshoes_popular_searches"].params
    assert not ENDPOINTS["terabyte_pc_builder"].required_params
    assert ENDPOINTS["terabyte_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["cobasi_store"].positional_optional_params[0].name == "slug"
    assert ENDPOINTS["netshoes_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["estantevirtual_copies"].positional_optional_params[0].name == "book_id"
    assert ENDPOINTS["estantevirtual_copy"].positional_optional_params[0].name == "copy_id"
    assert "AI assistant" not in ENDPOINTS["netshoes_questions"].summary
    assert all(p.doc for ep in w4 for p in ep.params)


# --- batch 7 wave 5 2026-11-27: 4 Brazil namespaces ---
# (C&A Brasil, Lojas Renner, Pichau, Dafiti)

BATCH7W5_1127 = {
    "cea": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "facets": ("facets", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "product": ("product", 1, 240.0),
        "shipping": ("shipping", 1, 240.0),
        "stores": ("stores", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
    },
    "renner": {
        "search": ("search", 1, 300.0),
        "category": ("category", 1, 300.0),
        "deals": ("deals", 1, 300.0),
        "product": ("product", 1, 300.0),
        "sku_price": ("sku-price", 1, 300.0),
        "stores": ("stores", 1, 300.0),
        "reviews": ("reviews", 1, 300.0),
    },
    "pichau": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "product": ("product", 1, 240.0),
        "product_live": ("product-live", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
        "installments": ("installments", 1, 240.0),
        "coupons": ("coupons", 1, 240.0),
        "categories": ("categories", 1, 240.0),
        "suggestions": ("suggestions", 1, 240.0),
    },
    "dafiti": {
        "search": ("search", 1, 240.0),
        "category": ("category", 1, 240.0),
        "brand": ("brand", 1, 240.0),
        "deals": ("deals", 1, 240.0),
        "product": ("product", 1, 240.0),
        "sizes": ("sizes", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
    },
}
BATCH7W5_1127_ONE_OF = {
    "cea_facets": (("query", "category", "brand", "collection_id"),),
    "cea_product": (("product_id", "sku", "slug", "url"),),
    "renner_product": (("product_id", "url"),),
    "renner_sku_price": (("product_id", "url"),),
    "pichau_product": (("url_key", "url"),),
    "pichau_product_live": (("url_key", "url"),),
    "pichau_installments": (("url_key", "url", "product_id"),),
    "dafiti_product": (("product_id", "sku", "url"),),
    "renner_reviews": (("product_id", "url"),),
    "dafiti_reviews": (("sku", "product_id", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH7W5_1127))
def test_batch7w5_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 4 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH7W5_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH7W5_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b"
        assert not re.search(ai, text.lower()), ep.key


BATCH7W5_1127_WIRE = [
    ("cea", "search", {"query": "vestido"}, "search"),
    (
        "cea", "search",
        {"query": "vestido", "sort": "price_asc", "page": 2, "page_size": 12},
        "search",
    ),
    ("cea", "category", {"category": "moda-feminina", "sort": "newest"}, "category"),
    ("cea", "brand", {"brand": "clock-house"}, "brand"),
    ("cea", "deals", {"collection_id": 19727, "sort": "discount"}, "deals"),
    ("cea", "facets", {"query": "jeans"}, "facets"),
    ("cea", "facets", {"collection_id": "19727"}, "facets"),
    ("cea", "suggestions", {"query": "vest"}, "suggestions"),
    ("cea", "suggestions", {}, "suggestions"),
    ("cea", "categories", {}, "categories"),
    ("cea", "product", {"product_id": "4536055"}, "product"),
    ("cea", "product", {"sku": "6493983"}, "product"),
    ("cea", "shipping", {"sku": "6493983", "cep": "01310100"}, "shipping"),
    ("cea", "stores", {"cep": "01310100"}, "stores"),
    ("renner", "search", {"query": "camiseta"}, "search"),
    (
        "renner", "search",
        {"query": "camiseta", "sort": "price_asc", "filters": ["4zo6za"], "page": 2},
        "search",
    ),
    ("renner", "category", {"category": "4zo6za", "filters": "xv9uau"}, "category"),
    ("renner", "deals", {}, "deals"),
    ("renner", "deals", {"list": "1l95pyv", "sort": "discount"}, "deals"),
    ("renner", "product", {"product_id": "931758127"}, "product"),
    ("renner", "product", {"product_id": "931758127", "sku": "931758135"}, "product"),
    ("renner", "sku_price", {"sku": "931758135", "product_id": "931758127"}, "sku-price"),
    ("renner", "stores", {"cep": "01310-100"}, "stores"),
    ("pichau", "search", {"query": "rtx 5060"}, "search"),
    (
        "pichau", "search",
        {"query": "rtx 5060", "sort": "price_asc", "page": 2, "filters": {"brand": "gainward"}},
        "search",
    ),
    ("pichau", "category", {"category": "hardware/placa-de-video"}, "category"),
    ("pichau", "brand", {"brand": "corsair", "sort": "price_desc"}, "brand"),
    ("pichau", "deals", {}, "deals"),
    ("pichau", "deals", {"deal": "open_box"}, "deals"),
    ("pichau", "deals", {"campaign": "blackfriday"}, "deals"),
    (
        "pichau", "product",
        {
            "url_key": (
                "placa-de-video-inno3d-geforce-rtx-5060-twin-x2-8gb-gddr7-128-bit-"
                "n50602-08d7-195071n-nac"
            ),
        },
        "product",
    ),
    (
        "pichau", "product_live",
        {
            "url_key": (
                "pc-gamer-pichau-isis-vi-amd-ryzen-5-5500-geforce-rtx-5060-8gb-16gb-ddr4-"
                "ssd-m-2-480gb-57268"
            ),
        },
        "product-live",
    ),
    (
        "pichau", "reviews",
        {"product_id": 31201, "page": 2, "rating": 5, "with_media": True},
        "reviews",
    ),
    ("pichau", "installments", {"product_id": 61004, "price": 3717.64}, "installments"),
    ("pichau", "coupons", {}, "coupons"),
    ("pichau", "categories", {"all": True}, "categories"),
    ("pichau", "suggestions", {"query": "rtx"}, "suggestions"),
    ("dafiti", "search", {"query": "vestido"}, "search"),
    ("dafiti", "search", {"query": "vestido", "sort": "discount", "page": 2}, "search"),
    ("dafiti", "category", {"category": "calcados-femininos/tenis"}, "category"),
    ("dafiti", "brand", {"brand": "asics"}, "brand"),
    ("dafiti", "deals", {}, "deals"),
    ("dafiti", "deals", {"sort": "price_asc"}, "deals"),
    ("dafiti", "product", {"product_id": "15221282"}, "product"),
    ("dafiti", "product", {"sku": "AS296SCU17ARY"}, "product"),
    ("dafiti", "sizes", {"sku": "AS296SCU17ARY"}, "sizes"),
    # reviews, added 2026-11-28
    ("renner", "reviews", {"product_id": "846044605"}, "reviews"),
    (
        "renner", "reviews",
        {
            "url": "https://www.lojasrenner.com.br/p/x/-/A-846044605-br.lr",
            "sort": "most_helpful",
            "page": 2,
        },
        "reviews",
    ),
    ("cea", "reviews", {"product_id": "3700395"}, "reviews"),
    (
        "cea", "reviews",
        {"product_id": 3700395, "filter": "with_photos", "per_page": 100},
        "reviews",
    ),
    ("dafiti", "reviews", {"sku": "SA232SHF08PKSX"}, "reviews"),
    ("dafiti", "reviews", {"product_id": "15221282", "rating": 1}, "reviews"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH7W5_1127_WIRE)
def test_batch7w5_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH7W5_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH7W5_1127_ONE_OF))
def test_batch7w5_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch7w5_1127_credits_wire_and_timeouts():
    """C&A Brasil, Lojas Renner, Pichau, Dafiti: 1 credit, 240 s floor (300 s on renner)."""
    for ns in BATCH7W5_1127:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    w5 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH7W5_1127]
    assert len(w5) == 36
    assert {ep.min_timeout for ep in w5 if ep.namespace != "renner"} == {240.0}
    assert {ep.min_timeout for ep in w5 if ep.namespace == "renner"} == {300.0}
    assert not [ep.key for ep in w5 if ep.credits_note]
    assert [p.name for p in ENDPOINTS["cea_shipping"].required_params] == ["sku", "cep"]
    assert [p.name for p in ENDPOINTS["cea_stores"].required_params] == ["cep"]
    assert [p.name for p in ENDPOINTS["cea_deals"].required_params] == ["collection_id"]
    assert [p.name for p in ENDPOINTS["renner_sku_price"].required_params] == ["sku"]
    assert [p.name for p in ENDPOINTS["pichau_reviews"].required_params] == ["product_id"]
    assert [p.name for p in ENDPOINTS["dafiti_sizes"].required_params] == ["sku"]
    assert not ENDPOINTS["cea_categories"].params
    assert not ENDPOINTS["pichau_coupons"].params
    assert not ENDPOINTS["renner_deals"].required_params
    assert not ENDPOINTS["dafiti_deals"].required_params
    assert ENDPOINTS["cea_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["cea_facets"].positional_optional_params[0].name == "query"
    assert ENDPOINTS["renner_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["pichau_product_live"].positional_optional_params[0].name == "url_key"
    assert ENDPOINTS["pichau_installments"].positional_optional_params[0].name == "url_key"
    assert ENDPOINTS["dafiti_product"].positional_optional_params[0].name == "product_id"
    # reviews, added 2026-11-28
    assert [p.name for p in ENDPOINTS["cea_reviews"].required_params] == ["product_id"]
    assert ENDPOINTS["renner_reviews"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["dafiti_reviews"].positional_optional_params[0].name == "sku"
    for key in ("renner_reviews", "cea_reviews", "dafiti_reviews"):
        names = [p.name for p in ENDPOINTS[key].params]
        assert names[-5:] == ["page", "per_page", "sort", "filter", "rating"], key
        text = ENDPOINTS[key].summary.lower()
        assert "verified" not in text and "trustvox" not in text, key
        assert "reviewer names are never returned" in text, key
        assert "up to 4 hours" in text, key


# --- batch 7 wave 6 2026-11-27: 2 Brazil namespaces (Riachuelo, Petz) ---

BATCH7W6_1127 = {
    "riachuelo": {
        "search": ("search", 1, 300.0),
        "category": ("category", 1, 180.0),
        "deals": ("deals", 1, 180.0),
        "product": ("product", 1, 180.0),
    },
    "petz": {
        "search": ("search", 1, 300.0),
        "category": ("category", 1, 300.0),
        "brand": ("brand", 1, 300.0),
        "deals": ("deals", 1, 300.0),
        "product": ("product", 1, 300.0),
        "stores": ("stores", 1, 300.0),
        "store": ("store", 1, 300.0),
    },
}
BATCH7W6_1127_ONE_OF = {
    "riachuelo_product": (("sku", "url"),),
    "petz_product": (("product_id", "url"),),
    "petz_store": (("slug", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH7W6_1127))
def test_batch7w6_1127_credits_paths_timeouts(namespace):
    """Every endpoint of the 2 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH7W6_1127[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH7W6_1127_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag)\b"
        assert not re.search(ai, text.lower()), ep.key
        assert "as a browser" not in text, ep.key


BATCH7W6_1127_WIRE = [
    ("riachuelo", "search", {"query": "vestido"}, "search"),
    (
        "riachuelo", "search",
        {
            "query": "vestido", "sort": "price_asc",
            "filters": {"filter_size": ["p", "m"]}, "page": 2,
        },
        "search",
    ),
    ("riachuelo", "category", {"category": "feminino", "sort": "newest"}, "category"),
    (
        "riachuelo", "category",
        {"category": "feminino/colecao-feminino/vestido", "filters": {"brand": "pool-jeans"}},
        "category",
    ),
    ("riachuelo", "deals", {}, "deals"),
    ("riachuelo", "deals", {"department": "masculino", "sort": "discount"}, "deals"),
    ("riachuelo", "deals", {"campaign": "campanha/r/promo/oferta-especial", "page": 2}, "deals"),
    ("riachuelo", "product", {"sku": "16519710"}, "product"),
    (
        "riachuelo", "product",
        {"url": "https://www.riachuelo.com.br/vestido-midi-gode-feminino-lequinha-com-bolso-marrom-16195833_sku"},
        "product",
    ),
    ("petz", "search", {"query": "ração golden"}, "search"),
    ("petz", "search", {"query": "ração golden", "sort": "price_asc", "page": 2}, "search"),
    ("petz", "category", {"category": "cachorro/racao", "sort": "newest"}, "category"),
    ("petz", "brand", {"brand": "royal-canin"}, "brand"),
    ("petz", "deals", {}, "deals"),
    ("petz", "deals", {"collection": "PF-racoes", "sort": "price_desc"}, "deals"),
    ("petz", "product", {"product_id": "191628"}, "product"),
    ("petz", "product", {"product_id": 191628}, "product"),
    (
        "petz", "product",
        {"url": "https://www.petz.com.br/produto/racao-golden-special-para-caes-adultos-sabor-frango-e-carne-71343"},
        "product",
    ),
    ("petz", "stores", {}, "stores"),
    ("petz", "stores", {"state": "SP", "city": "São Paulo"}, "stores"),
    ("petz", "store", {"slug": "petz-aclimacao"}, "store"),
    ("petz", "store", {"url": "https://www.petz.com.br/loja/petz-aclimacao"}, "store"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH7W6_1127_WIRE)
def test_batch7w6_1127_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH7W6_1127[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH7W6_1127_ONE_OF))
def test_batch7w6_1127_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch7w6_1127_credits_wire_and_timeouts():
    """Riachuelo and Petz: 1 credit; 300 s floor on petz and riachuelo search, 180 s otherwise."""
    for ns in BATCH7W6_1127:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    w6 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH7W6_1127]
    assert len(w6) == 11
    assert not [ep.key for ep in w6 if ep.credits_note]
    assert {ep.min_timeout for ep in w6 if ep.namespace == "petz"} == {300.0}
    assert ENDPOINTS["riachuelo_search"].min_timeout == 300.0
    pages = [ep for ep in w6 if ep.namespace == "riachuelo" and ep.method != "search"]
    assert {ep.min_timeout for ep in pages} == {180.0}
    assert [p.name for p in ENDPOINTS["riachuelo_search"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["riachuelo_category"].required_params] == ["category"]
    assert [p.name for p in ENDPOINTS["petz_brand"].required_params] == ["brand"]
    assert not ENDPOINTS["riachuelo_deals"].required_params
    assert not ENDPOINTS["petz_deals"].required_params
    assert not ENDPOINTS["petz_stores"].required_params
    assert ENDPOINTS["riachuelo_product"].positional_optional_params[0].name == "sku"
    assert ENDPOINTS["petz_product"].positional_optional_params[0].name == "product_id"
    assert ENDPOINTS["petz_store"].positional_optional_params[0].name == "slug"
    assert "Grupo Petz Cobasi) or one of its collections" in ENDPOINTS["petz_deals"].summary
    assert all(p.doc for ep in w6 for p in ep.params)


# --- batch 8 wave 1: Global Industrial, MSC, Zoro ---

BATCH8W1_1128 = {
    "globalindustrial": {
        "search": ("search", 1, 180.0),
        "category": ("category", 1, 180.0),
        "brand": ("brand", 1, 180.0),
        "product": ("product", 1, 180.0),
        "clearance": ("clearance", 1, 180.0),
    },
    "msc": {
        "search": ("search", 1, 300.0),
        "category": ("category", 1, 300.0),
        "product": ("product", 1, 300.0),
        "clearance": ("clearance", 1, 180.0),
        "locations": ("locations", 1, 180.0),
    },
    "zoro": {
        "search": ("search", 1, 180.0),
        "category": ("category", 1, 180.0),
        "brand": ("brand", 1, 180.0),
        "product": ("product", 1, 180.0),
        "availability": ("availability", 1, 240.0),
        "reviews": ("reviews", 1, 240.0),
    },
}
BATCH8W1_1128_ONE_OF = {
    "globalindustrial_product": (("url", "item"),),
    "msc_category": (("navid", "url"),),
    "msc_product": (("msc_number", "url"),),
    "zoro_category": (("category", "code"),),
    "zoro_product": (("zoro_no", "url"),),
    "zoro_availability": (("zoro_no", "url"),),
    "zoro_reviews": (("zoro_no", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH8W1_1128))
def test_batch8w1_1128_credits_paths_timeouts(namespace):
    """Every endpoint of the 3 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH8W1_1128[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH8W1_1128_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag|training|grounding)\b"
        assert not re.search(ai, text.lower()), ep.key
        assert "as a browser" not in text, ep.key
        # us-only markets: the refused-only country input is not in the signature
        if namespace in ("msc", "zoro"):
            assert "country" not in [p.name for p in ep.params], ep.key


BATCH8W1_1128_WIRE = [
    ("globalindustrial", "search", {"query": "nitrile gloves"}, "search"),
    (
        "globalindustrial", "search",
        {"query": "drum truck", "brand": "Wesco", "market": "ca"},
        "search",
    ),
    (
        "globalindustrial", "category",
        {"path": "/c/carts-trucks/hand_trucks/drum_trucks_cradles"},
        "category",
    ),
    (
        "globalindustrial", "category",
        {
            "path": "/c/carts-trucks/hand_trucks/drum_trucks_cradles",
            "brand": "Wesco", "group": 42311,
        },
        "category",
    ),
    (
        "globalindustrial", "category",
        {"path": "/t/carts-trucks", "group": "42311", "market": "ca"},
        "category",
    ),
    ("globalindustrial", "brand", {"brand": "Wesco"}, "brand"),
    ("globalindustrial", "brand", {"brand": "Valley Craft", "market": "ca"}, "brand"),
    ("globalindustrial", "product", {"item": "652508"}, "product"),
    (
        "globalindustrial", "product",
        {"url": "https://www.globalindustrial.com/p/dispenser-truck-poly-drums"},
        "product",
    ),
    ("globalindustrial", "product", {"item": "652508", "market": "ca"}, "product"),
    ("globalindustrial", "clearance", {}, "clearance"),
    (
        "globalindustrial", "clearance",
        {"category": "PRIME30", "brand": "Global Industrial"},
        "clearance",
    ),
    ("msc", "search", {"query": "drill bit"}, "search"),
    ("msc", "search", {"query": "drill bit", "sort": "price_desc", "page": 3}, "search"),
    ("msc", "category", {"navid": "2106186"}, "category"),
    ("msc", "category", {"navid": 2106186, "sort": "rating", "page": 2}, "category"),
    ("msc", "category", {"url": "https://www.mscdirect.com/browse/tn?navid=2106186"}, "category"),
    ("msc", "product", {"msc_number": "00647354"}, "product"),
    ("msc", "product", {"url": "https://www.mscdirect.com/product/details/00647354"}, "product"),
    ("msc", "clearance", {}, "clearance"),
    ("msc", "clearance", {"list": "web_specials"}, "clearance"),
    ("msc", "locations", {}, "locations"),
    (
        "msc", "locations",
        {"type": "Customer Fulfillment Center", "state": "PA", "location_country": "United States"},
        "locations",
    ),
    ("zoro", "search", {"query": "3m n95 respirator"}, "search"),
    ("zoro", "search", {"query": "safety glasses", "page": 2}, "search"),
    ("zoro", "category", {"category": "safety-glasses/c/6214"}, "category"),
    ("zoro", "category", {"slug": "safety-glasses", "code": "6214", "page": 3}, "category"),
    ("zoro", "brand", {"brand": "Mcr Safety"}, "brand"),
    ("zoro", "brand", {"brand": "https://www.zoro.com/b/3M/", "page": 2}, "brand"),
    ("zoro", "product", {"zoro_no": "G2426514"}, "product"),
    (
        "zoro", "product",
        {"url": "https://www.zoro.com/mcr-safety-bearkat-bk1-safety-glasses-duramass-hard-coat-clear-lens-non-slip-temple-frameless-bk110/i/G2426514/"},
        "product",
    ),
    ("zoro", "availability", {"zoro_no": "G2426514"}, "availability"),
    ("zoro", "reviews", {"zoro_no": "G2426514"}, "reviews"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH8W1_1128_WIRE)
def test_batch8w1_1128_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH8W1_1128[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH8W1_1128_ONE_OF))
def test_batch8w1_1128_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch8w1_1128_credits_wire_and_timeouts():
    """Global Industrial, MSC and Zoro: 1 credit; 300 s on slow MSC pages, 240 s on Zoro pages."""
    for ns in BATCH8W1_1128:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    w1 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH8W1_1128]
    assert len(w1) == 16
    assert not [ep.key for ep in w1 if ep.credits_note]
    assert all(p.doc for ep in w1 for p in ep.params)
    assert [p.name for p in ENDPOINTS["globalindustrial_search"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["globalindustrial_category"].required_params] == ["path"]
    assert [p.name for p in ENDPOINTS["globalindustrial_brand"].required_params] == ["brand"]
    assert not ENDPOINTS["globalindustrial_clearance"].required_params
    assert [p.name for p in ENDPOINTS["msc_search"].required_params] == ["query"]
    assert not ENDPOINTS["msc_clearance"].required_params
    assert not ENDPOINTS["msc_locations"].required_params
    assert [p.name for p in ENDPOINTS["zoro_search"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["zoro_brand"].required_params] == ["brand"]
    assert ENDPOINTS["globalindustrial_product"].positional_optional_params[0].name == "item"
    assert ENDPOINTS["msc_category"].positional_optional_params[0].name == "navid"
    assert ENDPOINTS["msc_product"].positional_optional_params[0].name == "msc_number"
    assert ENDPOINTS["zoro_category"].positional_optional_params[0].name == "category"
    for m in ("product", "availability", "reviews"):
        assert ENDPOINTS[f"zoro_{m}"].positional_optional_params[0].name == "zoro_no"
    assert '"See price in cart"' in ENDPOINTS["globalindustrial_product"].summary
    assert "a Grainger company" in ENDPOINTS["zoro_search"].summary


# --- batch 8 wave 2 2026-11-28: B-Stock, McMaster-Carr, Sally Beauty, Liquidation.com ---

BATCH8W2_1128 = {
    "bstock": {
        "search": ("search", 1, 180.0),
        "lot": ("lot", 1, 180.0),
        "storefronts": ("storefronts", 1, 180.0),
        "filters": ("filters", 1, 180.0),
    },
    "mcmaster": {
        "product": ("product", 1, 180.0),
        "search": ("search", 1, 300.0),
        "categories": ("categories", 1, 180.0),
    },
    "sallybeauty": {
        "search": ("search", 1, 180.0),
        "category": ("category", 1, 180.0),
        "clearance": ("clearance", 1, 180.0),
        "product": ("product", 1, 180.0),
        "stores": ("stores", 1, 180.0),
        "store_stock": ("store-stock", 1, 180.0),
        "suggestions": ("suggestions", 1, 180.0),
        "brands": ("brands", 1, 180.0),
        "reviews": ("reviews", 1, 240.0),
    },
    "liquidation": {
        "search": ("search", 1, 180.0),
        "lot": ("lot", 1, 180.0),
        "manifest": ("manifest", 1, 180.0),
        "closed": ("closed", 1, 180.0),
    },
}
BATCH8W2_1128_ONE_OF = {
    "bstock_lot": (("id", "url"),),
    "mcmaster_product": (("part_number", "url"),),
    "mcmaster_search": (("query", "category"),),
    "sallybeauty_product": (("product_id", "url"),),
    "sallybeauty_store_stock": (("product_id", "url"),),
    "sallybeauty_reviews": (("product_id", "url"),),
    "liquidation_lot": (("id", "url"),),
    "liquidation_manifest": (("id", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH8W2_1128))
def test_batch8w2_1128_credits_paths_timeouts(namespace):
    """Every endpoint of the 4 new namespaces: path, credits floor, timeout floor, one-of."""
    want = BATCH8W2_1128[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH8W2_1128_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag|training|grounding)\b"
        assert not re.search(ai, text.lower()), ep.key
        assert "as a browser" not in text, ep.key
        # McMaster-Carr has one US storefront: the refused-only country input is not exposed
        if namespace == "mcmaster":
            assert "country" not in [p.name for p in ep.params], ep.key


BATCH8W2_1128_WIRE = [
    ("bstock", "search", {"q": "laptop"}, "search"),
    (
        "bstock", "search",
        {"storefront": ["Target", "Walmart"], "condition": "Like New", "sort": "end_time",
         "limit": 50, "offset": 50},
        "search",
    ),
    ("bstock", "lot", {"id": "6b05cd6821e9e20881d2a998"}, "lot"),
    (
        "bstock", "lot",
        {"url": "https://bstock.com/buy/listings/details/6b05cd6821e9e20881d2a998"},
        "lot",
    ),
    ("bstock", "storefronts", {}, "storefronts"),
    ("bstock", "filters", {}, "filters"),
    ("mcmaster", "product", {"part_number": "91251A540"}, "product"),
    ("mcmaster", "product", {"url": "https://www.mcmaster.com/91251A540/"}, "product"),
    ("mcmaster", "search", {"query": "hose clamps", "per_page": 10}, "search"),
    ("mcmaster", "search", {"category": "hose-clamps/worm-drive-clamps~~", "offset": 10}, "search"),
    ("mcmaster", "categories", {}, "categories"),
    ("sallybeauty", "search", {"query": "purple shampoo"}, "search"),
    (
        "sallybeauty", "search",
        {"query": "shampoo", "site": "cosmoprof-us", "sort": "newest", "page": 2,
         "filters": {"brandcustom": "Redken"}},
        "search",
    ),
    ("sallybeauty", "category", {"category": "hair-color", "sort": "price_asc"}, "category"),
    ("sallybeauty", "clearance", {"department": "nails", "price_max": 10}, "clearance"),
    ("sallybeauty", "product", {"product_id": "SBS-302313"}, "product"),
    ("sallybeauty", "stores", {"postal_code": "75201", "radius": 30}, "stores"),
    (
        "sallybeauty", "store_stock",
        {"product_id": "SBS-302313", "postal_code": "90012"},
        "store-stock",
    ),
    ("sallybeauty", "suggestions", {"query": "wahl"}, "suggestions"),
    ("sallybeauty", "brands", {"site": "sally-ca"}, "brands"),
    ("sallybeauty", "reviews", {"product_id": "SBS-345331"}, "reviews"),
    ("liquidation", "search", {"q": "laptop"}, "search"),
    (
        "liquidation", "search",
        {"condition": "returns", "lot_size": ["pallet", "truckload"], "sort": "current_bid",
         "order": "desc", "page": 2},
        "search",
    ),
    ("liquidation", "lot", {"id": "21648824"}, "lot"),
    ("liquidation", "manifest", {"id": "21648824"}, "manifest"),
    ("liquidation", "closed", {"seller": "Titan Electronics", "category": "1004"}, "closed"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH8W2_1128_WIRE)
def test_batch8w2_1128_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH8W2_1128[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH8W2_1128_ONE_OF))
def test_batch8w2_1128_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch8w2_1128_credits_wire_and_timeouts():
    """B-Stock, McMaster-Carr, Sally Beauty, Liquidation.com: 1 credit; 300 s / 240 s floors."""
    for ns in BATCH8W2_1128:
        assert {ep.credits for ep in ENDPOINTS.values() if ep.namespace == ns} == {1}, ns
    w2 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH8W2_1128]
    assert len(w2) == 20
    assert not [ep.key for ep in w2 if ep.credits_note]
    assert all(p.doc for ep in w2 for p in ep.params)
    assert [p.name for p in ENDPOINTS["sallybeauty_search"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["sallybeauty_category"].required_params] == ["category"]
    assert [p.name for p in ENDPOINTS["sallybeauty_suggestions"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["liquidation_closed"].required_params] == ["seller"]
    assert not ENDPOINTS["bstock_search"].required_params
    assert not ENDPOINTS["liquidation_search"].required_params
    assert ENDPOINTS["bstock_lot"].positional_optional_params[0].name == "id"
    assert ENDPOINTS["mcmaster_product"].positional_optional_params[0].name == "part_number"
    assert ENDPOINTS["mcmaster_search"].positional_optional_params[0].name == "query"
    for m in ("product", "store_stock", "reviews"):
        assert ENDPOINTS[f"sallybeauty_{m}"].positional_optional_params[0].name == "product_id"
    assert "full manifest needs a signed-in buyer account" in ENDPOINTS["bstock_lot"].summary
    assert "Bidder identities are not returned" in ENDPOINTS["liquidation_lot"].summary


# --- batch 8 wave 3 2026-11-28: Ferguson, SupplyHouse.com ---

BATCH8W3_1128 = {
    "ferguson": {
        "search": ("search", 2, 240.0),
        "category": ("category", 2, 240.0),
        "product": ("product", 4, 180.0),
    },
    "supplyhouse": {
        "search": ("search", 1, 250.0),
        "category": ("category", 1, 250.0),
        "brand": ("brand", 1, 250.0),
        "product": ("product", 1, 250.0),
        "reviews": ("reviews", 1, 250.0),
        "questions": ("questions", 1, 250.0),
        "categories": ("categories", 1, 180.0),
    },
}
BATCH8W3_1128_ONE_OF = {
    "ferguson_product": (("item", "url"),),
    "supplyhouse_product": (("product_id", "url"),),
    "supplyhouse_reviews": (("product_id", "url"),),
    "supplyhouse_questions": (("product_id", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH8W3_1128))
def test_batch8w3_1128_credits_paths_timeouts(namespace):
    """Every endpoint of the 2 new namespaces: path, credits, timeout floor, one-of."""
    want = BATCH8W3_1128[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH8W3_1128_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag|training|grounding)\b"
        assert not re.search(ai, text.lower()), ep.key
        assert "as a browser" not in text, ep.key
        # Both are US-only storefronts: the refused-only country input is not exposed
        assert "country" not in [p.name for p in ep.params], ep.key
        # Ferguson: never Build.com / Ferguson Home
        assert "build.com" not in text.lower() and "ferguson home" not in text.lower(), ep.key


BATCH8W3_1128_WIRE = [
    ("ferguson", "search", {"q": "pex tubing"}, "search"),
    ("ferguson", "search", {"q": "1/2 ball valve", "page": 2, "sort": "best_selling"}, "search"),
    ("ferguson", "category", {"category": "water-heaters/tankless-water-heaters"}, "category"),
    ("ferguson", "product", {"item": "4606091"}, "product"),
    (
        "ferguson", "product",
        {"url": "https://www.ferguson.com/product/fnw-figure-x432-ball-valve/4606091.html"},
        "product",
    ),
    ("supplyhouse", "search", {"query": "hot surface igniter", "page": 2}, "search"),
    ("supplyhouse", "category", {"category": "PEX-Fittings-525000"}, "category"),
    ("supplyhouse", "brand", {"brand": "PVI"}, "brand"),
    ("supplyhouse", "product", {"product_id": "PXLE038"}, "product"),
    (
        "supplyhouse", "product",
        {"url": "https://www.supplyhouse.com/Bluefin-PXLE038-3-8-Poly-PEX-Crimp-Elbow"},
        "product",
    ),
    ("supplyhouse", "reviews", {"product_id": "PXLE038", "page": 2}, "reviews"),
    ("supplyhouse", "questions", {"product_id": "007-F5"}, "questions"),
    ("supplyhouse", "categories", {}, "categories"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH8W3_1128_WIRE)
def test_batch8w3_1128_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH8W3_1128[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH8W3_1128_ONE_OF))
def test_batch8w3_1128_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch8w3_1128_credits_notes_and_params():
    """Ferguson: 2 / 2 / 4 with notes on search and product; SupplyHouse: 1 credit everywhere."""
    w3 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH8W3_1128]
    assert len(w3) == 10
    assert {ep.credits for ep in w3 if ep.namespace == "supplyhouse"} == {1}
    assert sorted(ep.key for ep in w3 if ep.credits_note) == ["ferguson_product", "ferguson_search"]
    assert "2 when the page names no price" in ENDPOINTS["ferguson_product"].credits_note
    assert "4 when" in ENDPOINTS["ferguson_search"].credits_note
    assert all(p.doc for ep in w3 for p in ep.params)
    assert [p.name for p in ENDPOINTS["ferguson_search"].required_params] == ["q"]
    assert [p.name for p in ENDPOINTS["ferguson_category"].required_params] == ["category"]
    assert [p.name for p in ENDPOINTS["supplyhouse_search"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["supplyhouse_category"].required_params] == ["category"]
    assert [p.name for p in ENDPOINTS["supplyhouse_brand"].required_params] == ["brand"]
    assert ENDPOINTS["ferguson_product"].positional_optional_params[0].name == "item"
    for m in ("product", "reviews", "questions"):
        assert ENDPOINTS[f"supplyhouse_{m}"].positional_optional_params[0].name == "product_id"
    assert not ENDPOINTS["supplyhouse_categories"].params
    assert "carry no prices" in ENDPOINTS["ferguson_search"].summary
    assert "signed-in customers only" in ENDPOINTS["ferguson_product"].summary
    assert "No reviewer names" in ENDPOINTS["supplyhouse_reviews"].summary
    assert "price_hidden" in ENDPOINTS["supplyhouse_product"].summary


# --- batch 8 wave 4 2026-11-28: DigiKey, Mouser Electronics, RS Components ---

BATCH8W4_1128 = {
    "digikey": {
        "search": ("search", 2, 300.0),
        "product": ("product", 4, 300.0),
        "categories": ("categories", 2, 300.0),
    },
    "mouser": {
        "search": ("search", 2, 300.0),
        "product": ("product", 2, 300.0),
        "categories": ("categories", 2, 300.0),
        "manufacturer": ("manufacturer", 2, 300.0),
    },
    "rscomponents": {
        "search": ("search", 2, 240.0),
        "product": ("product", 2, 240.0),
        "category": ("category", 2, 240.0),
        "brand": ("brand", 2, 240.0),
    },
}
BATCH8W4_1128_ONE_OF = {
    "digikey_search": (("query", "category_id"),),
    "digikey_product": (("url", "digikey_part_number"),),
    "mouser_search": (("query", "category"),),
    "mouser_product": (("mouser_part_number", "url"),),
    "mouser_manufacturer": (("manufacturer", "url"),),
    "rscomponents_product": (("stock_number", "url"),),
}


@pytest.mark.parametrize("namespace", sorted(BATCH8W4_1128))
def test_batch8w4_1128_credits_paths_timeouts(namespace):
    """Every endpoint of the 3 new namespaces: path, credits, timeout floor, one-of, copy rules."""
    want = BATCH8W4_1128[namespace]
    eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == namespace}
    assert sorted(eps) == sorted(want)
    for method, (segment, credits, timeout) in want.items():
        ep = eps[method]
        assert ep.http == "POST", ep.key
        assert ep.path == f"/api/v1/{namespace}/{segment}", ep.key
        assert ep.credits == credits, ep.key
        assert ep.min_timeout == timeout, ep.key
        assert tuple(tuple(g) for g in ep.one_of) == BATCH8W4_1128_ONE_OF.get(ep.key, ()), ep.key
        text = " ".join([ep.summary, ep.credits_note or ""] + [p.doc for p in ep.params])
        assert not BATCH7_1127_BANNED.search(text.lower()), ep.key
        ai = r"\b(ai|agents?|agentic|mcp|llms?|chatbots?|rag|training|grounding)\b"
        assert not re.search(ai, text.lower()), ep.key
        assert "real-time" not in text.lower() and "real time" not in text.lower(), ep.key
        assert "country" in [p.name for p in ep.params], ep.key


BATCH8W4_1128_WIRE = [
    ("digikey", "search", {"query": "LM7805"}, "search"),
    (
        "digikey", "search",
        {
            "query": "LM317",
            "category_id": "699",
            "filters": {"-1": ["296"], "-2": ["5"]},
            "country": "de",
        },
        "search",
    ),
    (
        "digikey", "product",
        {"url": "https://www.digikey.com/en/products/detail/texas-instruments/SN74HCT02N/376866"},
        "product",
    ),
    ("digikey", "product", {"digikey_part_number": "497-1575-5-ND", "country": "ca"}, "product"),
    ("digikey", "categories", {}, "categories"),
    ("digikey", "categories", {"category_id": 32}, "categories"),
    ("mouser", "search", {"query": "LM7805", "page": 2, "country": "uk"}, "search"),
    ("mouser", "search", {"category": "semiconductors/integrated-circuits-ics"}, "search"),
    ("mouser", "product", {"mouser_part_number": "595-NE555P"}, "product"),
    ("mouser", "categories", {}, "categories"),
    ("mouser", "manufacturer", {"manufacturer": "texas-instruments"}, "manufacturer"),
    ("rscomponents", "search", {"query": "BC547", "page": 2}, "search"),
    ("rscomponents", "product", {"stock_number": "221-5535", "country": "de"}, "product"),
    (
        "rscomponents", "product",
        {"url": "https://uk.rs-online.com/web/p/timer-circuits/2215535"},
        "product",
    ),
    (
        "rscomponents", "category",
        {"path": "semiconductors/power-management-ics/voltage-regulators"},
        "category",
    ),
    ("rscomponents", "brand", {"brand": "texas-instruments", "country": "au"}, "brand"),
]


@pytest.mark.parametrize(("namespace", "method", "kwargs", "segment"), BATCH8W4_1128_WIRE)
def test_batch8w4_1128_wire(namespace, method, kwargs, segment, monkeypatch):
    ep = ENDPOINTS[f"{namespace}_{method}"]
    wire = {p.name: p.wire_field for p in ep.params}
    body = {wire[k]: v for k, v in kwargs.items()}
    seen: list[tuple[str, dict, float]] = []

    def fake_request(http, path, *, timeout, json=None, **_):
        seen.append((path, json, timeout))
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    client = ScavioClient(api_key="sk_test")
    getattr(getattr(client, namespace), method)(**kwargs)
    timeout = BATCH8W4_1128[namespace][method][2]
    assert seen == [(f"/api/v1/{namespace}/{segment}", body, timeout)]


@pytest.mark.parametrize("key", sorted(BATCH8W4_1128_ONE_OF))
def test_batch8w4_1128_one_of_is_enforced(key):
    ep = ENDPOINTS[key]
    client = ScavioClient(api_key="sk_test")
    required = {p.name: "x" for p in ep.params if p.required}
    with pytest.raises(ScavioError):
        getattr(getattr(client, ep.namespace), ep.method)(**required)


def test_batch8w4_1128_credits_notes_and_params():
    """DigiKey: 2 / 4 (part number) / 2, note on product; Mouser and RS: 2 credits each."""
    w4 = [ep for ep in ENDPOINTS.values() if ep.namespace in BATCH8W4_1128]
    assert len(w4) == 11
    assert {ep.credits for ep in w4 if ep.namespace != "digikey"} == {2}
    assert [ep.key for ep in w4 if ep.credits_note] == ["digikey_product"]
    note = ENDPOINTS["digikey_product"].credits_note
    assert "2 credits by link" in note and "held at 4" in note
    assert all(p.doc for ep in w4 for p in ep.params)
    assert [p.name for p in ENDPOINTS["rscomponents_search"].required_params] == ["query"]
    assert [p.name for p in ENDPOINTS["rscomponents_category"].required_params] == ["path"]
    assert [p.name for p in ENDPOINTS["rscomponents_brand"].required_params] == ["brand"]
    assert ENDPOINTS["digikey_search"].positional_optional_params[0].name == "query"
    assert ENDPOINTS["digikey_product"].positional_optional_params[0].name == "url"
    assert ENDPOINTS["mouser_product"].positional_optional_params[0].name == "mouser_part_number"
    assert ENDPOINTS["rscomponents_product"].positional_optional_params[0].name == "stock_number"
    assert "25 rows" in ENDPOINTS["digikey_search"].summary
    assert "filter_check" in ENDPOINTS["digikey_search"].summary
    assert "substitutes" in ENDPOINTS["digikey_product"].summary
    assert "does not open by number" in ENDPOINTS["mouser_product"].summary
    assert "us.rs-online.com" in ENDPOINTS["rscomponents_search"].summary
    assert "unit_price_inc_vat" in ENDPOINTS["rscomponents_product"].summary
    assert "not applicable as filters" in ENDPOINTS["rscomponents_category"].summary
