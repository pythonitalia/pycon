import pytest
from django.test import override_settings
from pretix import CreateOrderInput, CreateOrderTicket, create_order
from pretix.exceptions import PretixError


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_creates_order(conference, requests_mock):
    requests_mock.post(
        f"https://pretix/api/organizers/events/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        tickets=[CreateOrderTicket(ticket_id="123", quantity=1, variation=None)],
    )

    result = create_order(conference, order_data)

    assert result.payment_url == "http://example.com"


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_raises_when_response_is_400(conference, requests_mock):
    requests_mock.post(
        f"https://pretix/api/organizers/events/orders/", status_code=400, json={}
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        tickets=[CreateOrderTicket(ticket_id="123", quantity=1, variation=None)],
    )

    with pytest.raises(PretixError):
        create_order(conference, order_data)
