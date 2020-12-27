from django.test import override_settings
from django.utils import timezone
from hotels.models import HotelRoomReservation
from pretix.exceptions import PretixError
from pytest import mark


def test_cannot_create_order_unlogged(graphql_client, user, conference, mocker):
    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on CreateOrderResult {
                    paymentUrl
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [
                    {
                        "ticketId": "1",
                        "attendeeName": "ABC",
                        "attendeeEmail": "patrick.arminio@gmail.com",
                        "variation": "1",
                        "answers": [{"questionId": "1", "value": "Example"}],
                    }
                ],
                "hotelRooms": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert response["errors"][0]["message"] == "User not logged in"


@override_settings(FRONTEND_URL="http://test.it")
def test_calls_create_order(graphql_client, user, conference, mocker):
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on CreateOrderResult {
                    paymentUrl
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [
                    {
                        "ticketId": "1",
                        "attendeeName": "ABC",
                        "attendeeEmail": "patrick.arminio@gmail.com",
                        "variation": "1",
                        "answers": [{"questionId": "1", "value": "Example"}],
                    }
                ],
                "hotelRooms": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called_once()


@override_settings(FRONTEND_URL="http://test.it")
def test_handles_payment_url_set_to_none(graphql_client, user, conference, mocker):
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    # this happens when the order is free
    create_order_mock.return_value.payment_url = None
    create_order_mock.return_value.code = "123"

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on CreateOrderResult {
                    paymentUrl
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [
                    {
                        "ticketId": "1",
                        "attendeeName": "ABC",
                        "attendeeEmail": "patrick.arminio@gmail.com",
                        "variation": "1",
                        "answers": [{"questionId": "1", "value": "Example"}],
                    }
                ],
                "hotelRooms": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "http://test.it/en/orders/123/confirmation"
    )

    create_order_mock.assert_called_once()


def test_handles_errors(graphql_client, user, conference, mocker):
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.side_effect = PretixError("Example")

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [
                    {
                        "attendeeName": "ABC",
                        "attendeeEmail": "patrick.arminio@gmail.com",
                        "ticketId": "1",
                        "variation": "1",
                    }
                ],
                "hotelRooms": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["message"] == "Example"

    create_order_mock.assert_called_once()


@override_settings(FRONTEND_URL="http://test.it")
@mark.django_db
def test_order_hotel_room(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    room = hotel_room_factory(conference=conference)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                ... on CreateOrderResult {
                    paymentUrl
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-01",
                        "checkout": "2020-01-10",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["paymentUrl"] == (
        "https://example.com?return_url=http://test.it/en/orders/123/confirmation"
    )

    reservation = HotelRoomReservation.objects.filter(room=room).first()

    assert reservation.user == user
    assert reservation.checkin == timezone.datetime(2020, 1, 1).date()
    assert reservation.checkout == timezone.datetime(2020, 1, 10).date()

    create_order_mock.assert_called_once()


def test_cannot_order_hotel_room_with_checkin_before_conference(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    room = hotel_room_factory(conference=conference)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2019-01-01",
                        "checkout": "2019-01-10",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == "Invaild check-in date"

    create_order_mock.assert_not_called()


def test_cannot_order_hotel_room_with_checkin_after_conference(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    room = hotel_room_factory(conference=conference)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-20",
                        "checkout": "2020-01-22",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == "Invaild check-in date"

    create_order_mock.assert_not_called()


def test_cannot_order_hotel_room_with_checkout_after_conference(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    room = hotel_room_factory(conference=conference)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-02",
                        "checkout": "2020-01-22",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == "Invaild check-out date"

    create_order_mock.assert_not_called()


def test_cannot_order_hotel_room_with_checkout_before_the_checkin(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    room = hotel_room_factory(conference=conference)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-03",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == "Invaild check-out date"

    create_order_mock.assert_not_called()


def test_cannot_order_room_with_random_room_id(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    hotel_room_factory(conference=conference)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": "94990540",
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-03",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == "Room 94990540 not found"

    create_order_mock.assert_not_called()


def test_cannot_order_sold_out_room(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    room = hotel_room_factory(conference=conference, total_capacity=0)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-03",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == f"Room {room.id} is sold out"

    create_order_mock.assert_not_called()


def test_cannot_order_room_of_a_different_conference(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    create_order_mock = mocker.patch("api.orders.mutations.create_order")

    room = hotel_room_factory(total_capacity=5)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-03",
                    }
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == f"Room {room.id} not found"

    create_order_mock.assert_not_called()


def test_cannot_buy_more_room_than_available(
    graphql_client, hotel_room_factory, user, conference_factory, mocker
):
    graphql_client.force_login(user)

    create_order_mock = mocker.patch("api.orders.mutations.create_order")
    create_order_mock.return_value.payment_url = "https://example.com"
    create_order_mock.return_value.code = "123"

    conference = conference_factory(
        start=timezone.make_aware(timezone.datetime(2020, 1, 1)),
        end=timezone.make_aware(timezone.datetime(2020, 1, 10)),
    )

    room = hotel_room_factory(conference=conference, total_capacity=2)

    response = graphql_client.query(
        """mutation CreateOrder($code: String!, $input: CreateOrderInput!) {
            createOrder(conference: $code, input: $input) {
                __typename

                ... on CreateOrderResult {
                    paymentUrl
                }

                ... on Error {
                    message
                }
            }
        }""",
        variables={
            "code": conference.code,
            "input": {
                "tickets": [],
                "paymentProvider": "stripe",
                "email": "patrick.arminio@gmail.com",
                "hotelRooms": [
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-06",
                    },
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-06",
                    },
                    {
                        "roomId": str(room.id),
                        "checkin": "2020-01-05",
                        "checkout": "2020-01-06",
                    },
                ],
                "invoiceInformation": {
                    "isBusiness": False,
                    "company": "",
                    "name": "Patrick",
                    "street": "",
                    "zipcode": "92100",
                    "city": "Avellino",
                    "country": "IT",
                    "vatId": "",
                    "fiscalCode": "",
                },
                "locale": "en",
            },
        },
    )

    assert not response.get("errors")
    assert response["data"]["createOrder"]["__typename"] == "Error"
    assert response["data"]["createOrder"]["message"] == "Too many rooms"

    create_order_mock.assert_not_called()
