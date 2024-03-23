from pycon.middleware import (
    force_pycon_host,
)


def test_force_host_middleware(rf):
    request = rf.get("/")

    def check_request(r):
        assert request.headers["X-Forwarded-Proto"] == "https"
        assert request.headers["Host"] == "pycon.it"

    middleware = force_pycon_host(check_request)
    middleware(request)
