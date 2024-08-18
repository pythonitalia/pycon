from pytest import raises

from integrations.slack import SlackIncomingWebhookError, send_message


def test_send_message_successful(requests_mock):
    mock_post_message = requests_mock.post(
        "https://slack.com/api/chat.postMessage", status_code=200, json={"ok": True}
    )
    send_message([], [], oauth_token="123", channel_id="c1")

    payload = mock_post_message.last_request.json()
    assert mock_post_message.called
    assert payload["channel"] == "c1"


def test_send_message_error(requests_mock):
    requests_mock.post(
        "https://slack.com/api/chat.postMessage",
        status_code=200,
        json={"ok": False, "error": "error"},
    )

    with raises(SlackIncomingWebhookError) as exc:
        send_message([], [], oauth_token="123", channel_id="c1")

    assert exc.value.args[0] == "error"


def test_send_message_without_channel_does_nothing(requests_mock):
    mock_post_message = requests_mock.post(
        "https://slack.com/api/chat.postMessage", status_code=200, json={"ok": True}
    )
    send_message([], [], oauth_token="123", channel_id="")

    assert not mock_post_message.called


def test_send_message_without_token_does_nothing(requests_mock):
    mock_post_message = requests_mock.post(
        "https://slack.com/api/chat.postMessage", status_code=200, json={"ok": True}
    )
    send_message([], [], oauth_token="", channel_id="c1")

    assert not mock_post_message.called
