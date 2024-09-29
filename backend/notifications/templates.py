from enum import Enum


class EmailTemplate(str, Enum):
    # Grants
    GRANT_VOUCHER_CODE = "grants-voucher-code"

    # Users
    RESET_PASSWORD = "reset-password"

    # Submissions
    SPEAKER_COMMUNICATION = "speaker-communication"

    def __str__(self) -> str:
        return str.__str__(self)
