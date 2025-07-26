import pytest
from api.utils import get_ip, validate_url


def test_get_ip(rf):
    request = rf.get("/", HTTP_X_FORWARDED_FOR="1.1.1.1")
    assert get_ip(request) == "1.1.1.1"


def test_get_ip_with_remote_addr(rf):
    request = rf.get("/", REMOTE_ADDR="2.2.2.2")
    assert get_ip(request) == "2.2.2.2"


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.google.com", True),
        ("http://www.google.com", True),
        ("https://www.google.com/search?q=test", True),
        ("https://www.google.com/search?q=test", True),
        ("https://www.google.com/search?q=test", True),
        ("http://", False),
        ("https://", False),
    ],
)
def test_validate_url(url, expected):
    assert validate_url(url) == expected
