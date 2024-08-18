import logging
from django.utils import timezone
from django.conf import settings
from notifications.emails import get_email_backend
from notifications.models import SentEmail
from django.db import transaction
from pycon.celery import app

logger = logging.getLogger(__name__)


@app.task
def send_pending_emails():
    pending_emails = SentEmail.objects.pending().values_list("id", flat=True)
    total_pending_emails = pending_emails.count()

    if total_pending_emails == 0:
        return

    logger.info(f"Found {pending_emails.count()} pending emails")

    for email_id in pending_emails.all():
        with transaction.atomic():
            sent_email = (
                SentEmail.objects.select_for_update(skip_locked=True)
                .filter(
                    id=email_id,
                )
                .first()
            )

            if not sent_email:
                continue

            if not sent_email.is_pending:
                continue

            logger.info(f"Sending email {sent_email.id}")

            from_email = settings.DEFAULT_EMAIL_FROM
            backend = get_email_backend(
                settings.PYTHONIT_EMAIL_BACKEND, environment=settings.ENVIRONMENT
            )
            message_id = backend.send_raw_email(
                from_=from_email,
                to=sent_email.recipient_email,
                subject=sent_email.subject,
                body=sent_email.body,
                reply_to=sent_email.reply_to,
                cc=sent_email.cc_addresses,
                bcc=sent_email.bcc_addresses,
            )

            sent_email.status = SentEmail.Status.sent
            sent_email.sent_at = timezone.now()
            sent_email.message_id = message_id
            sent_email.save(update_fields=["status", "sent_at", "message_id"])

            logger.info(f"Email {sent_email.id} sent with message id {message_id}")
