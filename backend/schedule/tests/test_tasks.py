from conferences.tests.factories import SpeakerVoucherFactory
from i18n.strings import LazyI18nString
from datetime import datetime
from unittest.mock import ANY, patch
from django.test import override_settings

from schedule.tasks import (
    notify_new_schedule_invitation_answer_slack,
    send_schedule_invitation_email,
    send_schedule_invitation_plain_message,
    send_speaker_communication_email,
    send_speaker_voucher_email,
    send_submission_time_slot_changed_email,
)
from schedule.tests.factories import ScheduleItemFactory
from submissions.tests.factories import SubmissionFactory
import time_machine
from conferences.models.speaker_voucher import SpeakerVoucher
from users.tests.factories import UserFactory
from schedule.models import ScheduleItem
from django.utils import timezone
from pythonit_toolkit.emails.templates import EmailTemplate

import pytest

pytestmark = pytest.mark.django_db


@override_settings(FRONTEND_URL="https://frontend/")
def test_send_schedule_invitation_email():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    schedule_item = ScheduleItemFactory(
        conference__name=LazyI18nString({"en": "Conf"}),
        submission__title=LazyI18nString({"en": "Title Submission"}),
        submission__speaker=user,
        type=ScheduleItem.TYPES.talk,
    )

    with patch("schedule.tasks.send_email") as email_mock:
        send_schedule_invitation_email(
            schedule_item_id=schedule_item.id,
            is_reminder=False,
        )

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to="marco@placeholder.it",
        subject="[Conf] Your submission has been accepted!",
        variables={
            "submissionTitle": "Title Submission",
            "firstname": "Marco Acierno",
            "invitationlink": f"https://frontend/schedule/invitation/{schedule_item.submission.hashid}",
            "conferenceName": "Conf",
        },
    )

    schedule_item.refresh_from_db()

    assert schedule_item.speaker_invitation_sent_at is not None


@override_settings(FRONTEND_URL="https://frontend/")
def test_send_schedule_invitation_email_reminder():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    schedule_item = ScheduleItemFactory(
        submission__title=LazyI18nString({"en": "Title Submission"}),
        submission__speaker=user,
        conference__name=LazyI18nString({"en": "Conf"}),
        type=ScheduleItem.TYPES.talk,
    )

    with patch("schedule.tasks.send_email") as email_mock:
        send_schedule_invitation_email(
            schedule_item_id=schedule_item.id,
            is_reminder=True,
        )

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to="marco@placeholder.it",
        subject=(
            "[Conf] Reminder: Your submission has been accepted, confirm your presence"
        ),
        variables={
            "submissionTitle": "Title Submission",
            "firstname": "Marco Acierno",
            "invitationlink": f"https://frontend/schedule/invitation/{schedule_item.submission.hashid}",
            "conferenceName": "Conf",
        },
    )


@override_settings(FRONTEND_URL="https://frontend/")
def test_send_submission_time_slot_changed_email():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    schedule_item = ScheduleItemFactory(
        submission__speaker=user,
        submission__title=LazyI18nString({"en": "Title Submission"}),
        conference__name=LazyI18nString({"en": "Conf"}),
        type=ScheduleItem.TYPES.talk,
    )

    with patch("schedule.tasks.send_email") as email_mock:
        send_submission_time_slot_changed_email(schedule_item_id=schedule_item.id)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_SCHEDULE_TIME_CHANGED,
        to="marco@placeholder.it",
        subject="[Conf] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": "Title Submission",
            "firstname": "Marco Acierno",
            "invitationlink": f"https://frontend/schedule/invitation/{schedule_item.submission.hashid}",
            "conferenceName": "Conf",
        },
    )


