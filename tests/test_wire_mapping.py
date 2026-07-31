"""Every endpoint, every parameter -> wire-field mapping, on sync and async."""

from __future__ import annotations

import inspect

import pytest

from scavio import AsyncScavioClient, ScavioClient
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
    for ep in ENDPOINTS.values():
        if ep.key in retired:
            assert ep.summary.startswith("RETIRED:"), ep.key
            assert ep.credits == 0, ep.key
        elif ep.namespace == "linkedin":
            assert ep.credits == 1, ep.key


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
