from unittest.mock import patch

from pythonit_toolkit.emails.backends.ses import SESEmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate
from ward import test


@test("send email via ses")
async def _():
    with patch("pythonit_toolkit.emails.backends.ses.boto3") as mock_boto:
        SESEmailBackend("production").send_email(
            template=EmailTemplate.RESET_PASSWORD,
            subject="Subject",
            from_="test@email.it",
            to="destination@email.it",
            variables={"a": "b", "c": "d"},
        )

    mock_boto.client.return_value.send_templated_email.assert_called_once_with(
        Source="test@email.it",
        Destination={"ToAddresses": ["destination@email.it"]},
        Template="pythonit-production-reset-password",
        TemplateData='{"subject": "Subject", "a": "b", "c": "d"}',
    )


@test("send email without variables")
async def _():
    with patch("pythonit_toolkit.emails.backends.ses.boto3") as mock_boto:
        SESEmailBackend("production").send_email(
            template=EmailTemplate.RESET_PASSWORD,
            subject="Subject",
            from_="test@email.it",
            to="destination@email.it",
        )

    mock_boto.client.return_value.send_templated_email.assert_called_once_with(
        Source="test@email.it",
        Destination={"ToAddresses": ["destination@email.it"]},
        Template="pythonit-production-reset-password",
        TemplateData='{"subject": "Subject"}',
    )
