from ward import test

from users.api.tests.graphql_client import graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("cannot login with non existent user")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
        }
    }
    """
    response = await graphql_client.query(
        query, variables={"input": {"email": "hah@pycon.it", "password": "ciao"}}
    )

    assert not response.errors
    assert response.data["login"]["__typename"] == "UsernameAndPasswordCombinationWrong"


@test("cannot login with empty password")
async def _(graphql_client=graphql_client, db=db):
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
    response = await graphql_client.query(
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
async def _(graphql_client=graphql_client, db=db):
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
    response = await graphql_client.query(
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


@test("cannot login with wrong password")
async def _(graphql_client=graphql_client, user_factory=user_factory, db=db):
    user = await user_factory(email="test@email.it", password="hello")

    query = """
    mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
        }
    }
    """
    response = await graphql_client.query(
        query, variables={"input": {"email": user.email, "password": "nope"}}
    )

    assert not response.errors
    assert response.data["login"]["__typename"] == "UsernameAndPasswordCombinationWrong"


@test("can login")
async def _(graphql_client=graphql_client, user_factory=user_factory, db=db):
    user = await user_factory(email="test@email.it", password="hello")

    query = """
    mutation($input: LoginInput!) {
        login(input: $input) {
            __typename

            ... on LoginSuccess {
                user {
                    id
                    email
                }
                token
            }
        }
    }
    """
    response = await graphql_client.query(
        query, variables={"input": {"email": user.email, "password": "hello"}}
    )

    assert not response.errors, response.errors
    assert response.data["login"]["__typename"] == "LoginSuccess"
    assert response.data["login"]["user"] == {"id": user.id, "email": user.email}
    assert response.data["login"]["token"] is not None
