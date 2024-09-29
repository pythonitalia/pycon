from enum import Enum


class EmailTemplate(str, Enum):
    # Grants
    GRANT_APPROVED = "grants-approved"
    GRANT_WAITING_LIST = "grants-waiting-list"
    GRANT_WAITING_LIST_UPDATE = "grants-waiting-list-update"
    GRANT_VOUCHER_CODE = "grants-voucher-code"
    GRANT_REJECTED = "grants-rejected"

    # Users
    RESET_PASSWORD = "reset-password"

    # Submissions
    SUBMISSION_SCHEDULE_TIME_CHANGED = "submission-schedule-time-change"
    SPEAKER_COMMUNICATION = "speaker-communication"

    def __str__(self) -> str:
        return str.__str__(self)
