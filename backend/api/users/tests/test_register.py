import pytest
from users.models import User

from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_register(full_response_graphql_client):
    body, response = full_response_graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterSuccess {
                    user {
                        id
                        email
                        fullname
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "test@email.it",
                "password": "testtesttest",
                "fullname": "Fullname",
            }
        },
    )

    assert body["data"]["register"]["__typename"] == "RegisterSuccess"
    user_id = body["data"]["register"]["user"]["id"]
    user = User.objects.get(id=user_id)

    assert str(user.id) == str(user.id)
    assert user.email == "test@email.it"
    assert user.fullname == "Fullname"

    assert "pythonitalia_sessionid" in response.cookies


def test_register_with_used_email_fails(full_response_graphql_client):
    another_user = UserFactory(
        email="test@email.it", password="another", full_name="Another user"
    )

    body, response = full_response_graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
            }
        }""",
        variables={
            "input": {
                "email": "test@email.it",
                "password": "password123",
                "fullname": "New Name",
            }
        },
    )

    assert body["data"]["register"]["__typename"] == "EmailAlreadyUsed"
    assert "pythonitalia_sessionid" not in response.cookies
    another_user.refresh_from_db()
    assert another_user.fullname == "Another user"
    assert another_user.check_password("another")


@pytest.mark.parametrize(
    "attempt_email", ("test@EMAIL.it", "TEST@EMAIL.it", "teST@eMaIl.it")
)
def test_register_with_used_email_normalised(
    full_response_graphql_client, attempt_email
):
    another_user = UserFactory(
        email="test@email.it", password="another", full_name="Another user"
    )

    body, response = full_response_graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
            }
        }""",
        variables={
            "input": {
                "email": attempt_email,
                "password": "password123",
                "fullname": "New Name",
            }
        },
    )

    assert body["data"]["register"]["__typename"] == "EmailAlreadyUsed"
    assert "pythonitalia_sessionid" not in response.cookies
    another_user.refresh_from_db()
    assert another_user.fullname == "Another user"
    assert another_user.check_password("another")


def test_register_fullname_is_required(full_response_graphql_client):
    body, response = full_response_graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterErrors {
                    errors {
                        fullname
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "test@email.it",
                "password": "password123",
                "fullname": "",
            }
        },
    )

    assert body["data"]["register"]["__typename"] == "RegisterErrors"
    assert body["data"]["register"]["errors"]["fullname"] == ["Fullname is required"]

    assert "pythonitalia_sessionid" not in response.cookies


def test_register_multiple_errors(full_response_graphql_client):
    body, response = full_response_graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterErrors {
                    errors {
                        password
                        fullname
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "test@email.it",
                "password": "",
                "fullname": "",
            }
        },
    )

    assert body["data"]["register"]["__typename"] == "RegisterErrors"
    assert body["data"]["register"]["errors"]["fullname"] == ["Fullname is required"]
    assert body["data"]["register"]["errors"]["password"] == ["Password is required"]

    assert "pythonitalia_sessionid" not in response.cookies


def test_register_password_is_required(full_response_graphql_client):
    body, response = full_response_graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterErrors {
                    errors {
                        password
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "test@email.it",
                "password": "",
                "fullname": "Fullname",
            }
        },
    )

    assert body["data"]["register"]["__typename"] == "RegisterErrors"
    assert body["data"]["register"]["errors"]["password"] == ["Password is required"]

    assert "pythonitalia_sessionid" not in response.cookies


def test_register_email_is_required(graphql_client):
    response = graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterErrors {
                    errors {
                        email
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "",
                "password": "testtest",
                "fullname": "Fullname",
            }
        },
    )

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["errors"]["email"] == ["Email is required"]


def test_register_email_should_be_valid(graphql_client):
    response = graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterErrors {
                    errors {
                        email
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "invalid.email",
                "password": "testtest",
                "fullname": "Fullname",
            }
        },
    )

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["errors"]["email"] == ["Email is not valid"]


def test_register_password_should_be_at_least_8_chars(graphql_client):
    response = graphql_client.query(
        """mutation($input: RegisterInput!) {
            register(input: $input) {
                __typename
                ... on RegisterErrors {
                    errors {
                        password
                    }
                }
            }
        }""",
        variables={
            "input": {
                "email": "invalid.email",
                "password": "a",
                "fullname": "Fullname",
            }
        },
    )

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["errors"]["password"] == [
        "Password must be at least 8 characters"
    ]
