from conferences.tests.factories import ConferenceFactory
import pytest
from django.test import override_settings

from pretix import get_invoices

pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_gets_invoices(requests_mock):
    conference = ConferenceFactory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/invoices",
        json={"next": None, "results": []},
    )

    invoices = get_invoices(conference)

    assert list(invoices) == []
