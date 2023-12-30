from datetime import datetime
from unittest.mock import patch

import pytest
import time_machine
from conferences.models.speaker_voucher import SpeakerVoucher
from users.tests.factories import UserFactory
from schedule.models import ScheduleItem
from django.utils import timezone
from pythonit_toolkit.emails.templates import EmailTemplate

from domain_events.handler import (
    handle_new_cfp_submission,
    handle_new_schedule_invitation_answer,
    handle_schedule_invitation_sent,
    handle_speaker_communication_sent,
    handle_speaker_voucher_email_sent,
    handle_submission_time_slot_changed,
)


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_handle_new_cfp_submission(conference_factory):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    conference = conference_factory(
        slack_new_proposal_comment_incoming_webhook_url="https://123",
        slack_new_proposal_incoming_webhook_url="https://456",
    )

    data = {
        "title": "test_title",
        "elevator_pitch": "test_elevator_pitch",
        "submission_type": "test_submission_type",
        "admin_url": "test_admin_url",
        "topic": "test_topic",
        "duration": "50",
        "speaker_id": user.id,
        "conference_id": conference.id,
        "tags": "a,b",
    }

    with patch("domain_events.handler.slack") as slack_mock:
        handle_new_cfp_submission(data)

    slack_mock.send_message.assert_called_once()
    assert "Marco Acierno" in str(slack_mock.send_message.mock_calls[0])
    assert "https://456" in str(slack_mock.send_message.mock_calls[0])


def test_handle_schedule_invitation_sent():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    data = {
        "speaker_id": user.id,
        "invitation_url": "https://url",
        "submission_title": "Title title",
    }

    with patch("domain_events.handler.send_email") as email_mock:
        handle_schedule_invitation_sent(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to="marco@placeholder.it",
        subject="[PyCon Italia 2023] Your submission was accepted!",
        variables={
            "submissionTitle": "Title title",
            "firstname": "Marco Acierno",
            "invitationlink": "https://url",
        },
    )


def test_handle_schedule_invitation_sent_reminder():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    data = {
        "speaker_id": user.id,
        "invitation_url": "https://url",
        "submission_title": "Title title",
        "is_reminder": True,
    }

    with patch("domain_events.handler.send_email") as email_mock:
        handle_schedule_invitation_sent(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to="marco@placeholder.it",
        subject=(
            "[PyCon Italia 2023] Reminder: Your submission was "
            "accepted, confirm your presence"
        ),
        variables={
            "submissionTitle": "Title title",
            "firstname": "Marco Acierno",
            "invitationlink": "https://url",
        },
    )


def test_handle_submission_time_slot_changed():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    data = {
        "speaker_id": user.id,
        "invitation_url": "https://url",
        "submission_title": "Title title",
    }

    with patch("domain_events.handler.send_email") as email_mock:
        handle_submission_time_slot_changed(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_SCHEDULE_TIME_CHANGED,
        to="marco@placeholder.it",
        subject="[PyCon Italia 2023] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": "Title title",
            "firstname": "Marco Acierno",
            "invitationlink": "https://url",
        },
    )


def test_handle_new_schedule_invitation_answer(
    settings, schedule_item_factory, submission_factory
):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    settings.SPEAKERS_EMAIL_ADDRESS = "speakers@placeholder.com"
    schedule_item = schedule_item_factory(
        type=ScheduleItem.TYPES.talk, submission=submission_factory(speaker=user)
    )
    data = {
        "speaker_id": user.id,
        "schedule_item_id": schedule_item.id,
        "speaker_notes": "Sub",
        "invitation_admin_url": "https://admin",
        "schedule_item_admin_url": "https://schedule",
    }

    with patch("domain_events.handler.slack") as slack_mock:
        handle_new_schedule_invitation_answer(data)

    slack_mock.send_message.assert_called_once()


