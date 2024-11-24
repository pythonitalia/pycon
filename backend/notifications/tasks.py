from celery.exceptions import MaxRetriesExceededError
import logging
import smtplib
from uuid import uuid4
from notifications.models import SentEmail
from django.db import transaction
from pycon.celery import app
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection

logger = logging.getLogger(__name__)


@app.task(
    bind=True,
    retry_backoff=5,
    max_retries=5,
)
@transaction.atomic()
def send_pending_email(self, sent_email_id: int):
    logger.info(
        "Sending sent_email=%s (retry=%s of %s)",
        sent_email_id,
        self.request.retries,
        self.max_retries,
    )

    sent_email = (
        SentEmail.objects.select_for_update(skip_locked=True)
        .pending()
        .filter(id=sent_email_id)
        .first()
    )

    if not sent_email:
        return

    try:
        email_backend_connection = get_connection()

        message_id = send_email(sent_email, email_backend_connection)
        sent_email.mark_as_sent(message_id)
    except smtplib.SMTPException as e:
        try:
            raise self.retry(e)
        except MaxRetriesExceededError:
            sent_email.mark_as_failed()
            logger.error(
                "Failed to send email sent_email_id=%s",
                sent_email.id,
            )
            return
    except Exception as e:
        sent_email.mark_as_failed()
        logger.error(
            "Failed to send email sent_email_id=%s",
            sent_email.id,
        )
        raise e

    logger.info(
        "Email sent_email_id=%s sent with message_id=%s",
        sent_email.id,
        message_id,
    )


def send_email(sent_email, email_backend_connection):
    logger.info(f"Sending sent_email_id={sent_email.id}")

    email_message = EmailMultiAlternatives(
        subject=sent_email.subject,
        body=sent_email.text_body,
        from_email=sent_email.from_email,
        to=[sent_email.recipient_email],
        cc=sent_email.cc_addresses,
        bcc=sent_email.bcc_addresses,
        reply_to=[sent_email.reply_to],
        connection=email_backend_connection,
    )
    email_message.attach_alternative(sent_email.body, "text/html")
    email_message.send()
    return email_message.extra_headers.get("message_id", f"local-{uuid4()}")
