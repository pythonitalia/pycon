from unittest.mock import patch

import stripe
from django.conf import settings
from django.urls import reverse
from orders.enums import PaymentState
from orders.models import Order
from pytest import mark
from stripe.error import AuthenticationError, CardError, RateLimitError
from tickets.models import Ticket

stripe.api_key = settings.STRIPE_SECRET_KEY


@mark.django_db
def test_buy_conference_ticket(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    response = graphql_client.query(
        """mutation ($conference: ID!, $items: [CartItem!]) {
            buyTicketWithStripe(input: {
                conference: $conference,
                items: $items
            }) {
                __typename

                ... on StripeClientSecret {
                    clientSecret
                }
            }
        }""",
        variables={
            "conference": fare.conference.code,
            "items": [{"id": fare.id, "quantity": 1}],
        },
    )

    assert "errors" not in response, response["errors"]

    assert response["data"]["buyTicketWithStripe"]["__typename"] == "StripeClientSecret"
    assert response["data"]["buyTicketWithStripe"]["clientSecret"]

    order = Order.objects.first()

    assert order.items.count() == 1

    item = order.items.all()[0]

    assert item.quantity == 1
    assert item.item_object == fare
    assert item.unit_price == fare.price


@mark.django_db
def test_empty_items_fails(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    response = graphql_client.query(
        """
    mutation ($conference: ID!, $items: [CartItem!]) {
        buyTicketWithStripe(input: {
            conference: $conference,
            items: $items
        }) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """,
        variables={"conference": fare.conference.code, "items": []},
    )

    assert "errors" not in response

    assert (
        response["data"]["buyTicketWithStripe"]["__typename"]
        == "BuyTicketWithStripeErrors"
    )
    assert response["data"]["buyTicketWithStripe"]["items"] == [
        "This field is required.",
        "The cart is empty",
    ]


@mark.django_db
def test_authentication_error_fails_the_order(
    graphql_client, user, ticket_fare_factory
):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    with patch(
        "payments.providers.stripe.stripe.PaymentIntent.create",
        side_effect=AuthenticationError,
    ):
        response = graphql_client.query(
            """
        mutation ($conference: ID!, $items: [CartItem!]) {
            buyTicketWithStripe(input: {
                conference: $conference,
                items: $items
            }) {
                __typename

                ... on GenericPaymentError {
                    message
                }
            }
        }
        """,
            variables={
                "conference": fare.conference.code,
                "items": [{"id": fare.id, "quantity": 1}],
            },
        )

    assert (
        response["data"]["buyTicketWithStripe"]["__typename"] == "GenericPaymentError"
    )
    assert (
        response["data"]["buyTicketWithStripe"]["message"]
        == "Something went wrong on our side, please try again"
    )

    order = Order.objects.first()

    assert order.state == PaymentState.FAILED


@mark.django_db
def test_ratelimit_error_fails_the_order(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    with patch(
        "payments.providers.stripe.stripe.PaymentIntent.create",
        side_effect=RateLimitError,
    ):
        response = graphql_client.query(
            """
        mutation ($conference: ID!, $items: [CartItem!]) {
            buyTicketWithStripe(input: {
                conference: $conference,
                items: $items
            }) {
                __typename

                ... on GenericPaymentError {
                    message
                }
            }
        }
        """,
            variables={
                "conference": fare.conference.code,
                "items": [{"id": fare.id, "quantity": 1}],
            },
        )

    assert (
        response["data"]["buyTicketWithStripe"]["__typename"] == "GenericPaymentError"
    )
    assert (
        response["data"]["buyTicketWithStripe"]["message"]
        == "Please try again in a few hours"
    )

    order = Order.objects.first()

    assert order.state == PaymentState.FAILED


@mark.django_db
def test_carderror_fails_the_order(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    with patch(
        "payments.providers.stripe.stripe.PaymentIntent.create",
        side_effect=CardError(
            "a", "b", "c", json_body={"error": {"message": "Invalid card"}}
        ),
    ):
        response = graphql_client.query(
            """
        mutation ($conference: ID!, $items: [CartItem!]) {
            buyTicketWithStripe(input: {
                conference: $conference,
                items: $items
            }) {
                __typename

                ... on GenericPaymentError {
                    message
                }
            }
        }
        """,
            variables={
                "conference": fare.conference.code,
                "items": [{"id": fare.id, "quantity": 1}],
            },
        )

    assert (
        response["data"]["buyTicketWithStripe"]["__typename"] == "GenericPaymentError"
    )
    assert response["data"]["buyTicketWithStripe"]["message"] == "Invalid card"

    order = Order.objects.first()

    assert order.state == PaymentState.FAILED


@mark.django_db
def test_invalid_ticket_fare_id_fails(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    response = graphql_client.query(
        """
    mutation ($conference: ID!, $items: [CartItem!]) {
        buyTicketWithStripe(input: {
            conference: $conference,
            items: $items
        }) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """,
        variables={
            "conference": fare.conference.code,
            "items": [{"id": 100, "quantity": 1}],
        },
    )

    assert (
        response["data"]["buyTicketWithStripe"]["__typename"]
        == "BuyTicketWithStripeErrors"
    )
    assert response["data"]["buyTicketWithStripe"]["items"] == [
        "Ticket 100 does not exist"
    ]


@mark.django_db
def test_expired_ticket_fare_fails(graphql_client, user, expired_ticket_fare):
    graphql_client.force_login(user)

    response = graphql_client.query(
        """
    mutation ($conference: ID!, $items: [CartItem!]) {
        buyTicketWithStripe(input: {
            conference: $conference,
            items: $items
        }) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """,
        variables={
            "conference": expired_ticket_fare.conference.code,
            "items": [{"id": expired_ticket_fare.id, "quantity": 1}],
        },
    )

    assert (
        response["data"]["buyTicketWithStripe"]["__typename"]
        == "BuyTicketWithStripeErrors"
    )
    assert response["data"]["buyTicketWithStripe"]["items"] == [
        f"Ticket {expired_ticket_fare.id} is not available anymore"
    ]


@mark.django_db
def test_fullfil_complete_order_via_webhook(
    order_factory, order_item_factory, ticket_fare_factory, http_client
):
    ticket_fare = ticket_fare_factory()

    order = order_factory(
        transaction_id="stripe-transaction-id", amount=50, state=PaymentState.PROCESSING
    )

    order_item_factory(
        order=order, item_object=ticket_fare, quantity=1, unit_price=ticket_fare.price
    )

    user = order.user

    with patch(
        "payments.providers.stripe.views.stripe.Webhook.construct_event"
    ) as construct_event:
        construct_event.return_value.type = "payment_intent.succeeded"
        construct_event.return_value.data.object.id = "stripe-transaction-id"

        response = http_client.post(reverse("stripe:process-order"))

    assert response.status_code == 200

    order.refresh_from_db()

    assert order.state == PaymentState.COMPLETE

    assigned_tickets = Ticket.objects.filter(user=user).all()

    assert len(assigned_tickets) == 1
    assert assigned_tickets[0].ticket_fare == ticket_fare


@mark.django_db
def test_failing_order_via_webhook(
    order_factory, order_item_factory, ticket_fare_factory, http_client
):
    ticket_fare = ticket_fare_factory()

    order = order_factory(
        transaction_id="stripe-transaction-id", amount=50, state=PaymentState.PROCESSING
    )

    order_item_factory(
        order=order, item_object=ticket_fare, quantity=1, unit_price=ticket_fare.price
    )

    user = order.user

    with patch(
        "payments.providers.stripe.views.stripe.Webhook.construct_event"
    ) as construct_event:
        construct_event.return_value.type = "payment_intent.payment_failed"
        construct_event.return_value.data.object.id = "stripe-transaction-id"

        response = http_client.post(reverse("stripe:process-order"))

    assert response.status_code == 200

    order.refresh_from_db()

    assert order.state == PaymentState.FAILED

    assigned_tickets = Ticket.objects.filter(user=user).all()

    assert len(assigned_tickets) == 0


def test_process_order_only_works_in_post(http_client):
    response = http_client.get(reverse("stripe:process-order"))
    assert response.status_code == 403


def test_process_order_does_not_crash_with_unknown_type(http_client):
    with patch(
        "payments.providers.stripe.views.stripe.Webhook.construct_event"
    ) as construct_event:
        construct_event.return_value.type = "stripe.something"

        response = http_client.post(reverse("stripe:process-order"))

    assert response.status_code == 400
