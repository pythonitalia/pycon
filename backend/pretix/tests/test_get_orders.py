import pytest
from django.test import override_settings

from pretix import get_invoices


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_gets_invoices(conference, requests_mock):
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/invoices",
        json={"next": None, "results": []},
    )

    invoices = get_invoices(conference)

    assert list(invoices) == []
