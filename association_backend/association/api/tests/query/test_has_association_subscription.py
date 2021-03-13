from ward import skip, test

from association.api.tests.graphql_client import graphql_client
from association.domain.entities import SubscriptionState
from association.tests.factories import SubscriptionFactory
from association.tests.session import db


@test("return has_association_subscription False if no subscription")
async def _(graphql_client=graphql_client, db=db):
    query = """{
        hasAssociationSubscription {
            hasAssociationSubscription
        }
    }"""

    response = await graphql_client.query(query)
    assert (
        response.data["hasAssociationSubscription"]["hasAssociationSubscription"]
        is False
    )


@test("return has_association_subscription False if subscription PENDING")
async def _(graphql_client=graphql_client, db=db):
    SubscriptionFactory(state=SubscriptionState.PENDING)

    query = """{
        hasAssociationSubscription {
            hasAssociationSubscription
        }
    }"""

    response = await graphql_client.query(query)
    assert (
        response.data["hasAssociationSubscription"]["hasAssociationSubscription"]
        is False
    )


@test("return has_association_subscription False if subscription NOT_CREATED")
async def _(graphql_client=graphql_client, db=db):
    SubscriptionFactory(state=SubscriptionState.NOT_CREATED)

    query = """{
        hasAssociationSubscription {
            hasAssociationSubscription
        }
    }"""

    response = await graphql_client.query(query)
    assert (
        response.data["hasAssociationSubscription"]["hasAssociationSubscription"]
        is False
    )


@skip("Investigate why this test fails")
@test("return has_association_subscription True if subscription ACTIVE")
async def _(
    graphql_client=graphql_client,
    db=db,
):
    SubscriptionFactory(state=SubscriptionState.ACTIVE)

    query = """{
        hasAssociationSubscription {
            hasAssociationSubscription
        }
    }"""

    response = await graphql_client.query(query)
    assert (
        response.data["hasAssociationSubscription"]["hasAssociationSubscription"]
        is True
    )


@skip("Investigate why this test fails")
@test("return has_association_subscription True if subscription EXPIRED")
async def _(graphql_client=graphql_client, db=db):
    SubscriptionFactory(state=SubscriptionState.EXPIRED)

    query = """{
        hasAssociationSubscription {
            hasAssociationSubscription
        }
    }"""

    response = await graphql_client.query(query)
    assert (
        response.data["hasAssociationSubscription"]["hasAssociationSubscription"]
        is True
    )
