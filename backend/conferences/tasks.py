from django.utils import timezone
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from grants.tasks import get_name
import logging
from pycon.celery import app

logger = logging.getLogger(__name__)


@app.task
def send_conference_voucher_email(conference_voucher_id):
    from conferences.models import ConferenceVoucher

    conference_voucher = ConferenceVoucher.objects.get(id=conference_voucher_id)
    conference = conference_voucher.conference

    user = conference_voucher.user
    voucher_code = conference_voucher.voucher_code

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.voucher_code
    )

    email_template.send_email(
        recipient=user,
        placeholders={
            "voucher_code": voucher_code,
            "voucher_type": conference_voucher.voucher_type,
            "user_name": get_name(user, "there"),
        },
    )

    conference_voucher.voucher_email_sent_at = timezone.now()
    conference_voucher.save()
