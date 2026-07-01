from __future__ import annotations

import asyncio
import collections
import threading
import time


class SyncRateLimiter:
    """Thread-safe sliding-window limiter (max N requests per rolling second)."""

    def __init__(self, max_per_second: int) -> None:
        self._max = max_per_second
        self._timestamps: collections.deque[float] = collections.deque()
        self._lock = threading.Lock()

    def _cleanup(self, now: float) -> None:
        while self._timestamps and now - self._timestamps[0] >= 1.0:
            self._timestamps.popleft()

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            self._cleanup(now)
            if len(self._timestamps) >= self._max:
                sleep_time = 1.0 - (now - self._timestamps[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                self._cleanup(time.monotonic())
            self._timestamps.append(time.monotonic())


class AsyncRateLimiter:
    """asyncio sliding-window limiter mirroring :class:`SyncRateLimiter`.

    Acquisition is serialized with an ``asyncio.Lock`` so concurrent coroutines
    are throttled to at most ``max_per_second`` starts per rolling second. The
    lock is created lazily on first use to avoid binding to an event loop at
    construction time (matters on Python 3.9).
    """

    def __init__(self, max_per_second: int) -> None:
        self._max = max_per_second
        self._timestamps: collections.deque[float] = collections.deque()
        self._lock: asyncio.Lock | None = None

    def _cleanup(self, now: float) -> None:
        while self._timestamps and now - self._timestamps[0] >= 1.0:
            self._timestamps.popleft()

    async def wait(self) -> None:
        if self._lock is None:
            self._lock = asyncio.Lock()
        async with self._lock:
            now = time.monotonic()
            self._cleanup(now)
            if len(self._timestamps) >= self._max:
                sleep_time = 1.0 - (now - self._timestamps[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                self._cleanup(time.monotonic())
            self._timestamps.append(time.monotonic())
