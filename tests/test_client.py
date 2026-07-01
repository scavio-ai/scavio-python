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
        client.search("test", gl="fr", hl="en", start=10)
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"] == {
            "query": "test",
            "gl": "fr",
            "hl": "en",
            "start": 10,
        }

    @patch("scavio._http.requests.post")
    def test_google_namespace_hits_v2(self, mock_post):
        mock_post.return_value = _mock_response(200, {"results": []})
        client = ScavioClient(api_key="sk_test")
        client.google.search("test")
        call_kwargs = mock_post.call_args
        assert "/api/v2/google" in call_kwargs[0][0]


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


class TestGoogleV2:
    """Google v2 namespace: correct passthrough paths + body."""

    @patch("scavio._http.requests.post")
    def test_search(self, mock_post):
        mock_post.return_value = _mock_response(200, {"organic_results": []})
        client = ScavioClient(api_key="sk_test")
        client.google.search("cold brew")
        assert mock_post.call_args[0][0] == "https://api.scavio.dev/api/v2/google"
        assert mock_post.call_args[1]["json"] == {"query": "cold brew"}

    @patch("scavio._http.requests.post")
    def test_paths(self, mock_post):
        mock_post.return_value = _mock_response(200, {})
        client = ScavioClient(api_key="sk_test")
        cases = [
            (lambda: client.google.ai_mode("q"), "/api/v2/google/ai-mode"),
            (lambda: client.google.maps_search("q"), "/api/v2/google/maps/search"),
            (lambda: client.google.maps_place("ChIJ"), "/api/v2/google/maps/place"),
            (lambda: client.google.maps_reviews("0x1:0x2"), "/api/v2/google/maps/reviews"),
            (lambda: client.google.shopping("laptop"), "/api/v2/google/shopping"),
            (lambda: client.google.shopping_product(catalog_id="700", query="laptop"), "/api/v2/google/shopping/product"),
            (lambda: client.google.shopping_stores("700", "tok"), "/api/v2/google/shopping/product/stores"),
            (lambda: client.google.flights("JFK", "LAX", "2026-12-15"), "/api/v2/google/flights"),
            (lambda: client.google.hotels("Bali", "2026-08-01", "2026-08-03"), "/api/v2/google/hotels"),
            (lambda: client.google.hotels_detail("tok", "2026-08-01", "2026-08-03"), "/api/v2/google/hotels/detail"),
            (lambda: client.google.news("openai"), "/api/v2/google/news"),
            (lambda: client.google.trends("bitcoin"), "/api/v2/google/trends"),
            (lambda: client.google.trending("US"), "/api/v2/google/trending"),
        ]
        for call, path in cases:
            call()
            assert mock_post.call_args[0][0] == f"https://api.scavio.dev{path}", path

    @patch("scavio._http.requests.post")
    def test_passthrough_and_drops_none(self, mock_post):
        mock_post.return_value = _mock_response(200, {})
        client = ScavioClient(api_key="sk_test")
        client.google.search("q", gl="us", hl="en")
        assert mock_post.call_args[1]["json"] == {"query": "q", "gl": "us", "hl": "en"}
        # place details: only the provided id is sent, None is dropped
        client.google.maps_place("ChIJ")
        assert mock_post.call_args[1]["json"] == {"place_id": "ChIJ"}

    @patch("scavio._http.requests.post")
    def test_shopping_product_full_flow(self, mock_post):
        mock_post.return_value = _mock_response(200, {})
        client = ScavioClient(api_key="sk_test")
        client.google.shopping_product(catalog_id="700", query="laptop")
        assert mock_post.call_args[1]["json"] == {"catalog_id": "700", "query": "laptop"}
