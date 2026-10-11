"""Verify the signed completion webhooks sent for crawl and batch jobs."""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional, Union

SIGNATURE_HEADER = "Scavio-Signature"


def verify_webhook(
    secret: str,
    header: Optional[str],
    body: Union[str, bytes],
    tolerance: int = 300,
    *,
    now: Optional[float] = None,
) -> bool:
    """Return True when ``header`` is a valid Scavio signature for ``body``.

    Crawl and batch jobs started with a ``webhook_url`` POST their final status
    to it with the header ``Scavio-Signature: t=<unix seconds>,v1=<hex>``, where
    ``v1`` is the HMAC-SHA256 of ``"<t>.<raw body>"`` keyed with the job's
    ``webhook_secret`` (returned once, when the job is created).

    Args:
        secret: The ``webhook_secret`` from the crawl/batch creation response.
        header: The ``Scavio-Signature`` request header value.
        body: The RAW request body, exactly as received (bytes or str). Do not
            re-serialize parsed JSON: any whitespace change breaks the signature.
        tolerance: Maximum age (and clock skew) of the timestamp, in seconds.
        now: Override the current Unix time (for tests).

    Returns:
        False for a missing, malformed, stale or non-matching signature. The
        comparison is constant-time.
    """
    if not secret or not header or not isinstance(header, str):
        return False
    parts: dict[str, str] = {}
    for item in header.split(","):
        key, sep, value = item.partition("=")
        if sep:
            parts[key.strip()] = value.strip()
    signature = parts.get("v1")
    try:
        timestamp = int(parts.get("t", ""))
    except ValueError:
        return False
    if not signature:
        return False
    current = time.time() if now is None else now
    if abs(current - timestamp) > tolerance:
        return False
    raw = body.encode("utf-8") if isinstance(body, str) else bytes(body)
    expected = hmac.new(
        secret.encode("utf-8"), str(timestamp).encode("ascii") + b"." + raw, hashlib.sha256
    ).hexdigest()
    try:
        return hmac.compare_digest(expected, signature.lower())
    except TypeError:  # non-ASCII signature text
        return False
