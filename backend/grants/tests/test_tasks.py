from datetime import datetime, timezone
from unittest.mock import patch
from conferences.tests.factories import ConferenceFactory, DeadlineFactory

import pytest
from users.tests.factories import UserFactory

from grants.tests.factories import GrantFactory
from grants.tasks import (
    send_grant_reply_waiting_list_update_email,
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
)
from grants.models import Grant

pytestmark = pytest.mark.django_db


def test_send_grant_reply_rejected_email(sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_rejected
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize("en")


def test_send_grant_reply_waiting_list_email(settings, sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
        type="custom",
        name={
            "en": "Update Grants in Waiting List",
            "it": "Update Grants in Waiting List",
        },
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_waiting_list
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize("en")
    assert sent_email.placeholders["grants_update_deadline"] == "1 March 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"


def test_handle_grant_reply_sent_reminder(settings, sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
        approved_type=Grant.ApprovedType.ticket_only,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        total_amount=680,
        user=user,
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize("en")
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert sent_email.placeholders["has_approved_travel"] == False
    assert sent_email.placeholders["has_approved_accommodation"] == False
    assert sent_email.placeholders["is_reminder"] == True


def test_handle_grant_approved_ticket_travel_accommodation_reply_sent(settings, sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
        approved_type=Grant.ApprovedType.ticket_travel_accommodation,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        travel_amount=680,
        user=user,
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize("en")
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["travel_amount"] == "680"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert sent_email.placeholders["has_approved_travel"] == True
    assert sent_email.placeholders["has_approved_accommodation"] == True
    assert sent_email.placeholders["is_reminder"] == False


def test_handle_grant_approved_ticket_travel_accommodation_fails_with_no_amount(
    settings,
):
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
        approved_type=Grant.ApprovedType.ticket_travel_accommodation,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        travel_amount=0,
        user=user,
    )

    with pytest.raises(
        ValueError, match="Grant travel amount is set to Zero, can't send the email!"
    ):
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)


def test_handle_grant_approved_ticket_only_reply_sent(settings, sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
        approved_type=Grant.ApprovedType.ticket_only,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        total_amount=680,
        user=user,
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize("en")
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert sent_email.placeholders["has_approved_travel"] == False
    assert sent_email.placeholders["has_approved_accommodation"] == False
    assert sent_email.placeholders["is_reminder"] == False


def test_handle_grant_approved_travel_reply_sent(settings, sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
        approved_type=Grant.ApprovedType.ticket_travel,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        total_amount=680,
        travel_amount=400,
        user=user,
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_approved
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == grant.conference.name.localize("en")
    assert sent_email.placeholders["start_date"] == "2 May"
    assert sent_email.placeholders["end_date"] == "6 May"
    assert sent_email.placeholders["deadline_date_time"] == "1 February 2023 23:59 UTC"
    assert sent_email.placeholders["deadline_date"] == "1 February 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
    assert sent_email.placeholders["visa_page_link"] == "https://pycon.it/visa"
    assert sent_email.placeholders["has_approved_travel"] == True
    assert sent_email.placeholders["has_approved_accommodation"] == False
    assert sent_email.placeholders["travel_amount"] == "400"
    assert sent_email.placeholders["is_reminder"] == False


def test_send_grant_reply_waiting_list_update_email(settings, sent_emails):
    from notifications.tests.factories import EmailTemplateFactory
    from notifications.models import EmailTemplateIdentifier
    
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
        type="custom",
        name={
            "en": "Update Grants in Waiting List",
            "it": "Update Grants in Waiting List",
        },
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
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_waiting_list_update
    assert sent_email.email_template.conference == grant.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["conference_name"] == conference_name
    assert sent_email.placeholders["grants_update_deadline"] == "1 March 2023"
    assert sent_email.placeholders["reply_url"] == "https://pycon.it/grants/reply/"
