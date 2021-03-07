import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from association.api.tests.graphql_client import graphql_client
from association.domain.exceptions import CustomerNotAvailable
from association.tests.factories import SubscriptionFactory
from association.tests.session import db
from ward import skip, test

rome_tz = ZoneInfo("Europe/Rome")


@test("Customer portal url returned")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        customerPortal {
            __typename
            ... on CustomerPortalResponse {
                __typename
                billingPortalUrl
            }
        }
    }
    """
    with patch(
        "association.domain.services.customer_portal",
        return_value="https://stripe.com/stripe_test_customer_portal/cus_test_12345",
    ) as service_mock:
        response = await graphql_client.query(query, variables={})
        assert response.data["customerPortal"]["__typename"] == "CustomerPortalResponse"
        assert (
            response.data["customerPortal"]["billingPortalUrl"]
            == "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
        )
        service_mock.assert_called_once()


@test("Customer Not Available")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        customerPortal {
            __typename
            ... on CustomerNotAvailableError {
                __typename
                message
            }
        }
    }
    """
    with patch("association.domain.services.customer_portal") as service_mock:
        service_mock.side_effect = CustomerNotAvailable()
        response = await graphql_client.query(query, variables={})
        print(response.data)
        assert (
            response.data["customerPortal"]["__typename"] == "CustomerNotAvailableError"
        )
        assert response.data["customerPortal"]["message"] == "Customer not available"
        assert not response.errors
        service_mock.assert_called_once()


@skip("JWT check not implemented")
@test("Jwt not valid")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        customerPortal {
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
        "association.domain.services.customer_portal",
        # new_callable=AsyncMock,
        return_value=SubscriptionFactory(expiration_date=mocked_datetime),
    ) as service_mock:
        response = await graphql_client.query(query, variables={})
        service_mock.assert_called_once()
        assert response.data["JWTValidationError"]["__typename"] == "JWTValidationError"
        assert response.data["JWTValidationError"]["expirationDate"] == mocked_datetime
        assert response.data["JWTValidationError"]["msg"] == "Invalid User"
