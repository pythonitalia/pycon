import pytest
from unittest.mock import patch

from association_membership.enums import MembershipStatus
from association_membership.tests.factories import (
    StripeCustomerFactory,
    MembershipFactory,
)
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_subscribe_user_to_association(
    graphql_client,
):
    graphql_client.force_login(UserFactory())

    query = """mutation {
        subscribeUserToAssociation {
            __typename
            ... on CheckoutSession {
                stripeSessionId
            }
        }
    }"""

    with patch(
        "api.association_membership.mutations.subscribe_user_to_association.stripe.checkout.Session.create",
    ) as mock_create_session, patch(
        "api.association_membership.mutations.subscribe_user_to_association.stripe.Customer.create"
    ) as mock_customers_create:
        mock_customers_create.return_value.id = "cus_created"
        mock_create_session.return_value.id = "cs_xxx"
        response = graphql_client.query(query, variables={})

    assert (
        response["data"]["subscribeUserToAssociation"]["__typename"]
        == "CheckoutSession"
    )
    assert response["data"]["subscribeUserToAssociation"]["stripeSessionId"] == "cs_xxx"


def test_subscribe_user_to_association_with_existing_canceled_subscription(
    graphql_client,
):
    membership = MembershipFactory(status=MembershipStatus.CANCELED)
    StripeCustomerFactory(user_id=membership.user_id, stripe_customer_id="cus_123")

    graphql_client.force_login(membership.user)

    query = """mutation {
        subscribeUserToAssociation {
            __typename
            ... on CheckoutSession {
                stripeSessionId
            }
        }
    }"""

    with patch(
        "api.association_membership.mutations.subscribe_user_to_association.stripe.checkout.Session.create",
    ) as mock_create:
        mock_create.return_value.id = "cs_xxx"
        response = graphql_client.query(query, variables={})

    assert (
        response["data"]["subscribeUserToAssociation"]["__typename"]
        == "CheckoutSession"
    )
    assert response["data"]["subscribeUserToAssociation"]["stripeSessionId"] == "cs_xxx"


def test_cannot_subscribe_to_association_with_existing_active_subscription(
    graphql_client,
):
    membership = MembershipFactory(status=MembershipStatus.ACTIVE)

    graphql_client.force_login(membership.user)

    query = """mutation {
        subscribeUserToAssociation {
            __typename
        }
    }"""

    response = graphql_client.query(query, variables={})

    assert (
        response["data"]["subscribeUserToAssociation"]["__typename"]
        == "AlreadySubscribed"
    )
