import pytest
from django.test import override_settings

from api.pretix.types import Option
from api.users.types import User

pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_tickets(
    user,
    conference_factory,
    requests_mock,
    pretix_user_tickets,
    pretix_categories,
    pretix_questions,
):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets?attendee_email={user.email}",
        json=pretix_user_tickets,
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories",
        json=pretix_categories,
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions",
        json=pretix_questions,
    )
    user = User.resolve_reference(user.id, user.email)
    tickets = user.tickets(info=None, conference=conference.code, language="en")

    assert len(tickets) == 1
    ticket = tickets[0]

    assert ticket.id == 2
    assert ticket.name == "Sheldon Cooper"
    assert ticket.email == "sheldon@cooper.com"

    assert ticket.item.id == 1
    assert ticket.item.name == "Regular ticket"
    assert ticket.item.description == "Regular ticket fare"
    assert ticket.item.category == "Tickets"
    assert ticket.item.category_internal_name == "tickets"
    assert ticket.item.tax_rate == "0.00"
    assert ticket.item.active is True
    assert ticket.item.default_price == "500.00"
    assert ticket.item.available_from is None
    assert ticket.item.available_until is None
    assert ticket.item.quantity_left is None

    assert len(ticket.item.questions) == 3
    assert ticket.item.questions[0].id == 1
    assert ticket.item.questions[0].name == "Vat number"
    assert ticket.item.questions[0].required is True
    assert ticket.item.questions[0].answer is None

    assert ticket.item.questions[1].id == 2
    assert ticket.item.questions[1].name == "Food preferences"
    assert ticket.item.questions[1].required is True
    assert ticket.item.questions[1].options == [
        Option(id=4, name="No preferences"),
        Option(id=5, name="Vegetarian"),
        Option(id=6, name="Vegan"),
    ]
    assert ticket.item.questions[1].answer.answer == "No preferences"

    assert ticket.item.questions[2].id == 3
    assert ticket.item.questions[2].name == "Intollerances / Allergies"
    assert ticket.item.questions[2].required is False
    assert ticket.item.questions[2].answer.answer == "Cat"


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_tickets_returns_all_tickets(
    user,
    conference_factory,
    requests_mock,
    pretix_user_tickets,
    pretix_user_non_admission_ticket,
    pretix_categories,
    pretix_questions,
):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets?attendee_email={user.email}",
        json=[
            pretix_user_tickets[0],
            pretix_user_non_admission_ticket,
        ],
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories",
        json=pretix_categories,
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions",
        json=pretix_questions,
    )
    user = User.resolve_reference(user.id, user.email)
    tickets = user.tickets(info=None, conference=conference.code, language="en")

    assert len(tickets) == 2
