from pycon.signing import require_signed_request


def _fake_view_function(request):
    pass


def test_require_signed_request_with_no_signature(rf):
    request = rf.get("/")

    return_value = require_signed_request(_fake_view_function)(request)

    assert return_value.status_code == 403
    assert return_value.content.decode() == "Missing signature."


def test_require_signed_request_fallbacks_to_sh(rf):
    request = rf.get("/?sh=123")

    return_value = require_signed_request(_fake_view_function)(request)

    assert return_value.status_code == 403
    assert return_value.content.decode() == "Invalid signature."


def test_require_signed_request_with_invalid_signature(rf):
    request = rf.get("/?sig=123")

    return_value = require_signed_request(_fake_view_function)(request)

    assert return_value.status_code == 403
    assert return_value.content.decode() == "Invalid signature."
