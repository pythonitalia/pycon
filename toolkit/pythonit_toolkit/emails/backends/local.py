from typing import Optional

from pythonit_toolkit.emails.templates import EmailTemplate

from .base import EmailBackend


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
        variables: Optional[dict[str, str]] = None,
    ):
        print("=== Email sending ===")
        print(f"Template: {template}")
        print(f"From: {from_}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Variables: {str(variables)}")
        print("=== End Email sending ===")
