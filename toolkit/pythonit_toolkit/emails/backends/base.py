from abc import ABC, abstractmethod
from typing import Optional

from pythonit_toolkit.emails.templates import EmailTemplate


class EmailBackend(ABC):
    def __init__(self, environment: Optional[str] = None) -> None:
        self.environment = environment

    @abstractmethod
    def send_email(
        self,
        *,
        template: EmailTemplate,
        subject: str,
        from_: str,
        to: str,
        variables: Optional[dict[str, str]] = None
    ):
        pass
