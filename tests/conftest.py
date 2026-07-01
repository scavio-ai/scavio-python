from __future__ import annotations

from typing import Any

import pytest

from scavio import AsyncScavioClient, ScavioClient


def patch_sync(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Intercept the sync transport, capturing the outgoing method/path/body."""
    captured: dict[str, Any] = {}

    def fake_request(method: str, path: str, *, json: Any = None, **_: Any) -> dict[str, Any]:
        captured.update(method=method, path=path, json=json)
        return {"ok": True}

    monkeypatch.setattr("scavio._client.sync_request", fake_request)
    return captured


def patch_async(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Intercept the async transport, capturing the outgoing method/path/body."""
    captured: dict[str, Any] = {}

    async def fake_request(method: str, path: str, *, json: Any = None, **_: Any) -> dict[str, Any]:
        captured.update(method=method, path=path, json=json)
        return {"ok": True}

    monkeypatch.setattr("scavio._async_client.async_request", fake_request)
    return captured


@pytest.fixture
def sync_client() -> ScavioClient:
    return ScavioClient(api_key="sk_test")


@pytest.fixture
def async_client() -> AsyncScavioClient:
    return AsyncScavioClient(api_key="sk_test")
