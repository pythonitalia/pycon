from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from emails.templates import EmailTemplate


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
        variables: Optional[Dict[str, str]] = None,
        reply_to: List[str] = None,
    ) -> str:
        pass
