from base64 import urlsafe_b64encode

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import override_settings
from pytest import mark


def _request_password_reset(graphql_client, email):
    return graphql_client.query(
        """mutation($email: String!) {
        requestPasswordReset(input: {
            email: $email
        }) {
            __typename

            ... on OperationResult {
                ok
            }

            ... on RequestPasswordResetMutationErrors {
                email
                nonFieldErrors
            }
        }
    }""",
        variables={"email": email},
    )


def _reset_password(graphql_client, token, userid, password):
    b64_userid = urlsafe_b64encode(bytes(str(userid), "utf-8")).decode("utf-8")
    return graphql_client.query(
        """mutation($encodedUserId: String!, $token: String!, $password: String!) {
        resetPassword(input: {
            encodedUserId: $encodedUserId,
            token: $token,
            password: $password
        }) {
            __typename

            ... on OperationResult {
                ok
            }

            ... on ResetPasswordMutationErrors {
                nonFieldErrors
                token
                password
                encodedUserId
            }
        }
    }""",
        variables={"encodedUserId": b64_userid, "token": token, "password": password},
    )


@override_settings(FRONTEND_URL="http://test.it")
@mark.django_db
def test_request_reset_password_email_for_a_existing_user(user_factory, graphql_client):
    user = user_factory()
    response = _request_password_reset(graphql_client, user.email)

    assert response["data"]["requestPasswordReset"]["__typename"] == "OperationResult"
    assert response["data"]["requestPasswordReset"]["ok"] is True

    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    html_body = email.alternatives[0][0]

    token = default_token_generator.make_token(user)
    userid = urlsafe_b64encode(bytes(str(user.id), "utf-8")).decode("utf-8")

    assert email.to == [user.email]
    assert f"http://test.it/en/reset-password/{userid}/{token}" in email.body
    assert f"http://test.it/en/reset-password/{userid}/{token}" in html_body


@mark.django_db
def test_request_reset_password_with_invalid_user_no_email_sent(
    user_factory, graphql_client
):
    user_factory(email="nina@nana.it")
    response = _request_password_reset(graphql_client, "gianluigi@giorgio.it")

    assert response["data"]["requestPasswordReset"]["__typename"] == "OperationResult"
    assert response["data"]["requestPasswordReset"]["ok"] is True

    assert len(mail.outbox) == 0


@mark.django_db
def test_change_password_via_token(user_factory, graphql_client):
    user = user_factory(password="old")
    token = default_token_generator.make_token(user)

    assert user.check_password("old")

    response = _reset_password(graphql_client, token, user.id, "new")

    user.refresh_from_db()

    assert response["data"]["resetPassword"]["__typename"] == "OperationResult"
    assert response["data"]["resetPassword"]["ok"] is True

    assert not user.check_password("old")
    assert user.check_password("new")


@mark.django_db
def test_cannot_reuse_same_reset_password_token_multiple_times(
    user_factory, graphql_client
):
    user = user_factory(password="old")
    token = default_token_generator.make_token(user)

    assert user.check_password("old")

    response = _reset_password(graphql_client, token, user.id, "new")

    assert response["data"]["resetPassword"]["__typename"] == "OperationResult"
    assert response["data"]["resetPassword"]["ok"] is True

    user.refresh_from_db()
    assert user.check_password("new")

    response = _reset_password(graphql_client, token, user.id, "another")

    assert (
        response["data"]["resetPassword"]["__typename"] == "ResetPasswordMutationErrors"
    )
    assert response["data"]["resetPassword"]["token"] == ["Invalid token"]


@mark.django_db
def test_cannot_reset_password_of_an_unkown_user(user_factory, graphql_client):
    user = user_factory(password="old")
    token = default_token_generator.make_token(user)

    response = _reset_password(graphql_client, token, 5, "another")

    assert (
        response["data"]["resetPassword"]["__typename"] == "ResetPasswordMutationErrors"
    )
    assert response["data"]["resetPassword"]["encodedUserId"] == ["Invalid user"]
