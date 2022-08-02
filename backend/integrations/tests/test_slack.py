from unittest.mock import patch

from pytest import raises
from requests import Response

from integrations.slack import SlackIncomingWebhookError, send_message


def test_send_message_successful():
    r = Response()
    r.status_code = 200

    with patch("integrations.slack.post") as m:
        m.return_value = r
        send_message([], [], token="123")

    assert m.called


def test_send_message_error():
    r = Response()
    r.status_code = 400

    with patch("integrations.slack.post") as m:
        m.return_value = r
        with raises(SlackIncomingWebhookError):
            send_message([], [], token="123")
