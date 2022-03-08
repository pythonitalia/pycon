from unittest.mock import call

import pytest
from django.utils import timezone

from schedule.admin import (
    send_schedule_invitation_reminder_to_waiting,
    send_schedule_invitation_to_all,
    send_schedule_invitation_to_uninvited,
)
from schedule.models import ScheduleItem

pytestmark = pytest.mark.django_db


def test_send_schedule_invitation_to_all(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = conference_factory()
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=None,
    )
    schedule_item_2 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=None,
    )

    send_schedule_invitation_to_all(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    assert mock_send_invitation.call_count == 2
    mock_send_invitation.assert_has_calls(
        [
            call(
                schedule_item_1,
                is_reminder=False,
            ),
            call(
                schedule_item_2,
                is_reminder=False,
            ),
        ],
        any_order=True,
    )

    schedule_item_1.refresh_from_db()
    schedule_item_2.refresh_from_db()

    assert schedule_item_1.speaker_invitation_sent_at is not None
    assert schedule_item_2.speaker_invitation_sent_at is not None


def test_send_schedule_invitation_to_uninvited(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = conference_factory()
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=None,
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )

    send_schedule_invitation_to_uninvited(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    mock_send_invitation.assert_called_once_with(
        schedule_item_1,
        is_reminder=False,
    )


def test_send_schedule_invitation_reminder_to_waiting(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = conference_factory()
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )
    schedule_item_2 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=None,
    )

    send_schedule_invitation_reminder_to_waiting(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    mock_send_invitation.assert_called_once_with(
        schedule_item_1,
        is_reminder=True,
    )

    schedule_item_2.refresh_from_db()
    assert schedule_item_2.speaker_invitation_sent_at is None


def test_send_schedule_invitation_reminder_to_all_waiting(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = conference_factory()
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )
    schedule_item_2 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=submission_factory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )

    send_schedule_invitation_reminder_to_waiting(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    assert mock_send_invitation.call_count == 2
    mock_send_invitation.assert_has_calls(
        [
            call(
                schedule_item_1,
                is_reminder=True,
            ),
            call(
                schedule_item_2,
                is_reminder=True,
            ),
        ],
        any_order=True,
    )
