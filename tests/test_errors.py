"""Status-code -> exception mapping and error metadata."""

from __future__ import annotations

import pytest

from scavio import (
    BadRequestError,
    InsufficientCreditsError,
    InvalidAPIKeyError,
    NotFoundError,
    RateLimitError,
    ScavioAPIError,
    ScavioAPIStatusError,
)
from scavio._http import _handle_error


@pytest.mark.parametrize(
    "status,exc",
    [
        (400, BadRequestError),
        (401, InvalidAPIKeyError),
        (402, InsufficientCreditsError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, ScavioAPIError),
        (418, ScavioAPIError),
    ],
)
def test_status_maps_to_exception(status, exc):
    body = {"error": "boom"}
    with pytest.raises(exc) as info:
        _handle_error(status, body)
    err = info.value
    assert isinstance(err, ScavioAPIStatusError)
    assert err.status_code == status
    assert err.response_body == body


def test_nested_error_message_extracted():
    with pytest.raises(BadRequestError) as info:
        _handle_error(400, {"error": {"message": "nested"}})
    assert "nested" in str(info.value)


def test_scavio_api_error_positional_compat():
    err = ScavioAPIError(503, "upstream")
    assert err.status_code == 503
    assert "503" in str(err)
    assert "upstream" in str(err)


def test_specific_errors_carry_defaults():
    err = RateLimitError()
    assert "Rate limit" in str(err)
    assert err.status_code is None


def test_google_error_envelope_message_extracted():
    # Custom Search compatible endpoint errors use Google's envelope.
    body = {
        "error": {
            "code": 400,
            "message": "Image search is not supported.",
            "errors": [
                {
                    "message": "Image search is not supported.",
                    "domain": "global",
                    "reason": "invalid",
                }
            ],
            "status": "INVALID_ARGUMENT",
            "details": {"param": "searchType"},
        }
    }
    with pytest.raises(BadRequestError) as info:
        _handle_error(400, body)
    assert "Image search is not supported." in str(info.value)
    assert info.value.response_body == body
