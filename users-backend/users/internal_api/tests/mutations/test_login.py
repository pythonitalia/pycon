from ward import test

from users.tests.api import internalapi_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("login")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")
    user = await user_factory(email="testuser@user.it", password="hello", is_staff=True)

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            id
            email
        }
    }"""

    response = await internalapi_graphql_client.query(
        query,
        variables={
            "input": {"email": user.email, "password": "hello", "staffOnly": True}
        },
    )

    assert not response.errors
    assert response.data["login"]["id"] == str(user.id)
    assert response.data["login"]["email"] == user.email


@test("cannot login if only staff allowed")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")
    user = await user_factory(
        email="testuser@user.it", password="hello", is_staff=False
    )

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            id
            email
        }
    }"""

    response = await internalapi_graphql_client.query(
        query,
        variables={
            "input": {"email": user.email, "password": "hello", "staffOnly": True}
        },
    )

    assert not response.errors
    assert not response.data["login"]


@test("cannot login with wrong password")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")
    user = await user_factory(email="testuser@user.it", password="hello", is_staff=True)

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            id
            email
        }
    }"""

    response = await internalapi_graphql_client.query(
        query,
        variables={
            "input": {"email": user.email, "password": "hellowrong", "staffOnly": True}
        },
    )

    assert not response.errors
    assert not response.data["login"]


@test("cannot login with empty password")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login(issuer="pycon-backend")
    user = await user_factory(email="testuser@user.it", password="hello", is_staff=True)

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            id
            email
        }
    }"""

    response = await internalapi_graphql_client.query(
        query,
        variables={"input": {"email": user.email, "password": "", "staffOnly": True}},
    )

    assert (
        "ensure this value has at least 1 characters" in response.errors[0]["message"]
    )
    assert not response.data["login"]
