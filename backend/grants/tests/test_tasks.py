from datetime import datetime, timezone
from decimal import Decimal

import pytest
import time_machine

from conferences.models.conference_voucher import ConferenceVoucher
from conferences.tests.factories import (
    ConferenceFactory,
    ConferenceVoucherFactory,
    DeadlineFactory,
)
from grants.models import Grant
from grants.tasks import (
    create_and_send_voucher_to_grantee,
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
    send_grant_reply_waiting_list_update_email,
)
from grants.tests.factories import GrantFactory, GrantReimbursementFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_send_grant_reply_rejected_email(sent_emails):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    grant = GrantFactory(user=user)

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_rejected,
    )

    send_grant_reply_rejected_email(grant_id=grant.id)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier == EmailTemplateIdentifier.grant_rejected
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize(
        "en"
    )


def test_send_grant_reply_waiting_list_email(settings, sent_emails):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    conference = ConferenceFactory()

    settings.FRONTEND_URL = "https://pycon.it"
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    DeadlineFactory(
        start=datetime(2023, 3, 1, 23, 59, tzinfo=timezone.utc),
        conference=conference,
        type="grants_waiting_list_update",
    )
    grant = GrantFactory(conference=conference, user=user)

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_waiting_list,
    )

    send_grant_reply_waiting_list_email(grant_id=grant.id)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier
        == EmailTemplateIdentifier.grant_waiting_list
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize(
        "en"
    )
    assert sent_email.placeholders["grants_update_deadline"] == "1 March 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"


def test_handle_grant_reply_sent_reminder(settings, sent_emails):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    settings.FRONTEND_URL = "https://pycon.it"
    conference = ConferenceFactory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    grant = GrantFactory(
        conference=conference,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        user=user,
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__ticket=True,
        category__max_amount=Decimal("680"),
        granted_amount=Decimal("680"),
    )

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_approved,
    )

    send_grant_reply_approved_email(grant_id=grant.id, is_reminder=True)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize(
        "en"
    )
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert sent_email.placeholders["ticket_only"]
    assert sent_email.placeholders["total_amount"] is None
    assert sent_email.placeholders["is_reminder"]


def test_handle_grant_approved_ticket_travel_accommodation_reply_sent(
    settings, sent_emails
):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    settings.FRONTEND_URL = "https://pycon.it"

    conference = ConferenceFactory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = GrantFactory(
        conference=conference,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        user=user,
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__travel=True,
        category__max_amount=Decimal("680"),
        granted_amount=Decimal("680"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__accommodation=True,
        granted_amount=Decimal("200"),
    )

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_approved,
    )

    send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize(
        "en"
    )
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    # Total amount is 680 (travel) + 200 (accommodation) = 880, excluding ticket
    assert sent_email.placeholders["total_amount"] == "880"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert not sent_email.placeholders["ticket_only"]
    assert not sent_email.placeholders["is_reminder"]


def test_handle_grant_approved_ticket_only_reply_sent(settings, sent_emails):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    settings.FRONTEND_URL = "https://pycon.it"

    conference = ConferenceFactory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = GrantFactory(
        conference=conference,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        user=user,
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__ticket=True,
        category__max_amount=Decimal("680"),
        granted_amount=Decimal("680"),
    )

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_approved,
    )

    send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize(
        "en"
    )
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert sent_email.placeholders["ticket_only"]
    assert sent_email.placeholders["total_amount"] is None
    assert not sent_email.placeholders["is_reminder"]


def test_handle_grant_approved_travel_reply_sent(settings, sent_emails):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    settings.FRONTEND_URL = "https://pycon.it"

    conference = ConferenceFactory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = GrantFactory(
        conference=conference,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        user=user,
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__ticket=True,
        category__max_amount=Decimal("280"),
        granted_amount=Decimal("280"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=conference,
        category__travel=True,
        category__max_amount=Decimal("400"),
        granted_amount=Decimal("400"),
    )

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_approved,
    )

    send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize(
        "en"
    )
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    # Total amount is 400 (travel only), excluding ticket
    assert sent_email.placeholders["total_amount"] == "400"
    assert not sent_email.placeholders["ticket_only"]
    assert not sent_email.placeholders["is_reminder"]


def test_send_grant_approved_email_raises_for_no_reimbursements(settings) -> None:
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    settings.FRONTEND_URL = "https://pycon.it"

    conference = ConferenceFactory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
    )

    grant = GrantFactory(
        conference=conference,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        user=user,
    )
    # No reimbursements - this is an invalid state

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_approved,
    )

    with pytest.raises(
        ValueError, match="has no reimbursement amount and is not ticket-only"
    ):
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)


