from conferences.tests.factories import ConferenceFactory
import pytest
from django.test import override_settings

from pretix import get_order


pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_gets_order(requests_mock):
    conference = ConferenceFactory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/ABC/",
        json={"code": "ABC"},
    )

    order = get_order(conference, "ABC")

    assert order["code"] == "ABC"


@override_settings(PRETIX_API="https://pretix/api/")
def test_return_none_when_404(requests_mock):
    conference = ConferenceFactory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/ABC/",
        status_code=404,
    )

    assert get_order(conference, "ABC") is None
