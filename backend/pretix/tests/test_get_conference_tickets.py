import pytest
from api.pretix.query import get_conference_tickets
from api.pretix.types import Option
from django.test import override_settings


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets_no_tickets(conference, requests_mock):
    requests_mock.get(
        "https://pretix/api/organizers/events/items", json={"results": []}
    )
    requests_mock.get(
        "https://pretix/api/organizers/events/questions", json={"results": []}
    )
    assert get_conference_tickets(conference, "en") == []


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets(
    conference, requests_mock, pretix_items, pretix_questions
):
    requests_mock.get("https://pretix/api/organizers/events/items", json=pretix_items)
    requests_mock.get(
        "https://pretix/api/organizers/events/questions", json=pretix_questions
    )
    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 2

    ticket = tickets[0]

    assert ticket.name == "Regular ticket"
    assert ticket.questions[0].name == "Codice Fiscale"
    assert ticket.questions[1].name == "Food preferences"
    assert ticket.questions[1].options == [
        Option(id=4, name="No preferences"),
        Option(id=5, name="Vegetarian"),
        Option(id=6, name="Vegan"),
    ]
