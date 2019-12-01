from django.test import override_settings
from pytest import mark

from .fake_pretix import FAKE_PRETIX_ITEMS, FAKE_PRETIX_ORDER


def _query_orders(graphql_client, conference, language):
    return graphql_client.query(
        """
    query Orders($conference: String!, $language: String!) {
        me {
            orders(conference: $conference) {
                code
                status
                url
                total
                positions {
                    id
                    name(language: $language)
                    attendeeName
                    attendeeEmail
                    price
                }
            }
        }
    }
    """,
        variables={"conference": conference.code, "language": language},
    )


@override_settings(PRETIX_API="https://pretix/api/")
@mark.django_db
def test_get_user_orders(graphql_client, user, conference_factory, requests_mock):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    graphql_client.force_login(user)

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/orders?email={user.email}",
        json={"count": 1, "results": [FAKE_PRETIX_ORDER]},
    )

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/items", json=FAKE_PRETIX_ITEMS
    )

    response = _query_orders(graphql_client, conference, "en")

    assert len(response["data"]["me"]["orders"]) == 1

    order = response["data"]["me"]["orders"][0]
    positions = order.pop("positions")

    assert {
        "code": "A5AFZ",
        "status": "PENDING",
        "url": "https://fake-order-url/",
        "total": "3000.00",
    } == order

    assert {
        "id": 10,
        "name": "Regular ticket",
        "attendeeName": "Jake",
        "attendeeEmail": None,
        "price": "2000.00",
    } in positions

    assert {
        "id": 11,
        "name": "Reduced ticket",
        "attendeeName": "Jack",
        "attendeeEmail": None,
        "price": "1000.00",
    } in positions


@override_settings(PRETIX_API="https://pretix/api/")
@mark.django_db
def test_get_user_orders_without_any_order(
    graphql_client, user, conference_factory, requests_mock
):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    graphql_client.force_login(user)

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/orders?email={user.email}",
        json={"count": 0, "results": []},
    )

    items_mock = requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/items", json=FAKE_PRETIX_ITEMS
    )

    response = _query_orders(graphql_client, conference, "en")

    assert response["data"], response["errors"]
    assert len(response["data"]["me"]["orders"]) == 0
    assert not items_mock.called


@override_settings(PRETIX_API="https://pretix/api/")
@mark.django_db
def test_get_user_orders_with_italian_language_and_fallback_to_english_if_not_found(
    graphql_client, user, conference_factory, requests_mock
):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")
    graphql_client.force_login(user)

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/orders?email={user.email}",
        json={"count": 1, "results": [FAKE_PRETIX_ORDER]},
    )

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/items", json=FAKE_PRETIX_ITEMS
    )

    response = _query_orders(graphql_client, conference, "it")

    assert len(response["data"]["me"]["orders"]) == 1

    order = response["data"]["me"]["orders"][0]
    positions = order.pop("positions")

    assert {
        "id": 10,
        "name": "Ticket base",
        "attendeeName": "Jake",
        "attendeeEmail": None,
        "price": "2000.00",
    } in positions

    assert {
        "id": 11,
        "name": "Reduced ticket",
        "attendeeName": "Jack",
        "attendeeEmail": None,
        "price": "1000.00",
    } in positions
