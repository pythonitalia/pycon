from ward import test

from users.tests.api import internalapi_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("get users by emails")
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
    query = """query($emails: [String!]!) {
        usersByEmails(emails: $emails) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"emails": [user_1.email, user_2.email]}
    )

    assert not response.errors
    assert len(response.data["usersByEmails"]) == 2
    assert {"id": str(user_1.id)} in response.data["usersByEmails"]
    assert {"id": str(user_2.id)} in response.data["usersByEmails"]


@test("get users by emails with no emails passed returns nothing")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")

    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($emails: [String!]!) {
        usersByEmails(emails: $emails) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(query, variables={"emails": []})
    assert not response.errors
    assert len(response.data["usersByEmails"]) == 0


@test("user is not returned if the email does not exist")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")

    await user_factory(email="testuser@user.it", fullname="Name", is_staff=False)
    await user_factory(email="testuser2@user.it", fullname="Another", is_staff=False)
    await user_factory(email="testuser3@user.it", fullname="Name", is_staff=False)

    query = """query($emails: [String!]!) {
        usersByEmails(emails: $emails) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"emails": ["sushi@user.it"]}
    )
    assert not response.errors
    assert len(response.data["usersByEmails"]) == 0


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

    query = """query($emails: [String!]!) {
        usersByEmails(emails: $emails) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"emails": [user_1.email, user_2.email]}
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

    query = """query($emails: [String!]!) {
        usersByEmails(emails: $emails) {
            id
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"emails": [user_1.email, user_2.email]}
    )
    assert response.errors[0]["message"] == "Forbidden"
    assert not response.data
