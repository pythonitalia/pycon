import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from association.api.tests.graphql_client import graphql_client
from association.domain.exceptions import AlreadySubscribed
from association.tests.factories import SubscriptionFactory
from association.tests.session import db
from ward import skip, test

rome_tz = ZoneInfo("Europe/Rome")


@test("Subscription created")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
            __typename
            ... on SubscriptionResponse {
                __typename
                creationDate
                stripeCustomerId
                userId
                state
                stripeSessionId
                expirationDate
                stripeId
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
            response.data["subscribeUserToAssociation"]["__typename"]
            == "SubscriptionResponse"
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
                expirationDate
                message
            }
        }
    }
    """
    mocked_datetime = datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    with patch(
        "association.domain.services.subscribe_user_to_association"
    ) as service_mock:
        service_mock.side_effect = AlreadySubscribed(expiration_date=mocked_datetime)
        response = await graphql_client.query(query, variables={})
        service_mock.assert_called_once()
        assert not response.errors
        assert (
            response.data["subscribeUserToAssociation"]["__typename"]
            == "AlreadySubscribedError"
        )
        assert response.data["subscribeUserToAssociation"]["expirationDate"] == (
            mocked_datetime.isoformat()
        )
        assert (
            response.data["subscribeUserToAssociation"]["message"]
            == "You are already subscribed"
        )


@skip("JWT check not implemented")
@test("Jwt not valid")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        subscribeUserToAssociation {
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
        "association.domain.services.subscribe_user_to_association",
        # new_callable=AsyncMock,
        return_value=SubscriptionFactory(expiration_date=mocked_datetime),
    ) as service_mock:
        response = await graphql_client.query(query, variables={})
        service_mock.assert_called_once()
        assert response.data["JWTValidationError"]["__typename"] == "JWTValidationError"
        assert response.data["JWTValidationError"]["expirationDate"] == mocked_datetime
        assert response.data["JWTValidationError"]["msg"] == "Invalid User"
