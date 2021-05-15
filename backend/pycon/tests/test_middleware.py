from pytest import raises
from pythonit_toolkit.headers import PASTAPORTO_X_HEADER
from pythonit_toolkit.pastaporto.test import fake_pastaporto_token_for_user

from pycon.middleware import (
    CustomAuthenticationMiddleware,
    force_pycon_host,
    pastaporto_auth,
)


def test_force_host_middleware(rf):
    request = rf.get("/")

    def check_request(r):
        assert request.META["HTTP_X_FORWARDED_PROTO"] == "https"
        assert request.META["HTTP_HOST"] == "pycon.it"

    middleware = force_pycon_host(check_request)
    middleware(request)


def test_skip_auth_if_graphql(rf):
    request = rf.get("/graphql")
    request.session = {}

    CustomAuthenticationMiddleware(lambda: None).process_request(request)
    with raises(AttributeError):
        getattr(request, "user")


def test_auth_is_included_if_not_graphql(rf):
    request = rf.get("/")
    request.session = {}

    CustomAuthenticationMiddleware(lambda: None).process_request(request)
    assert request.user


def test_pastaporto_auth_with_token(rf, settings):
    settings.PASTAPORTO_SECRET = "abc"
    token = fake_pastaporto_token_for_user(
        {"id": 1, "email": "test@user.it"},
        "abc",
        staff=True,
    )

    request = rf.get("/graphql", **{f"HTTP_{PASTAPORTO_X_HEADER}": token})

    def check(_):
        assert request.pastaporto.is_authenticated is True
        assert request.pastaporto.user_info is not None
        assert request.pastaporto.user_info.id == 1
        assert request.pastaporto.user_info.email == "test@user.it"

    middleware = pastaporto_auth(check)
    middleware(request)


def test_pastaporto_auth_without_token(rf):
    request = rf.get("/graphql")

    def check(_):
        assert request.pastaporto.is_authenticated is False

    middleware = pastaporto_auth(check)
    middleware(request)
