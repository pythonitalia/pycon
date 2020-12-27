from django.test import override_settings
from pytest import mark

from .fake_pretix import FAKE_PRETIX_ITEMS, FAKE_PRETIX_ORDER


def _query_orders(graphql_client, conference):
    return graphql_client.query(
        """
    query Orders($conference: String!) {
        me {
            orders(conference: $conference) {
                code
                status
                url
                total
            }
        }
    }
    """,
        variables={"conference": conference.code},
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

    response = _query_orders(graphql_client, conference)

    assert len(response["data"]["me"]["orders"]) == 1

    order = response["data"]["me"]["orders"][0]

    assert {
        "code": "A5AFZ",
        "status": "PENDING",
        "url": "https://fake-order-url/",
        "total": "3000.00",
    } == order


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

    response = _query_orders(graphql_client, conference)

    assert response["data"], response["errors"]
    assert len(response["data"]["me"]["orders"]) == 0
    assert not items_mock.called
