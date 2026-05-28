from __future__ import annotations

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from scavio import AsyncScavioClient, InvalidAPIKeyError, MissingAPIKeyError


def _mock_httpx_response(
    status_code: int = 200, body: dict | None = None
) -> httpx.Response:
    resp = httpx.Response(
        status_code=status_code,
        json=body or {},
        request=httpx.Request("POST", "https://test.com"),
    )
    return resp


class TestAsyncClientInit:
    def test_missing_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(MissingAPIKeyError):
                AsyncScavioClient()

    def test_api_key_from_param(self):
        client = AsyncScavioClient(api_key="sk_test")
        assert client._api_key == "sk_test"


class TestAsyncContextManager:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AsyncScavioClient(api_key="sk_test") as client:
            assert client._http_client is not None
        assert client._http_client is None


class TestAsyncGoogleSearch:
    @pytest.mark.asyncio
    async def test_basic_search(self):
        client = AsyncScavioClient(api_key="sk_test")
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.post.return_value = _mock_httpx_response(200, {"results": []})
        client._http_client = mock_client

        result = await client.search("test query")
        assert result == {"results": []}
        mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_params(self):
        client = AsyncScavioClient(api_key="sk_test")
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.post.return_value = _mock_httpx_response(200, {"results": []})
        client._http_client = mock_client

        await client.search("test", country_code="fr", search_type="news")
        call_kwargs = mock_client.post.call_args
        assert call_kwargs[1]["json"] == {
            "query": "test",
            "country_code": "fr",
            "search_type": "news",
        }


class TestAsyncErrorHandling:
    @pytest.mark.asyncio
    async def test_401_raises_invalid_key(self):
        client = AsyncScavioClient(api_key="sk_bad")
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.post.return_value = _mock_httpx_response(
            401, {"error": "Invalid API key"}
        )
        client._http_client = mock_client

        with pytest.raises(InvalidAPIKeyError):
            await client.search("test")


class TestAsyncAmazon:
    @pytest.mark.asyncio
    async def test_search(self):
        client = AsyncScavioClient(api_key="sk_test")
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.post.return_value = _mock_httpx_response(200, {"data": []})
        client._http_client = mock_client

        await client.amazon.search("headphones")
        call_kwargs = mock_client.post.call_args
        assert call_kwargs[1]["json"] == {"query": "headphones"}


class TestAsyncTikTok:
    @pytest.mark.asyncio
    async def test_profile(self):
        client = AsyncScavioClient(api_key="sk_test")
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.post.return_value = _mock_httpx_response(200, {"data": {}})
        client._http_client = mock_client

        await client.tiktok.profile(username="tiktok")
        call_kwargs = mock_client.post.call_args
        assert call_kwargs[1]["json"] == {"username": "tiktok"}


class TestAsyncUsage:
    @pytest.mark.asyncio
    async def test_get_usage(self):
        client = AsyncScavioClient(api_key="sk_test")
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = _mock_httpx_response(
            200, {"plan": "free", "credit_balance": 100}
        )
        client._http_client = mock_client

        usage = await client.get_usage()
        assert usage["plan"] == "free"
