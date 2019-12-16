import pytest
from api.pretix.query import get_conference_tickets
from django.test import override_settings


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets_no_tickets(conference, requests_mock):
    requests_mock.get(
        "https://pretix/api/organizers/events/items", json={"results": []}
    )
    assert get_conference_tickets(conference, "en") == []


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets(conference, requests_mock, pretix_items):
    requests_mock.get("https://pretix/api/organizers/events/items", json=pretix_items)
    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 2

    ticket = tickets[0]

    assert ticket.name == "Regular ticket"
