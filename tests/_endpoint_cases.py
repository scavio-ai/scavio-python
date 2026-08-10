"""Shared helpers driving the exhaustive wire-mapping tests.

For every endpoint in the spec these build a full set of argument values and the
exact wire body they must serialize to, so a single table exercises every
parameter -> wire-field mapping (aliases, digit fields, None-dropping) across
both the sync and async clients.
"""

from __future__ import annotations

import re
from typing import Any

from scavio._spec import ENDPOINTS, NAMESPACES, Endpoint, Param

# Core endpoints (namespace "_core", i.e. extract) are hand-written top-level
# methods, not namespace attributes, so the namespace-driven table skips them;
# they are covered by their own tests.
POST_KEYS = [
    key
    for key, ep in ENDPOINTS.items()
    if ep.http == "POST" and ep.namespace in NAMESPACES
]
GET_KEYS = [key for key, ep in ENDPOINTS.items() if ep.http == "GET"]


def value_for(param: Param) -> Any:
    """A representative, distinctive value for a parameter given its annotation.

    Order matters: ``Optional[list[int]]`` contains "int" and
    ``Optional[list[Literal[1, 2]]]`` contains "Literal", so the compound forms
    have to be recognised before the scalar fallbacks.
    """
    annotation = param.annotation
    str_literal = re.search(r'Literal\["([^"]+)"', annotation)
    if str_literal:
        return str_literal.group(1)
    int_literal = re.search(r"Literal\[(\d+)", annotation)
    if int_literal:
        value = int(int_literal.group(1))
        return [value] if "list[Literal[" in annotation else value
    if annotation.startswith("Optional[Union[str"):
        # Accepts a scalar, a list, or a comma-joined string; send the scalar.
        return f"val_{param.name}"
    if "list[str]" in annotation:
        return [f"val_{param.name}"]
    if "list[int]" in annotation:
        return [7]
    if "float" in annotation:
        return 19.99
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
