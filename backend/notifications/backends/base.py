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
