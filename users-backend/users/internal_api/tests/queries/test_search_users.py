from ward import test

from users.tests.api import internalapi_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("search users")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")

    user_1 = await user_factory(
        email="testuser@user.it", fullname="Name", is_staff=False
    )
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    user_3 = await user_factory(
        email="testuser3@user.it", fullname="Name", is_staff=False
    )

    query = """query($query: String!) {
        searchUsers(query: $query) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"query": "name"}
    )
    assert not response.errors
    assert len(response.data["searchUsers"]) == 2
    assert {"id": str(user_1.id)} in response.data["searchUsers"]
    assert {"id": str(user_3.id)} in response.data["searchUsers"]


@test("cannot call without token")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($query: String!) {
        searchUsers(query: $query) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"query": "name"}
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

    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($query: String!) {
        searchUsers(query: $query) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"query": "name"}
    )
    assert response.errors[0]["message"] == "Forbidden"
    assert not response.data
