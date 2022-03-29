from unittest.mock import call

import pytest
import time_machine
from django.utils import timezone

from schedule.admin import (
    generate_voucher_codes,
    send_schedule_invitation_reminder_to_waiting,
    send_schedule_invitation_to_all,
    send_schedule_invitation_to_uninvited,
    send_voucher_via_email,
)
from schedule.models import ScheduleItem, SpeakerVoucher

pytestmark = pytest.mark.django_db


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email(
    rf,
    schedule_item_factory,
    conference_factory,
    submission_factory,
    speaker_voucher_factory,
    mocker,
):
    mocker.patch("schedule.admin.messages")
    mock_send_email = mocker.patch("schedule.admin.send_speaker_voucher_email")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=600),
    )

    speaker_voucher_1 = speaker_voucher_factory(
        conference=conference,
        user_id=500,
        pretix_voucher_id=1,
    )
    speaker_voucher_2 = speaker_voucher_factory(
        conference=conference,
        user_id=600,
        pretix_voucher_id=2,
    )

    send_voucher_via_email(
        None, rf.get("/"), queryset=SpeakerVoucher.objects.filter(conference=conference)
    )

    mock_send_email.assert_has_calls(
        [
            call(speaker_voucher_1),
            call(speaker_voucher_2),
        ]
    )

    speaker_voucher_1.refresh_from_db()
    speaker_voucher_2.refresh_from_db()

    assert speaker_voucher_1.voucher_email_sent_at == timezone.now()
    assert speaker_voucher_2.voucher_email_sent_at == timezone.now()


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email_requires_filtering_by_conference(
    rf,
    schedule_item_factory,
    conference_factory,
    submission_factory,
    speaker_voucher_factory,
    mocker,
):
    mock_messages = mocker.patch("schedule.admin.messages")
    mock_send_email = mocker.patch("schedule.admin.send_speaker_voucher_email")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    conference_2 = conference_factory(pretix_speaker_voucher_quota_id=123)

    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference_2,
        submission=submission_factory(conference=conference_2, speaker_id=600),
    )

    speaker_voucher_1 = speaker_voucher_factory(
        conference=conference,
        user_id=500,
        pretix_voucher_id=1,
    )
    speaker_voucher_2 = speaker_voucher_factory(
        conference=conference_2,
        user_id=600,
        pretix_voucher_id=2,
    )

    request = rf.get("/")
    send_voucher_via_email(
        None,
        request,
        queryset=SpeakerVoucher.objects.filter(
            conference__in=[conference, conference_2]
        ),
    )

    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )
    mock_send_email.assert_not_called()

    speaker_voucher_1.refresh_from_db()
    speaker_voucher_2.refresh_from_db()

    assert speaker_voucher_1.voucher_email_sent_at is None
    assert speaker_voucher_2.voucher_email_sent_at is None


