import pytest
from django.test import override_settings
from pretix import get_orders


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_gets_orders(conference, requests_mock):
    requests_mock.get(
        f"https://pretix/api/organizers/events/orders",
        json={"next": None, "results": []},
    )

    orders = get_orders(conference)

    assert list(orders) == []
