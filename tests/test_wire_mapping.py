"""Every endpoint, every parameter -> wire-field mapping, on sync and async."""

from __future__ import annotations

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
    client.amazon.product("B09XS7JWHH", domain="co.uk")
    assert captured["json"] == {"query": "B09XS7JWHH", "domain": "co.uk"}


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
