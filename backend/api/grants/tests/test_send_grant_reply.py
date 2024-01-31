from unittest.mock import ANY

import pytest

from grants.models import Grant
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
        "message": message,
        "instance": grant.id,
    }

    return graphql_client.query(document, variables={"input": variables})


def test_user_is_not_the_owner(graphql_client, user, grant_factory):
    graphql_client.force_login(user)
    other_user = UserFactory()
    grant = grant_factory(user_id=other_user.id)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "SendGrantReplyError"
    assert (
        response["data"]["sendGrantReply"]["message"]
        == "You cannot reply to this grant"
    )


def test_user_cannot_reply_if_status_is_pending(graphql_client, user, grant_factory):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.pending)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "SendGrantReplyError"
    assert (
        response["data"]["sendGrantReply"]["message"]
        == "You cannot reply to this grant"
    )


def test_user_cannot_reply_if_status_is_rejected(graphql_client, user, grant_factory):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.rejected)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "SendGrantReplyError"
    assert (
        response["data"]["sendGrantReply"]["message"]
        == "You cannot reply to this grant"
    )


def test_status_is_not_updated_when_the_reply_is_need_info(
    graphql_client, user, grant_factory
):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)

    response = _send_grant_reply(graphql_client, grant, status="need_info")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"

    grant.refresh_from_db()
    assert grant.status == Grant.Status.waiting_for_confirmation


def test_status_is_updated_when_reply_is_confrimed(graphql_client, user, grant_factory):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)

    response = _send_grant_reply(graphql_client, grant, status="confirmed")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"

    grant.refresh_from_db()
    assert grant.status == Grant.Status.confirmed


def test_status_is_updated_when_reply_is_refused(graphql_client, user, grant_factory):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)

    response = _send_grant_reply(graphql_client, grant, status="refused")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"

    grant.refresh_from_db()
    assert grant.status == Grant.Status.refused


def test_send_plain_when_user_send_a_message(
    graphql_client, user, grant_factory, mocker
):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)
    mock_publisher = mocker.patch("api.grants.mutations.send_new_plain_chat")

    response = _send_grant_reply(
        graphql_client, grant, status="need_info", message="wtf"
    )

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"
    mock_publisher.delay.assert_called_once_with(grant_id=grant.id, message="wtf")


def test_call_notify_new_grant_reply(rf, graphql_client, user, grant_factory, mocker):
    graphql_client.force_login(user)
    grant = grant_factory(user_id=user.id, status=Grant.Status.waiting_for_confirmation)
    mock_publisher = mocker.patch("api.grants.mutations.notify_new_grant_reply_slack")
    mock_plain_publisher = mocker.patch("api.grants.mutations.send_new_plain_chat")

    response = _send_grant_reply(graphql_client, grant, status="refused", message="wtf")

    assert response["data"]["sendGrantReply"]["__typename"] == "Grant"
    mock_publisher.delay.assert_called_once_with(grant_id=grant.id, admin_url=ANY)
    mock_plain_publisher.delay.assert_called()
