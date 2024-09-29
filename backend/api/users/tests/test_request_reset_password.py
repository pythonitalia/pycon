from unittest import mock
from unittest.mock import patch
import pytest

from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_request_reset_password(graphql_client):
    user = UserFactory(full_name="Sushi Op", email="reset@example.org")

    with patch(
        "api.users.mutations.request_reset_password.EmailTemplate"
    ) as mock_email_template:
        body = graphql_client.query(
            """mutation($email: String!) {
                requestResetPassword(email: $email) {
                    __typename
                    ... on OperationSuccess {
                        ok
                    }
                }
            }""",
            variables={"email": user.email},
        )

    assert body["data"]["requestResetPassword"]["__typename"] == "OperationSuccess"
    assert body["data"]["requestResetPassword"]["ok"] is True

    mock_email_template.objects.system_templates().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Sushi Op",
            "reset_password_link": mock.ANY,
        },
    )


def test_request_reset_password_fails_with_not_active_user(graphql_client):
    user = UserFactory(email="reset@example.org", is_active=False)

    body = graphql_client.query(
        """mutation($email: String!) {
            requestResetPassword(email: $email) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={"email": user.email},
    )

    assert body["data"]["requestResetPassword"]["__typename"] == "OperationSuccess"
    assert body["data"]["requestResetPassword"]["ok"] is False


def test_request_reset_password_fails_with_not_existing_user(graphql_client):
    UserFactory(email="reset@example.org", is_active=True)

    body = graphql_client.query(
        """mutation($email: String!) {
            requestResetPassword(email: $email) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={"email": "another@example.org"},
    )

    assert body["data"]["requestResetPassword"]["__typename"] == "OperationSuccess"
    assert body["data"]["requestResetPassword"]["ok"] is False


def test_request_reset_password_fails_with_empty_email(graphql_client):
    UserFactory(email="reset@example.org", is_active=True)

    body = graphql_client.query(
        """mutation($email: String!) {
            requestResetPassword(email: $email) {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={"email": ""},
    )

    assert body["data"]["requestResetPassword"]["__typename"] == "OperationSuccess"
    assert body["data"]["requestResetPassword"]["ok"] is False
