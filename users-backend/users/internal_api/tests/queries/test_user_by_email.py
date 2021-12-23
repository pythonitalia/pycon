from ward import test

from users.tests.api import internalapi_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("correctly gets the user when sending a valid email")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="association-backend")

    user_1 = await user_factory(
        email="testuser@user.it", fullname="Name", is_staff=False
    )
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($email: String!) {
        userByEmail(email: $email) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"email": user_1.email}
    )
    assert not response.errors
    assert response.data["userByEmail"]["id"] == str(user_1.id)


@test("returns None when the email doesn't exist")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="association-backend")

    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($email: String!) {
        userByEmail(email: $email) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"email": "testemail@email.it"}
    )
    assert not response.errors
    assert response.data["userByEmail"] is None


@test("returns None with invalid email")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="association-backend")

    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($email: String!) {
        userByEmail(email: $email) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"email": "testemail"}
    )
    assert not response.errors
    assert response.data["userByEmail"] is None


@test("requires authentication")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($email: String!) {
        userByEmail(email: $email) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"email": "testemail"}
    )
    assert response.errors[0]["message"] == "Forbidden"
    assert response.data["userByEmail"] is None
