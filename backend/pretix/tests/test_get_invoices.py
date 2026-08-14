import pytest
from django.test import override_settings

from conferences.tests.factories import ConferenceFactory
from pretix import get_items, get_orders

pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_gets_orders(requests_mock):
    conference = ConferenceFactory()
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"next": None, "results": []},
    )

    orders = get_orders(conference)

    assert list(orders) == []


@override_settings(
    PRETIX_API="http://pretix/api/v1/",
    PRETIX_API_HOST="localhost:8345",
    PRETIX_API_TOKEN="local-token",
)
def test_gets_paginated_orders_through_internal_host(requests_mock):
    conference = ConferenceFactory()
    path = "organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/"
    requests_mock.get(
        f"http://pretix/api/v1/{path}?status=p",
        json={
            "next": f"http://localhost:8345/api/v1/{path}?page=2&status=p",
            "results": [{"code": "FIRST"}],
        },
    )
    requests_mock.get(
        f"http://pretix/api/v1/{path}?page=2&status=p",
        json={"next": None, "results": [{"code": "SECOND"}]},
    )

    orders = get_orders(conference, {"status": "p"})

    assert [order["code"] for order in orders] == ["FIRST", "SECOND"]
    assert requests_mock.request_history[0].headers["Host"] == "localhost:8345"
    assert requests_mock.request_history[1].headers["Host"] == "localhost:8345"


@override_settings(
    PRETIX_API="http://pretix/api/v1/",
    PRETIX_API_HOST="localhost:8345",
    PRETIX_API_TOKEN="local-token",
)
def test_gets_all_paginated_items(requests_mock):
    conference = ConferenceFactory()
    path = "organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/"
    requests_mock.get(
        f"http://pretix/api/v1/{path}",
        json={
            "next": f"http://localhost:8345/api/v1/{path}?page=2",
            "results": [{"id": 1, "name": {"en": "Regular"}}],
        },
    )
    requests_mock.get(
        f"http://pretix/api/v1/{path}?page=2",
        json={
            "next": None,
            "results": [{"id": 2, "name": {"en": "Student"}}],
        },
    )

    items = get_items(conference)

    assert items == {
        "1": {"id": 1, "name": {"en": "Regular"}},
        "2": {"id": 2, "name": {"en": "Student"}},
    }
