"""Client construction, configuration, and lifecycle."""

from __future__ import annotations

import pytest

from scavio import AsyncScavioClient, MissingAPIKeyError, ScavioClient, ScavioError


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("SCAVIO_API_KEY", "sk_env")
    client = ScavioClient()
    assert client._api_key == "sk_env"


def test_explicit_key_overrides_env(monkeypatch):
    monkeypatch.setenv("SCAVIO_API_KEY", "sk_env")
    client = ScavioClient(api_key="sk_explicit")
    assert client._api_key == "sk_explicit"


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("SCAVIO_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyError):
        ScavioClient()


def test_base_url_trailing_slash_stripped():
    client = ScavioClient(api_key="k", base_url="https://example.com/")
    assert client._base_url == "https://example.com"


def test_default_timeout_is_float():
    client = ScavioClient(api_key="k")
    assert isinstance(client._timeout, float)


@pytest.mark.parametrize("rps", [0, 11, -1])
def test_invalid_rps_rejected(rps):
    with pytest.raises(ScavioError):
        ScavioClient(api_key="k", max_requests_per_second=rps)


@pytest.mark.parametrize("rps", [1, 5, 10])
def test_valid_rps_accepted(rps):
    ScavioClient(api_key="k", max_requests_per_second=rps)


def test_namespaces_present():
    client = ScavioClient(api_key="k")
    for ns in ("google", "amazon", "walmart", "youtube", "reddit", "tiktok", "instagram"):
        assert hasattr(client, ns)


def test_sync_context_manager():
    with ScavioClient(api_key="k") as client:
        assert isinstance(client, ScavioClient)


async def test_async_context_manager_and_close():
    async with AsyncScavioClient(api_key="k") as client:
        client._ensure_client()
        assert client._http_client is not None
    assert client._http_client is None


async def test_async_close_alias():
    client = AsyncScavioClient(api_key="k")
    client._ensure_client()
    await client.close()
    assert client._http_client is None
