from pythonit_toolkit.emails.templates import EmailTemplate
import pytest

from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_request_reset_password(graphql_client, sent_emails):
    user = UserFactory(email="reset@example.org")

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

    assert sent_emails[0]["template"] == EmailTemplate.RESET_PASSWORD
    assert sent_emails[0]["subject"] == "Reset your password"
    assert (
        "https://pycon.it/reset-password/"
        in sent_emails[0]["variables"]["resetpasswordlink"]
    )


def test_request_reset_password_fails_with_not_active_user(graphql_client, sent_emails):
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

    assert len(sent_emails) == 0


def test_request_reset_password_fails_with_not_existing_user(
    graphql_client, sent_emails
):
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

    assert len(sent_emails) == 0


def test_request_reset_password_fails_with_empty_email(graphql_client, sent_emails):
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

    assert len(sent_emails) == 0
