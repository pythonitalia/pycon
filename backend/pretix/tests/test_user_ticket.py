from django.test import override_settings

from pretix import get_user_ticket


@override_settings(PRETIX_API="https://pretix/api/")
def test_user_ticket(requests_mock, user, conference_factory, pretix_user_tickets):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = user.email.upper()

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets?attendee_email={user.email}",
        json=pretix_user_tickets,
    )

    ticket = get_user_ticket(conference, user.email, pretix_user_tickets[0]["id"])

    assert ticket
    assert ticket["id"] == pretix_user_tickets[0]["id"]
    assert (
        ticket["attendee_name"].lower()
        == pretix_user_tickets[0]["attendee_name"].lower()
    )
    assert ticket["attendee_email"] == pretix_user_tickets[0]["attendee_email"]
