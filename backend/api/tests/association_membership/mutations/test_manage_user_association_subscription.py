import pytest
from unittest.mock import patch

from association_membership.enums import MembershipStatus
from association_membership.tests.factories import (
    StripeCustomerFactory,
    MembershipFactory,
)
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_manage_user_subscription(graphql_client):
    membership = MembershipFactory(status=MembershipStatus.ACTIVE)
    StripeCustomerFactory(user_id=membership.user_id)

    graphql_client.force_login(membership.user)

    query = """mutation {
        manageUserSubscription {
            __typename
            ... on CustomerPortalResponse {
                billingPortalUrl
            }
        }
    }"""

    with patch(
        "api.association_membership.mutations.manage_user_subscription.stripe.billing_portal.Session.create",
    ) as mock_create:
        mock_create.return_value.url = (
            "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
        )
        response = graphql_client.query(query, variables={})

    assert (
        response["data"]["manageUserSubscription"]["__typename"]
        == "CustomerPortalResponse"
    )
    assert (
        response["data"]["manageUserSubscription"]["billingPortalUrl"]
        == "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
    )


def test_cannot_manage_user_subscription_unlogged(graphql_client):
    query = """mutation {
        manageUserSubscription {
            __typename
            ... on CustomerPortalResponse {
                billingPortalUrl
            }
        }
    }"""

    response = graphql_client.query(query, variables={})

    assert response["errors"][0]["message"] == "User not logged in"


def test_cannot_manage_subscription_if_user_doesnt_have_one(graphql_client):
    membership = MembershipFactory(status=MembershipStatus.ACTIVE)
    StripeCustomerFactory(user_id=membership.user_id)

    logged_user = UserFactory()

    # but logged user doesn't have one
    graphql_client.force_login(logged_user)

    query = """mutation {
        manageUserSubscription {
            __typename
        }
    }"""

    response = graphql_client.query(query, variables={})

    assert response["data"]["manageUserSubscription"]["__typename"] == "NoSubscription"


def test_cannot_manage_subscription_if_all_subscriptions_are_canceled(graphql_client):
    membership = MembershipFactory(status=MembershipStatus.CANCELED)
    StripeCustomerFactory(user_id=membership.user_id)

    graphql_client.force_login(membership.user)

    query = """mutation {
        manageUserSubscription {
            __typename
        }
    }"""

    response = graphql_client.query(query, variables={})

    assert response["data"]["manageUserSubscription"]["__typename"] == "NoSubscription"


def test_cannot_manage_subscription_if_not_subscribed_via_stripe(graphql_client):
    membership = MembershipFactory(status=MembershipStatus.ACTIVE)

    graphql_client.force_login(membership.user)

    query = """mutation {
        manageUserSubscription {
            __typename
        }
    }"""

    response = graphql_client.query(query, variables={})

    assert (
        response["data"]["manageUserSubscription"]["__typename"]
        == "NotSubscribedViaStripe"
    )
