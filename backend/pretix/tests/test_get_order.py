import pytest
from django.test import override_settings
from pretix import get_order


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_gets_order(conference, requests_mock):
    requests_mock.get(
        f"https://pretix/api/organizers/events/orders/ABC/", json={"code": "ABC"}
    )

    order = get_order(conference, "ABC")

    assert order["code"] == "ABC"


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_return_none_when_404(conference, requests_mock):
    requests_mock.get(
        f"https://pretix/api/organizers/events/orders/ABC/", status_code=404
    )

    assert get_order(conference, "ABC") is None
