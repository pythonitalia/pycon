from typing import Dict, List, Optional
from uuid import uuid4

from notifications.templates import EmailTemplate

from notifications.backends.base import EmailBackend


class LocalEmailBackend(EmailBackend):
    def __init__(self, environment: Optional[str] = None) -> None:
        super().__init__(environment=environment)

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

        print("=== Email sending ===")
        print(f"Template: {template}")
        print(f"From: {from_}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Variables: {str(variables)}")
        print(f"Reply to: {str(reply_to)}")
        print("=== End Email sending ===")

        return f"messageid-{uuid4()}"
