from ward import test

from users.tests.api import internalapi_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("get users by ids")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")

    user_1 = await user_factory(
        email="testuser@user.it", fullname="Name", is_staff=False
    )
    user_2 = await user_factory(
        email="testuser2@user.it", fullname="Another", is_staff=False
    )
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($ids: [ID!]!) {
        usersByIds(ids: $ids) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"ids": [user_1.id, user_2.id]}
    )
    assert not response.errors
    assert len(response.data["usersByIds"]) == 2
    assert {"id": str(user_1.id)} in response.data["usersByIds"]
    assert {"id": str(user_2.id)} in response.data["usersByIds"]


@test("get users by ids with no ids passed returns nothing")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")

    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($ids: [ID!]!) {
        usersByIds(ids: $ids) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(query, variables={"ids": []})
    assert not response.errors
    assert len(response.data["usersByIds"]) == 0


@test("user is not returned if the id does not exist")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")

    await user_factory(id=1, email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(
        id=2, email="testuser2@user.it", fullname="Another", is_staff=False
    )
    await user_factory(id=3, email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($ids: [ID!]!) {
        usersByIds(ids: $ids) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(query, variables={"ids": [50]})
    assert not response.errors
    assert len(response.data["usersByIds"]) == 0


@test("cannot call without token")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    user_1 = await user_factory(
        email="testuser@user.it", fullname="Name", is_staff=False
    )
    user_2 = await user_factory(
        email="testuser2@user.it", fullname="Another", is_staff=False
    )
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($ids: [ID!]!) {
        usersByIds(ids: $ids) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"ids": [user_1.id, user_2.id]}
    )
    assert response.errors[0]["message"] == "Forbidden"
    assert not response.data


@test("cannot call token of not allowed service")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="not-allowed-service")

    user_1 = await user_factory(
        email="testuser@user.it", fullname="Name", is_staff=False
    )
    user_2 = await user_factory(
        email="testuser2@user.it", fullname="Another", is_staff=False
    )
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($ids: [ID!]!) {
        usersByIds(ids: $ids) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"ids": [user_1.id, user_2.id]}
    )
    assert response.errors[0]["message"] == "Forbidden"
    assert not response.data
