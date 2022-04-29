import pytest
from django.test import override_settings

from api.pretix.types import Option
from api.users.types import User

pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_tickets(
    user, conference_factory, requests_mock, pretix_user_tickets, pretix_categories
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

    assert len(ticket.item.questions) == 2
    assert ticket.item.questions[0].id == 2
    assert ticket.item.questions[0].name == "Food preferences"
    assert ticket.item.questions[0].required is True
    assert ticket.item.questions[0].options == [
        Option(id=1, name="Sushi"),
        Option(id=2, name="Fiorentina Meat"),
        Option(id=3, name="Thai"),
    ]
    assert ticket.item.questions[0].answer.answer == "Fiorentina Meat"
    assert ticket.item.questions[1].id == 4
    assert ticket.item.questions[1].name == "Intollerance"
    assert ticket.item.questions[1].required is True
    assert ticket.item.questions[1].answer.answer == "Cat"
