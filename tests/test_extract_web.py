"""client.extract as a callable namespace: backward compatibility, map/crawl/batch
wire mapping, the wait helper, and webhook signature verification."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import inspect
import json as jsonlib
from typing import Any

import httpx
import pytest
import requests

import scavio
from scavio import (
    AsyncScavioClient,
    ScavioClient,
    ScavioError,
    ScavioJobTimeoutError,
    ScavioTimeoutError,
    verify_webhook,
)
from scavio._extract import AsyncExtractNamespace, ExtractNamespace
from scavio._spec import ENDPOINTS

# ---------------------------------------------------------------------------
# Backward compatibility: client.extract(url, ...) is byte-for-byte unchanged.
#
# The literals below were captured from scavio 0.22.0 (extract as a plain
# method) before the namespace change, at the lowest level the SDK touches:
# the arguments handed to requests.post and the bytes httpx puts on the wire.
# Only User-Agent carries the package version, so it is compared against
# __version__ rather than a literal.
# ---------------------------------------------------------------------------

PRE_0_23_SYNC = [
    (
        {"args": ("https://x",), "kwargs": {"format": "text", "mode": "ultra"}},
        {
            "url": "https://api.scavio.dev/api/v1/extract",
            "json": {"url": "https://x", "format": "text", "mode": "ultra"},
            "timeout": 30.0,
            "body": b'{"url": "https://x", "format": "text", "mode": "ultra"}',
        },
    ),
    (
        {"args": ("https://example.com",), "kwargs": {}},
        {
            "url": "https://api.scavio.dev/api/v1/extract",
            "json": {"url": "https://example.com"},
            "timeout": 30.0,
            "body": b'{"url": "https://example.com"}',
        },
    ),
]

PRE_0_23_ASYNC_BODIES = [
    (("https://x",), {"format": "text", "mode": "ultra"},
     b'{"url":"https://x","format":"text","mode":"ultra"}'),
    (("https://example.com",), {}, b'{"url":"https://example.com"}'),
]


def _expected_headers() -> dict[str, str]:
    return {
        "Authorization": "Bearer sk_test",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Client-Source": "scavio-python",
        "User-Agent": f"scavio-python/{scavio.__version__}",
    }


class _Resp:
    status_code = 200
    headers: dict[str, str] = {}

    def __init__(self, payload: Any = None) -> None:
        self._payload = payload if payload is not None else {"ok": True}

    def json(self) -> Any:
        return self._payload


@pytest.mark.parametrize(("call", "expected"), PRE_0_23_SYNC)
def test_backcompat_sync_extract_identical_on_the_wire(call, expected, monkeypatch):
    seen: dict[str, Any] = {}

    def fake_post(url, **kwargs):
        seen["url"] = url
        seen["kwargs"] = kwargs
        return _Resp({"data": {"content": "x"}})

    def forbidden(*_a, **_k):
        raise AssertionError("extract must POST")

    monkeypatch.setattr("scavio._http.requests.post", fake_post)
    monkeypatch.setattr("scavio._http.requests.get", forbidden)
    monkeypatch.setattr("scavio._http.requests.delete", forbidden)

    out = ScavioClient(api_key="sk_test").extract(*call["args"], **call["kwargs"])

    assert out == {"data": {"content": "x"}}
    assert seen["url"] == expected["url"]
    # Exactly the same keyword set as 0.22.0: no params=, no extra headers.
    assert set(seen["kwargs"]) == {"json", "headers", "timeout"}
    assert seen["kwargs"]["json"] == expected["json"]
    assert seen["kwargs"]["timeout"] == expected["timeout"]
    assert seen["kwargs"]["headers"] == _expected_headers()
    prepared = requests.Request(
        "POST", seen["url"], json=seen["kwargs"]["json"], headers=seen["kwargs"]["headers"]
    ).prepare()
    assert prepared.body == expected["body"]


@pytest.mark.parametrize(("args", "kwargs", "body"), PRE_0_23_ASYNC_BODIES)
async def test_backcompat_async_extract_identical_on_the_wire(args, kwargs, body):
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"data": {"content": "x"}})

    client = AsyncScavioClient(api_key="sk_test")
    client._http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    out = await client.extract(*args, **kwargs)
    await client.aclose()

    assert out == {"data": {"content": "x"}}
    (req,) = seen
    assert req.method == "POST"
    assert str(req.url) == "https://api.scavio.dev/api/v1/extract"
    assert req.content == body
    for name, value in _expected_headers().items():
        assert req.headers[name] == value
    assert "idempotency-key" not in req.headers


def test_backcompat_extract_signature_and_positional_call():
    for client in (ScavioClient(api_key="sk_test"), AsyncScavioClient(api_key="sk_test")):
        sig = inspect.signature(client.extract)
        assert list(sig.parameters) == ["url", "format", "mode"]
        assert sig.parameters["url"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert sig.parameters["format"].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters["mode"].kind is inspect.Parameter.KEYWORD_ONLY
        assert all(sig.parameters[p].default is None for p in ("format", "mode"))


def test_backcompat_extract_url_as_keyword(monkeypatch):
    seen: dict[str, Any] = {}
    monkeypatch.setattr(
        "scavio._http.requests.post",
        lambda url, **kw: seen.update(url=url, **kw) or _Resp(),
    )
    ScavioClient(api_key="sk_test").extract(url="https://example.com", mode="advanced")
    assert seen["json"] == {"url": "https://example.com", "mode": "advanced"}


def test_extract_is_a_callable_namespace():
    sync_client = ScavioClient(api_key="sk_test")
    async_client = AsyncScavioClient(api_key="sk_test")
    assert isinstance(sync_client.extract, ExtractNamespace)
    assert isinstance(async_client.extract, AsyncExtractNamespace)
    assert sync_client.extract is sync_client.extract  # one object per client
    for ns in (sync_client.extract, async_client.extract):
        assert callable(ns)
        for m in ("map", "crawl", "crawl_status", "cancel_crawl",
                  "batch", "batch_status", "cancel_batch"):
            assert callable(getattr(ns, m)), m


# ---------------------------------------------------------------------------
# Signatures are pinned to the spec, and sync == async.
# ---------------------------------------------------------------------------

JOB_CONTROLS = ["idempotency_key", "wait", "poll_interval", "wait_timeout"]
SPEC_BACKED = {"map": "extract_map", "crawl": "extract_crawl", "batch": "extract_batch"}


def _named(sig: inspect.Signature) -> list[str]:
    return [
        n for n, p in sig.parameters.items()
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    ]


@pytest.mark.parametrize(("method", "key"), SPEC_BACKED.items())
def test_signatures_cover_the_spec_exactly(method, key):
    sig = inspect.signature(getattr(ScavioClient(api_key="sk_test").extract, method))
    names = [n for n in _named(sig) if n not in JOB_CONTROLS]
    assert names == [p.name for p in ENDPOINTS[key].params]


@pytest.mark.parametrize(
    "method",
    ["__call__", "map", "crawl", "crawl_status", "cancel_crawl",
     "batch", "batch_status", "cancel_batch"],
)
def test_sync_and_async_signatures_match(method):
    s = inspect.signature(getattr(ExtractNamespace, method))
    a = inspect.signature(getattr(AsyncExtractNamespace, method))
    assert list(s.parameters) == list(a.parameters)
    for name, p in s.parameters.items():
        q = a.parameters[name]
        assert (p.kind, p.default, p.annotation) == (q.kind, q.default, q.annotation), name
    assert inspect.iscoroutinefunction(getattr(AsyncExtractNamespace, method))


# ---------------------------------------------------------------------------
# Wire mapping of every new call.
# ---------------------------------------------------------------------------


def _patch_send_sync(monkeypatch, responses=None):
    calls: list[dict[str, Any]] = []
    queue = list(responses or [])

    def fake(method, path, *, json=None, params=None, extra_headers=None, **_):
        calls.append(dict(method=method, path=path, json=json, params=params,
                          headers=extra_headers))
        return queue.pop(0) if queue else {"data": {"id": "job_1", "status": "queued"}}

    monkeypatch.setattr("scavio._client.sync_request", fake)
    return calls


def _patch_send_async(monkeypatch, responses=None):
    calls: list[dict[str, Any]] = []
    queue = list(responses or [])

    async def fake(method, path, *, json=None, params=None, extra_headers=None, **_):
        calls.append(dict(method=method, path=path, json=json, params=params,
                          headers=extra_headers))
        return queue.pop(0) if queue else {"data": {"id": "job_1", "status": "queued"}}

    monkeypatch.setattr("scavio._async_client.async_request", fake)
    return calls


MAP_ALL = dict(
    search="docs api", limit=50, sitemap="only", include_subdomains=True,
    include_paths=["/docs/**"], exclude_paths=["/docs/old/**"],
    ignore_query_parameters=False, mode="advanced",
)
CRAWL_ALL = dict(
    max_pages=2, max_depth=1, include_paths=["/docs/**"], exclude_paths=["/blog/**"],
    allow_subdomains=False, ignore_query_parameters=True, sitemap="skip",
    format="text", mode="ultra", webhook_url="https://hooks.example.com/scavio",
)


def test_map_wire(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    ScavioClient(api_key="sk_test").extract.map("https://scavio.dev", **MAP_ALL)
    (c,) = calls
    assert (c["method"], c["path"]) == ("POST", "/api/v1/extract/map")
    assert c["json"] == {"url": "https://scavio.dev", **MAP_ALL}
    assert c["params"] is None and c["headers"] is None


def test_map_drops_unset(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    ScavioClient(api_key="sk_test").extract.map("https://scavio.dev", limit=5)
    assert calls[0]["json"] == {"url": "https://scavio.dev", "limit": 5}


def test_crawl_wire_with_idempotency_key(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    ScavioClient(api_key="sk_test").extract.crawl(
        "https://scavio.dev/docs", idempotency_key="k-1", **CRAWL_ALL
    )
    (c,) = calls
    assert (c["method"], c["path"]) == ("POST", "/api/v1/extract/crawl")
    assert c["json"] == {"url": "https://scavio.dev/docs", **CRAWL_ALL}
    assert c["headers"] == {"Idempotency-Key": "k-1"}


def test_crawl_generates_an_idempotency_key_per_call(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.extract.crawl("https://a.example")
    client.extract.crawl("https://a.example")
    keys = [c["headers"]["Idempotency-Key"] for c in calls]
    assert all(len(k) == 36 for k in keys) and keys[0] != keys[1]
    assert calls[0]["json"] == {"url": "https://a.example"}


def test_batch_wire(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    ScavioClient(api_key="sk_test").extract.batch(
        ["https://a.example", "https://b.example"], format="html", mode="normal",
        webhook_url="https://hooks.example.com/x", idempotency_key="b-1",
    )
    (c,) = calls
    assert (c["method"], c["path"]) == ("POST", "/api/v1/extract/batch")
    assert c["json"] == {
        "urls": ["https://a.example", "https://b.example"],
        "format": "html", "mode": "normal", "webhook_url": "https://hooks.example.com/x",
    }
    assert c["headers"] == {"Idempotency-Key": "b-1"}


def test_extra_passthrough_and_collision(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    client = ScavioClient(api_key="sk_test")
    client.extract.crawl("https://a.example", **{"future_field": 1})
    assert calls[0]["json"] == {"url": "https://a.example", "future_field": 1}
    with pytest.raises(TypeError):
        client.extract.map("https://a.example", limit=1, **{"limit": 2})


@pytest.mark.parametrize("job", ["crawl", "batch"])
def test_status_wire(job, monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    ns = ScavioClient(api_key="sk_test").extract
    getattr(ns, f"{job}_status")("job_9", cursor="25", limit=10, status="failed",
                                 include_content=False)
    getattr(ns, f"{job}_status")("job_9")
    getattr(ns, f"{job}_status")("job_9", include_content=True)
    assert [c["method"] for c in calls] == ["GET"] * 3
    assert {c["path"] for c in calls} == {f"/api/v1/extract/{job}/job_9"}
    assert calls[0]["params"] == {"cursor": "25", "limit": "10", "status": "failed",
                                  "include_content": "false"}
    assert calls[1]["params"] == {}
    assert calls[2]["params"] == {"include_content": "true"}
    assert all(c["json"] is None and c["headers"] is None for c in calls)


@pytest.mark.parametrize("job", ["crawl", "batch"])
def test_cancel_wire(job, monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    getattr(ScavioClient(api_key="sk_test").extract, f"cancel_{job}")("job_9")
    (c,) = calls
    assert (c["method"], c["path"], c["json"]) == ("DELETE", f"/api/v1/extract/{job}/job_9", None)


def test_empty_job_id_rejected(monkeypatch):
    _patch_send_sync(monkeypatch)
    with pytest.raises(ScavioError):
        ScavioClient(api_key="sk_test").extract.crawl_status("")


async def test_async_wire(monkeypatch):
    calls = _patch_send_async(monkeypatch)
    ns = AsyncScavioClient(api_key="sk_test").extract
    await ns.map("https://scavio.dev", **MAP_ALL)
    await ns.crawl("https://scavio.dev/docs", idempotency_key="k", **CRAWL_ALL)
    await ns.batch(["https://a.example"], idempotency_key="b")
    await ns.crawl_status("c1", limit=5, include_content=False)
    await ns.batch_status("b1", cursor="3")
    await ns.cancel_crawl("c1")
    await ns.cancel_batch("b1")
    assert [(c["method"], c["path"]) for c in calls] == [
        ("POST", "/api/v1/extract/map"),
        ("POST", "/api/v1/extract/crawl"),
        ("POST", "/api/v1/extract/batch"),
        ("GET", "/api/v1/extract/crawl/c1"),
        ("GET", "/api/v1/extract/batch/b1"),
        ("DELETE", "/api/v1/extract/crawl/c1"),
        ("DELETE", "/api/v1/extract/batch/b1"),
    ]
    assert calls[0]["json"] == {"url": "https://scavio.dev", **MAP_ALL}
    assert calls[1]["json"] == {"url": "https://scavio.dev/docs", **CRAWL_ALL}
    assert calls[1]["headers"] == {"Idempotency-Key": "k"}
    assert calls[2]["json"] == {"urls": ["https://a.example"]}
    assert calls[3]["params"] == {"limit": "5", "include_content": "false"}
    assert calls[4]["params"] == {"cursor": "3"}


# ---------------------------------------------------------------------------
# Transport: 202, query strings, DELETE and the extra header reach the HTTP layer.
# ---------------------------------------------------------------------------


def test_transport_accepts_202_and_sends_header(monkeypatch):
    seen: dict[str, Any] = {}

    class Accepted(_Resp):
        status_code = 202

    def fake_post(url, **kw):
        seen.update(url=url, **kw)
        return Accepted({"data": {"id": "crawl_1", "status": "queued"}, "credits_used": 0})

    monkeypatch.setattr("scavio._http.requests.post", fake_post)
    out = ScavioClient(api_key="sk_test").extract.crawl("https://a.example", idempotency_key="z")
    assert out["data"]["id"] == "crawl_1"
    assert seen["headers"]["Idempotency-Key"] == "z"
    assert seen["headers"]["Authorization"] == "Bearer sk_test"


def test_transport_get_with_query_and_delete(monkeypatch):
    seen: list[tuple[str, str, dict[str, Any]]] = []
    monkeypatch.setattr(
        "scavio._http.requests.get",
        lambda url, **kw: seen.append(("GET", url, kw)) or _Resp(),
    )
    monkeypatch.setattr(
        "scavio._http.requests.delete",
        lambda url, **kw: seen.append(("DELETE", url, kw)) or _Resp(),
    )
    client = ScavioClient(api_key="sk_test")
    client.extract.batch_status("b1", limit=3, include_content=False)
    client.extract.cancel_batch("b1")
    client.get_usage()
    assert seen[0][1] == "https://api.scavio.dev/api/v1/extract/batch/b1"
    assert seen[0][2]["params"] == {"limit": "3", "include_content": "false"}
    assert seen[1][0] == "DELETE" and "params" not in seen[1][2]
    # Plain GETs go out exactly as before: no params= keyword at all.
    assert set(seen[2][2]) == {"headers", "timeout"}


async def test_async_transport_202_query_delete():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.method == "POST":
            return httpx.Response(202, json={"data": {"id": "batch_1", "status": "queued"}})
        return httpx.Response(200, json={"data": {"id": "batch_1", "status": "running"}})

    client = AsyncScavioClient(api_key="sk_test")
    client._http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    created = await client.extract.batch(["https://a.example"], idempotency_key="i-1")
    await client.extract.batch_status("batch_1", status="succeeded", include_content=True)
    await client.extract.cancel_batch("batch_1")
    await client.aclose()
    assert created["data"]["id"] == "batch_1"
    assert seen[0].headers["idempotency-key"] == "i-1"
    assert jsonlib.loads(seen[0].content) == {"urls": ["https://a.example"]}
    assert str(seen[1].url) == (
        "https://api.scavio.dev/api/v1/extract/batch/batch_1"
        "?status=succeeded&include_content=true"
    )
    assert seen[2].method == "DELETE"


# ---------------------------------------------------------------------------
# wait=True
# ---------------------------------------------------------------------------


def _status(state: str, results=None, cursor=None) -> dict[str, Any]:
    return {"data": {"id": "crawl_1", "status": state, "pages": {"succeeded": 3},
                     "credits_used": 3, "results": results or [], "next_cursor": cursor}}


def test_crawl_wait_polls_then_collects_every_page(monkeypatch):
    created = {"data": {"id": "crawl_1", "status": "queued", "webhook_secret": "whsec_x"},
               "credits_used": 0}
    calls = _patch_send_sync(monkeypatch, [
        created,
        _status("queued"),
        _status("running"),
        _status("completed"),
        _status("completed", [{"url": "a"}, {"url": "b"}], cursor="2"),
        _status("completed", [{"url": "c"}], cursor=None),
    ])
    monkeypatch.setattr("scavio._extract.time.sleep", lambda s: None)
    out = ScavioClient(api_key="sk_test").extract.crawl("https://a.example", max_pages=3,
                                                         wait=True, poll_interval=0.01)
    assert [r["url"] for r in out["data"]["results"]] == ["a", "b", "c"]
    assert out["data"]["status"] == "completed" and out["data"]["next_cursor"] is None
    assert out["created"]["webhook_secret"] == "whsec_x"
    polls = calls[1:4]
    assert all(c["params"] == {"limit": "1", "include_content": "false"} for c in polls)
    assert calls[4]["params"] == {"limit": "100"}
    assert calls[5]["params"] == {"cursor": "2", "limit": "100"}


def test_wait_returns_failed_and_cancelled_jobs_without_raising(monkeypatch):
    for state in ("failed", "cancelled"):
        _patch_send_sync(monkeypatch, [
            {"data": {"id": "batch_1", "status": "queued"}},
            _status(state),
            _status(state, [{"url": "a", "status": "failed"}]),
        ])
        out = ScavioClient(api_key="sk_test").extract.batch(["https://a.example"], wait=True)
        assert out["data"]["status"] == state


def test_wait_timeout_raises_with_job_id(monkeypatch):
    responses = [{"data": {"id": "crawl_7", "status": "queued"}}] + [_status("running")] * 50
    _patch_send_sync(monkeypatch, responses)
    monkeypatch.setattr("scavio._extract.time.sleep", lambda s: None)
    with pytest.raises(ScavioJobTimeoutError) as info:
        ScavioClient(api_key="sk_test").extract.crawl(
            "https://a.example", wait=True, poll_interval=5, wait_timeout=1
        )
    assert info.value.job_id == "crawl_7" and info.value.job_type == "crawl"
    assert info.value.last_status["data"]["status"] == "running"
    assert isinstance(info.value, ScavioTimeoutError)


async def test_async_crawl_wait(monkeypatch):
    _patch_send_async(monkeypatch, [
        {"data": {"id": "crawl_1", "status": "queued"}},
        _status("running"),
        _status("completed"),
        _status("completed", [{"url": "a"}]),
    ])

    async def no_sleep(_s):
        return None

    monkeypatch.setattr("scavio._extract.asyncio.sleep", no_sleep)
    out = await AsyncScavioClient(api_key="sk_test").extract.crawl("https://a.example",
                                                                   wait=True)
    assert out["data"]["results"] == [{"url": "a"}]
    assert asyncio.iscoroutinefunction(AsyncExtractNamespace.crawl)


# ---------------------------------------------------------------------------
# TikTok video transcript
# ---------------------------------------------------------------------------


def test_tiktok_video_transcript_wire(monkeypatch):
    calls = _patch_send_sync(monkeypatch)
    captured: dict[str, Any] = {}

    def fake(method, path, *, json=None, **_):
        captured.update(method=method, path=path, json=json)
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake)
    client = ScavioClient(api_key="sk_test")
    client.tiktok.video_transcript("7609177768793787679", language="en")
    assert captured == {"method": "POST", "path": "/api/v1/tiktok/video/transcript",
                        "json": {"video_id": "7609177768793787679", "language": "en"}}
    client.tiktok.video_transcript(url="https://www.tiktok.com/@u/video/1")
    assert captured["json"] == {"url": "https://www.tiktok.com/@u/video/1"}
    with pytest.raises(ScavioError):
        client.tiktok.video_transcript()
    assert calls == []


# ---------------------------------------------------------------------------
# verify_webhook
# ---------------------------------------------------------------------------

SECRET = "whsec_0123456789abcdef"
BODY = '{"id":"crawl_1","type":"crawl","status":"completed"}'


def _sign(body: bytes | str, t: int, secret: str = SECRET) -> str:
    raw = body.encode() if isinstance(body, str) else body
    v1 = hmac.new(secret.encode(), f"{t}.".encode() + raw, hashlib.sha256).hexdigest()
    return f"t={t},v1={v1}"


def test_verify_webhook_valid_str_and_bytes():
    t = 1_800_000_000
    header = _sign(BODY, t)
    assert verify_webhook(SECRET, header, BODY, now=t)
    assert verify_webhook(SECRET, header, BODY.encode(), now=t + 299)
    assert verify_webhook(SECRET, header.replace(",", ", "), BODY, now=t)
    assert scavio.verify_webhook is verify_webhook


def test_verify_webhook_matches_the_backend_signer():
    # backend/src/services/webhooks-out.ts signWebhook: HMAC-SHA256 of "<t>.<body>".
    t = 1_700_000_000
    expected_v1 = hmac.new(SECRET.encode(), f"{t}.{BODY}".encode(), hashlib.sha256).hexdigest()
    assert verify_webhook(SECRET, f"t={t},v1={expected_v1}", BODY, now=t)


def test_verify_webhook_rejects_tampering():
    t = 1_800_000_000
    header = _sign(BODY, t)
    assert not verify_webhook(SECRET, header, BODY.replace("completed", "failed"), now=t)
    assert not verify_webhook("whsec_other", header, BODY, now=t)
    assert not verify_webhook(SECRET, header.replace(f"t={t}", f"t={t + 1}"), BODY, now=t)


def test_verify_webhook_rejects_stale_and_future():
    t = 1_800_000_000
    header = _sign(BODY, t)
    assert not verify_webhook(SECRET, header, BODY, now=t + 301)
    assert not verify_webhook(SECRET, header, BODY, now=t - 301)
    assert verify_webhook(SECRET, header, BODY, tolerance=1000, now=t + 900)


@pytest.mark.parametrize(
    "header",
    [None, "", "garbage", "t=abc,v1=00", "v1=deadbeef", "t=1800000000", "t=1800000000,v1=",
     "t=1800000000,v1=éé"],
)
def test_verify_webhook_rejects_malformed(header):
    assert verify_webhook(SECRET, header, BODY, now=1_800_000_000) is False
