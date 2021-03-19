from unittest.mock import patch

from ward import test

from association.api.tests.graphql_client import graphql_client
from association.domain.exceptions import CustomerNotAvailable
from association.tests.session import db


@test("Customer portal url returned")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        manageUserAssociationSubscription {
            __typename
            ... on CustomerPortalResponse {
                __typename
                billingPortalUrl
            }
        }
    }
    """
    with patch(
        "association.domain.services.manage_user_association_subscription",
        return_value="https://stripe.com/stripe_test_customer_portal/cus_test_12345",
    ) as service_mock:
        response = await graphql_client.query(query, variables={})
        assert (
            response.data["manageUserAssociationSubscription"]["__typename"]
            == "CustomerPortalResponse"
        )
        assert (
            response.data["manageUserAssociationSubscription"]["billingPortalUrl"]
            == "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
        )
        service_mock.assert_called_once()


@test("Customer Not Available")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation {
        manageUserAssociationSubscription {
            __typename
            ... on CustomerNotAvailableError {
                __typename
                message
            }
        }
    }
    """
    with patch(
        "association.domain.services.manage_user_association_subscription",
        return_value="https://stripe.com/stripe_test_customer_portal/cus_test_12345",
    ) as service_mock:
        service_mock.side_effect = CustomerNotAvailable()
        response = await graphql_client.query(query, variables={})
        assert (
            response.data["manageUserAssociationSubscription"]["__typename"]
            == "CustomerNotAvailableError"
        )
        assert (
            response.data["manageUserAssociationSubscription"]["message"]
            == "Customer not available"
        )
        assert not response.errors
        service_mock.assert_called_once()
