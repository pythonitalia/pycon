import logging
from typing import Any


from notifications.models import SentEmail, SentEmailEvent


logger = logging.getLogger(__file__)


def ses_event(payload: Any) -> None:
    message_id = payload["mail"]["messageId"]
    affected_recipients = _get_affected_recipients(payload)
    timestamp = _get_timestamp(payload)

    sent_email = SentEmail.objects.get_by_message_id(message_id)

    if not sent_email:
        logger.error("SentEmail not found for message_id=%s", message_id)
        return

    recipient_email_address = sent_email.recipient_email

    if any(
        recipient_email_address == bounced_recipient
        for bounced_recipient in affected_recipients
    ):
        sent_email.record_event(SentEmailEvent.Event.bounced, timestamp, payload)


def _get_affected_recipients(payload: Any) -> list[str]:
    notification_type = payload["eventType"]
    match notification_type:
        case "Bounce":
            return [
                recipient["emailAddress"]
                for recipient in payload["complaint"]["bouncedRecipients"]
            ]
        case "Complaint":
            return [
                recipient["emailAddress"]
                for recipient in payload["complaint"]["complainedRecipients"]
            ]
        case "Delivery":
            return payload["delivery"]["recipients"]
        case _:
            return payload["mail"]["destination"]


def _get_timestamp(payload: dict) -> str:
    notification_type = payload["eventType"]
    match notification_type:
        case "Bounce":
            return payload["bounce"]["timestamp"]
        case "Complaint":
            return payload["complaint"]["timestamp"]
        case "Delivery":
            return payload["delivery"]["timestamp"]
        case _:
            return payload["mail"]["timestamp"]
