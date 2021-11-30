from datetime import datetime, timedelta
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
    requests_mock.get(
        "https://pretix/api/organizers/events/categories", json={"results": []}
    )
    requests_mock.get(
        "https://pretix/api/organizers/events/quotas", json={"results": []}
    )
    assert get_conference_tickets(conference, "en") == []


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets(
    conference,
    requests_mock,
    pretix_items,
    pretix_questions,
    pretix_categories,
    pretix_quotas,
):
    requests_mock.get("https://pretix/api/organizers/events/items", json=pretix_items)
    requests_mock.get(
        "https://pretix/api/organizers/events/questions", json=pretix_questions
    )
    requests_mock.get(
        "https://pretix/api/organizers/events/categories", json=pretix_categories
    )
    requests_mock.get("https://pretix/api/organizers/events/quotas", json=pretix_quotas)
    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 2

    ticket = tickets[0]

    assert ticket.name == "Regular ticket"
    assert ticket.quantity_left == 118
    assert ticket.questions[0].name == "Codice Fiscale"
    assert ticket.questions[1].name == "Food preferences"
    assert ticket.questions[1].options == [
        Option(id=4, name="No preferences"),
        Option(id=5, name="Vegetarian"),
        Option(id=6, name="Vegan"),
    ]

    assert tickets[1].quantity_left is None


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets_hides_when_available_from_is_future(
    conference,
    requests_mock,
    pretix_items,
    pretix_questions,
    pretix_categories,
    pretix_quotas,
):
    for item in pretix_items["results"]:
        item["available_from"] = (datetime.now() + timedelta(days=1)).isoformat()
        item["available_until"] = None

    requests_mock.get("https://pretix/api/organizers/events/items", json=pretix_items)
    requests_mock.get(
        "https://pretix/api/organizers/events/questions", json=pretix_questions
    )
    requests_mock.get(
        "https://pretix/api/organizers/events/categories", json=pretix_categories
    )
    requests_mock.get("https://pretix/api/organizers/events/quotas", json=pretix_quotas)
    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 0

@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets_hides_when_available_until_is_past(
    conference,
    requests_mock,
    pretix_items,
    pretix_questions,
    pretix_categories,
    pretix_quotas,
):
    for item in pretix_items["results"]:
        item["available_from"] = None
        item["available_until"] = (datetime.now() - timedelta(days=1)).isoformat()

    requests_mock.get("https://pretix/api/organizers/events/items", json=pretix_items)
    requests_mock.get(
        "https://pretix/api/organizers/events/questions", json=pretix_questions
    )
    requests_mock.get(
        "https://pretix/api/organizers/events/categories", json=pretix_categories
    )
    requests_mock.get("https://pretix/api/organizers/events/quotas", json=pretix_quotas)
    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 0
