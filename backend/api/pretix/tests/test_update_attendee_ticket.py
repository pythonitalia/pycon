from django.test import override_settings


@override_settings(PRETIX_API="https://pretix/api/")
def test_cannot_update_ticket_if_i_am_not_the_owner(
    graphql_client, requests_mock, user, conference_factory, pretix_user_tickets
):
    graphql_client.force_login(user)
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = "not@my.com"

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets?attendee_email={user.email}",
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
                "name": "Ester",
                "email": "ester@pycon.it",
            },
        },
    )

    assert (
        response["errors"][0]["message"] == "You are not allowed to update this ticket."
    )


@override_settings(PRETIX_API="https://pretix/api/")
def test_update_ticket_errors_handling(
    graphql_client, mocker, requests_mock, user, conference_factory
):
    graphql_client.force_login(user)
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    mocker.patch("pretix.is_ticket_owner", return_value=True)

    requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        text="Not Found",
        status_code=404,
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
                "id": "999",
                "name": "Ester",
                "email": "ester@pycon.it",
            },
        },
    )

    assert "404 Client Error" in response["errors"][0]["message"]


@override_settings(PRETIX_API="https://pretix/api/")
def test_update_ticket(
    graphql_client,
    requests_mock,
    user,
    conference_factory,
    pretix_user_tickets,
    update_user_ticket,
    pretix_categories,
    pretix_questions,
):
    graphql_client.force_login(user)
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = user.email
    pretix_user_tickets[0]["id"] = 999

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets?attendee_email={user.email}",
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
    requests_mock.patch(
        "https://pretix/api/organizers/org/events/event/orderpositions/999/",
        json=update_user_ticket,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/categories",
        json=pretix_categories,
    )
    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/questions",
        json=pretix_questions,
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            __typename
            ... on AttendeeTicket {
                id
                name
                email
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
                "name": "Penny",
                "email": user.email,
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["name"] == "Penny"
    assert response["data"]["updateAttendeeTicket"]["email"] == user.email
    assert response["data"]["updateAttendeeTicket"]["__typename"] == "AttendeeTicket"


@override_settings(PRETIX_API="https://pretix/api/")
def test_update_email_reassign_the_ticket(
    graphql_client,
    requests_mock,
    user,
    conference_factory,
    pretix_user_tickets,
    update_user_ticket,
    pretix_categories,
):
    graphql_client.force_login(user)
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    pretix_user_tickets[0]["attendee_email"] = user.email
    pretix_user_tickets[0]["id"] = "999"

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/tickets/attendee-tickets?attendee_email={user.email}",
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
        "https://pretix/api/organizers/org/events/event/categories",
        json=pretix_categories,
    )

    query = """
    mutation UpdateTicket($conference: String!, $input: UpdateAttendeeTicketInput!) {
        updateAttendeeTicket(conference: $conference, input: $input) {
            __typename
             ... on TicketReassigned {
                id
                email
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
                "name": pretix_user_tickets[0]["attendee_name"],
                "email": "penny@hofstadter.com",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateAttendeeTicket"]["id"] == "999"
    assert response["data"]["updateAttendeeTicket"]["email"] == "penny@hofstadter.com"
    assert response["data"]["updateAttendeeTicket"]["__typename"] == "TicketReassigned"
