import stripe

from pytest import mark

from django.conf import settings

from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


@mark.django_db
def test_buy_conference_ticket(graphql_client, user, ticket_fare_factory):
    graphql_client.force_login(user)

    fare = ticket_fare_factory()

    response = graphql_client.query("""
    mutation ($conference: ID!, $items: [CartItem]!) {
        buyTicketWithStripe(input: {
            conference: $conference,
            items: $items
        }) {
            __typename

            ... on StripeClientSecret {
                clientSecret
            }
        }
    }
    """, variables={
        'conference': fare.conference.code,
        'items': [
            {'id': fare.id, 'quantity': 1}
        ]
    })

    assert response['data']['buyTicketWithStripe']['__typename'] == 'StripeClientSecret'
    assert response['data']['buyTicketWithStripe']['clientSecret']

    order = Order.objects.first()

    assert order.items.count() == 1

    item = order.items.all()[0]

    assert item.quantity == 1
    assert item.item_object == fare
    assert item.unit_price == fare.price
