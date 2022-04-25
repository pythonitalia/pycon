import pytest
from django.test import override_settings

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

    assert tickets[0] is False
