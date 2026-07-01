"""Shared helpers driving the exhaustive wire-mapping tests.

For every endpoint in the spec these build a full set of argument values and the
exact wire body they must serialize to, so a single table exercises every
parameter -> wire-field mapping (aliases, digit fields, None-dropping) across
both the sync and async clients.
"""

from __future__ import annotations

import re
from typing import Any

from scavio._spec import ENDPOINTS, Endpoint, Param

POST_KEYS = [key for key, ep in ENDPOINTS.items() if ep.http == "POST"]
GET_KEYS = [key for key, ep in ENDPOINTS.items() if ep.http == "GET"]


def value_for(param: Param) -> Any:
    """A representative, distinctive value for a parameter given its annotation."""
    annotation = param.annotation
    match = re.search(r'Literal\["([^"]+)"', annotation)
    if match:
        return match.group(1)
    if "bool" in annotation:
        return True
    if "int" in annotation:
        return 7
    return f"val_{param.name}"


def values_and_expected(ep: Endpoint) -> tuple[dict[str, Any], dict[str, Any]]:
    """All-params kwargs plus the wire body they must produce."""
    values: dict[str, Any] = {}
    expected: dict[str, Any] = {}
    for param in ep.params:
        val = value_for(param)
        values[param.name] = val
        expected[param.wire_field] = val
    return values, expected
