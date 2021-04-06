from unittest.mock import patch

from ward import test

from association.api.tests.graphql_client import graphql_client
from association.domain.exceptions import (
    AlreadySubscribed,
    MultipleCustomerReturned,
    MultipleCustomerSubscriptionsReturned,
)
from association.tests.factories import StripeCheckoutSessionFactory
from association.tests.session import db


@test("Subscription created")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
            __typename
            ... on CheckoutSession {
                __typename
                stripeSessionId
                stripeCustomerId
                stripeSubscriptionId
            }
        }
    }
    """
    with patch(
        "association.domain.services.subscribe_user_to_association",
        return_value=StripeCheckoutSessionFactory.build(id="cs_test_12345"),
    ) as service_mock:
        response = await graphql_client.query(query, variables={})
        print(f"response: {response}")
        assert (
            response.data["subscribeUserToAssociation"]["__typename"]
            == "CheckoutSession"
        )
        assert (
            response.data["subscribeUserToAssociation"]["stripeSessionId"]
            == "cs_test_12345"
        )
        service_mock.assert_called_once()


@test("Already Subscribed")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
            __typename
            ... on AlreadySubscribedError {
                __typename
                message
            }
        }
    }
    """
    with patch(
        "association.domain.services.subscribe_user_to_association"
    ) as service_mock:
        service_mock.side_effect = AlreadySubscribed()
        response = await graphql_client.query(query, variables={})
        service_mock.assert_called_once()
        assert not response.errors
        assert (
            response.data["subscribeUserToAssociation"]["__typename"]
            == "AlreadySubscribedError"
        )
        assert (
            response.data["subscribeUserToAssociation"]["message"]
            == "You are already subscribed"
        )


@test("Multiple Customer Returned")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
            __typename
            ... on MultipleCustomerReturnedError {
                __typename
                message
            }
        }
    }
    """
    with patch(
        "association.domain.services.subscribe_user_to_association"
    ) as service_mock:
        service_mock.side_effect = MultipleCustomerReturned()
        response = await graphql_client.query(query, variables={})
        service_mock.assert_called_once()
        assert not response.errors
        assert (
            response.data["subscribeUserToAssociation"]["__typename"]
            == "MultipleCustomerReturnedError"
        )
        assert (
            response.data["subscribeUserToAssociation"]["message"]
            == "It seems you have multiple profiles registered on Stripe with the same email. You will be contacted by the association in the coming days"
        )


@test("Multiple Customer Subscriptions Returned")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
            __typename
            ... on MultipleCustomerSubscriptionsReturnedError {
                __typename
                message
            }
        }
    }
    """
    with patch(
        "association.domain.services.subscribe_user_to_association"
    ) as service_mock:
        service_mock.side_effect = MultipleCustomerSubscriptionsReturned()
        response = await graphql_client.query(query, variables={})
        service_mock.assert_called_once()
        assert not response.errors
        assert (
            response.data["subscribeUserToAssociation"]["__typename"]
            == "MultipleCustomerSubscriptionsReturnedError"
        )
        assert (
            response.data["subscribeUserToAssociation"]["message"]
            == "It seems you have multiple subscriptions registered on Stripe with the same customer. You will be contacted by the association in the coming days"
        )
