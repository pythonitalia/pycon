from unittest.mock import patch

from ward import test

from association.api.tests.graphql_client import graphql_client
from association.domain.exceptions import AlreadySubscribed, MultipleCustomerReturned
from association.tests.factories import SubscriptionFactory
from association.tests.session import db


@test("Subscription created")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
            __typename
            ... on Subscription {
                __typename
                creationDate
                stripeCustomerId
                userId
                state
                stripeSessionId
                stripeSubscriptionId
            }
        }
    }
    """
    with patch(
        "association.domain.services.subscribe_user_to_association",
        return_value=SubscriptionFactory(stripe_session_id="cs_test_12345"),
    ) as service_mock:
        response = await graphql_client.query(query, variables={})
        assert (
            response.data["subscribeUserToAssociation"]["__typename"] == "Subscription"
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
