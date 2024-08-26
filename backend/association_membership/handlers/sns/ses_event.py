import logging
from typing import Any


from notifications.models import SentEmail, SentEmailEvent


logger = logging.getLogger(__file__)


SES_EVENT_TYPE_TO_LOCAL_EVENT_TYPE = {
    "Bounce": SentEmailEvent.Event.bounced,
    "Complaint": SentEmailEvent.Event.complained,
    "Delivery": SentEmailEvent.Event.delivered,
    "Send": SentEmailEvent.Event.sent,
    "Reject": SentEmailEvent.Event.rejected,
    "Open": SentEmailEvent.Event.opened,
    "Click": SentEmailEvent.Event.clicked,
}


def ses_event(payload: Any) -> None:
    message_id = payload["mail"]["messageId"]
    affected_recipients = _get_affected_recipients(payload)
    timestamp = _get_timestamp(payload)
    event_type = payload["eventType"]

    try:
        sent_email = SentEmail.objects.get_by_message_id(message_id)
    except SentEmail.DoesNotExist:
        logger.error("SentEmail not found for message_id=%s", message_id)
        return

    recipient_email_address = sent_email.recipient_email

    if any(
        recipient_email_address == affected_recipient
        for affected_recipient in affected_recipients
    ):
        sent_email.record_event(
            SES_EVENT_TYPE_TO_LOCAL_EVENT_TYPE.get(event_type), timestamp, payload
        )


def _get_affected_recipients(payload: Any) -> list[str]:
    event_type = payload["eventType"]

    match event_type:
        case "Bounce":
            return [
                recipient["emailAddress"]
                for recipient in payload["bounce"]["bouncedRecipients"]
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
    event_type = payload["eventType"].lower()
    if event_type in ("bounce", "complaint", "delivery", "click", "open"):
        return payload[event_type]["timestamp"]

    return payload["mail"]["timestamp"]
