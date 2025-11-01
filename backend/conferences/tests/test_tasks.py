from conferences.tasks import send_conference_voucher_email
from notifications.tests.factories import EmailTemplateFactory
from conferences.tests.factories import ConferenceVoucherFactory
from datetime import datetime, timezone

import time_machine
from conferences.models.conference_voucher import ConferenceVoucher
from users.tests.factories import UserFactory
from notifications.models import EmailTemplateIdentifier

import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "voucher_type",
    [
        ConferenceVoucher.VoucherType.SPEAKER,
        ConferenceVoucher.VoucherType.CO_SPEAKER,
        ConferenceVoucher.VoucherType.GRANT,
    ],
)
def test_send_conference_voucher_email(voucher_type, sent_emails):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    conference_voucher = ConferenceVoucherFactory(
        user=user,
        voucher_type=voucher_type,
        voucher_code="ABC123",
    )

    EmailTemplateFactory(
        conference=conference_voucher.conference,
        identifier=EmailTemplateIdentifier.voucher_code,
    )

    with time_machine.travel("2020-10-10 10:00:00Z", tick=False):
        send_conference_voucher_email(conference_voucher_id=conference_voucher.id)

    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.voucher_code
    assert sent_email.email_template.conference == conference_voucher.conference
    assert sent_email.recipient == user
    assert sent_email.placeholders == {
        "voucher_code": "ABC123",
        "voucher_type": voucher_type,
        "user_name": "Marco Acierno",
    }

    conference_voucher.refresh_from_db()
    assert conference_voucher.voucher_email_sent_at == datetime(
        2020, 10, 10, 10, 0, 0, tzinfo=timezone.utc
    )
