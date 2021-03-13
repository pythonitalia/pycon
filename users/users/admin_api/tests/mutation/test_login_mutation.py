from ward import test

from users.tests.factories import user_factory
from users.tests.graphql_client import admin_graphql_client
from users.tests.session import db


@test("login only accepts admin users")
async def _(
    admin_graphql_client=admin_graphql_client, user_factory=user_factory, db=db
):
    user = await user_factory(
        email="notadmin@email.it", password="hello", is_staff=False
    )

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
        }
    }
    """
    response = await admin_graphql_client.query(
        query, variables={"input": {"email": user.email, "password": "hello"}}
    )

    assert not response.errors
    assert response.data["login"]["__typename"] == "WrongEmailOrPassword"


@test("login rejects wrong password")
async def _(
    admin_graphql_client=admin_graphql_client, user_factory=user_factory, db=db
):
    user = await user_factory(
        email="notadmin@email.it", password="hello", is_staff=True
    )

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
        }
    }
    """
    response = await admin_graphql_client.query(
        query, variables={"input": {"email": user.email, "password": "wrong"}}
    )

    assert not response.errors
    assert response.data["login"]["__typename"] == "WrongEmailOrPassword"


@test("login as admin user")
async def _(
    admin_graphql_client=admin_graphql_client, user_factory=user_factory, db=db
):
    user = await user_factory(
        email="notadmin@email.it", password="hello", is_staff=True
    )

    query = """mutation($input: LoginInput!) {
        login(input: $input) {
            __typename

            ... on LoginSuccess {
                user {
                    id
                }
            }
        }
    }
    """
    response = await admin_graphql_client.query(
        query, variables={"input": {"email": user.email, "password": "hello"}}
    )

    assert not response.errors
    assert response.data["login"]["__typename"] == "LoginSuccess"
    assert response.data["login"]["user"]["id"] == user.id


@test("cannot login with empty password")
async def _(admin_graphql_client=admin_graphql_client, db=db):
    query = """
    mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
            ... on LoginValidationError {
                errors {
                    password {
                        message
                        type
                    }
                    email {
                        message
                        type
                    }
                }
            }
        }
    }
    """
    response = await admin_graphql_client.query(
        query, variables={"input": {"email": "hah@pycon.it", "password": ""}}
    )

    assert not response.errors, response.errors
    assert response.data["login"] == {
        "__typename": "LoginValidationError",
        "errors": {
            "password": [
                {
                    "message": "ensure this value has at least 1 characters",
                    "type": "value_error.any_str.min_length",
                }
            ],
            "email": None,
        },
    }


@test("cannot login with empty email")
async def _(admin_graphql_client=admin_graphql_client, db=db):
    query = """
    mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
            ... on LoginValidationError {
                errors {
                    password {
                        message
                        type
                    }
                    email {
                        message
                        type
                    }
                }
            }
        }
    }
    """
    response = await admin_graphql_client.query(
        query, variables={"input": {"email": "", "password": "password"}}
    )

    assert not response.errors, response.errors
    assert not response.errors, response.errors
    assert response.data["login"] == {
        "__typename": "LoginValidationError",
        "errors": {
            "email": [
                {
                    "message": "value is not a valid email address",
                    "type": "value_error.email",
                }
            ],
            "password": None,
        },
    }
