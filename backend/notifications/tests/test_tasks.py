from unittest.mock import patch
import time_machine
from django.core import mail
from notifications.tasks import send_pending_emails
from notifications.models import SentEmail
from notifications.tests.factories import SentEmailFactory


def test_send_pending_emails_does_nothing_with_no_pending_emails():
    SentEmailFactory(status=SentEmail.Status.sent, sent_at="2020-01-01 12:00Z")
    SentEmailFactory(status=SentEmail.Status.sent, sent_at="2020-01-01 12:00Z")
    SentEmailFactory(status=SentEmail.Status.sent, sent_at="2020-01-01 12:00Z")
    SentEmailFactory(status=SentEmail.Status.sent, sent_at="2020-01-01 12:00Z")

    send_pending_emails()

    assert len(mail.outbox) == 0


def test_send_pending_emails_task_sends_data_correctly():
    pending_email_1 = SentEmailFactory(
        status=SentEmail.Status.pending,
        reply_to="reply@example.com",
        cc_addresses=["cc@example.com"],
        bcc_addresses=["bcc@example.com"],
        from_email="from@example.com",
        body="html body",
        text_body="text body",
        subject="subject",
    )

    send_pending_emails()

    assert len(mail.outbox) == 1

    assert mail.outbox[0].to == [pending_email_1.recipient_email]
    assert mail.outbox[0].reply_to == ["reply@example.com"]
    assert mail.outbox[0].cc == ["cc@example.com"]
    assert mail.outbox[0].bcc == ["bcc@example.com"]
    assert mail.outbox[0].from_email == "from@example.com"
    assert mail.outbox[0].body == "text body"
    assert mail.outbox[0].alternatives == [("html body", "text/html")]
    assert mail.outbox[0].subject == "subject"


def test_send_pending_emails_task_doesnt_double_send():
    pending_email_1 = SentEmailFactory(status=SentEmail.Status.pending)
    original_qs = SentEmail.objects.select_for_update(skip_locked=True).filter(
        id=pending_email_1.id
    )

    def side_effect(*args, **kwargs):
        pending_email_1.mark_as_sent("abc-abc")
        return original_qs

    with patch(
        "notifications.tasks.SentEmail.objects.select_for_update",
        side_effect=side_effect,
    ):
        send_pending_emails()

    pending_email_1.refresh_from_db()

    assert len(mail.outbox) == 0


def test_send_pending_emails_task():
    pending_email_1 = SentEmailFactory(status=SentEmail.Status.pending)
    pending_email_2 = SentEmailFactory(status=SentEmail.Status.pending)
    sent_email_1 = SentEmailFactory(
        status=SentEmail.Status.sent, message_id="abc-abc", sent_at="2020-01-01 12:00Z"
    )

    with time_machine.travel("2021-01-01 12:00Z", tick=False):
        send_pending_emails()

    pending_email_1.refresh_from_db()
    pending_email_2.refresh_from_db()
    sent_email_1.refresh_from_db()

    assert len(mail.outbox) == 2

    assert mail.outbox[0].to == [pending_email_1.recipient_email]
    assert mail.outbox[1].to == [pending_email_2.recipient_email]

    assert pending_email_1.status == SentEmail.Status.sent
    assert pending_email_1.message_id.startswith("local-")
    assert pending_email_1.sent_at.isoformat() == "2021-01-01T12:00:00+00:00"

    assert pending_email_2.status == SentEmail.Status.sent
    assert pending_email_2.message_id.startswith("local-")
    assert pending_email_2.sent_at.isoformat() == "2021-01-01T12:00:00+00:00"

    assert sent_email_1.status == SentEmail.Status.sent
    assert sent_email_1.message_id == "abc-abc"
    assert sent_email_1.sent_at.isoformat() == "2020-01-01T12:00:00+00:00"


def test_send_pending_emails_handles_failures(mocker):
    pending_email_1 = SentEmailFactory(
        status=SentEmail.Status.pending, created="2020-01-01 12:00Z"
    )
    pending_email_2 = SentEmailFactory(
        status=SentEmail.Status.pending, created="2020-01-02 12:00Z"
    )

    original_method = SentEmail.mark_as_sent

    def _side_effect(*args, **kwargs):
        if _side_effect.counter == 0:
            _side_effect.counter = 1
            raise ValueError("test")

        return original_method(pending_email_2, *args, **kwargs)

    _side_effect.counter = 0

    mocker.patch("notifications.tasks.SentEmail.mark_as_sent", side_effect=_side_effect)

    with time_machine.travel("2021-01-01 12:00Z", tick=False):
        send_pending_emails()

    pending_email_1.refresh_from_db()
    pending_email_2.refresh_from_db()

    assert len(mail.outbox) == 2

    assert mail.outbox[0].to == [pending_email_1.recipient_email]
    assert mail.outbox[1].to == [pending_email_2.recipient_email]

    assert pending_email_1.status == SentEmail.Status.failed
    assert pending_email_1.message_id == ""
    assert pending_email_1.sent_at is None

    assert pending_email_2.status == SentEmail.Status.sent
    assert pending_email_2.message_id.startswith("local-")
    assert pending_email_2.sent_at.isoformat() == "2021-01-01T12:00:00+00:00"