def test_generate_voucher_codes(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mocker.patch("schedule.admin.get_random_string", side_effect=["1", "2"])
    mock_create_voucher = mocker.patch(
        "schedule.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_2 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=600),
    )

    generate_voucher_codes(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_has_calls(
        [
            call(
                conference=conference,
                code="SPEAKER-1",
                comment=f"Voucher for speaker_id={schedule_item_1.submission.speaker_id}",
                tag="speakers",
                quota_id=schedule_item_1.conference.pretix_speaker_voucher_quota_id,
            ),
            call(
                conference=conference,
                code="SPEAKER-2",
                comment=f"Voucher for speaker_id={schedule_item_2.submission.speaker_id}",
                tag="speakers",
                quota_id=schedule_item_1.conference.pretix_speaker_voucher_quota_id,
            ),
        ],
    )

    assert SpeakerVoucher.objects.count() == 2

    speaker_voucher_1 = SpeakerVoucher.objects.get(user_id=500)
    assert speaker_voucher_1.voucher_code == "SPEAKER-1"
    assert speaker_voucher_1.conference_id == conference.id
    assert speaker_voucher_1.pretix_voucher_id == 1

    speaker_voucher_2 = SpeakerVoucher.objects.get(user_id=600)
    assert speaker_voucher_2.voucher_code == "SPEAKER-2"
    assert speaker_voucher_2.conference_id == conference.id
    assert speaker_voucher_2.pretix_voucher_id == 2


def test_generate_voucher_codes_doesnt_work_with_multiple_conferences(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mocker.patch("schedule.admin.get_random_string", side_effect=["1", "2"])
    mock_create_voucher = mocker.patch(
        "schedule.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mock_messages = mocker.patch("schedule.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    conference_2 = conference_factory(pretix_speaker_voucher_quota_id=123)

    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference_2,
        submission=submission_factory(conference=conference_2, speaker_id=600),
    )

    request = rf.get("/")

    generate_voucher_codes(
        None,
        request=request,
        queryset=ScheduleItem.objects.filter(conference__in=[conference, conference_2]),
    )

    mock_create_voucher.assert_not_called()
    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )

    assert SpeakerVoucher.objects.count() == 0


def test_generate_voucher_codes_needs_pretix_config_to_work(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mocker.patch("schedule.admin.get_random_string", side_effect=["1", "2"])
    mock_create_voucher = mocker.patch(
        "schedule.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mock_messages = mocker.patch("schedule.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=None)

    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )

    request = rf.get("/")

    generate_voucher_codes(
        None,
        request=request,
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_not_called()
    mock_messages.error.assert_called_once_with(
        request,
        "Please configure the speaker voucher quota ID in the conference settings",
    )

    assert SpeakerVoucher.objects.count() == 0


def test_generate_voucher_codes_only_created_once(
    rf,
    schedule_item_factory,
    conference_factory,
    submission_factory,
    mocker,
    speaker_voucher_factory,
):
    mocker.patch("schedule.admin.get_random_string", side_effect=["2"])
    mock_create_voucher = mocker.patch(
        "schedule.admin.create_voucher",
        side_effect=[
            {"id": 2},
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_2 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=600),
    )

    speaker_voucher_factory(
        conference=conference,
        user_id=500,
        voucher_code="SPEAKER-ABC",
        pretix_voucher_id=123,
    )

    generate_voucher_codes(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_called_once_with(
        conference=conference,
        code="SPEAKER-2",
        comment=f"Voucher for speaker_id={schedule_item_2.submission.speaker_id}",
        tag="speakers",
        quota_id=schedule_item_2.conference.pretix_speaker_voucher_quota_id,
    )

    assert SpeakerVoucher.objects.count() == 2

    # existing one untouched
    speaker_voucher_1 = SpeakerVoucher.objects.get(user_id=500)
    assert speaker_voucher_1.voucher_code == "SPEAKER-ABC"
    assert speaker_voucher_1.conference_id == conference.id
    assert speaker_voucher_1.pretix_voucher_id == 123

    speaker_voucher_2 = SpeakerVoucher.objects.get(user_id=600)
    assert speaker_voucher_2.voucher_code == "SPEAKER-2"
    assert speaker_voucher_2.conference_id == conference.id
    assert speaker_voucher_2.pretix_voucher_id == 2


def test_generate_voucher_codes_ignores_excluded_speakers(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mocker.patch("schedule.admin.get_random_string", side_effect=["1", "2"])
    mock_create_voucher = mocker.patch(
        "schedule.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=600),
        exclude_from_voucher_generation=True,
    )

    generate_voucher_codes(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_called_once_with(
        conference=conference,
        code="SPEAKER-1",
        comment=f"Voucher for speaker_id={schedule_item_1.submission.speaker_id}",
        tag="speakers",
        quota_id=schedule_item_1.conference.pretix_speaker_voucher_quota_id,
    )

    assert SpeakerVoucher.objects.count() == 1

    speaker_voucher_1 = SpeakerVoucher.objects.get(user_id=500)
    assert speaker_voucher_1.voucher_code == "SPEAKER-1"
    assert speaker_voucher_1.conference_id == conference.id
    assert speaker_voucher_1.pretix_voucher_id == 1


def test_generate_voucher_codes_ignores_excluded_speakers_even_when_has_multiple_items(
    rf, schedule_item_factory, conference_factory, submission_factory, mocker
):
    mocker.patch("schedule.admin.get_random_string", side_effect=["1", "2"])
    mock_create_voucher = mocker.patch(
        "schedule.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)
    schedule_item_1 = schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=500),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        submission=submission_factory(conference=conference, speaker_id=600),
    )
    schedule_item_factory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
        # Same speaker as 2, so 2 user_id 600 is excluded
        submission=submission_factory(conference=conference, speaker_id=600),
        exclude_from_voucher_generation=True,
    )

    generate_voucher_codes(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_called_once_with(
        conference=conference,
        code="SPEAKER-1",
        comment=f"Voucher for speaker_id={schedule_item_1.submission.speaker_id}",
        tag="speakers",
        quota_id=schedule_item_1.conference.pretix_speaker_voucher_quota_id,
    )

    assert SpeakerVoucher.objects.count() == 1

    speaker_voucher_1 = SpeakerVoucher.objects.get(user_id=500)
    assert speaker_voucher_1.voucher_code == "SPEAKER-1"
    assert speaker_voucher_1.conference_id == conference.id
    assert speaker_voucher_1.pretix_voucher_id == 1


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
