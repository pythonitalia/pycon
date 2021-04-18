from unittest.mock import patch

from pythonit_toolkit.api.graphql_test_client import SimulatedUser
from ward import test

from src.association.tests.api import graphql_client
from src.association.tests.session import db
from src.association_membership.domain.entities import SubscriptionStatus
from src.association_membership.tests.factories import SubscriptionFactory


@test("Subscribe user to association")
async def _(graphql_client=graphql_client, db=db):
    graphql_client.force_login(
        SimulatedUser(id=1, email="test@user.it", is_staff=False),
    )

    query = """mutation {
        subscribeUserToAssociation {
            __typename
            ... on CheckoutSession {
                stripeSessionId
            }
        }
    }"""

    with patch(
        "src.customers.domain.repository.stripe.checkout.Session.create",
    ) as mock_create_session, patch(
        "src.customers.domain.repository.stripe.Customer.list"
    ) as mock_customers_list, patch(
        "src.customers.domain.repository.stripe.Customer.create"
    ) as mock_customers_create:
        mock_customers_list.return_value.data = []
        mock_customers_create.return_value.id = "cus_created"
        mock_create_session.return_value.id = "cs_xxx"
        response = await graphql_client.query(query, variables={})

    assert (
        response.data["subscribeUserToAssociation"]["__typename"] == "CheckoutSession"
    )
    assert response.data["subscribeUserToAssociation"]["stripeSessionId"] == "cs_xxx"


@test("Subscribe user to association with existing canceled subscription")
async def _(graphql_client=graphql_client, db=db):
    await SubscriptionFactory(customer__user_id=1, status=SubscriptionStatus.CANCELED)

    graphql_client.force_login(
        SimulatedUser(id=1, email="test@user.it", is_staff=False),
    )

    query = """mutation {
        subscribeUserToAssociation {
            __typename
            ... on CheckoutSession {
                stripeSessionId
            }
        }
    }"""

    with patch(
        "src.customers.domain.repository.stripe.checkout.Session.create",
    ) as mock_create:
        mock_create.return_value.id = "cs_xxx"
        response = await graphql_client.query(query, variables={})

    assert (
        response.data["subscribeUserToAssociation"]["__typename"] == "CheckoutSession"
    )
    assert response.data["subscribeUserToAssociation"]["stripeSessionId"] == "cs_xxx"


@test("cannot subscribe to association with existing active subscription")
async def _(graphql_client=graphql_client, db=db):
    await SubscriptionFactory(customer__user_id=1, status=SubscriptionStatus.ACTIVE)

    graphql_client.force_login(
        SimulatedUser(id=1, email="test@user.it", is_staff=False),
    )

    query = """mutation {
        subscribeUserToAssociation {
            __typename
        }
    }"""

    response = await graphql_client.query(query, variables={})

    assert (
        response.data["subscribeUserToAssociation"]["__typename"] == "AlreadySubscribed"
    )
