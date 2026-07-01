"""Guarantee the sync and async surfaces stay identical and cover the spec."""

from __future__ import annotations

import inspect

import pytest

from scavio import AsyncScavioClient, ScavioClient
from scavio._spec import NAMESPACES, endpoints_for


@pytest.fixture(scope="module")
def clients():
    return ScavioClient(api_key="sk_test"), AsyncScavioClient(api_key="sk_test")


def _named_params(sig: inspect.Signature) -> list[str]:
    return [
        name
        for name, p in sig.parameters.items()
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    ]


def test_every_namespace_and_method_exists(clients):
    sync_client, async_client = clients
    for ns in NAMESPACES:
        assert hasattr(sync_client, ns), ns
        assert hasattr(async_client, ns), ns
        for ep in endpoints_for(ns):
            assert hasattr(getattr(sync_client, ns), ep.method), ep.key
            assert hasattr(getattr(async_client, ns), ep.method), ep.key


def test_sync_async_signatures_match(clients):
    sync_client, async_client = clients
    for ns in NAMESPACES:
        for ep in endpoints_for(ns):
            sync_sig = inspect.signature(getattr(getattr(sync_client, ns), ep.method))
            async_sig = inspect.signature(getattr(getattr(async_client, ns), ep.method))
            assert list(sync_sig.parameters) == list(async_sig.parameters), ep.key
            for name, param in sync_sig.parameters.items():
                other = async_sig.parameters[name]
                assert param.annotation == other.annotation, (ep.key, name)
                assert param.default == other.default, (ep.key, name)
                assert param.kind == other.kind, (ep.key, name)


def test_signatures_cover_spec_exactly(clients):
    sync_client, _ = clients
    for ns in NAMESPACES:
        for ep in endpoints_for(ns):
            sig = inspect.signature(getattr(getattr(sync_client, ns), ep.method))
            assert _named_params(sig) == [p.name for p in ep.params], ep.key


def test_async_methods_are_coroutines(clients):
    _, async_client = clients
    for ns in NAMESPACES:
        for ep in endpoints_for(ns):
            method = getattr(getattr(async_client, ns), ep.method)
            assert inspect.iscoroutinefunction(method), ep.key
