from datetime import datetime
from unittest.mock import patch

import pytest
from users.tests.factories import UserFactory
from django.utils import timezone
from pythonit_toolkit.emails.templates import EmailTemplate

from grants.tests.factories import GrantFactory
from grants.tasks import (
    send_grant_voucher_email,
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
)
from grants.models import Grant

pytestmark = pytest.mark.django_db


def test_send_grant_voucher_email(settings, grant_factory):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = grant_factory(
        user=user,
        voucher_code="ABC123",
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

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_rejected_email(grant_id=grant.id)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_REJECTED,
        to="marco@placeholder.it",
        subject=f"[{grant.conference.name}] Financial Aid Update",
        variables={
            "firstname": "Marco Acierno",
            "conferenceName": grant.conference.name.localize("en"),
        },
        reply_to=["grants@pycon.it"],
    )


def test_send_grant_reply_waiting_list_email(
    deadline_factory, conference, grant_factory, settings
):
    settings.FRONTEND_URL = "https://pycon.it"
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    deadline_factory(
        start=datetime(2023, 3, 1, 23, 59, tzinfo=timezone.utc),
        conference=conference,
        type="custom",
        name={
            "en": "Update Grants in Waiting List",
            "it": "Update Grants in Waiting List",
        },
    )
    grant = grant_factory(conference=conference, user=user)

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


def test_handle_grant_reply_sent_reminder(conference_factory, grant_factory, settings):
    settings.FRONTEND_URL = "https://pycon.it"
    conference = conference_factory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    grant = grant_factory(
        conference=conference,
        approved_type=Grant.ApprovedType.ticket_only,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        total_amount=680,
        user=user,
    )

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=True)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED_TICKET_ONLY,
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
        },
        reply_to=["grants@pycon.it"],
    )


def test_handle_grant_approved_ticket_travel_accommodation_reply_sent(
    conference_factory, grant_factory, settings
):
    settings.FRONTEND_URL = "https://pycon.it"

    conference = conference_factory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = grant_factory(
        conference=conference,
        approved_type=Grant.ApprovedType.ticket_travel_accommodation,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        travel_amount=680,
        user=user,
    )

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED_TICKET_TRAVEL_ACCOMMODATION,
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
        },
        reply_to=["grants@pycon.it"],
    )


def test_handle_grant_approved_ticket_only_reply_sent(
    conference_factory, grant_factory, settings
):
    settings.FRONTEND_URL = "https://pycon.it"

    conference = conference_factory(
        start=datetime(2023, 5, 2, tzinfo=timezone.utc),
        end=datetime(2023, 5, 5, tzinfo=timezone.utc),
    )
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    grant = grant_factory(
        conference=conference,
        approved_type=Grant.ApprovedType.ticket_only,
        applicant_reply_deadline=datetime(2023, 2, 1, 23, 59, tzinfo=timezone.utc),
        total_amount=680,
        user=user,
    )

    with patch("grants.tasks.send_email") as email_mock:
        send_grant_reply_approved_email(grant_id=grant.id, is_reminder=False)

    email_mock.assert_called_once_with(
        template=EmailTemplate.GRANT_APPROVED_TICKET_ONLY,
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
        },
        reply_to=["grants@pycon.it"],
    )