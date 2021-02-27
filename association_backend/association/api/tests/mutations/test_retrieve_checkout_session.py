import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from association.api.tests.graphql_client import graphql_client
from association.domain.exceptions import AlreadySubscribed
from association.tests.factories import SubscriptionFactory
from association.tests.session import db
from ward import skip, test

rome_tz = ZoneInfo("Europe/Rome")


@test("ok")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        retrieveCheckoutSession {
            __typename
            ... on SubscriptionResponse {
                __typename
                subscription {
                    creationDate
                    stripeCustomerId
                    userId
                    state
                    stripeSessionId
                    expirationDate
                    paymentDate
                    stripeId
                }
            }
        }
    }
    """
    with patch(
        "association.domain.services.do_checkout",
        return_value=SubscriptionFactory(stripe_session_id="cs_test_12345"),
    ) as do_checkout_mock:
        response = await graphql_client.query(query, variables={})
        do_checkout_mock.assert_called_once()
        assert (
            response.data["retrieveCheckoutSession"]["__typename"]
            == "SubscriptionResponse"
        )
        assert (
            response.data["retrieveCheckoutSession"]["subscription"]["stripeSessionId"]
            == "cs_test_12345"
        )


@test("Already Subscribed")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        retrieveCheckoutSession {
            __typename
            ... on AlreadySubscribedError {
                __typename
                expirationDate
                message
            }
        }
    }
    """
    mocked_datetime = datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    with patch("association.domain.services.do_checkout") as do_checkout_mock:
        do_checkout_mock.side_effect = AlreadySubscribed(
            expiration_date=mocked_datetime
        )
        response = await graphql_client.query(query, variables={})
        do_checkout_mock.assert_called_once()
        print(response.data)
        print(response.errors)
        assert not response.errors
        assert (
            response.data["retrieveCheckoutSession"]["__typename"]
            == "AlreadySubscribedError"
        )
        assert response.data["retrieveCheckoutSession"]["expirationDate"] == (
            mocked_datetime.isoformat()
        )
        assert (
            response.data["retrieveCheckoutSession"]["message"]
            == "You are already subscribed"
        )


@skip("JWT check not implemented")
@test("Jwt not valid")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        retrieveCheckoutSession {
            __typename
            ... on AlreadySubscribedError {
                __typename
                expiration_date
                message
            }
        }
    }
    """
    mocked_datetime = datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    with patch(
        "association.domain.services.do_checkout",
        # new_callable=AsyncMock,
        return_value=SubscriptionFactory(expiration_date=mocked_datetime),
    ) as do_checkout_mock:
        response = await graphql_client.query(query, variables={})
        do_checkout_mock.assert_called_once()
        assert response.data["JWTValidationError"]["__typename"] == "JWTValidationError"
        assert response.data["JWTValidationError"]["expirationDate"] == mocked_datetime
        assert response.data["JWTValidationError"]["msg"] == "Invalid User"
