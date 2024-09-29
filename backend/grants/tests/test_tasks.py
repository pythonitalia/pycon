from datetime import datetime, timezone
from unittest.mock import patch
from conferences.tests.factories import ConferenceFactory, DeadlineFactory

import pytest
from users.tests.factories import UserFactory
from notifications.templates import EmailTemplate

from grants.tests.factories import GrantFactory
from grants.tasks import (
    send_grant_reply_waiting_list_update_email,
    send_grant_voucher_email,
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
)
from grants.models import Grant

pytestmark = pytest.mark.django_db


def test_send_grant_voucher_email(settings):
    settings.FRONTEND_URL = "https://pycon.it"
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = GrantFactory(
        user=user,
        voucher_code="ABC123",
        approved_type=Grant.ApprovedType.ticket_only,
    )

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_voucher_email(grant_id=grant.id)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_VOUCHER_CODE,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Your Grant Voucher Code",
        variables={
            "firstname": "Marco Acierno",
            "voucherCode": "ABC123",
            "hasApprovedAccommodation": False,
            "visaPageLink": "https://pycon.it/visa",
        },
        reply_to=["grants@pycon.it"],
    )


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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_waiting_list_email(grant_id=grant.id)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_WAITING_LIST,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Financial Aid Update",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": grant.conference.name.localize("en"),
            "replyLink": "https://pycon.it/grants/reply/",
            "grantsUpdateDeadline": "1 March 2023",
        },
        reply_to=["grants@pycon.it"],
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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=True)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Reminder: Financial Aid Update",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": grant.conference.name.localize("en"),
            "startDate": "2 May",
            "endDate": "6 May",
            "deadlineDateTime": "1 February 2023 23:59 UTC",
            "deadlineDate": "1 February 2023",
            "replyLink": "https://pycon.it/grants/reply/",
            "visaPageLink": "https://pycon.it/visa",
            "hasApprovedTravel": False,
            "hasApprovedAccommodation": False,
        },
        reply_to=["grants@pycon.it"],
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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Financial Aid Update",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": grant.conference.name.localize("en"),
            "startDate": "2 May",
            "endDate": "6 May",
            "amount": "680",
            "deadlineDateTime": "1 February 2023 23:59 UTC",
            "deadlineDate": "1 February 2023",
            "replyLink": "https://pycon.it/grants/reply/",
            "visaPageLink": "https://pycon.it/visa",
            "hasApprovedTravel": True,
            "hasApprovedAccommodation": True,
        },
        reply_to=["grants@pycon.it"],
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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Financial Aid Update",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": grant.conference.name.localize("en"),
            "startDate": "2 May",
            "endDate": "6 May",
            "deadlineDateTime": "1 February 2023 23:59 UTC",
            "deadlineDate": "1 February 2023",
            "replyLink": "https://pycon.it/grants/reply/",
            "visaPageLink": "https://pycon.it/visa",
            "hasApprovedTravel": False,
            "hasApprovedAccommodation": False,
        },
        reply_to=["grants@pycon.it"],
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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Financial Aid Update",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": grant.conference.name.localize("en"),
            "startDate": "2 May",
            "endDate": "6 May",
            "deadlineDateTime": "1 February 2023 23:59 UTC",
            "deadlineDate": "1 February 2023",
            "replyLink": "https://pycon.it/grants/reply/",
            "visaPageLink": "https://pycon.it/visa",
            "hasApprovedTravel": True,
            "hasApprovedAccommodation": False,
            "amount": "400",
        },
        reply_to=["grants@pycon.it"],
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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_waiting_list_update_email(
            grant_id=grant.id,
        )

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_WAITING_LIST_UPDATE,
        to="marco@placeholder.it",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": conference_name,
            "grantsUpdateDeadline": "1 March 2023",
            "replyLink": "https://pycon.it/grants/reply/",
        },
        reply_to=["grants@pycon.it"],
        subject=f"[{conference_name}] Financial Aid Update",
    )