@pytest.mark.parametrize(
    "status",
    [
        ScheduleItem.STATUS.confirmed,
        ScheduleItem.STATUS.maybe,
        ScheduleItem.STATUS.rejected,
        ScheduleItem.STATUS.cant_attend,
        ScheduleItem.STATUS.cancelled,
    ],
)
@override_settings(SPEAKERS_EMAIL_ADDRESS="speakers@placeholder.com")
def test_notify_new_schedule_invitation_answer_slack(status):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    schedule_item = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk, submission__speaker=user, status=status
    )

    with patch("schedule.tasks.slack") as slack_mock:
        notify_new_schedule_invitation_answer_slack(
            schedule_item_id=schedule_item.id,
            invitation_admin_url="https://invitation/",
            schedule_item_admin_url="https://schedule_item/",
        )

    slack_mock.send_message.assert_called_once()


@override_settings(SPEAKERS_EMAIL_ADDRESS="speakers@placeholder.com")
def test_send_speaker_voucher_email():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    speaker_voucher = SpeakerVoucherFactory(
        user=user,
        voucher_type=SpeakerVoucher.VoucherType.SPEAKER,
        voucher_code="ABC123",
    )

    with patch("schedule.tasks.send_email") as email_mock:
        send_speaker_voucher_email(speaker_voucher_id=speaker_voucher.id)

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


@override_settings(SPEAKERS_EMAIL_ADDRESS="speakers@placeholder.com")
def test_send_speaker_voucher_email_cospeaker():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    speaker_voucher = SpeakerVoucherFactory(
        user=user,
        voucher_type=SpeakerVoucher.VoucherType.CO_SPEAKER,
        voucher_code="ABC123",
    )

    with patch("schedule.tasks.send_email") as email_mock, time_machine.travel(
        "2020-10-10 10:00:00Z", tick=False
    ):
        send_speaker_voucher_email(speaker_voucher_id=speaker_voucher.id)

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


@override_settings(SPEAKERS_EMAIL_ADDRESS="reply")
@pytest.mark.parametrize("has_ticket", [True, False])
def test_send_speaker_communication_email_to_speakers_without_ticket(
    requests_mock, conference_factory, has_ticket, settings
):
    conference = conference_factory()

    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    with patch("schedule.tasks.send_email") as email_mock:
        send_speaker_communication_email(
            subject="test subject",
            body="test body",
            user_id=user.id,
            conference_id=conference.id,
            only_speakers_without_ticket=True,
        )

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


@override_settings(SPEAKERS_EMAIL_ADDRESS="reply")
@pytest.mark.parametrize("has_ticket", [True, False])
def test_send_speaker_communication_email_to_everyone(
    settings, requests_mock, conference_factory, has_ticket
):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    conference = conference_factory()

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    with patch("schedule.tasks.send_email") as email_mock:
        send_speaker_communication_email(
            subject="test subject",
            body="test body",
            user_id=user.id,
            conference_id=conference.id,
            only_speakers_without_ticket=False,
        )

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


@override_settings(PLAIN_API="https://example.org/plain")
def test_send_schedule_invitation_plain_message(mocker):
    mock_plain = mocker.patch("schedule.tasks.plain")
    mock_plain.send_message.return_value = "id_123"

    schedule_item = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk, submission=SubmissionFactory()
    )

    send_schedule_invitation_plain_message(
        schedule_item_id=schedule_item.id,
        message="Test message",
    )

    mock_plain.send_message.assert_called_once_with(
        schedule_item.submission.speaker,
        title=ANY,
        message="Test message",
        existing_thread_id=None,
    )

    schedule_item.refresh_from_db()
    assert schedule_item.plain_thread_id == "id_123"


@override_settings(PLAIN_API="https://example.org/plain")
def test_send_schedule_invitation_plain_message_with_existing_thread(mocker):
    mock_plain = mocker.patch("schedule.tasks.plain")
    mock_plain.send_message.return_value = "thread_id"

    schedule_item = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        submission=SubmissionFactory(),
        plain_thread_id="thread_id",
    )

    send_schedule_invitation_plain_message(
        schedule_item_id=schedule_item.id,
        message="New message",
    )

    mock_plain.send_message.assert_called_once_with(
        schedule_item.submission.speaker,
        title="Additional message",
        message="New message",
        existing_thread_id="thread_id",
    )

    schedule_item.refresh_from_db()
    assert schedule_item.plain_thread_id == "thread_id"
