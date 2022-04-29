import pytest
from django.test import override_settings

from api.pretix.types import PretixOrderStatus
from api.users.types import User

pytestmark = pytest.mark.django_db


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_orders(
    user, conference_factory, requests_mock, pretix_order, pretix_items
):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/orders?email={user.email}",
        json={"count": 1, "results": [pretix_order]},
    )

    requests_mock.get(
        "https://pretix/api/organizers/org/events/event/items", json=pretix_items
    )

    user = User.resolve_reference(user.id, user.email)
    orders = user.orders(info=None, conference=conference.code)

    assert len(orders) == 1
    assert orders[0].code == "A5AFZ"
    assert orders[0].status == PretixOrderStatus.PENDING
    assert orders[0].url == "https://fake-order-url/"
    assert orders[0].total == "3000.00"


@override_settings(PRETIX_API="https://pretix/api/")
def test_get_user_orders_without_any_order(user, conference_factory, requests_mock):
    conference = conference_factory(pretix_organizer_id="org", pretix_event_id="event")

    requests_mock.get(
        f"https://pretix/api/organizers/org/events/event/orders?email={user.email}",
        json={"count": 0, "results": []},
    )

    user = User.resolve_reference(user.id, user.email)
    orders = user.orders(info=None, conference=conference.code)

    assert len(orders) == 0
