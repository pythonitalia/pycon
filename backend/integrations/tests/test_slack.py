from unittest.mock import patch

from django.test import override_settings
from pytest import raises
from requests import Response

from integrations.slack import SlackIncomingWebhookError, send_message


@override_settings(CFP_SLACK_INCOMING_WEBHOOK_URL="this-is-not-an-url")
def test_send_message_successful():
    r = Response()
    r.status_code = 200

    with patch("integrations.slack.post") as m:
        m.return_value = r
        send_message([], [], channel="cfp")

    assert m.called


@override_settings(CFP_SLACK_INCOMING_WEBHOOK_URL="this-is-not-an-url")
def test_send_message_error():
    r = Response()
    r.status_code = 400

    with patch("integrations.slack.post") as m:
        m.return_value = r
        with raises(SlackIncomingWebhookError):
            send_message([], [], channel="cfp")
