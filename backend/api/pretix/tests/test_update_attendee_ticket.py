from conferences.tests.factories import ConferenceFactory
import pytest
from django.test import override_settings

pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_cannot_update_ticket_if_i_am_not_the_owner(
    graphql_client, requests_mock, user, pretix_user_tickets
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = "not@my.com"

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets/?attendee_email={user.email}",
        json=pretix_user_tickets,
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            ... on AttendeeTicket {
                id
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": pretix_user_tickets[0]["id"],
                "attendeeName": {
                    "parts": {
                        "given_name": "Ester",
                        "family_name": "Bell",
                    },
                    "scheme": "given_family",
                },
                "attendeeEmail": "ester@pycon.it",
            },
        },
    )

    assert (
        response["errors"][0]["message"] == "You are not allowed to update this ticket."
    )


@override_settings(PRETIX_API="https://pretix/api/")
def test_invalid_data(graphql_client, mocker, requests_mock, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")
    mocker.patch("pretix.is_ticket_owner", return_value=True)

    requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        status_code=404,
        json={
            "attendee_email": ["Enter a valid email address."],
            "answers": [
                {"options": ['Invalid pk "344" - object does not exist.']},
                {},
                {"answer": ["This field may not be blank."]},
                {"answer": ["This field may not be blank."]},
            ],
        },
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            ... on UpdateAttendeeTicketErrors {
                errors {
                    attendeeEmail
                    attendeeName {
                        givenName
                        familyName
                        nonFieldErrors
                    }
                    answers {
                        answer
                        options
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": "999",
                "attendeeName": {
                    "parts": {
                        "given_name": "A",
                        "family_name": "B",
                    },
                    "scheme": "given_family",
                },
                "attendeeEmail": " foo@",
                "answers": [
                    {"answer": "No preferences", "question": "31", "options": ["344"]},
                    {"answer": "Vegan", "question": "32"},
                    {"answer": "", "question": "44"},
                    {"answer": "", "question": "43"},
                ],
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["errors"]["attendeeEmail"] == [
        "Enter a valid email address."
    ]
    errors_answers = response["data"]["updateAttendeeTicket"]["errors"]["answers"]
    assert errors_answers[0]["options"] == ['Invalid pk "344" - object does not exist.']
    assert errors_answers[1]["answer"] == []
    assert errors_answers[2]["answer"] == ["This field may not be blank."]
    assert errors_answers[3]["answer"] == ["This field may not be blank."]


@override_settings(PRETIX_API="https://pretix/api/")
def test_validate_empty_name(graphql_client, mocker, requests_mock, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")
    mocker.patch("pretix.is_ticket_owner", return_value=True)

    requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        status_code=200,
        json={},
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            ... on UpdateAttendeeTicketErrors {
                errors {
                    attendeeEmail
                    attendeeName {
                        givenName
                        familyName
                        nonFieldErrors
                    }
                    answers {
                        answer
                        options
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": "999",
                "attendeeName": {
                    "parts": {
                        "given_name": "",
                        "family_name": "Bell",
                    },
                    "scheme": "given_family",
                },
                "attendeeEmail": " foo@",
                "answers": [
                    {"answer": "No preferences", "question": "31", "options": ["344"]},
                    {"answer": "Vegan", "question": "32"},
                    {"answer": "", "question": "44"},
                    {"answer": "", "question": "43"},
                ],
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["errors"]["attendeeName"][
        "givenName"
    ] == ["This field may not be blank."]
    assert (
        response["data"]["updateAttendeeTicket"]["errors"]["attendeeName"]["familyName"]
        == []
    )


@override_settings(PRETIX_API="https://pretix/api/")
def test_update_ticket_with_answers(
    graphql_client,
    mocker,
    requests_mock,
    user,
    pretix_user_tickets,
    update_user_ticket,
    pretix_categories,
    pretix_questions,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")
    mocker.patch("pretix.is_ticket_owner", return_value=True)

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets/?attendee_email={user.email}",
        [
            {
                "json": [
                    {
                        **pretix_user_tickets[0],
                        "id": "999",
                        "attendee_email": user.email,
                    }
                ]
            },
            {
                "json": [
                    {
                        **pretix_user_tickets[0],
                        "id": "999",
                        "attendee_email": user.email,
                        "attendee_name": "Penny",
                    }
                ]
            },
        ],
    )
    mock_patch_position = requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        json=update_user_ticket,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories/",
        json=pretix_categories,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions/",
        json=pretix_questions,
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            __typename

            ... on AttendeeTicket {
                id
                attendeeName {
                    parts
                    scheme
                }
                attendeeEmail
                item {
                    questions {
                        answer {
                            answer
                        }
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": "999",
                "attendeeName": {
                    "parts": {
                        "given_name": "Jane",
                        "family_name": "Bell",
                    },
                    "scheme": "given_family",
                },
                "attendeeEmail": user.email,
                "answers": [
                    {"answer": "No preferences", "question": "31", "options": ["344"]},
                    {"answer": "Vegan", "question": "32"},
                    {"answer": "A", "question": "44"},
                    {"answer": "B", "question": "43"},
                ],
            },
        },
    )

    assert not response.get("errors")

    assert response["data"]["updateAttendeeTicket"]["__typename"] == "AttendeeTicket"

    last_call_body = mock_patch_position.last_request.json()
    assert last_call_body["attendee_name_parts"] == {
        "given_name": "Jane",
        "family_name": "Bell",
    }
    assert last_call_body["attendee_email"] == user.email
    assert last_call_body["answers"] == [
        {"question": "31", "options": ["344"], "answer": "No preferences"},
        {"question": "32", "answer": "Vegan"},
        {"question": "44", "answer": "A"},
        {"question": "43", "answer": "B"},
    ]


def test_cannot_update_empty_email(graphql_client, user, mocker):
    conference = ConferenceFactory()

    graphql_client.force_login(user)
    mocker.patch("pretix.is_ticket_owner", return_value=True)
    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            ... on UpdateAttendeeTicketErrors {
                errors {
                    attendeeEmail
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": "999",
                "attendeeEmail": "                            ",
                "attendeeName": {
                    "parts": {
                        "given_name": "Marco",
                        "family_name": "Bell",
                    },
                    "scheme": "given_family",
                },
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["errors"]["attendeeEmail"] == [
        "This field may not be blank."
    ]


@override_settings(PRETIX_API="https://pretix/api/")
def test_update_ticket(
    graphql_client,
    requests_mock,
    user,
    pretix_user_tickets,
    update_user_ticket,
    pretix_categories,
    pretix_questions,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = user.email
    pretix_user_tickets[0]["id"] = 999

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets/?attendee_email={user.email}",
        [
            {
                "json": [
                    {
                        **pretix_user_tickets[0],
                        "id": "999",
                        "attendee_email": user.email,
                    }
                ]
            },
            {
                "json": [
                    {
                        **pretix_user_tickets[0],
                        "id": "999",
                        "attendee_email": user.email,
                        "attendee_name_parts": {
                            "family_name": "Bell",
                            "given_name": "Penny",
                            "scheme": "given_family",
                        },
                    }
                ]
            },
        ],
    )
    mock_patch_position = requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        json=update_user_ticket,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories/",
        json=pretix_categories,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions/",
        json=pretix_questions,
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            __typename
            ... on AttendeeTicket {
                id
                attendeeName {
                    parts
                    scheme
                }
                attendeeEmail
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": "999",
                "attendeeName": {
                    "parts": {
                        "given_name": "Penny",
                        "family_name": "Bell",
                    },
                    "scheme": "given_family",
                },
                "attendeeEmail": user.email,
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["attendeeName"] == {
        "parts": {
            "given_name": "Penny",
            "family_name": "Bell",
        },
        "scheme": "given_family",
    }
    assert response["data"]["updateAttendeeTicket"]["attendeeEmail"] == user.email
    assert response["data"]["updateAttendeeTicket"]["__typename"] == "AttendeeTicket"
    last_call_body = mock_patch_position.last_request.json()
    assert last_call_body["attendee_name_parts"] == {
        "family_name": "Bell",
        "given_name": "Penny",
    }
    assert last_call_body["attendee_email"] == user.email
    assert "answers" not in last_call_body


@override_settings(PRETIX_API="https://pretix/api/")
def test_update_email_reassign_the_ticket(
    graphql_client,
    requests_mock,
    user,
    pretix_user_tickets,
    update_user_ticket,
    pretix_categories,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = user.email
    pretix_user_tickets[0]["id"] = "999"

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets/?attendee_email={user.email}",
        [
            {
                "json": [
                    {
                        **pretix_user_tickets[0],
                        "id": "999",
                        "attendee_email": user.email,
                    }
                ]
            },
            {"json": []},
        ],
    )
    requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        json=update_user_ticket,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories/",
        json=pretix_categories,
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            __typename
            ... on TicketReassigned {
                id
                attendeeEmail
            }
        }
    }
    """

    response = graphql_client.query(
        query,
        variables={
            "conference": conference.code,
            "input": {
                "id": "999",
                "attendeeName": {
                    "parts": {
                        "given_name": pretix_user_tickets[0]["attendee_name"],
                        "family_name": "Bell",
                    },
                    "scheme": "given_family",
                },
                "attendeeEmail": "penny@hofstadter.com",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["id"] == "999"
    assert (
        response["data"]["updateAttendeeTicket"]["attendeeEmail"]
        == "penny@hofstadter.com"
    )
    assert response["data"]["updateAttendeeTicket"]["__typename"] == "TicketReassigned"
