import time_machine
import pytest
from api.users.mutations.request_reset_password import _create_reset_password_token

from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_reset_password(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )
    token = _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "newpassword1",
            }
        },
    )

    assert body["data"]["resetPassword"]["ok"] is True
    user.refresh_from_db()
    assert user.check_password("newpassword1")
    assert user.jwt_auth_id == 2


def test_cannot_reset_password_of_not_active_user(graphql_client):
    user = UserFactory(
        email="reset@example.org",
        password="old-password",
        jwt_auth_id=1,
        is_active=False,
    )
    token = _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "newpassword1",
            }
        },
    )

    assert body["data"]["resetPassword"]["ok"] is False
    user.refresh_from_db()
    assert user.check_password("old-password")
    assert user.jwt_auth_id == 1


def test_cannot_reset_password_of_not_existing_user(graphql_client):
    user = UserFactory(
        email="reset@example.org",
        password="old-password",
        jwt_auth_id=1,
        is_active=False,
    )
    token = _create_reset_password_token(user=user)
    user.delete()

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "newpassword1",
            }
        },
    )

    assert body["data"]["resetPassword"]["ok"] is False


def test_cannot_reuse_reset_password_token(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )
    token = _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "newpassword1",
            }
        },
    )

    assert body["data"]["resetPassword"]["ok"] is True
    user.refresh_from_db()
    assert user.check_password("newpassword1")
    assert user.jwt_auth_id == 2

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on ResetPasswordErrors {
                    errors {
                        token
                    }
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "anotherchange",
            }
        },
    )

    assert body["data"]["resetPassword"]["__typename"] == "ResetPasswordErrors"
    assert body["data"]["resetPassword"]["errors"]["token"] == ["Invalid token"]
    user.refresh_from_db()
    assert user.check_password("newpassword1")
    assert user.jwt_auth_id == 2


def test_cannot_use_expired_token(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )

    with time_machine.travel("1995-10-10 10:00:00", tick=False):
        token = _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on ResetPasswordErrors {
                    errors {
                        token
                    }
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "anotherchange",
            }
        },
    )

    assert body["data"]["resetPassword"]["__typename"] == "ResetPasswordErrors"
    assert body["data"]["resetPassword"]["errors"]["token"] == ["Token has expired"]
    user.refresh_from_db()
    assert user.check_password("old-password")
    assert user.jwt_auth_id == 1


def test_cannot_use_random_invalid_token(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on ResetPasswordErrors {
                    errors {
                        token
                    }
                }
            }
        }""",
        variables={
            "input": {
                "token": "hell1",
                "newPassword": "anotherchange",
            }
        },
    )

    assert body["data"]["resetPassword"]["__typename"] == "ResetPasswordErrors"
    assert body["data"]["resetPassword"]["errors"]["token"] == ["Invalid token"]
    user.refresh_from_db()
    assert user.check_password("old-password")
    assert user.jwt_auth_id == 1


def test_token_cannot_be_empty(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )

    _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on ResetPasswordErrors {
                    errors {
                        token
                    }
                }
            }
        }""",
        variables={
            "input": {
                "token": "",
                "newPassword": "newpassword1",
            }
        },
    )

    assert body["data"]["resetPassword"]["__typename"] == "ResetPasswordErrors"
    assert body["data"]["resetPassword"]["errors"]["token"] == ["Token is required"]
    user.refresh_from_db()
    assert user.check_password("old-password")
    assert user.jwt_auth_id == 1


def test_new_password_cannot_be_empty(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )

    token = _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on ResetPasswordErrors {
                    errors {
                        newPassword
                    }
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "",
            }
        },
    )

    assert body["data"]["resetPassword"]["__typename"] == "ResetPasswordErrors"
    assert body["data"]["resetPassword"]["errors"]["newPassword"] == [
        "New password is required"
    ]
    user.refresh_from_db()
    assert user.check_password("old-password")
    assert user.jwt_auth_id == 1


def test_new_password_has_to_be_at_least_8_chars(graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )

    token = _create_reset_password_token(user=user)

    body = graphql_client.query(
        """mutation($input: ResetPasswordInput!) {
            resetPassword(input: $input) {
                __typename
                ... on ResetPasswordErrors {
                    errors {
                        newPassword
                    }
                }
            }
        }""",
        variables={
            "input": {
                "token": token,
                "newPassword": "short",
            }
        },
    )

    assert body["data"]["resetPassword"]["__typename"] == "ResetPasswordErrors"
    assert body["data"]["resetPassword"]["errors"]["newPassword"] == [
        "Password must be at least 8 characters"
    ]
    user.refresh_from_db()
    assert user.check_password("old-password")
    assert user.jwt_auth_id == 1
