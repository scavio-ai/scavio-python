#!/usr/bin/env python3
"""Generate the sync and async namespace classes from ``scavio/_spec.py``.

The generated modules (``scavio/_namespaces_sync.py`` and
``scavio/_namespaces_async.py``) contain one class per provider, each with fully
typed, individually documented methods. Because both files are emitted from the
same spec by the same template, the sync and async surfaces are guaranteed to
stay in lock-step (a property additionally enforced by tests/test_parity.py).

Usage:
    python scripts/gen_namespaces.py        # rewrite both generated modules
    python scripts/gen_namespaces.py --check # fail if they are out of date
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import textwrap
from pathlib import Path

_PKG_ROOT = Path(__file__).resolve().parent.parent


def _load_spec():
    """Import scavio/_spec.py in isolation.

    Loading the module by path (rather than ``import scavio._spec``) avoids
    triggering the package ``__init__``, which imports the very namespace
    modules this script generates.
    """
    spec_path = _PKG_ROOT / "scavio" / "_spec.py"
    module_spec = importlib.util.spec_from_file_location("_scavio_spec", spec_path)
    assert module_spec and module_spec.loader
    module = importlib.util.module_from_spec(module_spec)
    # Register before exec so dataclass processing can resolve cls.__module__.
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    return module


_spec = _load_spec()
NAMESPACES = _spec.NAMESPACES
Endpoint = _spec.Endpoint
endpoints_for = _spec.endpoints_for

# Human-facing class name and one-line description per namespace.
_NS_META = {
    "google": ("Google", "Google endpoints (SERP, Maps, Shopping, Flights, Hotels, News, Trends)."),
    "amazon": ("Amazon", "Amazon product search, product detail, and seller offer endpoints."),
    "walmart": ("Walmart", "Walmart product search and lookup endpoints."),
    "youtube": ("YouTube", "YouTube search, video, transcript, channel, comment, and streams endpoints."),
    "reddit": ("Reddit", "Reddit search, post, comment, subreddit, user, and trending endpoints."),
    "x": ("X", "X search, tweet, and user endpoints."),
    "tiktok": ("TikTok", "TikTok profile, video, transcript, hashtag, and search endpoints."),
    "instagram": ("Instagram", "Instagram profile, media, and search endpoints."),
    "linkedin": ("LinkedIn", "LinkedIn person, company, job, post, and search endpoints."),
    "tiktok_shop": (
        "TikTokShop",
        "TikTok Shop search, product, review, category, shop, and URL-resolution endpoints.",
    ),
    "threads": ("Threads", "Threads profile, post, comment, and people-search endpoints."),
    "kuaishou": (
        "Kuaishou",
        "Kuaishou (China) profile, video, comment, search, tag, and trending endpoints.",
    ),
    "ebay": ("Ebay", "eBay live and sold listing search, listing detail, and seller endpoints."),
    "target": ("Target", "Target search, category, product, and review endpoints."),
    "home_depot": ("HomeDepot", "Home Depot search, product, and review endpoints."),
    "zillow": ("Zillow", "Zillow listing search, property detail, and agent-review endpoints."),
    "booking": ("Booking", "Booking.com property search, hotel detail, and review endpoints."),
    "tripadvisor": (
        "Tripadvisor",
        "Tripadvisor location lookup, listing search, location detail, and review endpoints.",
    ),
    "indeed": ("Indeed", "Indeed job search, job detail, company, and company-review endpoints."),
    "airbnb": ("Airbnb", "Airbnb stay search, listing detail, and review endpoints."),
    "glassdoor": (
        "Glassdoor",
        "Glassdoor company lookup, employer profile, review, and salary endpoints.",
    ),
    "yelp": ("Yelp", "Yelp business search, business detail, and review endpoints."),
    "app_store": ("AppStore", "Apple App Store search, app detail, and review endpoints."),
    "google_play": ("GooglePlay", "Google Play search, app detail, and review endpoints."),
    "sec": (
        "SEC",
        "SEC EDGAR company lookup, filer profile, filings, XBRL facts, and full-text search.",
    ),
    "redfin": ("Redfin", "Redfin listing search, property detail, and market-stats endpoints."),
    "companies_house": (
        "CompaniesHouse",
        "UK Companies House register search, company, officer, and filing-history endpoints.",
    ),
    "g2": ("G2", "G2 software search, product profile, and review endpoints."),
    "capterra": ("Capterra", "Capterra software search, product profile, and review endpoints."),
    "google_ads": (
        "GoogleAds",
        "Google Ads Transparency advertiser lookup, ad search, and creative endpoints.",
    ),
    "meta_ads": (
        "MetaAds",
        "Meta Ad Library keyword search, advertiser ads, and single-ad endpoints.",
    ),
    "costco": (
        "Costco",
        "Costco search, product, warehouse price, stock, gas, coupon, deal, and clearance endpoints.",
    ),
    "trustpilot": (
        "Trustpilot",
        "Trustpilot business search, profile, review, and category endpoints.",
    ),
    "realtor": (
        "Realtor",
        "Realtor.com listing search, property, location, market, and agent endpoints.",
    ),
    "rightmove": (
        "Rightmove",
        "Rightmove UK property search, listing, sold price, and agent endpoints.",
    ),
    "mercadolibre": (
        "MercadoLibre",
        "Mercado Libre listing search, product, review, question, and best-seller endpoints.",
    ),
    "chatgpt": (
        "ChatGPT",
        "ChatGPT answers with cited sources, web searches and recommended products.",
    ),
    "gemini": (
        "Gemini",
        "Google Gemini answers with cited sources and recommended products.",
    ),
    "decathlon": (
        "Decathlon",
        "Decathlon sporting goods search and product detail across 7 country domains.",
    ),
    "specs": (
        "Specs",
        "Spec's search, product detail with every store's price, and store locator endpoints.",
    ),
    "lowes": (
        "Lowes",
        "Lowe's store-level search, product detail, store locator, and review endpoints.",
    ),
    "sams_club": (
        "SamsClub",
        "Sam's Club search, club-level product detail, club locator, Instant Savings, category, and review endpoints.",
    ),
    "canadian_tire": (
        "CanadianTire",
        "Canadian Tire store-level search, product, store locator, availability, clearance, and deal endpoints.",
    ),
    "dollar_general": (
        "DollarGeneral",
        "Dollar General store-level search, product, store locator with unit counts, deal, and coupon endpoints.",
    ),
    "heb": (
        "Heb",
        "HEB grocery search, product detail, and store locator endpoints, store-targetable.",
    ),
    "kroger": (
        "Kroger",
        "Kroger grocery search and product detail endpoints.",
    ),
}

_HEADER = '''# This file is auto-generated by scripts/gen_namespaces.py from scavio/_spec.py.
# Do NOT edit by hand: edit the spec and re-run `python scripts/gen_namespaces.py`.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union

if TYPE_CHECKING:
    from .{client_module} import {client_class}

'''


def _class_name(namespace: str, is_async: bool) -> str:
    base = _NS_META[namespace][0]
    return f"_Async{base}Namespace" if is_async else f"_{base}Namespace"


def _signature_lines(ep: Endpoint) -> list[str]:
    """Build the multi-line parameter list (one param per line, 8-space indent)."""
    lines = ["        self,"]
    for p in ep.required_params:
        lines.append(f"        {p.name}: {p.annotation},")
    for p in ep.positional_optional_params:
        lines.append(f"        {p.name}: {p.annotation} = None,")
    optional = ep.optional_params
    if optional:
        lines.append("        *,")
        for p in optional:
            lines.append(f"        {p.name}: {p.annotation} = None,")
    if ep.http != "GET":
        lines.append("        **extra: Any,")
    return lines


def _docstring_lines(ep: Endpoint) -> list[str]:
    out = [f'        """{ep.summary}', ""]
    if ep.http == "GET":
        out.append("        No API key required. Returns the API response as a dict.")
    elif ep.credits_note:
        # Body-priced surfaces (walmart, threads, kuaishou, extract): the real
        # cost is a function of the request body, so the flat line below would
        # be wrong by up to 40x. credits_note is a complete sentence.
        out.extend(
            f"        {line}"
            for line in textwrap.wrap(
                f"{ep.credits_note} Returns the API response as a dict.", width=88
            )
        )
    else:
        plural = "s" if ep.credits != 1 else ""
        out.append(
            f"        Costs {ep.credits} credit{plural}. Returns the API response as a dict."
        )
    if ep.params or ep.http != "GET":
        out.append("")
        out.append("        Args:")
        for p in ep.params:
            out.append(f"            {p.name}: {p.doc}")
        if ep.http != "GET":
            out.append(
                "            extra: Additional wire parameters passed through verbatim."
            )
    out.append('        """')
    return out


