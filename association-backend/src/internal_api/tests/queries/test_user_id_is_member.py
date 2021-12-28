from ward import each, test

from src.association.tests.session import db
from src.association_membership.domain.entities import SubscriptionStatus
from src.association_membership.tests.factories import SubscriptionFactory
from src.internal_api.tests.fixtures import internalapi_graphql_client


@test("user does not exist")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
):
    internalapi_graphql_client.force_service_login(
        issuer="pycon-backend", audience="association-backend"
    )

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": "1"})
    assert not response.errors
    assert response.data["userIdIsMember"] is False


@test("user is a member")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
):
    await SubscriptionFactory(user_id=1, status=SubscriptionStatus.ACTIVE)

    internalapi_graphql_client.force_service_login(
        issuer="pycon-backend", audience="association-backend"
    )

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": "1"})
    assert not response.errors
    assert response.data["userIdIsMember"] is True


@test("user has a {status} membership so is not a member")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    status=each(SubscriptionStatus.CANCELED, SubscriptionStatus.PENDING),
):
    await SubscriptionFactory(user_id=1, status=status)

    internalapi_graphql_client.force_service_login(
        issuer="pycon-backend", audience="association-backend"
    )

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": "1"})
    assert not response.errors
    assert response.data["userIdIsMember"] is False


@test("requires authentication")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
):
    await SubscriptionFactory(user_id=1, status=SubscriptionStatus.ACTIVE)

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": "1"})
    assert response.errors[0]["message"] == "Forbidden"
    assert not response.data


@test("requires authentication of allowed service")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
):
    await SubscriptionFactory(user_id=1, status=SubscriptionStatus.ACTIVE)
    internalapi_graphql_client.force_service_login(
        issuer="random-service", audience="association-backend"
    )

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": "1"})
    assert response.errors[0]["message"] == "Forbidden"
    assert not response.data


@test("invalid id raises an error")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
):
    internalapi_graphql_client.force_service_login(
        issuer="pycon-backend", audience="association-backend"
    )

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": "abc-1"})
    assert (
        response.errors[0]["message"]
        == "invalid literal for int() with base 10: 'abc-1'"
    )
    assert not response.data


@test("empty id raises an error")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
):
    internalapi_graphql_client.force_service_login(
        issuer="pycon-backend", audience="association-backend"
    )

    query = """query($id: ID!) {
        userIdIsMember(id: $id)
    }"""

    response = await internalapi_graphql_client.query(query, variables={"id": ""})
    assert response.errors[0]["message"] == "Invalid ID"
    assert not response.data
