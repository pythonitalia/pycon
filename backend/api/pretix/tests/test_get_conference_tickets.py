from datetime import timedelta

import pytest
from django.test import override_settings
from django.utils import timezone

from api.pretix.query import get_conference_tickets
from api.pretix.types import Option


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_get_conference_tickets_no_tickets(conference, requests_mock):
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
        json={"results": []},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={"results": []},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/categories",
        json={"results": []},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/quotas",
        json={"results": []},
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
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
        json=pretix_items,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json=pretix_questions,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/categories",
        json=pretix_categories,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/quotas",
        json=pretix_quotas,
    )

    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 2
    ticket = tickets[0]
    assert ticket.id == 1
    assert ticket.language == "en"
    assert ticket.name == "Regular ticket"
    assert ticket.description == "Regular ticket fare"
    assert ticket.category == "Tickets"
    assert ticket.category_internal_name == "tickets"
    assert ticket.tax_rate == "0.00"
    assert ticket.active is True
    assert ticket.default_price == "500.00"
    assert ticket.available_from is None
    assert ticket.available_until is None
    assert ticket.quantity_left == 118

    assert ticket.questions[0].id == 1
    assert ticket.questions[0].name == "Vat number"
    assert ticket.questions[0].required is True
    assert ticket.questions[1].id == 2
    assert ticket.questions[1].name == "Food preferences"
    assert ticket.questions[1].required is True
    assert ticket.questions[1].options == [
        Option(id=4, name="No preferences"),
        Option(id=5, name="Vegetarian"),
        Option(id=6, name="Vegan"),
    ]

    assert tickets[1].variations[0].id == 1
    assert tickets[1].variations[0].value == "Small"
    assert tickets[1].variations[0].description == "slim fit"
    assert tickets[1].variations[0].active is True
    assert tickets[1].variations[0].default_price == "20.00"
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
        item["available_from"] = (timezone.now() + timedelta(days=1)).isoformat()
        item["available_until"] = None

    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
        json=pretix_items,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json=pretix_questions,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/categories",
        json=pretix_categories,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/quotas",
        json=pretix_quotas,
    )

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
        item["available_until"] = (timezone.now() - timedelta(days=1)).isoformat()

    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
        json=pretix_items,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json=pretix_questions,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/categories",
        json=pretix_categories,
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/quotas",
        json=pretix_quotas,
    )

    tickets = get_conference_tickets(conference, "en")

    assert len(tickets) == 0
