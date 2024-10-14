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


def test_send_grant_reply_rejected_email():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    grant = GrantFactory(user=user)

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_rejected_email(grant_id=grant.id)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": grant.conference.name.localize("en"),
        },
    )


def test_send_grant_reply_waiting_list_email(settings):
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

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_waiting_list_email(grant_id=grant.id)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": grant.conference.name.localize("en"),
            "grants_update_deadline": "1 March 2023",
            "reply_url": "https://pycon.it/grants/reply/",
        },
    )


def test_handle_grant_reply_sent_reminder(settings):
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

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=True)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": grant.conference.name.localize("en"),
            "start_date": "2 May",
            "end_date": "6 May",
            "deadline_date_time": "1 February 2023 23:59 UTC",
            "deadline_date": "1 February 2023",
            "reply_url": "https://pycon.it/grants/reply/",
            "visa_page_link": "https://pycon.it/visa",
            "has_approved_travel": False,
            "has_approved_accommodation": False,
            "is_reminder": True,
        },
    )


def test_handle_grant_approved_ticket_travel_accommodation_reply_sent(settings):
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

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": grant.conference.name.localize("en"),
            "start_date": "2 May",
            "end_date": "6 May",
            "travel_amount": "680",
            "deadline_date_time": "1 February 2023 23:59 UTC",
            "deadline_date": "1 February 2023",
            "reply_url": "https://pycon.it/grants/reply/",
            "visa_page_link": "https://pycon.it/visa",
            "has_approved_travel": True,
            "has_approved_accommodation": True,
            "is_reminder": False,
        },
    )


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


def test_handle_grant_approved_ticket_only_reply_sent(settings):
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

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": grant.conference.name.localize("en"),
            "start_date": "2 May",
            "end_date": "6 May",
            "deadline_date_time": "1 February 2023 23:59 UTC",
            "deadline_date": "1 February 2023",
            "reply_url": "https://pycon.it/grants/reply/",
            "visa_page_link": "https://pycon.it/visa",
            "has_approved_travel": False,
            "has_approved_accommodation": False,
            "is_reminder": False,
        },
    )


def test_handle_grant_approved_travel_reply_sent(settings):
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

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": grant.conference.name.localize("en"),
            "start_date": "2 May",
            "end_date": "6 May",
            "deadline_date_time": "1 February 2023 23:59 UTC",
            "deadline_date": "1 February 2023",
            "reply_url": "https://pycon.it/grants/reply/",
            "visa_page_link": "https://pycon.it/visa",
            "has_approved_travel": True,
            "has_approved_accommodation": False,
            "travel_amount": "400",
            "is_reminder": False,
        },
    )


def test_send_grant_reply_waiting_list_update_email(settings):
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

    with patch("grants.tasks.EmailTemplate") as mock_email_template:
        send_grant_reply_waiting_list_update_email(
            grant_id=grant.id,
        )

    mock_email_template.objects.for_conference().get_by_identifier().send_email.assert_called_once_with(
        recipient=user,
        placeholders={
            "user_name": "Marco Acierno",
            "conference_name": conference_name,
            "grants_update_deadline": "1 March 2023",
            "reply_url": "https://pycon.it/grants/reply/",
        },
    )
