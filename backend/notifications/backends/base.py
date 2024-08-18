from typing import Dict, List, Optional

from notifications.templates import EmailTemplate


class EmailBackend:
    def __init__(self, environment: Optional[str] = None) -> None:
        self.environment = environment

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
        raise NotImplementedError()

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
        raise NotImplementedError()
