import json
from typing import Optional

import boto3
from pythonit_toolkit.emails.templates import EmailTemplate

from .base import EmailBackend


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
        variables: Optional[dict[str, str]] = None,
    ):
        variables = {"subject": subject, **(variables or {})}
        self.ses.send_templated_email(
            Source=from_,
            Destination={"ToAddresses": [to]},
            Template=f"pythonit-{self.environment}-{template}",
            TemplateData=json.dumps(variables),
        )