def test_handle_speaker_voucher_email_sent(settings, speaker_voucher_factory):
    settings.SPEAKERS_EMAIL_ADDRESS = "speakers@placeholder.com"
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    speaker_voucher = speaker_voucher_factory(
        user=user,
        voucher_type=SpeakerVoucher.VoucherType.SPEAKER,
        voucher_code="ABC123",
    )

    data = {
        "speaker_voucher_id": speaker_voucher.id,
    }

    with patch("domain_events.handler.send_email") as email_mock:
        handle_speaker_voucher_email_sent(data)

    conf_name = speaker_voucher.conference.name.localize("en")
    email_mock.assert_called_once_with(
        template=EmailTemplate.SPEAKER_VOUCHER_CODE,
        to="marco@placeholder.it",
        subject=f"[{conf_name}] Your Speaker Voucher Code",
        variables={
            "firstname": "Marco Acierno",
            "voucherCode": "ABC123",
            "is_speaker_voucher": True,
        },
        reply_to=["speakers@placeholder.com"],
    )


def test_handle_speaker_voucher_email_sent_cospeaker(settings, speaker_voucher_factory):
    settings.SPEAKERS_EMAIL_ADDRESS = "speakers@placeholder.com"
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    speaker_voucher = speaker_voucher_factory(
        user=user,
        voucher_type=SpeakerVoucher.VoucherType.CO_SPEAKER,
        voucher_code="ABC123",
    )

    data = {
        "speaker_voucher_id": speaker_voucher.id,
    }

    with patch("domain_events.handler.send_email") as email_mock, time_machine.travel(
        "2020-10-10 10:00:00Z", tick=False
    ):
        handle_speaker_voucher_email_sent(data)

    speaker_voucher.refresh_from_db()
    assert speaker_voucher.voucher_email_sent_at == datetime(
        2020, 10, 10, 10, 0, 0, tzinfo=timezone.utc
    )

    conf_name = speaker_voucher.conference.name.localize("en")
    email_mock.assert_called_once_with(
        template=EmailTemplate.SPEAKER_VOUCHER_CODE,
        to="marco@placeholder.it",
        subject=f"[{conf_name}] Your Speaker Voucher Code",
        variables={
            "firstname": "Marco Acierno",
            "voucherCode": "ABC123",
            "is_speaker_voucher": False,
        },
        reply_to=["speakers@placeholder.com"],
    )


@pytest.mark.parametrize("has_ticket", [True, False])
def test_handle_speaker_communication_sent_to_speakers_without_ticket(
    settings, requests_mock, conference_factory, has_ticket
):
    settings.SPEAKERS_EMAIL_ADDRESS = "reply"
    conference = conference_factory()

    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    data = {
        "user_id": user.id,
        "subject": "test subject",
        "body": "test body",
        "only_speakers_without_ticket": True,
        "conference_id": conference.id,
    }
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    with patch("domain_events.handler.send_email") as email_mock:
        handle_speaker_communication_sent(data)

    if not has_ticket:
        email_mock.assert_called_once_with(
            template=EmailTemplate.SPEAKER_COMMUNICATION,
            to="marco@placeholder.it",
            subject=f"[{conference.name.localize('en')}] test subject",
            variables={
                "firstname": "Marco Acierno",
                "body": "test body",
            },
            reply_to=[settings.SPEAKERS_EMAIL_ADDRESS],
        )
    else:
        email_mock.assert_not_called()


@pytest.mark.parametrize("has_ticket", [True, False])
def test_handle_speaker_communication_sent_to_everyone(
    settings, requests_mock, conference_factory, has_ticket
):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    settings.SPEAKERS_EMAIL_ADDRESS = "reply"
    conference = conference_factory()
    data = {
        "user_id": user.id,
        "subject": "test subject",
        "body": "test body",
        "only_speakers_without_ticket": False,
        "conference_id": conference.id,
    }
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    with patch("domain_events.handler.send_email") as email_mock:
        handle_speaker_communication_sent(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SPEAKER_COMMUNICATION,
        to="marco@placeholder.it",
        subject=f"[{conference.name.localize('en')}] test subject",
        variables={
            "firstname": "Marco Acierno",
            "body": "test body",
        },
        reply_to=[settings.SPEAKERS_EMAIL_ADDRESS],
    )
