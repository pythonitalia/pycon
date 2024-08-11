from conferences.tests.factories import ConferenceFactory
import pytest
from django.test import override_settings


pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_tickets(
    user,
    requests_mock,
    pretix_user_tickets,
    pretix_categories,
    pretix_questions,
    graphql_client,
):
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets/?attendee_email={user.email}",
        json=pretix_user_tickets,
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories/",
        json=pretix_categories,
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions/",
        json=pretix_questions,
    )

    graphql_client.force_login(user)
    response = graphql_client.query(
        """query($conference: String!) {
            me {
                tickets(conference: $conference, language: "en") {
                    id
                    attendeeName {
                        parts
                        scheme
                    }
                    attendeeEmail
                    item {
                        id
                        name
                        description
                        category
                        categoryInternalName
                        taxRate
                        active
                        defaultPrice
                        availableFrom
                        availableUntil
                        quantityLeft
                        questions {
                            id
                            name
                            required
                            options {
                                id
                                name
                            }
                            answer {
                                answer
                            }
                        }
                    }
                }
            }
        }""",
        variables={"conference": conference.code},
    )

    tickets = response["data"]["me"]["tickets"]

    assert len(tickets) == 1
    ticket = tickets[0]

    assert ticket["id"] == "2"
    assert ticket["attendeeName"] == {
        "parts": {
            "given_name": "Sheldon",
            "family_name": "Cooper",
        },
        "scheme": "given_family",
    }
    assert ticket["attendeeEmail"] == "sheldon@cooper.com"

    assert ticket["item"]["id"] == "1"
    assert ticket["item"]["name"] == "Regular ticket"
    assert ticket["item"]["description"] == "Regular ticket fare"
    assert ticket["item"]["category"] == "Tickets"
    assert ticket["item"]["categoryInternalName"] == "tickets"
    assert ticket["item"]["taxRate"] == 0.0
    assert ticket["item"]["active"] is True
    assert ticket["item"]["defaultPrice"] == "500.00"
    assert ticket["item"]["availableFrom"] is None
    assert ticket["item"]["availableUntil"] is None
    assert ticket["item"]["quantityLeft"] is None

    assert len(ticket["item"]["questions"]) == 3
    assert ticket["item"]["questions"][0]["id"] == "1"
    assert ticket["item"]["questions"][0]["name"] == "Vat number"
    assert ticket["item"]["questions"][0]["required"] is True
    assert ticket["item"]["questions"][0]["answer"] is None

    assert ticket["item"]["questions"][1]["id"] == "2"
    assert ticket["item"]["questions"][1]["name"] == "Food preferences"
    assert ticket["item"]["questions"][1]["required"] is True
    assert ticket["item"]["questions"][1]["options"] == [
        {"id": "4", "name": "No preferences"},
        {"id": "5", "name": "Vegetarian"},
        {"id": "6", "name": "Vegan"},
    ]
    assert ticket["item"]["questions"][1]["answer"]["answer"] == "No preferences"

    assert ticket["item"]["questions"][2]["id"] == "3"
    assert ticket["item"]["questions"][2]["name"] == "Intollerances / Allergies"
    assert ticket["item"]["questions"][2]["required"] is False
    assert ticket["item"]["questions"][2]["answer"]["answer"] == "Cat"


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_tickets_returns_all_tickets(
    user,
    requests_mock,
    pretix_user_tickets,
    pretix_user_non_admission_ticket,
    pretix_categories,
    pretix_questions,
    graphql_client,
):
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets/?attendee_email={user.email}",
        json=[
            pretix_user_tickets[0],
            pretix_user_non_admission_ticket,
        ],
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories/",
        json=pretix_categories,
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions/",
        json=pretix_questions,
    )

    graphql_client.force_login(user)
    response = graphql_client.query(
        """query($conference: String!) {
            me {
                tickets(conference: $conference, language: "en") {
                    id
                }
            }
        }""",
        variables={"conference": conference.code},
    )

    assert len(response["data"]["me"]["tickets"]) == 2

    ids = [int(ticket["id"]) for ticket in response["data"]["me"]["tickets"]]
    assert pretix_user_tickets[0]["id"] in ids
    assert pretix_user_non_admission_ticket["id"] in ids
