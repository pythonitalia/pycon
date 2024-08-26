import pytest
from association_membership.tests.handlers.sns.payloads import (
    BOUNCE_PAYLOAD,
    CLICK_PAYLOAD,
    COMPLAINT_PAYLOAD,
    DELIVERY_PAYLOAD,
    OPEN_PAYLOAD,
    SEND_PAYLOAD,
)
from association_membership.handlers.sns import ses_event
from notifications.models import SentEmailEvent
from notifications.tests.factories import SentEmailFactory


@pytest.mark.parametrize(
    "payload, event_name",
    [
        (BOUNCE_PAYLOAD, SentEmailEvent.Event.bounced),
        (OPEN_PAYLOAD, SentEmailEvent.Event.opened),
        (CLICK_PAYLOAD, SentEmailEvent.Event.clicked),
        (DELIVERY_PAYLOAD, SentEmailEvent.Event.delivered),
        (COMPLAINT_PAYLOAD, SentEmailEvent.Event.complained),
        (SEND_PAYLOAD, SentEmailEvent.Event.sent),
    ],
)
def test_receive_ses_event(payload, event_name):
    sent_email = SentEmailFactory(
        recipient__email="recipient-email@example.com",
        message_id="1111111111111111-11111111-1111-1111-1111-111111111111-000000",
    )
    other_sent_email = SentEmailFactory(
        recipient=sent_email.recipient,
        message_id="222222222222222222222-message",
    )
    other_person_sent_email = SentEmailFactory(
        message_id="33333333333333333-message",
    )

    ses_event(payload)

    sent_email.refresh_from_db()
    other_sent_email.refresh_from_db()
    other_person_sent_email.refresh_from_db()

    assert sent_email.events.count() == 1
    assert other_sent_email.events.count() == 0
    assert other_person_sent_email.events.count() == 0

    event = sent_email.events.first()

    assert event.event == event_name
    assert event.payload == payload
    assert event.timestamp is not None


def test_ses_event_with_no_matching_message():
    sent_email = SentEmailFactory(
        recipient__email="recipient-email@example.com",
        message_id="333333333333333333-message",
    )
    other_sent_email = SentEmailFactory(
        recipient=sent_email.recipient,
        message_id="222222222222222222222-message",
    )

    ses_event(BOUNCE_PAYLOAD)

    sent_email.refresh_from_db()
    other_sent_email.refresh_from_db()

    assert sent_email.events.count() == 0
    assert other_sent_email.events.count() == 0


def test_ses_event_caused_by_another_recipient_is_not_reported():
    sent_email = SentEmailFactory(
        recipient__email="actual-recipient-email@example.com",
        message_id="1111111111111111-11111111-1111-1111-1111-111111111111-000000",
    )
    other_sent_email = SentEmailFactory(
        recipient=sent_email.recipient,
        message_id="222222222222222222222-message",
    )

    ses_event(BOUNCE_PAYLOAD)

    sent_email.refresh_from_db()
    other_sent_email.refresh_from_db()

    assert sent_email.events.count() == 0
    assert other_sent_email.events.count() == 0
