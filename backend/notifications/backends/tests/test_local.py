from unittest.mock import patch

from notifications.backends.local import LocalEmailBackend
from notifications.templates import EmailTemplate


def test_local_email_just_logs():
    with patch("notifications.backends.local.print") as mock_logger:
        LocalEmailBackend().send_email(
            template=EmailTemplate.RESET_PASSWORD,
            from_="from@from.it",
            to="hello@world.it",
            subject="Hello World!",
            variables={"a": "b", "c": "d"},
            reply_to=["test@placeholder.com"],
        )

    assert mock_logger.call_count == 8
    mock_logger.assert_any_call("=== Email sending ===")
    mock_logger.assert_any_call(f"Template: {str(EmailTemplate.RESET_PASSWORD)}")
    mock_logger.assert_any_call("From: from@from.it")
    mock_logger.assert_any_call("To: hello@world.it")
    mock_logger.assert_any_call("Subject: Hello World!")
    mock_logger.assert_any_call("Variables: {'a': 'b', 'c': 'd'}")
    mock_logger.assert_any_call("Reply to: ['test@placeholder.com']")
    mock_logger.assert_any_call("=== End Email sending ===")
