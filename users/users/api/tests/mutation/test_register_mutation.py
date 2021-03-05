from ward import each, test

from users.tests.factories import user_factory
from users.tests.graphql_client import graphql_client
from users.tests.session import db


@test("can register")
async def _(graphql_client=graphql_client, db=db):
    query = """mutation($input: RegisterInput!) {
        register(input: $input) {
            __typename

            ... on RegisterSuccess {
                user {
                    id
                    email
                    fullname
                }

                token
            }
        }
    }
    """
    response = await graphql_client.query(
        query,
        variables={"input": {"email": "marco@provider.it", "password": "ciaomondo"}},
    )

    assert not response.errors, response.errors

    assert response.data["register"]["__typename"] == "RegisterSuccess"
    assert response.data["register"]["user"]["id"] is not None
    assert response.data["register"]["user"]["email"] == "marco@provider.it"
    assert response.data["register"]["user"]["fullname"] == ""
    assert response.data["register"]["token"] is not None


@test("cannot register if the email is already used by other users")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    await user_factory(email="hah@pycon.it")

    query = """mutation($input: RegisterInput!) {
        register(input: $input) {
            __typename
            ... on EmailAlreadyUsed {
                message
            }
        }
    }
    """
    response = await graphql_client.query(
        query,
        variables={"input": {"email": "hah@pycon.it", "password": "verylongpassword"}},
    )

    assert not response.errors, response.errors
    assert response.data["register"]["__typename"] == "EmailAlreadyUsed"


@test("cannot register with invalid password")
async def _(graphql_client=graphql_client, password=each("", "short"), db=db):
    query = """mutation($input: RegisterInput!) {
        register(input: $input) {
            __typename
            ... on RegisterValidationError {
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
        query, variables={"input": {"email": "hah@pycon.it", "password": password}}
    )

    assert not response.errors, response.errors
    assert response.data["register"] == {
        "__typename": "RegisterValidationError",
        "errors": {
            "password": [
                {
                    "message": "ensure this value has at least 8 characters",
                    "type": "value_error.any_str.min_length",
                }
            ],
            "email": None,
        },
    }


@test("cannot register with invalid email")
async def _(graphql_client=graphql_client, email=each("", "invalid.email"), db=db):
    query = """mutation($input: RegisterInput!) {
        register(input: $input) {
            __typename
            ... on RegisterValidationError {
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
        query, variables={"input": {"email": email, "password": "ciaomondo!"}}
    )

    assert not response.errors, response.errors
    assert response.data["register"] == {
        "__typename": "RegisterValidationError",
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