def test_send_grant_reply_waiting_list_update_email(settings, sent_emails):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    settings.FRONTEND_URL = "https://pycon.it"
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    grant = GrantFactory(user=user)
    DeadlineFactory(
        conference=grant.conference,
        start=datetime(2023, 3, 1, 23, 59, tzinfo=timezone.utc),
        type="grants_waiting_list_update",
    )
    conference_name = grant.conference.name.localize("en")

    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.grant_waiting_list_update,
    )

    send_grant_reply_waiting_list_update_email(
        grant_id=grant.id,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1

    sent_email = emails_sent.first()
    assert (
        sent_email.email_template.identifier
        == EmailTemplateIdentifier.grant_waiting_list_update
    )
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user

    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == conference_name
    assert sent_email.placeholders["grants_update_deadline"] == "1 March 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"


def test_send_grant_waiting_list_email_missing_deadline():
    grant = GrantFactory()

    with pytest.raises(ValueError, match="missing grants_waiting_list_update deadline"):
        send_grant_reply_waiting_list_email(grant_id=grant.id)


def test_create_and_send_voucher_to_grantee(mocker):
    mock_create = mocker.patch(
        "conferences.vouchers.create_voucher", return_value={"id": 123}
    )
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    grant = GrantFactory(status=Grant.Status.confirmed)

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    voucher = ConferenceVoucher.objects.get(
        conference=grant.conference,
        user=grant.user,
        voucher_type=ConferenceVoucher.VoucherType.GRANT,
    )

    mock_create.assert_called_once()
    mock_send_email.delay.assert_called_once_with(conference_voucher_id=voucher.id)


def test_create_and_send_voucher_to_grantee_does_nothing_if_not_confirmed(mocker):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    grant = GrantFactory(status=Grant.Status.waiting_for_confirmation)

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    mock_create.assert_not_called()
    mock_send_email.delay.assert_not_called()


def test_create_and_send_voucher_to_grantee_does_nothing_if_no_user(mocker):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    grant = GrantFactory(status=Grant.Status.confirmed)
    Grant.objects.filter(pk=grant.pk).update(user_id=None)
    grant.refresh_from_db()

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    mock_create.assert_not_called()
    mock_send_email.delay.assert_not_called()


@pytest.mark.parametrize(
    "voucher_type",
    [
        ConferenceVoucher.VoucherType.SPEAKER,
        ConferenceVoucher.VoucherType.GRANT,
    ],
)
def test_create_and_send_voucher_to_grantee_does_nothing_if_voucher_exists(
    mocker, voucher_type
):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    grant = GrantFactory(status=Grant.Status.confirmed)
    ConferenceVoucherFactory(
        conference=grant.conference,
        user=grant.user,
        voucher_type=voucher_type,
        voucher_email_sent_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    mock_create.assert_not_called()
    mock_send_email.delay.assert_not_called()


@pytest.mark.parametrize(
    "voucher_type",
    [
        ConferenceVoucher.VoucherType.SPEAKER,
        ConferenceVoucher.VoucherType.GRANT,
    ],
)
def test_create_and_send_voucher_to_grantee_queues_email_when_voucher_exists_but_never_sent(
    mocker, voucher_type
):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    grant = GrantFactory(status=Grant.Status.confirmed)
    voucher = ConferenceVoucherFactory(
        conference=grant.conference,
        user=grant.user,
        voucher_type=voucher_type,
        voucher_email_sent_at=None,
    )

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    mock_create.assert_not_called()
    mock_send_email.delay.assert_called_once_with(conference_voucher_id=voucher.id)


def test_create_and_send_voucher_to_grantee_upgrades_co_speaker(mocker):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    grant = GrantFactory(status=Grant.Status.confirmed)
    voucher = ConferenceVoucherFactory(
        conference=grant.conference,
        user=grant.user,
        voucher_type=ConferenceVoucher.VoucherType.CO_SPEAKER,
    )

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    voucher.refresh_from_db()
    assert voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT

    mock_create.assert_not_called()
    mock_send_email.delay.assert_called_once_with(conference_voucher_id=voucher.id)


def test_create_and_send_voucher_to_grantee_upgrades_co_speaker_clears_email_sent_at(
    mocker, sent_emails
):
    from notifications.models import EmailTemplateIdentifier
    from notifications.tests.factories import EmailTemplateFactory

    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    grant = GrantFactory(status=Grant.Status.confirmed)
    prior_sent = datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc)
    ConferenceVoucherFactory(
        conference=grant.conference,
        user=grant.user,
        voucher_type=ConferenceVoucher.VoucherType.CO_SPEAKER,
        voucher_email_sent_at=prior_sent,
    )
    EmailTemplateFactory(
        conference=grant.conference,
        identifier=EmailTemplateIdentifier.voucher_code,
    )

    with time_machine.travel("2020-10-10 10:00:00Z", tick=False):
        create_and_send_voucher_to_grantee(grant_id=grant.id)

    mock_create.assert_not_called()
    voucher = ConferenceVoucher.objects.get(
        conference=grant.conference,
        user=grant.user,
    )
    assert voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert voucher.voucher_email_sent_at == datetime(
        2020, 10, 10, 10, 0, 0, tzinfo=timezone.utc
    )
    assert sent_emails().count() == 1
    sent_email = sent_emails().first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.voucher_code
    assert (
        sent_email.placeholders["voucher_type"] == ConferenceVoucher.VoucherType.GRANT
    )


def test_create_and_send_voucher_to_grantee_creates_when_voucher_on_other_conference(
    mocker,
):
    mock_create = mocker.patch(
        "conferences.vouchers.create_voucher", return_value={"id": 123}
    )
    mock_send_email = mocker.patch("conferences.tasks.send_conference_voucher_email")

    other_conference = ConferenceFactory()
    grant = GrantFactory(status=Grant.Status.confirmed)
    ConferenceVoucherFactory(
        conference=other_conference,
        user=grant.user,
        voucher_type=ConferenceVoucher.VoucherType.SPEAKER,
    )

    create_and_send_voucher_to_grantee(grant_id=grant.id)

    assert (
        ConferenceVoucher.objects.for_conference(grant.conference)
        .filter(
            user=grant.user,
            voucher_type=ConferenceVoucher.VoucherType.GRANT,
        )
        .exists()
    )

    voucher = ConferenceVoucher.objects.get(
        conference=grant.conference,
        user=grant.user,
        voucher_type=ConferenceVoucher.VoucherType.GRANT,
    )

    mock_create.assert_called_once()
    mock_send_email.delay.assert_called_once_with(conference_voucher_id=voucher.id)
