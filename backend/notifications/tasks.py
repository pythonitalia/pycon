import logging
from uuid import uuid4
from pycon.celery_utils import OnlyOneAtTimeTask
from notifications.models import SentEmail
from django.db import transaction
from pycon.celery import app
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection

logger = logging.getLogger(__name__)


@app.task(base=OnlyOneAtTimeTask)
def send_pending_emails():
    pending_emails = (
        SentEmail.objects.pending().order_by("created").values_list("id", flat=True)
    )
    total_pending_emails = pending_emails.count()

    if total_pending_emails == 0:
        return

    logger.info(f"Found {pending_emails.count()} pending emails")

    email_backend_connection = get_connection()

    for email_id in pending_emails.iterator():
        with transaction.atomic():
            sent_email = (
                SentEmail.objects.select_for_update(skip_locked=True)
                .filter(
                    id=email_id,
                )
                .first()
            )

            if not sent_email or not sent_email.is_pending:
                continue

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

            message_id = email_message.extra_headers.get(
                "message_id", f"local-{uuid4()}"
            )
            sent_email.mark_as_sent(message_id)

            logger.info(
                f"Email sent_email_id={sent_email.id} sent with message_id={message_id}"
            )
