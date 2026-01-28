from datetime import datetime, timezone
from decimal import Decimal

import pytest

from conferences.tests.factories import ConferenceFactory, DeadlineFactory
from grants.tasks import (
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
    """Verify error is raised when grant has no valid reimbursements."""
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
    # No deadline created

    with pytest.raises(ValueError, match="missing grants_waiting_list_update deadline"):
        send_grant_reply_waiting_list_email(grant_id=grant.id)
