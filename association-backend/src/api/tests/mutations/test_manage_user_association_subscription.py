from unittest.mock import patch

from pythonit_toolkit.api.graphql_test_client import SimulatedUser
from ward import test

from src.association.tests.api import graphql_client
from src.association.tests.session import db
from src.association_membership.domain.entities import SubscriptionStatus
from src.association_membership.tests.factories import SubscriptionFactory


@test("Manage user subscription")
async def _(graphql_client=graphql_client, db=db):
    await SubscriptionFactory(customer__user_id=1, status=SubscriptionStatus.ACTIVE)

    graphql_client.force_login(
        SimulatedUser(id=1, email="test@user.it", is_staff=False),
    )

    query = """mutation {
        manageUserSubscription {
            __typename
            ... on CustomerPortalResponse {
                billingPortalUrl
            }
        }
    }"""

    with patch(
        "src.customers.domain.repository.stripe.billing_portal.Session.create",
    ) as mock_create:
        mock_create.return_value.url = (
            "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
        )
        response = await graphql_client.query(query, variables={})

    assert (
        response.data["manageUserSubscription"]["__typename"]
        == "CustomerPortalResponse"
    )
    assert (
        response.data["manageUserSubscription"]["billingPortalUrl"]
        == "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
    )


@test("Cannot manage user subscription unlogged")
async def _(graphql_client=graphql_client, db=db):
    query = """mutation {
        manageUserSubscription {
            __typename
            ... on CustomerPortalResponse {
                billingPortalUrl
            }
        }
    }"""

    response = await graphql_client.query(query, variables={})

    assert response.errors[0]["message"] == "Not authenticated"


@test("Cannot manage subscription if user doesnt have one")
async def _(graphql_client=graphql_client, db=db):
    # user id 5 has a subscription
    await SubscriptionFactory(customer__user_id=5, status=SubscriptionStatus.ACTIVE)

    # but user 1 doesn't have one
    graphql_client.force_login(
        SimulatedUser(id=1, email="test@user.it", is_staff=False),
    )

    query = """mutation {
        manageUserSubscription {
            __typename
        }
    }"""

    response = await graphql_client.query(query, variables={})

    assert response.data["manageUserSubscription"]["__typename"] == "NoSubscription"


@test("Cannot manage subscription if all subscriptions are canceled")
async def _(graphql_client=graphql_client, db=db):
    await SubscriptionFactory(customer__user_id=1, status=SubscriptionStatus.CANCELED)

    graphql_client.force_login(
        SimulatedUser(id=1, email="test@user.it", is_staff=False),
    )

    query = """mutation {
        manageUserSubscription {
            __typename
        }
    }"""

    response = await graphql_client.query(query, variables={})

    assert response.data["manageUserSubscription"]["__typename"] == "NoSubscription"
