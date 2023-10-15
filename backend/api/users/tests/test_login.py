import pytest

from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_login(full_response_graphql_client):
    user = UserFactory(email="test@example.org", password="test")

    body, response = full_response_graphql_client.query(
        """mutation($input: LoginInput!) {
            login(input: $input) {
                __typename
                ... on LoginSuccess {
                    user {
                        id
                    }
                }
            }
        }""",
        variables={"input": {"email": user.email, "password": "test"}},
    )

    assert body["data"]["login"]["__typename"] == "LoginSuccess"
    assert body["data"]["login"]["user"]["id"] == str(user.id)
    assert "pythonitalia_sessionid" in response.cookies


def test_logins_fails_with_wrong_password(graphql_client):
    user = UserFactory(email="test@example.org", password="test")

    response = graphql_client.query(
        """mutation($input: LoginInput!) {
            login(input: $input) {
                __typename
            }
        }""",
        variables={"input": {"email": user.email, "password": "incorrect"}},
    )

    assert response["data"]["login"]["__typename"] == "WrongEmailOrPassword"


def test_logins_fails_with_all_wrong(graphql_client):
    UserFactory(email="test@example.org", password="test")

    response = graphql_client.query(
        """mutation($input: LoginInput!) {
            login(input: $input) {
                __typename
            }
        }""",
        variables={"input": {"email": "random@exampl.org", "password": "incorrect"}},
    )

    assert response["data"]["login"]["__typename"] == "WrongEmailOrPassword"


def test_logins_fails_with_empty_email(graphql_client):
    UserFactory(email="test@example.org", password="test")

    response = graphql_client.query(
        """mutation($input: LoginInput!) {
            login(input: $input) {
                __typename
                ... on LoginErrors {
                    errors {
                        email
                        password
                    }
                }
            }
        }""",
        variables={"input": {"email": "", "password": "incorrect"}},
    )

    assert response["data"]["login"]["__typename"] == "LoginErrors"
    assert response["data"]["login"]["errors"]["email"] == ["Email is required"]
    assert response["data"]["login"]["errors"]["password"] == []


def test_logins_fails_with_invalid_email(graphql_client):
    UserFactory(email="test@example.org", password="test")

    response = graphql_client.query(
        """mutation($input: LoginInput!) {
            login(input: $input) {
                __typename
                ... on LoginErrors {
                    errors {
                        email
                        password
                    }
                }
            }
        }""",
        variables={"input": {"email": "not.an.email", "password": "incorrect"}},
    )

    assert response["data"]["login"]["__typename"] == "LoginErrors"
    assert response["data"]["login"]["errors"]["email"] == ["Email is not valid"]
    assert response["data"]["login"]["errors"]["password"] == []


def test_logins_fails_with_empty_password(graphql_client):
    UserFactory(email="test@example.org", password="test")

    response = graphql_client.query(
        """mutation($input: LoginInput!) {
            login(input: $input) {
                __typename
                ... on LoginErrors {
                    errors {
                        email
                        password
                    }
                }
            }
        }""",
        variables={"input": {"email": "test@test.it", "password": ""}},
    )

    assert response["data"]["login"]["__typename"] == "LoginErrors"
    assert response["data"]["login"]["errors"]["email"] == []
    assert response["data"]["login"]["errors"]["password"] == ["Password is required"]
