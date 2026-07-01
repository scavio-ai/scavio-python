from __future__ import annotations

import email.utils
import random
from dataclasses import dataclass, field
from typing import Optional

# Statuses that are safe to retry: rate limiting plus transient upstream errors.
DEFAULT_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class RetryConfig:
    """Policy for retrying transient failures with exponential backoff + jitter.

    Attributes:
        max_retries: Number of additional attempts after the first request.
            ``0`` disables retries entirely.
        base_delay: Base backoff in seconds; attempt ``n`` waits up to
            ``base_delay * 2**n`` (before jitter).
        max_delay: Upper bound (seconds) on any single backoff wait.
        retry_statuses: HTTP status codes that trigger a retry.
    """

    max_retries: int = 2
    base_delay: float = 0.5
    max_delay: float = 8.0
    retry_statuses: frozenset[int] = field(default=DEFAULT_RETRY_STATUSES)

    def should_retry_status(self, status_code: int, attempt: int) -> bool:
        return attempt < self.max_retries and status_code in self.retry_statuses

    def should_retry_exception(self, attempt: int) -> bool:
        return attempt < self.max_retries

    def backoff(self, attempt: int, retry_after: Optional[float] = None) -> float:
        """Seconds to sleep before the next attempt.

        Honors a ``Retry-After`` value when present; otherwise uses exponential
        backoff with full jitter (``random.uniform(0, capped_delay)``).
        """
        if retry_after is not None:
            return min(max(retry_after, 0.0), self.max_delay)
        capped = min(self.max_delay, self.base_delay * (2**attempt))
        return random.uniform(0.0, capped)


def parse_retry_after(header: Optional[str]) -> Optional[float]:
    """Parse a ``Retry-After`` header (delta-seconds or HTTP-date) to seconds."""
    if not header:
        return None
    header = header.strip()
    try:
        return float(header)
    except ValueError:
        pass
    try:
        parsed = email.utils.parsedate_to_datetime(header)
    except (TypeError, ValueError):
        return None
    if parsed is None:
        return None
    import datetime as _dt

    now = _dt.datetime.now(tz=parsed.tzinfo)
    return max((parsed - now).total_seconds(), 0.0)
