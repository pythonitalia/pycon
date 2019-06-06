import stripe

from pytest import mark

from django.conf import settings

from conferences.models import Ticket
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


@mark.django_db
def test_buy_conference_ticket(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    ticket_fare = ticket_fare_factory()
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on TicketsPayment {
                order {
                    id
                }

                tickets {
                    id

                    ticketFare {
                        id
                    }
                }
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'TicketsPayment'
    assert len(resp['data']['buyTicketWithStripe']['tickets']) == 1

    ticket = Ticket.objects.get(id=resp['data']['buyTicketWithStripe']['tickets'][0]['id'])

    assert ticket.user == user
    assert ticket.ticket_fare == ticket_fare

    order = Order.objects.get(id=resp['data']['buyTicketWithStripe']['order']['id'])

    assert order.amount == ticket_fare.price

    item = order.items.first()

    assert order.items.all().count() == 1
    assert item.description == ticket_fare.order_description
    assert item.unit_price == ticket_fare.price
    assert item.quantity == 1


@mark.django_db
def test_at_least_one_payment_method_or_intent_is_required(graphql_client, user, ticket_fare):
    graphql_client.force_login(user)

    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename


            ... on BuyTicketWithStripeErrors {
                nonFieldErrors
                items
                conference
                paymentMethodId
                paymentIntentId
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
        }
    })

    assert resp['errors']
    assert resp['errors'][0]['message'] == 'You need to specify at least a payment_method_id or a payment_intent_id'


@mark.django_db
def test_cannot_specify_both_payment_method_and_intent(graphql_client, user, ticket_fare):
    graphql_client.force_login(user)

    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_visa",
            'paymentIntentId': "pi_aaaaaaaaaaa_bbbbb",
        }
    })

    assert resp['errors'][0]['message'] == 'You cannot specify both payment_method_id and payment_intent_id'


@mark.django_db
def test_cannot_buy_expired_ticket(graphql_client, user, expired_ticket_fare):
    graphql_client.force_login(user)

    conference = expired_ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': expired_ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'BuyTicketWithStripeErrors'
    assert resp['data']['buyTicketWithStripe']['items'] == [
        f'Ticket {expired_ticket_fare.id} is not available anymore'
    ]


@mark.django_db
def test_cannot_buy_not_valid_ticket(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    ticket_fare = ticket_fare_factory(start=None)
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'BuyTicketWithStripeErrors'
    assert resp['data']['buyTicketWithStripe']['items'] == [
        f'Ticket {ticket_fare.id} is not available anymore'
    ]


@mark.django_db
def test_cannot_buy_with_invalid_ticket_id(graphql_client, user, expired_ticket_fare):
    graphql_client.force_login(user)

    ticket_fare = expired_ticket_fare
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': 9999
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'BuyTicketWithStripeErrors'
    assert resp['data']['buyTicketWithStripe']['items'] == [
        f'Ticket 9999 does not exist'
    ]


@mark.django_db
def test_cannot_buy_with_empty_cart(graphql_client, user, expired_ticket_fare):
    graphql_client.force_login(user)

    ticket_fare = expired_ticket_fare
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
            }
        }
    }
    """, variables={
        'input': {
            'items': [],
            'conference': conference.code,
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'BuyTicketWithStripeErrors'
    assert resp['data']['buyTicketWithStripe']['items'] == [
        'This field is required.',
        'The cart is empty',
    ]


@mark.django_db
def test_cannot_buy_without_the_conference_code(graphql_client, user, expired_ticket_fare):
    graphql_client.force_login(user)

    ticket_fare = expired_ticket_fare
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on BuyTicketWithStripeErrors {
                items
                conference
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': 1
            }],
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['errors']
    assert 'In field "conference": Expected "ID!", found null.' in resp['errors'][0]['message']


@mark.django_db
def test_cannot_buy_with_invalid_conference_code(graphql_client, user, expired_ticket_fare):
    graphql_client.force_login(user)

    ticket_fare = expired_ticket_fare
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on BuyTicketWithStripeErrors {
                conference
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa111111111100000000000',
            'paymentMethodId': "pm_card_visa"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'BuyTicketWithStripeErrors'
    assert resp['data']['buyTicketWithStripe']['conference'] == [
        'Select a valid choice. That choice is not one of the available choices.',
    ]


@mark.django_db
def test_payment_requires_3d_verification(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    ticket_fare = ticket_fare_factory()
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on Stripe3DValidationRequired {
                clientSecret
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_threeDSecure2Required"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'Stripe3DValidationRequired'
    assert 'clientSecret' in resp['data']['buyTicketWithStripe']


@mark.django_db
def test_payment_fails_when_the_user_does_not_have_funds(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    ticket_fare = ticket_fare_factory()
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on GenericPaymentFailedError {
                message
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_chargeDeclinedInsufficientFunds"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'GenericPaymentFailedError'
    assert resp['data']['buyTicketWithStripe']['message'] == 'Your card has insufficient funds.'

    assert Order.objects.all().count() == 0
    assert Ticket.objects.all().count() == 0


@mark.django_db
def test_payment_fails_because_declined(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    ticket_fare = ticket_fare_factory()
    conference = ticket_fare.conference

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on GenericPaymentFailedError {
                message
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentMethodId': "pm_card_chargeDeclined"
        }
    })

    assert resp['data']['buyTicketWithStripe']['__typename'] == 'GenericPaymentFailedError'
    assert resp['data']['buyTicketWithStripe']['message'] == 'Your card was declined.'

    assert Order.objects.all().count() == 0
    assert Ticket.objects.all().count() == 0


@mark.django_db
def test_pay_with_intent_of_different_amount(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    # 500 euro
    ticket_fare = ticket_fare_factory(price=500)
    conference = ticket_fare.conference

    intent = stripe.PaymentIntent.create(
        # 300 cents!
        amount=300,
        currency='eur',
        payment_method='pm_card_visa'
    )

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentIntentId': intent.id
        }
    })

    assert resp['errors'][0]['message'] == 'Payment intent amount and cart amount different'
    assert Order.objects.all().count() == 0
    assert Ticket.objects.all().count() == 0


@mark.django_db
def test_pay_fails_after_3d_validation(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    ticket_fare = ticket_fare_factory(price=10)
    conference = ticket_fare.conference

    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='eur',
        payment_method='pm_card_chargeDeclined'
    )

    resp = graphql_client.query("""
    mutation($input: BuyTicketWithStripeInput!) {
          buyTicketWithStripe(input: $input) {
            __typename

            ... on GenericPaymentFailedError {
                message
            }
        }
    }
    """, variables={
        'input': {
            'items': [{
                'quantity': 1, 'id': ticket_fare.id
            }],
            'conference': conference.code,
            'paymentIntentId': intent.id
        }
    })

    assert 'errors' not in resp
    assert resp['data']['buyTicketWithStripe']['__typename'] == 'GenericPaymentFailedError'
    assert resp['data']['buyTicketWithStripe']['message'] == 'Your card was declined.'

    assert Order.objects.all().count() == 0
    assert Ticket.objects.all().count() == 0
