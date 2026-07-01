"""Retry / backoff behavior for both transports."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import requests

import scavio._http as http
from scavio import (
    BadRequestError,
    RateLimitError,
    ScavioAPIError,
    ScavioConnectionError,
    ScavioTimeoutError,
)
from scavio._http import async_request, sync_request
from scavio._ratelimit import AsyncRateLimiter, SyncRateLimiter
from scavio._retry import RetryConfig


class FakeResp:
    def __init__(self, status: int, body: Any = None, headers: dict | None = None):
        self.status_code = status
        self._body = body if body is not None else {}
        self.headers = headers or {}

    def json(self) -> Any:
        return self._body


def _run_sync(monkeypatch, responses, *, max_retries=2):
    calls = {"n": 0}
    seq = iter(responses)

    def transport(url, **_):
        calls["n"] += 1
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(http.requests, "post", transport)
    monkeypatch.setattr(http.time, "sleep", lambda _s: None)
    result = sync_request(
        "POST",
        "/x",
        api_key="k",
        base_url="https://api.scavio.dev",
        timeout=1.0,
        rate_limiter=SyncRateLimiter(1000),
        retry=RetryConfig(max_retries=max_retries, base_delay=0.0),
    )
    return result, calls


def test_retries_5xx_then_succeeds(monkeypatch):
    result, calls = _run_sync(
        monkeypatch, [FakeResp(503), FakeResp(502), FakeResp(200, {"ok": 1})]
    )
    assert result == {"ok": 1}
    assert calls["n"] == 3


def test_retry_exhausted_raises_rate_limit(monkeypatch):
    with pytest.raises(RateLimitError):
        _run_sync(monkeypatch, [FakeResp(429), FakeResp(429), FakeResp(429)])


def test_no_retry_on_400(monkeypatch):
    with pytest.raises(BadRequestError):
        _, calls = _run_sync(monkeypatch, [FakeResp(400, {"error": "bad"})])


def test_retries_disabled(monkeypatch):
    with pytest.raises(ScavioAPIError):
        _run_sync(monkeypatch, [FakeResp(503)], max_retries=0)


def test_timeout_retried_then_success(monkeypatch):
    result, calls = _run_sync(
        monkeypatch, [requests.Timeout(), FakeResp(200, {"ok": 1})], max_retries=1
    )
    assert result == {"ok": 1}
    assert calls["n"] == 2


def test_timeout_exhausted_wrapped(monkeypatch):
    with pytest.raises(ScavioTimeoutError):
        _run_sync(monkeypatch, [requests.Timeout()], max_retries=0)


def test_connection_error_exhausted_wrapped(monkeypatch):
    with pytest.raises(ScavioConnectionError):
        _run_sync(
            monkeypatch,
            [requests.ConnectionError(), requests.ConnectionError()],
            max_retries=1,
        )


def test_retry_after_header_honored(monkeypatch):
    slept: list[float] = []
    seq = iter([FakeResp(429, headers={"Retry-After": "0"}), FakeResp(200, {"ok": 1})])

    def transport(url, **_):
        item = next(seq)
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(http.requests, "post", transport)
    monkeypatch.setattr(http.time, "sleep", lambda s: slept.append(s))
    result = sync_request(
        "POST",
        "/x",
        api_key="k",
        base_url="https://api.scavio.dev",
        timeout=1.0,
        rate_limiter=SyncRateLimiter(1000),
        retry=RetryConfig(max_retries=1),
    )
    assert result == {"ok": 1}
    assert slept == [0.0]


# ------------------------------- async --------------------------------------


class FakeAsyncClient:
    def __init__(self, responses):
        self._seq = iter(responses)
        self.calls = 0

    async def post(self, url, **_):
        self.calls += 1
        item = next(self._seq)
        if isinstance(item, Exception):
            raise item
        return item

    async def get(self, url, **_):
        return await self.post(url)


async def _run_async(monkeypatch, responses, *, max_retries=2):
    async def no_sleep(_s):
        return None

    monkeypatch.setattr(http.asyncio, "sleep", no_sleep)
    fake = FakeAsyncClient(responses)
    result = await async_request(
        "POST",
        "/x",
        api_key="k",
        base_url="https://api.scavio.dev",
        timeout=1.0,
        http_client=fake,
        rate_limiter=AsyncRateLimiter(1000),
        retry=RetryConfig(max_retries=max_retries, base_delay=0.0),
    )
    return result, fake


async def test_async_retries_then_succeeds(monkeypatch):
    result, fake = await _run_async(
        monkeypatch, [FakeResp(503), FakeResp(200, {"ok": 1})]
    )
    assert result == {"ok": 1}
    assert fake.calls == 2


async def test_async_network_error_wrapped(monkeypatch):
    with pytest.raises(ScavioConnectionError):
        await _run_async(
            monkeypatch,
            [httpx.ConnectError("boom"), httpx.ConnectError("boom")],
            max_retries=1,
        )


async def test_async_timeout_wrapped(monkeypatch):
    with pytest.raises(ScavioTimeoutError):
        await _run_async(monkeypatch, [httpx.ReadTimeout("slow")], max_retries=0)
