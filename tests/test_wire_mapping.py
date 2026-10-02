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
    # Live costs mirror the upstream price tiers the backend bills on: 0.001 usd
    # -> 1 credit, 0.01 -> 10, 0.03 -> 30. Pinned per key so a drift from the
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

BODY_PRICED = {"walmart", "threads", "kuaishou", "_core"}


def test_every_body_priced_endpoint_carries_a_credits_note():
    for ep in ENDPOINTS.values():
        if ep.namespace in BODY_PRICED:
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
        "target": 4,
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
        "_core": 1,
    }
    counts: dict[str, int] = {}
    for ep in ENDPOINTS.values():
        if ep.namespace in expected:
            counts[ep.namespace] = counts.get(ep.namespace, 0) + 1
    assert counts == expected
    assert sum(expected.values()) == 94


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
