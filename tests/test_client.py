from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from scavio import (
    BadRequestError,
    InsufficientCreditsError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    RateLimitError,
    ScavioClient,
)


def _mock_response(status_code: int = 200, body: dict | None = None) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = body or {}
    return resp


class TestClientInit:
    def test_missing_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(MissingAPIKeyError):
                ScavioClient()

    def test_api_key_from_param(self):
        client = ScavioClient(api_key="sk_test")
        assert client._api_key == "sk_test"

    def test_api_key_from_env(self):
        with patch.dict("os.environ", {"SCAVIO_API_KEY": "sk_env"}):
            client = ScavioClient()
            assert client._api_key == "sk_env"

    def test_param_overrides_env(self):
        with patch.dict("os.environ", {"SCAVIO_API_KEY": "sk_env"}):
            client = ScavioClient(api_key="sk_param")
            assert client._api_key == "sk_param"

    def test_custom_base_url(self):
        client = ScavioClient(api_key="sk_test", base_url="https://custom.api.com/")
        assert client._base_url == "https://custom.api.com"

    def test_context_manager(self):
        with ScavioClient(api_key="sk_test") as client:
            assert client._api_key == "sk_test"


class TestNamespaces:
    def test_has_all_namespaces(self):
        client = ScavioClient(api_key="sk_test")
        assert hasattr(client, "google")
        assert hasattr(client, "amazon")
        assert hasattr(client, "walmart")
        assert hasattr(client, "youtube")
        assert hasattr(client, "reddit")
        assert hasattr(client, "tiktok")


class TestGoogleSearch:
    @patch("scavio._http.requests.post")
    def test_basic_search(self, mock_post):
        mock_post.return_value = _mock_response(200, {"results": []})
        client = ScavioClient(api_key="sk_test")
        result = client.search("test query")
        assert result == {"results": []}
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"] == {"query": "test query"}

    @patch("scavio._http.requests.post")
    def test_search_with_params(self, mock_post):
        mock_post.return_value = _mock_response(200, {"results": []})
        client = ScavioClient(api_key="sk_test")
        client.search("test", country_code="fr", search_type="news", page=2)
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"] == {
            "query": "test",
            "country_code": "fr",
            "search_type": "news",
            "page": 2,
        }

    @patch("scavio._http.requests.post")
    def test_google_namespace_alias(self, mock_post):
        mock_post.return_value = _mock_response(200, {"results": []})
        client = ScavioClient(api_key="sk_test")
        client.google.search("test")
        call_kwargs = mock_post.call_args
        assert "/api/v1/google" in call_kwargs[0][0]


class TestAmazon:
    @patch("scavio._http.requests.post")
    def test_search(self, mock_post):
        mock_post.return_value = _mock_response(200, {"data": []})
        client = ScavioClient(api_key="sk_test")
        client.amazon.search("headphones", domain="co.uk")
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"] == {"query": "headphones", "domain": "co.uk"}

    @patch("scavio._http.requests.post")
    def test_product(self, mock_post):
        mock_post.return_value = _mock_response(200, {"data": {}})
        client = ScavioClient(api_key="sk_test")
        client.amazon.product("B09V3KXJPB")
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"] == {"query": "B09V3KXJPB"}


class TestErrorHandling:
    @patch("scavio._http.requests.post")
    def test_401_raises_invalid_key(self, mock_post):
        mock_post.return_value = _mock_response(401, {"error": "Invalid API key"})
        client = ScavioClient(api_key="sk_bad")
        with pytest.raises(InvalidAPIKeyError):
            client.search("test")

    @patch("scavio._http.requests.post")
    def test_402_raises_insufficient_credits(self, mock_post):
        mock_post.return_value = _mock_response(
            402, {"error": "Insufficient credits"}
        )
        client = ScavioClient(api_key="sk_test")
        with pytest.raises(InsufficientCreditsError):
            client.search("test")

    @patch("scavio._http.requests.post")
    def test_429_raises_rate_limit(self, mock_post):
        mock_post.return_value = _mock_response(429, {"error": "Rate limit exceeded"})
        client = ScavioClient(api_key="sk_test")
        with pytest.raises(RateLimitError):
            client.search("test")

    @patch("scavio._http.requests.post")
    def test_400_raises_bad_request(self, mock_post):
        mock_post.return_value = _mock_response(400, {"error": "Missing query"})
        client = ScavioClient(api_key="sk_test")
        with pytest.raises(BadRequestError):
            client.search("")


class TestHeaders:
    @patch("scavio._http.requests.post")
    def test_auth_header(self, mock_post):
        mock_post.return_value = _mock_response(200, {})
        client = ScavioClient(api_key="sk_test123")
        client.search("test")
        headers = mock_post.call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer sk_test123"
        assert headers["X-Client-Source"] == "scavio-python"

    @patch("scavio._http.requests.get")
    def test_get_usage(self, mock_get):
        mock_get.return_value = _mock_response(
            200, {"plan": "free", "credit_balance": 100}
        )
        client = ScavioClient(api_key="sk_test")
        usage = client.get_usage()
        assert usage["plan"] == "free"
        assert usage["credit_balance"] == 100


class TestTikTok:
    @patch("scavio._http.requests.post")
    def test_profile(self, mock_post):
        mock_post.return_value = _mock_response(200, {"data": {}})
        client = ScavioClient(api_key="sk_test")
        client.tiktok.profile(username="tiktok")
        assert mock_post.call_args[1]["json"] == {"username": "tiktok"}

    @patch("scavio._http.requests.post")
    def test_search_videos(self, mock_post):
        mock_post.return_value = _mock_response(200, {"data": []})
        client = ScavioClient(api_key="sk_test")
        client.tiktok.search_videos("cooking", count=5)
        assert mock_post.call_args[1]["json"] == {"keyword": "cooking", "count": 5}
