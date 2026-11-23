"""Every endpoint, every parameter -> wire-field mapping, on sync and async."""

from __future__ import annotations

import inspect

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
        "home_depot": 3,
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
    assert sum(expected.values()) == 135


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
    """sephora/ulta/aldi/micro_center/walgreens/cvs (0.32.0): 20 endpoints, priced per method."""
    expected = {
        "sephora": {"search": 1, "category": 1, "product": 2},  # product 2 since 0.50.1
        "ulta": {"search": 1, "category": 1, "product": 1, "stores": 1},
        "aldi": {"search": 1, "product": 1, "stores": 1},
        "micro_center": {"search": 2, "product": 2, "stores": 1},
        "walgreens": {"search": 2, "product": 2, "stores": 2, "stock": 4},
        "cvs": {"search": 1, "product": 1, "stock": 1},
    }
    for ns, methods in expected.items():
        eps = {ep.method: ep for ep in ENDPOINTS.values() if ep.namespace == ns}
        assert {m: ep.credits for m, ep in eps.items()} == methods, ns
        wire_ns = ns.replace("_", "")
        for m, ep in eps.items():
            assert ep.path == f"/api/v1/{wire_ns}/{m}", ep.key
    assert sum(len(m) for m in expected.values()) == 20


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
    """best_buy (0.39.0): 9 endpoints on /api/v1/bestbuy, 120 s timeout floor.

    search, product, reviews and prices 2 credits; category 2 (3 on a pcmcat
    page, stated in credits_note); deals 3; stores and suggestions 1;
    availability 2 flat.
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
