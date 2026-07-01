"""Sliding-window rate limiters (sync + async)."""

from __future__ import annotations

import pytest

from scavio import _ratelimit
from scavio._ratelimit import AsyncRateLimiter, SyncRateLimiter


def test_sync_limiter_allows_up_to_max(monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr(_ratelimit.time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(_ratelimit.time, "sleep", lambda s: slept.append(s))
    rl = SyncRateLimiter(2)
    rl.wait()
    rl.wait()
    assert slept == []


def test_sync_limiter_throttles_beyond_max(monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr(_ratelimit.time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(_ratelimit.time, "sleep", lambda s: slept.append(s))
    rl = SyncRateLimiter(2)
    rl.wait()
    rl.wait()
    rl.wait()  # third within the same frozen second must sleep
    assert slept and slept[0] == pytest.approx(1.0)


async def test_async_limiter_throttles_beyond_max(monkeypatch):
    slept: list[float] = []

    async def fake_sleep(s):
        slept.append(s)

    monkeypatch.setattr(_ratelimit.time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(_ratelimit.asyncio, "sleep", fake_sleep)
    rl = AsyncRateLimiter(1)
    await rl.wait()
    await rl.wait()  # second within the same frozen second must sleep
    assert slept and slept[0] == pytest.approx(1.0)
