import json
from typing import Any, Dict, List, Optional
import html
import boto3
from notifications.templates import EmailTemplate
from notifications.emails import SafeString
from notifications.backends.base import EmailBackend


class SESEmailBackend(EmailBackend):
    def __init__(self, environment: str) -> None:
        super().__init__(environment)
        self.ses = boto3.client("ses")

    def send_email(
        self,
        *,
        template: EmailTemplate,
        subject: str,
        from_: str,
        to: str,
        variables: Optional[Dict[str, str]] = None,
        reply_to: List[str] = None,
    ) -> str:
        reply_to = reply_to or []

        variables = self.encode_vars({"subject": subject, **(variables or {})})
        response = self.ses.send_templated_email(
            Source=from_,
            Destination={"ToAddresses": [to]},
            Template=f"pythonit-{self.environment}-{template}",
            TemplateData=json.dumps(variables),
            ReplyToAddresses=reply_to,
            ConfigurationSetName="primary",
        )
        return response["MessageId"]

    def encode_vars(self, variables: dict[str, Any]) -> dict[str, Any]:
        vars = dict()

        for key, value in variables.items():
            if isinstance(value, str) and not isinstance(value, SafeString):
                value = html.escape(value)

            vars[key] = value

        return vars

    def send_raw_email(
        self,
        *,
        from_: str,
        to: str,
        subject: str,
        body: str,
        reply_to: list[str] = None,
        cc: list[str] = None,
        bcc: list[str] = None,
    ) -> str:
        response = self.ses.send_email(
            Source=from_,
            Destination={
                "ToAddresses": [to],
                "CcAddresses": cc or [],
                "BccAddresses": bcc or [],
            },
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body},
                    "Html": {"Data": body},
                },
            },
            ReplyToAddresses=reply_to or [],
            ConfigurationSetName="primary",
        )

        return response["MessageId"]
