from pytest import mark

from pretix import user_has_admission_ticket

pytestmark = mark.django_db


@mark.parametrize("has_ticket", [True, False])
def test_user_has_admission_ticket(
    settings, has_ticket, conference_factory, requests_mock
):
    settings.PRETIX_API = "http://localhost:9090/"
    conference = conference_factory()

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    assert (
        user_has_admission_ticket(
            email="nina@fake-work-email.ca",
            event_organizer=conference.pretix_organizer_id,
            event_slug=conference.pretix_event_id,
        )
        is has_ticket
    )

    assert requests_mock.last_request.json() == {
        "attendee_email": "nina@fake-work-email.ca",
        "events": [
            {
                "organizer_slug": conference.pretix_organizer_id,
                "event_slug": conference.pretix_event_id,
            }
        ],
    }
