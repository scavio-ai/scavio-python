import pytest

from scavio._retry import parse_retry_after


@pytest.mark.parametrize("header", ["", "   ", "-1", "NaN", "Infinity", "1.5", "１"])
def test_parse_retry_after_rejects_invalid_delta_seconds(header):
    assert parse_retry_after(header) is None
