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
    SUBMISSION_ACCEPTED = "submission-accepted"
    SUBMISSION_REJECTED = "submission-rejected"
    SUBMISSION_IN_WAITING_LIST = "submission-in-waiting-list"
    SUBMISSION_SCHEDULE_TIME_CHANGED = "submission-schedule-time-change"
    SPEAKER_VOUCHER_CODE = "speaker-voucher-code"
    SPEAKER_COMMUNICATION = "speaker-communication"

    # Deprecated
    NEW_COMMENT_ON_SUBMISSION = "new-comment-on-submission"
    NEW_SCHEDULE_INVITATION_ANSWER = "new-schedule-invitation-answer"

    def __str__(self) -> str:
        return str.__str__(self)
