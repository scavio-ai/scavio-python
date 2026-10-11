"""The callable ``client.extract`` namespace: extract, map, crawl and batch.

``client.extract(url)`` has always been a top-level method. It is now a
callable namespace object, so that exact call keeps working unchanged (same
signature, same request on the wire) while the Extract family's multi-page
operations hang off it:

    client.extract(url)                  # one page, as before
    client.extract.map(url)              # a site's URLs
    client.extract.crawl(url)            # start a crawl job
    client.extract.crawl_status(job_id)  # progress + paged results
    client.extract.cancel_crawl(job_id)
    client.extract.batch(urls)           # start a batch job
    client.extract.batch_status(job_id)
    client.extract.cancel_batch(job_id)

Request bodies for map, crawl and batch are declared in ``_spec.py`` (keys
``extract_map``, ``extract_crawl``, ``extract_batch``) and built with
``build_body``, exactly like every generated namespace method; the signatures
below are pinned to those spec entries by tests/test_extract_web.py. This module
is hand-written (not generated) because it needs a callable object, path
parameters, query strings, DELETE and an ``Idempotency-Key`` header.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import TYPE_CHECKING, Any, Literal, Optional

from ._exceptions import ScavioError, ScavioJobTimeoutError
from ._params import build_body
from ._spec import ENDPOINTS

if TYPE_CHECKING:
    from ._async_client import AsyncScavioClient
    from ._client import ScavioClient

Format = Literal["html", "markdown", "text"]
Mode = Literal["normal", "advanced", "ultra"]
Sitemap = Literal["include", "only", "skip"]
ResultStatus = Literal["succeeded", "failed", "skipped"]

TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})
# Results per page when collecting a finished job for wait=True (the API max).
_COLLECT_PAGE_SIZE = 100

_EXTRACT_DOC = """Read any URL and return it as raw HTML, readability Markdown, or plain text.

        ``client.extract(url)`` is the single-page call it has always been; the
        same object also carries ``map``, ``crawl``, ``crawl_status``,
        ``cancel_crawl``, ``batch``, ``batch_status`` and ``cancel_batch``.
        Tier-priced by ``mode`` - 'normal' and 'advanced' cost 1 credit,
        'ultra' costs 2 - and only a successful extraction is billed, so a dead
        link, bot wall, or timeout costs nothing.

        Args:
            url: Page to read (1-2048 characters). http(s) only; a bare host is
                upgraded to https, and loopback, private, link-local, and
                metadata hosts are rejected with a 400.
            format: 'html' is the raw page, 'markdown' a readability extraction,
                'text' that markdown flattened to plain text. Server default
                'markdown'.
            mode: Tier, and the price-bearing parameter: 'normal' (1 credit),
                'advanced' for JavaScript-built pages (1 credit), 'ultra' for the
                hardest pages (2 credits). Server default 'normal'.

        Returns:
            ``{"url", "format", "mode", "content", "content_length"}``.
        """


def _job_path(job_type: str, job_id: str) -> str:
    if not job_id or not isinstance(job_id, str):
        raise ScavioError(f"{job_type} job id must be a non-empty string")
    return f"/api/v1/extract/{job_type}/{job_id}"


def _status_query(
    cursor: Optional[str],
    limit: Optional[int],
    status: Optional[str],
    include_content: Optional[bool],
) -> dict[str, str]:
    query: dict[str, str] = {}
    if cursor is not None:
        query["cursor"] = str(cursor)
    if limit is not None:
        query["limit"] = str(limit)
    if status is not None:
        query["status"] = status
    if include_content is not None:
        query["include_content"] = "true" if include_content else "false"
    return query


def _idempotency_header(key: Optional[str]) -> dict[str, str]:
    # A key is always sent: when the caller gives none, one is generated per
    # call, so the SDK's automatic retry of a timed-out or 5xx'd POST returns the
    # job the first attempt created instead of starting a second, billed one.
    return {"Idempotency-Key": key if key is not None else str(uuid.uuid4())}


def _collected(
    final: dict[str, Any], results: list[Any], created: dict[str, Any]
) -> dict[str, Any]:
    data = dict(final.get("data") or {})
    data["results"] = results
    data["next_cursor"] = None
    return {"data": data, "created": created.get("data", created)}


def _created_id(created: dict[str, Any], job_type: str) -> str:
    job_id = (created.get("data") or {}).get("id")
    if not job_id:
        raise ScavioError(f"{job_type} response carried no job id: {created!r}")
    return str(job_id)


class ExtractNamespace:
    """``client.extract``: call it for one page, or use its map/crawl/batch methods."""

    def __init__(self, client: "ScavioClient") -> None:
        self._client = client

    def __call__(
        self,
        url: str,
        *,
        format: Optional[Format] = None,
        mode: Optional[Mode] = None,
    ) -> dict[str, Any]:
        return self._client._call("extract", {"url": url, "format": format, "mode": mode}, {})

    __call__.__doc__ = _EXTRACT_DOC

    # -- map ---------------------------------------------------------------

    def map(
        self,
        url: str,
        *,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        sitemap: Optional[Sitemap] = None,
        include_subdomains: Optional[bool] = None,
        include_paths: Optional[list[str]] = None,
        exclude_paths: Optional[list[str]] = None,
        ignore_query_parameters: Optional[bool] = None,
        mode: Optional[Mode] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """List a site's page URLs from its sitemaps and start page.

        Synchronous: returns ``{"data": {"url", "links": [{"url", "source",
        "lastmod"?}], "total_found", "returned", "truncated", "sitemaps_read"},
        "credits_used", ...}``. Pages disallowed by robots.txt are left out.
        1 credit on the normal tier (up to 2 on 'advanced', up to 10 on 'ultra').
        See ``_spec.ENDPOINTS["extract_map"]`` for every argument.
        """
        values = {
            "url": url,
            "search": search,
            "limit": limit,
            "sitemap": sitemap,
            "include_subdomains": include_subdomains,
            "include_paths": include_paths,
            "exclude_paths": exclude_paths,
            "ignore_query_parameters": ignore_query_parameters,
            "mode": mode,
        }
        return self._client._call("extract_map", values, extra)

    # -- crawl -------------------------------------------------------------

    def crawl(
        self,
        url: str,
        *,
        max_pages: Optional[int] = None,
        max_depth: Optional[int] = None,
        include_paths: Optional[list[str]] = None,
        exclude_paths: Optional[list[str]] = None,
        allow_subdomains: Optional[bool] = None,
        ignore_query_parameters: Optional[bool] = None,
        sitemap: Optional[Sitemap] = None,
        format: Optional[Format] = None,
        mode: Optional[Mode] = None,
        webhook_url: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        wait: bool = False,
        poll_interval: float = 2.0,
        wait_timeout: Optional[float] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Start a crawl of one site; optionally wait for it and collect every page.

        Without ``wait`` this returns the queued job at once: ``{"data": {"id",
        "status", "status_url", "credits_per_page", "webhook_secret"?, ...},
        "credits_used": 0}``. Poll it with :meth:`crawl_status`.

        With ``wait=True`` it polls every ``poll_interval`` seconds until the job
        is completed, failed or cancelled, then pages through every result and
        returns ``{"data": {...final status..., "results": [every page],
        "next_cursor": None}, "created": {...the queued-job payload, including
        webhook_secret when a webhook_url was given...}}``. If ``wait_timeout``
        seconds pass first, :class:`ScavioJobTimeoutError` is raised carrying
        ``job_id``; the job keeps running.

        Billed per SUCCESSFUL page at extract's price for the tier: 'normal' and
        'advanced' 1 credit, 'ultra' 2. Failed and skipped pages are free.
        robots.txt is always obeyed. Results are kept 3 days.

        Args:
            idempotency_key: Sent as ``Idempotency-Key``; repeating a crawl with
                the same key within 24 hours returns the original job. When
                omitted, a fresh key is generated per call so automatic retries
                never start a duplicate job.
            wait: Poll until the job finishes and return every result.
            poll_interval: Seconds between status polls when waiting.
            wait_timeout: Give up waiting after this many seconds (None = no limit).

        See ``_spec.ENDPOINTS["extract_crawl"]`` for every body argument.
        """
        values = {
            "url": url,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "include_paths": include_paths,
            "exclude_paths": exclude_paths,
            "allow_subdomains": allow_subdomains,
            "ignore_query_parameters": ignore_query_parameters,
            "sitemap": sitemap,
            "format": format,
            "mode": mode,
            "webhook_url": webhook_url,
        }
        return self._start("crawl", "extract_crawl", values, extra, idempotency_key,
                           wait, poll_interval, wait_timeout)

    def crawl_status(
        self,
        job_id: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        status: Optional[ResultStatus] = None,
        include_content: Optional[bool] = None,
    ) -> dict[str, Any]:
        """A crawl's progress and one page of its results. Free.

        Returns ``{"data": {"id", "status", "stopped_reason", "pages":
        {"discovered", "queued", "succeeded", "failed", "skipped"},
        "credits_used", "expires_at", "results": [...], "next_cursor"}}``.

        Args:
            job_id: The crawl id returned by :meth:`crawl`.
            cursor: ``next_cursor`` from the previous response.
            limit: Results per response, 1-100 (server default 25).
            status: Only results with this status.
            include_content: False pages through results without their content
                (server default True).
        """
        return self._client._send(
            "GET", _job_path("crawl", job_id),
            params=_status_query(cursor, limit, status, include_content),
        )

    def cancel_crawl(self, job_id: str) -> dict[str, Any]:
        """Stop a queued or running crawl. Free; results so far stay available.

        Raises a 409 :class:`ScavioAPIError` if the crawl has already finished.
        """
        return self._client._send("DELETE", _job_path("crawl", job_id))

    # -- batch -------------------------------------------------------------

    def batch(
        self,
        urls: list[str],
        *,
        format: Optional[Format] = None,
        mode: Optional[Mode] = None,
        webhook_url: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        wait: bool = False,
        poll_interval: float = 2.0,
        wait_timeout: Optional[float] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Extract a list of URLs in one job; optionally wait and collect every page.

        Returns the queued job (``id``, ``status``, ``status_url``,
        ``urls_count``, ``invalid_urls``, ``credits_per_page``,
        ``webhook_secret``?) or, with ``wait=True``, every result in input order
        (same shape and timeout behavior as :meth:`crawl`). Billed per
        SUCCESSFUL page at extract's price for the tier ('normal'/'advanced' 1,
        'ultra' 2); failed pages and invalid URLs are free.
        See ``_spec.ENDPOINTS["extract_batch"]`` for every body argument.
        """
        values = {"urls": urls, "format": format, "mode": mode, "webhook_url": webhook_url}
        return self._start("batch", "extract_batch", values, extra, idempotency_key,
                           wait, poll_interval, wait_timeout)

    def batch_status(
        self,
        job_id: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        status: Optional[ResultStatus] = None,
        include_content: Optional[bool] = None,
    ) -> dict[str, Any]:
        """A batch's progress and one page of its results, in input order. Free.

        Same arguments and response shape as :meth:`crawl_status`.
        """
        return self._client._send(
            "GET", _job_path("batch", job_id),
            params=_status_query(cursor, limit, status, include_content),
        )

    def cancel_batch(self, job_id: str) -> dict[str, Any]:
        """Stop a queued or running batch. Free; results so far stay available.

        Raises a 409 :class:`ScavioAPIError` if the batch has already finished.
        """
        return self._client._send("DELETE", _job_path("batch", job_id))

    # -- internals -----------------------------------------------------------

    def _start(
        self,
        job_type: str,
        key: str,
        values: dict[str, Any],
        extra: dict[str, Any],
        idempotency_key: Optional[str],
        wait: bool,
        poll_interval: float,
        wait_timeout: Optional[float],
    ) -> dict[str, Any]:
        endpoint = ENDPOINTS[key]
        created = self._client._send(
            "POST", endpoint.path,
            json=build_body(endpoint, values, extra),
            headers=_idempotency_header(idempotency_key),
        )
        if not wait:
            return created
        return self._wait(job_type, _created_id(created, job_type), created,
                          poll_interval, wait_timeout)

    def _wait(
        self,
        job_type: str,
        job_id: str,
        created: dict[str, Any],
        poll_interval: float,
        wait_timeout: Optional[float],
    ) -> dict[str, Any]:
        path = _job_path(job_type, job_id)
        deadline = None if wait_timeout is None else time.monotonic() + wait_timeout
        last: Optional[dict[str, Any]] = None
        while True:
            last = self._client._send(
                "GET", path, params=_status_query(None, 1, None, False)
            )
            if (last.get("data") or {}).get("status") in TERMINAL_STATUSES:
                break
            if deadline is not None and time.monotonic() + poll_interval > deadline:
                raise ScavioJobTimeoutError(job_id, job_type, last)
            time.sleep(poll_interval)

        results: list[Any] = []
        cursor: Optional[str] = None
        final = last
        while True:
            page = self._client._send(
                "GET", path, params=_status_query(cursor, _COLLECT_PAGE_SIZE, None, None)
            )
            final = page
            data = page.get("data") or {}
            results.extend(data.get("results") or [])
            cursor = data.get("next_cursor")
            if not cursor:
                break
        return _collected(final, results, created)


class AsyncExtractNamespace:
    """``client.extract`` on the async client: same surface, every call awaitable."""

    def __init__(self, client: "AsyncScavioClient") -> None:
        self._client = client

    async def __call__(
        self,
        url: str,
        *,
        format: Optional[Format] = None,
        mode: Optional[Mode] = None,
    ) -> dict[str, Any]:
        return await self._client._call(
            "extract", {"url": url, "format": format, "mode": mode}, {}
        )

    __call__.__doc__ = _EXTRACT_DOC

    async def map(
        self,
        url: str,
        *,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        sitemap: Optional[Sitemap] = None,
        include_subdomains: Optional[bool] = None,
        include_paths: Optional[list[str]] = None,
        exclude_paths: Optional[list[str]] = None,
        ignore_query_parameters: Optional[bool] = None,
        mode: Optional[Mode] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.map`."""
        values = {
            "url": url,
            "search": search,
            "limit": limit,
            "sitemap": sitemap,
            "include_subdomains": include_subdomains,
            "include_paths": include_paths,
            "exclude_paths": exclude_paths,
            "ignore_query_parameters": ignore_query_parameters,
            "mode": mode,
        }
        return await self._client._call("extract_map", values, extra)

    async def crawl(
        self,
        url: str,
        *,
        max_pages: Optional[int] = None,
        max_depth: Optional[int] = None,
        include_paths: Optional[list[str]] = None,
        exclude_paths: Optional[list[str]] = None,
        allow_subdomains: Optional[bool] = None,
        ignore_query_parameters: Optional[bool] = None,
        sitemap: Optional[Sitemap] = None,
        format: Optional[Format] = None,
        mode: Optional[Mode] = None,
        webhook_url: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        wait: bool = False,
        poll_interval: float = 2.0,
        wait_timeout: Optional[float] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.crawl`."""
        values = {
            "url": url,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "include_paths": include_paths,
            "exclude_paths": exclude_paths,
            "allow_subdomains": allow_subdomains,
            "ignore_query_parameters": ignore_query_parameters,
            "sitemap": sitemap,
            "format": format,
            "mode": mode,
            "webhook_url": webhook_url,
        }
        return await self._start("crawl", "extract_crawl", values, extra, idempotency_key,
                                 wait, poll_interval, wait_timeout)

    async def crawl_status(
        self,
        job_id: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        status: Optional[ResultStatus] = None,
        include_content: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.crawl_status`."""
        return await self._client._send(
            "GET", _job_path("crawl", job_id),
            params=_status_query(cursor, limit, status, include_content),
        )

    async def cancel_crawl(self, job_id: str) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.cancel_crawl`."""
        return await self._client._send("DELETE", _job_path("crawl", job_id))

    async def batch(
        self,
        urls: list[str],
        *,
        format: Optional[Format] = None,
        mode: Optional[Mode] = None,
        webhook_url: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        wait: bool = False,
        poll_interval: float = 2.0,
        wait_timeout: Optional[float] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.batch`."""
        values = {"urls": urls, "format": format, "mode": mode, "webhook_url": webhook_url}
        return await self._start("batch", "extract_batch", values, extra, idempotency_key,
                                 wait, poll_interval, wait_timeout)

    async def batch_status(
        self,
        job_id: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        status: Optional[ResultStatus] = None,
        include_content: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.batch_status`."""
        return await self._client._send(
            "GET", _job_path("batch", job_id),
            params=_status_query(cursor, limit, status, include_content),
        )

    async def cancel_batch(self, job_id: str) -> dict[str, Any]:
        """Async :meth:`ExtractNamespace.cancel_batch`."""
        return await self._client._send("DELETE", _job_path("batch", job_id))

    async def _start(
        self,
        job_type: str,
        key: str,
        values: dict[str, Any],
        extra: dict[str, Any],
        idempotency_key: Optional[str],
        wait: bool,
        poll_interval: float,
        wait_timeout: Optional[float],
    ) -> dict[str, Any]:
        endpoint = ENDPOINTS[key]
        created = await self._client._send(
            "POST", endpoint.path,
            json=build_body(endpoint, values, extra),
            headers=_idempotency_header(idempotency_key),
        )
        if not wait:
            return created
        return await self._wait(job_type, _created_id(created, job_type), created,
                                poll_interval, wait_timeout)

    async def _wait(
        self,
        job_type: str,
        job_id: str,
        created: dict[str, Any],
        poll_interval: float,
        wait_timeout: Optional[float],
    ) -> dict[str, Any]:
        path = _job_path(job_type, job_id)
        deadline = None if wait_timeout is None else time.monotonic() + wait_timeout
        last: Optional[dict[str, Any]] = None
        while True:
            last = await self._client._send(
                "GET", path, params=_status_query(None, 1, None, False)
            )
            if (last.get("data") or {}).get("status") in TERMINAL_STATUSES:
                break
            if deadline is not None and time.monotonic() + poll_interval > deadline:
                raise ScavioJobTimeoutError(job_id, job_type, last)
            await asyncio.sleep(poll_interval)

        results: list[Any] = []
        cursor: Optional[str] = None
        final = last
        while True:
            page = await self._client._send(
                "GET", path, params=_status_query(cursor, _COLLECT_PAGE_SIZE, None, None)
            )
            final = page
            data = page.get("data") or {}
            results.extend(data.get("results") or [])
            cursor = data.get("next_cursor")
            if not cursor:
                break
        return _collected(final, results, created)
