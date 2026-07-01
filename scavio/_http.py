from __future__ import annotations

import asyncio
import os
import time
from typing import Any, Optional

import httpx
import requests

from ._exceptions import (
    BadRequestError,
    InsufficientCreditsError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    NotFoundError,
    RateLimitError,
    ScavioAPIError,
    ScavioConnectionError,
    ScavioTimeoutError,
)
from ._ratelimit import AsyncRateLimiter, SyncRateLimiter
from ._retry import RetryConfig, parse_retry_after
from ._version import __version__

BASE_URL = "https://api.scavio.dev"
DEFAULT_TIMEOUT = 30.0

_USER_AGENT = f"scavio-python/{__version__}"


def _resolve_api_key(api_key: Optional[str]) -> str:
    key = api_key or os.environ.get("SCAVIO_API_KEY")
    if not key:
        raise MissingAPIKeyError()
    return key


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Client-Source": "scavio-python",
        "User-Agent": _USER_AGENT,
    }


def _safe_json(text_or_resp: Any) -> dict[str, Any]:
    try:
        body = text_or_resp.json()
    except Exception:
        return {}
    return body if isinstance(body, dict) else {}


def _handle_error(status_code: int, body: dict[str, Any]) -> None:
    """Map a non-2xx response to the appropriate exception and raise it."""
    error: Any = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        error = error.get("message")
    message = str(error) if error else None
    response_body = body if isinstance(body, dict) and body else None

    if status_code == 400:
        raise BadRequestError(message, status_code=status_code, response_body=response_body)
    if status_code == 401:
        raise InvalidAPIKeyError(message, status_code=status_code, response_body=response_body)
    if status_code == 402:
        raise InsufficientCreditsError(
            message, status_code=status_code, response_body=response_body
        )
    if status_code == 404:
        raise NotFoundError(message, status_code=status_code, response_body=response_body)
    if status_code == 429:
        raise RateLimitError(message, status_code=status_code, response_body=response_body)
    raise ScavioAPIError(status_code, message or "Unknown error", response_body=response_body)


def sync_request(
    method: str,
    path: str,
    *,
    api_key: str,
    base_url: str,
    timeout: float,
    rate_limiter: SyncRateLimiter,
    retry: RetryConfig,
    json: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    url = f"{base_url}{path}"
    headers = _build_headers(api_key)
    attempt = 0

    while True:
        rate_limiter.wait()
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=timeout)
            else:
                resp = requests.post(url, json=json, headers=headers, timeout=timeout)
        except requests.Timeout as exc:
            if retry.should_retry_exception(attempt):
                time.sleep(retry.backoff(attempt))
                attempt += 1
                continue
            raise ScavioTimeoutError(str(exc)) from exc
        except requests.RequestException as exc:
            if retry.should_retry_exception(attempt):
                time.sleep(retry.backoff(attempt))
                attempt += 1
                continue
            raise ScavioConnectionError(str(exc)) from exc

        if resp.status_code == 200:
            return _safe_json(resp)

        if retry.should_retry_status(resp.status_code, attempt):
            retry_after = parse_retry_after(resp.headers.get("Retry-After"))
            time.sleep(retry.backoff(attempt, retry_after))
            attempt += 1
            continue

        _handle_error(resp.status_code, _safe_json(resp))


async def async_request(
    method: str,
    path: str,
    *,
    api_key: str,
    base_url: str,
    timeout: float,
    http_client: httpx.AsyncClient,
    rate_limiter: AsyncRateLimiter,
    retry: RetryConfig,
    json: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    url = f"{base_url}{path}"
    headers = _build_headers(api_key)
    attempt = 0

    while True:
        await rate_limiter.wait()
        try:
            if method == "GET":
                resp = await http_client.get(url, headers=headers, timeout=timeout)
            else:
                resp = await http_client.post(url, json=json, headers=headers, timeout=timeout)
        except httpx.TimeoutException as exc:
            if retry.should_retry_exception(attempt):
                await asyncio.sleep(retry.backoff(attempt))
                attempt += 1
                continue
            raise ScavioTimeoutError(str(exc)) from exc
        except httpx.TransportError as exc:
            if retry.should_retry_exception(attempt):
                await asyncio.sleep(retry.backoff(attempt))
                attempt += 1
                continue
            raise ScavioConnectionError(str(exc)) from exc

        if resp.status_code == 200:
            return _safe_json(resp)

        if retry.should_retry_status(resp.status_code, attempt):
            retry_after = parse_retry_after(resp.headers.get("Retry-After"))
            await asyncio.sleep(retry.backoff(attempt, retry_after))
            attempt += 1
            continue

        _handle_error(resp.status_code, _safe_json(resp))