def _method_lines(ep: Endpoint, is_async: bool) -> list[str]:
    kw = "async def" if is_async else "def"
    lines = [f"    {kw} {ep.method}("]
    lines.extend(_signature_lines(ep))
    lines.append("    ) -> dict[str, Any]:")
    lines.extend(_docstring_lines(ep))

    values = "{" + ", ".join(f'"{p.name}": {p.name}' for p in ep.params) + "}"
    call = f'self._client._call("{ep.key}", {values}, extra)'
    if ep.http == "GET":
        call = f'self._client._call("{ep.key}", {{}}, {{}})'
    lines.append(f"        return {'await ' if is_async else ''}{call}")
    return lines


def _class_lines(namespace: str, is_async: bool) -> list[str]:
    name = _class_name(namespace, is_async)
    _, description = _NS_META[namespace]
    client_class = "AsyncScavioClient" if is_async else "ScavioClient"

    lines = [f"class {name}:", f'    """{description}"""', ""]
    lines.append(f'    def __init__(self, client: "{client_class}") -> None:')
    lines.append("        self._client = client")
    for ep in endpoints_for(namespace):
        lines.append("")
        lines.extend(_method_lines(ep, is_async))
    return lines


def render(is_async: bool) -> str:
    client_class = "AsyncScavioClient" if is_async else "ScavioClient"
    client_module = "_async_client" if is_async else "_client"
    parts = [_HEADER.format(client_module=client_module, client_class=client_class)]

    class_names = [_class_name(ns, is_async) for ns in NAMESPACES]
    parts.append("__all__ = [\n" + "".join(f'    "{c}",\n' for c in class_names) + "]\n")

    for ns in NAMESPACES:
        parts.append("\n" + "\n".join(_class_lines(ns, is_async)) + "\n")
    return "".join(parts)


def target_path(is_async: bool) -> Path:
    fname = "_namespaces_async.py" if is_async else "_namespaces_sync.py"
    return _PKG_ROOT / "scavio" / fname


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the generated files are stale instead of writing them.",
    )
    args = parser.parse_args()

    stale = False
    for is_async in (False, True):
        path = target_path(is_async)
        content = render(is_async)
        if args.check:
            current = path.read_text() if path.exists() else ""
            if current != content:
                stale = True
                print(f"stale: {path}")
        else:
            path.write_text(content)
            print(f"wrote: {path}")

    if args.check and stale:
        print("Generated namespace files are out of date. Run: python scripts/gen_namespaces.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
