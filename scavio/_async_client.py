from __future__ import annotations

from typing import Any, Optional

import httpx

from ._http import BASE_URL, DEFAULT_TIMEOUT, _resolve_api_key, async_request


def _compact(body: dict[str, Any]) -> dict[str, Any]:
    """Drop keys whose value is None so unset params are not sent."""
    return {k: v for k, v in body.items() if v is not None}


class _AsyncGoogleNamespace:
    """Google endpoints (scrape.do engine, /api/v2/google).

    A faithful passthrough that returns Google's full response. Every endpoint
    costs 1 credit. Any additional scrape.do parameter can be passed as a
    keyword argument. See https://scavio.dev/docs/search-api.
    """

    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Google SERP search (includes the AI Overview when Google returns one)."""
        return await self._client._post("/api/v2/google", _compact({"query": query, **params}))

    async def ai_mode(self, query: str, **params: Any) -> dict[str, Any]:
        """Google AI Mode answer."""
        return await self._client._post("/api/v2/google/ai-mode", _compact({"query": query, **params}))

    async def maps_search(self, query: str, **params: Any) -> dict[str, Any]:
        """Google Maps local results."""
        return await self._client._post("/api/v2/google/maps/search", _compact({"query": query, **params}))

    async def maps_place(
        self, place_id: Optional[str] = None, *, data_cid: Optional[str] = None, **params: Any
    ) -> dict[str, Any]:
        """Google Maps place details. Provide place_id or data_cid."""
        return await self._client._post(
            "/api/v2/google/maps/place",
            _compact({"place_id": place_id, "data_cid": data_cid, **params}),
        )

    async def maps_reviews(
        self, data_id: Optional[str] = None, *, place_id: Optional[str] = None, **params: Any
    ) -> dict[str, Any]:
        """Google Maps reviews. Provide data_id or place_id."""
        return await self._client._post(
            "/api/v2/google/maps/reviews",
            _compact({"data_id": data_id, "place_id": place_id, **params}),
        )

    async def shopping(self, query: str, **params: Any) -> dict[str, Any]:
        """Google Shopping search results."""
        return await self._client._post("/api/v2/google/shopping", _compact({"query": query, **params}))

    async def shopping_product(
        self,
        *,
        catalog_id: Optional[str] = None,
        query: Optional[str] = None,
        product_id: Optional[str] = None,
        **params: Any,
    ) -> dict[str, Any]:
        """Google Shopping product. Pass catalog_id + query for full details and sellers."""
        return await self._client._post(
            "/api/v2/google/shopping/product",
            _compact({"catalog_id": catalog_id, "query": query, "product_id": product_id, **params}),
        )

    async def shopping_stores(
        self, catalog_id: str, next_page_token: str, **params: Any
    ) -> dict[str, Any]:
        """Google Shopping product sellers (continuation of shopping_product)."""
        return await self._client._post(
            "/api/v2/google/shopping/product/stores",
            _compact({"catalog_id": catalog_id, "next_page_token": next_page_token, **params}),
        )

    async def flights(
        self, departure_id: str, arrival_id: str, outbound_date: str, **params: Any
    ) -> dict[str, Any]:
        """Google Flights."""
        return await self._client._post(
            "/api/v2/google/flights",
            _compact({
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "outbound_date": outbound_date,
                **params,
            }),
        )

    async def hotels(
        self, query: str, check_in_date: str, check_out_date: str, **params: Any
    ) -> dict[str, Any]:
        """Google Hotels search."""
        return await self._client._post(
            "/api/v2/google/hotels",
            _compact({
                "query": query,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                **params,
            }),
        )

    async def hotels_detail(
        self, detail_token: str, check_in_date: str, check_out_date: str, **params: Any
    ) -> dict[str, Any]:
        """Google Hotels property details (from a hotels listing detail_token)."""
        return await self._client._post(
            "/api/v2/google/hotels/detail",
            _compact({
                "detail_token": detail_token,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                **params,
            }),
        )

    async def news(self, query: Optional[str] = None, **params: Any) -> dict[str, Any]:
        """Google News. Provide query or a topic/story/publication token."""
        return await self._client._post("/api/v2/google/news", _compact({"query": query, **params}))

    async def trends(self, query: str, **params: Any) -> dict[str, Any]:
        """Google Trends data."""
        return await self._client._post("/api/v2/google/trends", _compact({"query": query, **params}))

    async def trending(self, geo: str, **params: Any) -> dict[str, Any]:
        """Google Trending Now for a country."""
        return await self._client._post("/api/v2/google/trending", _compact({"geo": geo, **params}))


class _AsyncAmazonNamespace:
    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def search(
        self,
        query: str,
        *,
        domain: Optional[str] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        currency: Optional[str] = None,
        device: Optional[str] = None,
        sort_by: Optional[str] = None,
        start_page: Optional[int] = None,
        pages: Optional[int] = None,
        category_id: Optional[str] = None,
        merchant_id: Optional[str] = None,
        zip_code: Optional[str] = None,
        autoselect_variant: Optional[bool] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"query": query}
        if domain is not None:
            params["domain"] = domain
        if country is not None:
            params["country"] = country
        if language is not None:
            params["language"] = language
        if currency is not None:
            params["currency"] = currency
        if device is not None:
            params["device"] = device
        if sort_by is not None:
            params["sort_by"] = sort_by
        if start_page is not None:
            params["start_page"] = start_page
        if pages is not None:
            params["pages"] = pages
        if category_id is not None:
            params["category_id"] = category_id
        if merchant_id is not None:
            params["merchant_id"] = merchant_id
        if zip_code is not None:
            params["zip_code"] = zip_code
        if autoselect_variant is not None:
            params["autoselect_variant"] = autoselect_variant
        return await self._client._post("/api/v1/amazon/search", params)

    async def product(
        self,
        asin: str,
        *,
        domain: Optional[str] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        currency: Optional[str] = None,
        device: Optional[str] = None,
        zip_code: Optional[str] = None,
        autoselect_variant: Optional[bool] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"query": asin}
        if domain is not None:
            params["domain"] = domain
        if country is not None:
            params["country"] = country
        if language is not None:
            params["language"] = language
        if currency is not None:
            params["currency"] = currency
        if device is not None:
            params["device"] = device
        if zip_code is not None:
            params["zip_code"] = zip_code
        if autoselect_variant is not None:
            params["autoselect_variant"] = autoselect_variant
        return await self._client._post("/api/v1/amazon/product", params)


class _AsyncWalmartNamespace:
    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def search(
        self,
        query: str,
        *,
        domain: Optional[str] = None,
        device: Optional[str] = None,
        sort_by: Optional[str] = None,
        start_page: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        fulfillment_speed: Optional[str] = None,
        fulfillment_type: Optional[str] = None,
        delivery_zip: Optional[str] = None,
        store_id: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"query": query}
        if domain is not None:
            params["domain"] = domain
        if device is not None:
            params["device"] = device
        if sort_by is not None:
            params["sort_by"] = sort_by
        if start_page is not None:
            params["start_page"] = start_page
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if fulfillment_speed is not None:
            params["fulfillment_speed"] = fulfillment_speed
        if fulfillment_type is not None:
            params["fulfillment_type"] = fulfillment_type
        if delivery_zip is not None:
            params["delivery_zip"] = delivery_zip
        if store_id is not None:
            params["store_id"] = store_id
        return await self._client._post("/api/v1/walmart/search", params)

    async def product(
        self,
        product_id: str,
        *,
        domain: Optional[str] = None,
        device: Optional[str] = None,
        delivery_zip: Optional[str] = None,
        store_id: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"product_id": product_id}
        if domain is not None:
            params["domain"] = domain
        if device is not None:
            params["device"] = device
        if delivery_zip is not None:
            params["delivery_zip"] = delivery_zip
        if store_id is not None:
            params["store_id"] = store_id
        return await self._client._post("/api/v1/walmart/product", params)


class _AsyncYouTubeNamespace:
    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def search(
        self,
        query: str,
        *,
        upload_date: Optional[str] = None,
        type: Optional[str] = None,
        duration: Optional[str] = None,
        sort_by: Optional[str] = None,
        hd: Optional[bool] = None,
        subtitles: Optional[bool] = None,
        creative_commons: Optional[bool] = None,
        live: Optional[bool] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"search": query}
        if upload_date is not None:
            params["upload_date"] = upload_date
        if type is not None:
            params["type"] = type
        if duration is not None:
            params["duration"] = duration
        if sort_by is not None:
            params["sort_by"] = sort_by
        if hd is not None:
            params["hd"] = hd
        if subtitles is not None:
            params["subtitles"] = subtitles
        if creative_commons is not None:
            params["creative_commons"] = creative_commons
        if live is not None:
            params["live"] = live
        return await self._client._post("/api/v1/youtube/search", params)

    async def metadata(self, video_id: str) -> dict[str, Any]:
        return await self._client._post(
            "/api/v1/youtube/metadata", {"video_id": video_id}
        )


class _AsyncRedditNamespace:
    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def search(
        self,
        query: str,
        *,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"query": query}
        if type is not None:
            params["type"] = type
        if sort is not None:
            params["sort"] = sort
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/reddit/search", params)

    async def post(self, url: str) -> dict[str, Any]:
        return await self._client._post("/api/v1/reddit/post", {"url": url})


class _AsyncTikTokNamespace:
    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def profile(
        self,
        *,
        username: Optional[str] = None,
        sec_user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if sec_user_id is not None:
            params["sec_user_id"] = sec_user_id
        return await self._client._post("/api/v1/tiktok/profile", params)

    async def user_posts(
        self,
        sec_user_id: str,
        *,
        cursor: Optional[str] = None,
        count: Optional[int] = None,
        sort_type: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"sec_user_id": sec_user_id}
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        if sort_type is not None:
            params["sort_type"] = sort_type
        return await self._client._post("/api/v1/tiktok/user/posts", params)

    async def video(self, video_id: str) -> dict[str, Any]:
        return await self._client._post(
            "/api/v1/tiktok/video", {"video_id": video_id}
        )

    async def video_comments(
        self,
        video_id: str,
        *,
        cursor: Optional[str] = None,
        count: Optional[int] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"video_id": video_id}
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        return await self._client._post("/api/v1/tiktok/video/comments", params)

    async def comment_replies(
        self,
        video_id: str,
        comment_id: str,
        *,
        cursor: Optional[str] = None,
        count: Optional[int] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "video_id": video_id,
            "comment_id": comment_id,
        }
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        return await self._client._post(
            "/api/v1/tiktok/video/comments/replies", params
        )

    async def search_videos(
        self,
        keyword: str,
        *,
        cursor: Optional[str] = None,
        count: Optional[int] = None,
        sort_type: Optional[str] = None,
        publish_time: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"keyword": keyword}
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        if sort_type is not None:
            params["sort_type"] = sort_type
        if publish_time is not None:
            params["publish_time"] = publish_time
        return await self._client._post("/api/v1/tiktok/search/videos", params)

    async def search_users(
        self,
        keyword: str,
        *,
        cursor: Optional[str] = None,
        count: Optional[int] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"keyword": keyword}
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        return await self._client._post("/api/v1/tiktok/search/users", params)

    async def hashtag(
        self,
        *,
        hashtag_name: Optional[str] = None,
        hashtag_id: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if hashtag_name is not None:
            params["hashtag_name"] = hashtag_name
        if hashtag_id is not None:
            params["hashtag_id"] = hashtag_id
        return await self._client._post("/api/v1/tiktok/hashtag", params)

    async def hashtag_videos(
        self,
        hashtag_id: str,
        *,
        cursor: Optional[str] = None,
        count: Optional[int] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"hashtag_id": hashtag_id}
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        return await self._client._post("/api/v1/tiktok/hashtag/videos", params)

    async def user_followers(
        self,
        sec_user_id: str,
        *,
        count: Optional[int] = None,
        page_token: Optional[str] = None,
        min_time: Optional[int] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"sec_user_id": sec_user_id}
        if count is not None:
            params["count"] = count
        if page_token is not None:
            params["page_token"] = page_token
        if min_time is not None:
            params["min_time"] = min_time
        return await self._client._post("/api/v1/tiktok/user/followers", params)

    async def user_followings(
        self,
        sec_user_id: str,
        *,
        count: Optional[int] = None,
        page_token: Optional[str] = None,
        min_time: Optional[int] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"sec_user_id": sec_user_id}
        if count is not None:
            params["count"] = count
        if page_token is not None:
            params["page_token"] = page_token
        if min_time is not None:
            params["min_time"] = min_time
        return await self._client._post("/api/v1/tiktok/user/followings", params)


class _AsyncInstagramNamespace:
    def __init__(self, client: AsyncScavioClient) -> None:
        self._client = client

    async def profile(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        return await self._client._post("/api/v1/instagram/profile", params)

    async def user_posts(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        if count is not None:
            params["count"] = count
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/user/posts", params)

    async def user_reels(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        if count is not None:
            params["count"] = count
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/user/reels", params)

    async def user_tagged(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        if count is not None:
            params["count"] = count
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/user/tagged", params)

    async def user_stories(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        return await self._client._post("/api/v1/instagram/user/stories", params)

    async def post(
        self,
        *,
        url: Optional[str] = None,
        media_id: Optional[str] = None,
        shortcode: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if url is not None:
            params["url"] = url
        if media_id is not None:
            params["media_id"] = media_id
        if shortcode is not None:
            params["shortcode"] = shortcode
        return await self._client._post("/api/v1/instagram/post", params)

    async def post_comments(
        self,
        *,
        shortcode: Optional[str] = None,
        url: Optional[str] = None,
        cursor: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if shortcode is not None:
            params["shortcode"] = shortcode
        if url is not None:
            params["url"] = url
        if cursor is not None:
            params["cursor"] = cursor
        if sort_order is not None:
            params["sort_order"] = sort_order
        return await self._client._post("/api/v1/instagram/post/comments", params)

    async def comment_replies(
        self,
        media_id: str,
        comment_id: str,
        *,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "media_id": media_id,
            "comment_id": comment_id,
        }
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post(
            "/api/v1/instagram/post/comments/replies", params
        )

    async def search_users(
        self,
        keyword: str,
        *,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"keyword": keyword}
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/search/users", params)

    async def search_hashtags(
        self,
        keyword: str,
        *,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"keyword": keyword}
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/search/hashtags", params)

    async def user_followers(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        if count is not None:
            params["count"] = count
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/user/followers", params)

    async def user_followings(
        self,
        *,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if user_id is not None:
            params["user_id"] = user_id
        if count is not None:
            params["count"] = count
        if cursor is not None:
            params["cursor"] = cursor
        return await self._client._post("/api/v1/instagram/user/followings", params)


class AsyncScavioClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._api_key = _resolve_api_key(api_key)
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._http_client: Optional[httpx.AsyncClient] = None

        self.google = _AsyncGoogleNamespace(self)
        self.amazon = _AsyncAmazonNamespace(self)
        self.walmart = _AsyncWalmartNamespace(self)
        self.youtube = _AsyncYouTubeNamespace(self)
        self.reddit = _AsyncRedditNamespace(self)
        self.tiktok = _AsyncTikTokNamespace(self)
        self.instagram = _AsyncInstagramNamespace(self)

    async def _post(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        return await async_request(
            "POST",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            http_client=self._http_client,
            json=params,
        )

    async def _get(self, path: str) -> dict[str, Any]:
        return await async_request(
            "GET",
            path,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout,
            http_client=self._http_client,
        )

    async def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Shortcut for :meth:`google.search` (Google SERP via /api/v2/google)."""
        return await self.google.search(query, **params)

    async def get_usage(self) -> dict[str, Any]:
        return await self._get("/api/v1/usage")

    async def __aenter__(self) -> AsyncScavioClient:
        self._http_client = httpx.AsyncClient()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def close(self) -> None:
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
