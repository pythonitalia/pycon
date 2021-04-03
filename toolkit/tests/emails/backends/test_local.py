from unittest.mock import patch

from pythonit_toolkit.emails.backends.local import LocalEmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate
from ward import test


@test("send email just logs the email sent")
async def _():
    with patch("pythonit_toolkit.emails.backends.local.print") as mock_logger:
        LocalEmailBackend().send_email(
            template=EmailTemplate.RESET_PASSWORD,
            from_="from@from.it",
            to="hello@world.it",
            subject="Hello World!",
            variables={"a": "b", "c": "d"},
        )

    assert mock_logger.call_count == 7
    mock_logger.assert_any_call("=== Email sending ===")
    mock_logger.assert_any_call(f"Template: {str(EmailTemplate.RESET_PASSWORD)}")
    mock_logger.assert_any_call("From: from@from.it")
    mock_logger.assert_any_call("To: hello@world.it")
    mock_logger.assert_any_call("Subject: Hello World!")
    mock_logger.assert_any_call("Variables: {'a': 'b', 'c': 'd'}")
    mock_logger.assert_any_call("=== End Email sending ===")
