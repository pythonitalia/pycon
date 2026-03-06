from unittest.mock import ANY

import pytest
from django.contrib.admin.models import LogEntry

from grants.models import Grant
from grants.tests.factories import GrantFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _send_grant_reply(graphql_client, grant, *, status, message=""):
    document = """
    mutation sendGrantReply ($input: SendGrantReplyInput!) {
        sendGrantReply(input: $input) {
            __typename

            ...on Grant {
                id
            }

            ...on SendGrantReplyError {
                message
            }
        }
    }
    """

    variables = {
        "status": status,
        "instance": grant.id,
    }

    return graphql_client.query(document, variables={"input": variables})


def test_user_is_not_the_owner(graphql_client, user):
    graphql_client.force_login(user)
    other_user = UserFactory()
    grant = GrantFactory(user_id=other_user.id)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "SendGrantReplyError"
    assert (
        response["data"]["sendGrantReply"]["message"]
        == "You cannot reply to this grant"
    )


def test_user_cannot_reply_if_status_is_pending(graphql_client, user):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.pending)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "SendGrantReplyError"
    assert (
        response["data"]["sendGrantReply"]["message"]
        == "You cannot reply to this grant"
    )


def test_user_cannot_reply_if_status_is_rejected(graphql_client, user):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.rejected)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "SendGrantReplyError"
    assert (
        response["data"]["sendGrantReply"]["message"]
        == "You cannot reply to this grant"
    )


def test_status_is_updated_when_reply_is_confirmed(graphql_client, user):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)

    response = _send_grant_reply(graphql_client, grant, status="confirmed")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"

    grant.refresh_from_db()
    assert grant.status == Grant.Status.confirmed

    # Verify audit log entry was created correctly
    assert LogEntry.objects.filter(
        user=user,
        object_id=grant.id,
        change_message="Grantee has replied with status confirmed.",
    ).exists()


def test_status_is_updated_when_reply_is_refused(graphql_client, user):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"

    grant.refresh_from_db()
    assert grant.status == Grant.Status.refused

    # Verify audit log entry was created correctly
    assert LogEntry.objects.filter(
        user=user,
        object_id=grant.id,
        change_message="Grantee has replied with status refused.",
    ).exists()


def test_call_notify_new_grant_reply(graphql_client, user, mocker):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)
    mock_publisher = mocker.patch("api.grants.mutations.notify_new_grant_reply_slack")

    response = _send_grant_reply(graphql_client, grant, status="refused", message="wtf")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"
    mock_publisher.delay.assert_called_once_with(grant_id=grant.id, admin_url=ANY)


def test_create_voucher_when_grant_is_confirmed(graphql_client, user, mocker):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)
    mock_voucher_task = mocker.patch(
        "api.grants.mutations.create_and_send_grant_voucher"
    )

    response = _send_grant_reply(graphql_client, grant, status="confirmed")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"
    mock_voucher_task.delay.assert_called_once_with(grant_id=grant.id)


def test_voucher_not_created_when_grant_is_refused(graphql_client, user, mocker):
    graphql_client.force_login(user)
    grant = GrantFactory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)
    mock_voucher_task = mocker.patch(
        "api.grants.mutations.create_and_send_grant_voucher"
    )

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"
    mock_voucher_task.delay.assert_not_called()
