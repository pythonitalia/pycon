from api.utils import get_ip


def test_get_ip(rf):
    request = rf.get("/", HTTP_X_FORWARDED_FOR="1.1.1.1")
    assert get_ip(request) == "1.1.1.1"


def test_get_ip_with_remote_addr(rf):
    request = rf.get("/", REMOTE_ADDR="2.2.2.2")
    assert get_ip(request) == "2.2.2.2"
