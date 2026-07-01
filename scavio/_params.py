from __future__ import annotations

from typing import Any, Mapping

from ._exceptions import ScavioError
from ._spec import Endpoint


def build_body(
    endpoint: Endpoint,
    values: Mapping[str, Any],
    extra: Mapping[str, Any],
) -> dict[str, Any]:
    """Assemble the wire request body for an endpoint.

    - Validates any "one-of-required" parameter groups.
    - Maps Python argument names to their wire field names (e.g. ``asin`` ->
      ``query``, ``four_k`` -> ``4k``).
    - Drops arguments whose value is ``None`` so unset params are never sent.
    - Merges ``**extra`` verbatim (forward-compat passthrough), raising on a
      collision with an already-set wire field.
    """
    _validate_one_of(endpoint, values)

    wire_map = {p.name: p.wire_field for p in endpoint.params}
    body: dict[str, Any] = {}
    for name, value in values.items():
        if value is None:
            continue
        body[wire_map.get(name, name)] = value

    for key, value in extra.items():
        if key in body:
            raise TypeError(
                f"{endpoint.method}(): '{key}' was passed both as a typed "
                "argument and in **extra"
            )
        if value is not None:
            body[key] = value

    return body


def _validate_one_of(endpoint: Endpoint, values: Mapping[str, Any]) -> None:
    for group in endpoint.one_of:
        if not any(values.get(name) is not None for name in group):
            raise ScavioError(
                f"{endpoint.method}() requires one of: " + " or ".join(group)
            )
