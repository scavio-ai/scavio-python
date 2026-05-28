from __future__ import annotations

import collections
import os
import threading
import time
from typing import Any, Optional

import httpx
import requests

from ._exceptions import (
    BadRequestError,
    InsufficientCreditsError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    RateLimitError,
    ScavioAPIError,
)

BASE_URL = "https://api.scavio.dev"
DEFAULT_TIMEOUT = 30


class _RateLimiter:
    """Sliding-window rate limiter (requests per second)."""

    def __init__(self, max_per_second: int) -> None:
        self._max = max_per_second
        self._timestamps: collections.deque[float] = collections.deque()
        self._lock = threading.Lock()

    def _cleanup(self) -> None:
        now = time.monotonic()
        while self._timestamps and now - self._timestamps[0] >= 1.0:
            self._timestamps.popleft()

    def wait(self) -> None:
        with self._lock:
            self._cleanup()
            if len(self._timestamps) >= self._max:
                sleep_time = 1.0 - (time.monotonic() - self._timestamps[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                self._cleanup()
            self._timestamps.append(time.monotonic())


def _resolve_api_key(api_key: Optional[str]) -> str:
    key = api_key or os.environ.get("SCAVIO_API_KEY")
    if not key:
        raise MissingAPIKeyError()
    return key


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Client-Source": "scavio-python",
    }


def _handle_error(status_code: int, body: dict[str, Any]) -> None:
    error = body.get("error", "Unknown error")
    if isinstance(error, dict):
        error = error.get("message", "Unknown error")
    msg = str(error)

    if status_code == 400:
        raise BadRequestError(msg)
    if status_code == 401:
        raise InvalidAPIKeyError(msg)
    if status_code == 402:
        raise InsufficientCreditsError(msg)
    if status_code == 429:
        raise RateLimitError(msg)
    raise ScavioAPIError(status_code, msg)


def sync_request(
    method: str,
    path: str,
    *,
    api_key: str,
    base_url: str,
    timeout: int,
    rate_limiter: _RateLimiter,
    json: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    rate_limiter.wait()
    url = f"{base_url}{path}"
    headers = _build_headers(api_key)

    if method == "GET":
        resp = requests.get(url, headers=headers, timeout=timeout)
    else:
        resp = requests.post(url, json=json, headers=headers, timeout=timeout)

    if resp.status_code != 200:
        try:
            body = resp.json()
        except Exception:
            body = {}
        _handle_error(resp.status_code, body)

    return resp.json()


async def async_request(
    method: str,
    path: str,
    *,
    api_key: str,
    base_url: str,
    timeout: int,
    http_client: Optional[httpx.AsyncClient] = None,
    json: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    headers = _build_headers(api_key)
    url = f"{base_url}{path}"

    client = http_client or httpx.AsyncClient()
    should_close = http_client is None
    try:
        if method == "GET":
            resp = await client.get(url, headers=headers, timeout=timeout)
        else:
            resp = await client.post(url, json=json, headers=headers, timeout=timeout)

        if resp.status_code != 200:
            try:
                body = resp.json()
            except Exception:
                body = {}
            _handle_error(resp.status_code, body)

        return resp.json()
    finally:
        if should_close:
            await client.aclose()
