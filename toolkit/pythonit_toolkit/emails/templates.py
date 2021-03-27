from enum import Enum


class EmailTemplate(str, Enum):
    RESET_PASSWORD = "reset-password"

    def __str__(self) -> str:
        return str.__str__(self)
