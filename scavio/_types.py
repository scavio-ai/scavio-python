from __future__ import annotations

from typing import TypedDict


class AutoRecharge(TypedDict, total=False):
    """Auto-recharge configuration returned inside :class:`UsageResponse`."""

    enabled: bool
    threshold: int
    amount: int
    cost: int


class UsageResponse(TypedDict, total=False):
    """Shape of the ``get_usage()`` response.

    Returned as a plain ``dict`` at runtime; this ``TypedDict`` exists purely to
    give editors and type-checkers field completion.
    """

    plan: str
    credit_balance: int
    purchased_credits: int
    searches_used: int
    period_start: str
    auto_recharge: AutoRecharge
