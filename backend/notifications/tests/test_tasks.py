import smtplib
from unittest.mock import patch
from uuid import uuid4
import time_machine
from django.core import mail
from notifications.tasks import send_pending_email, send_pending_email_failed
from notifications.models import SentEmail
from notifications.tests.factories import SentEmailFactory


def test_send_pending_email_does_nothing_with_non_pending_email():
    sent_email = SentEmailFactory(
        status=SentEmail.Status.sent, sent_at="2020-01-01 12:00Z"
    )

    send_pending_email(sent_email.id)

    assert len(mail.outbox) == 0


def test_send_pending_email_task_sends_data_correctly():
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

    with time_machine.travel("2021-01-01 12:00Z", tick=False):
        send_pending_email(pending_email_1.id)

    assert len(mail.outbox) == 1

    assert mail.outbox[0].to == [pending_email_1.recipient_email]
    assert mail.outbox[0].reply_to == ["reply@example.com"]
    assert mail.outbox[0].cc == ["cc@example.com"]
    assert mail.outbox[0].bcc == ["bcc@example.com"]
    assert mail.outbox[0].from_email == "from@example.com"
    assert mail.outbox[0].body == "text body"
    assert mail.outbox[0].alternatives == [("html body", "text/html")]
    assert mail.outbox[0].subject == "subject"

    pending_email_1.refresh_from_db()

    assert len(mail.outbox) == 1

    assert pending_email_1.status == SentEmail.Status.sent
    assert pending_email_1.message_id.startswith("local-")
    assert pending_email_1.sent_at.isoformat() == "2021-01-01T12:00:00+00:00"


def test_send_pending_email_task_doesnt_double_send():
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
        send_pending_email(pending_email_1.id)

    pending_email_1.refresh_from_db()

    assert len(mail.outbox) == 0


def test_send_pending_email_failure():
    pending_email_1 = SentEmailFactory(
        status=SentEmail.Status.pending, created="2020-01-01 12:00Z"
    )

    send_pending_email_failed(
        None,
        smtplib.SMTPException("test"),
        uuid4().hex,
        (pending_email_1.id,),
        {},
        None,
    )

    pending_email_1.refresh_from_db()

    assert len(mail.outbox) == 0
    assert pending_email_1.status == SentEmail.Status.failed
