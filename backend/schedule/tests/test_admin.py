from submissions.tests.factories import SubmissionFactory
from conferences.tests.factories import ConferenceFactory, ConferenceVoucherFactory
from django.contrib import messages
from django.contrib.admin.sites import AdminSite
from unittest.mock import call

import pytest
from django.utils import timezone

from conferences.models import ConferenceVoucher
from schedule.admin import (
    ScheduleItemAdmin,
    mark_as_confirmed_action,
    mark_speakers_to_receive_vouchers,
    send_schedule_invitation_reminder_to_waiting,
    send_schedule_invitation_to_all,
    send_schedule_invitation_to_uninvited,
)
from schedule.models import ScheduleItem
from schedule.tests.factories import (
    ScheduleItemAdditionalSpeakerFactory,
    ScheduleItemFactory,
)
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_mark_speakers_to_receive_vouchers(rf, mocker):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string",
        side_effect=[
            "CODE1",
            "CODE2",
            "CODE3",
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=None,
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 2

    conference_voucher_1 = ConferenceVoucher.objects.get(
        user_id=schedule_item_1.submission.speaker_id
    )
    assert conference_voucher_1.voucher_code == "CODE1"
    assert conference_voucher_1.conference_id == conference.id
    assert conference_voucher_1.pretix_voucher_id is None
    assert conference_voucher_1.voucher_type == ConferenceVoucher.VoucherType.SPEAKER

    conference_voucher_2 = ConferenceVoucher.objects.get(
        user_id=schedule_item_2.submission.speaker_id
    )
    assert conference_voucher_2.voucher_code == "CODE2"
    assert conference_voucher_2.conference_id == conference.id
    assert conference_voucher_2.pretix_voucher_id is None
    assert conference_voucher_2.voucher_type == ConferenceVoucher.VoucherType.SPEAKER


def test_mark_speakers_to_receive_vouchers_includes_co_speakers(rf, mocker):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string",
        side_effect=["CODE1", "CODE2"],
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
        additional_speakers=2,
    )
    additional_speaker = (
        schedule_item_1.additional_speakers.order_by("id").first().user_id
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 2

    conference_voucher_1 = ConferenceVoucher.objects.get(
        user_id=schedule_item_1.submission.speaker_id
    )
    assert conference_voucher_1.voucher_code == "CODE1"
    assert conference_voucher_1.conference_id == conference.id
    assert conference_voucher_1.pretix_voucher_id is None
    assert conference_voucher_1.voucher_type == ConferenceVoucher.VoucherType.SPEAKER

    conference_voucher_2 = ConferenceVoucher.objects.get(user_id=additional_speaker)
    assert conference_voucher_2.voucher_code == "CODE2"
    assert conference_voucher_2.conference_id == conference.id
    assert conference_voucher_2.pretix_voucher_id is None
    assert conference_voucher_2.voucher_type == ConferenceVoucher.VoucherType.CO_SPEAKER


def test_additional_speakers_without_main_speaker_are_marked_for_a_speaker_voucher(
    rf, mocker
):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string", side_effect=["CODE1"]
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=None,
        additional_speakers=2,
    )
    additional_speaker = (
        schedule_item_1.additional_speakers.order_by("id").first().user_id
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 1

    speaker_voucher = ConferenceVoucher.objects.get(user_id=additional_speaker)
    assert speaker_voucher.voucher_code == "CODE1"
    assert speaker_voucher.conference_id == conference.id
    assert speaker_voucher.pretix_voucher_id is None
    assert speaker_voucher.voucher_type == ConferenceVoucher.VoucherType.SPEAKER


def test_speaker_with_both_main_talk_and_co_speaker_gets_a_speaker_voucher(
    rf,
    mocker,
):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string",
        side_effect=["CODE1", "CODE2", "CODE3"],
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)

    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )

    additional_speaker_schedule_item_2 = ScheduleItemAdditionalSpeakerFactory()
    schedule_item_2.additional_speakers.set([additional_speaker_schedule_item_2])

    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(
            conference=conference, speaker_id=additional_speaker_schedule_item_2.user_id
        ),
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 2

    speaker_voucher = ConferenceVoucher.objects.get(
        user_id=additional_speaker_schedule_item_2.user_id
    )
    assert speaker_voucher.conference_id == conference.id
    assert speaker_voucher.pretix_voucher_id is None
    assert speaker_voucher.voucher_type == ConferenceVoucher.VoucherType.SPEAKER

    assert ConferenceVoucher.objects.filter(
        user_id=schedule_item_2.submission.speaker_id
    ).exists()


def test_mark_speakers_to_receive_vouchers_doesnt_work_with_multiple_conferences(
    rf, mocker
):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string",
        side_effect=[
            "CODE1",
            "CODE2",
        ],
    )
    mock_messages = mocker.patch("custom_admin.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    conference_2 = ConferenceFactory(pretix_conference_voucher_quota_id=123)

    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference_2,
        submission=SubmissionFactory(conference=conference_2),
    )

    request = rf.get("/")

    mark_speakers_to_receive_vouchers(
        None,
        request=request,
        queryset=ScheduleItem.objects.filter(conference__in=[conference, conference_2]),
    )

    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )

    assert ConferenceVoucher.objects.count() == 0


def test_mark_speakers_to_receive_vouchers_only_created_once(
    rf,
    mocker,
):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string", side_effect=["CODE2"]
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )

    ConferenceVoucherFactory(
        conference=conference,
        user_id=schedule_item_1.submission.speaker_id,
        voucher_code="SPEAKER-ABC",
        pretix_voucher_id=123,
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 2

    # existing one untouched
    conference_voucher_1 = ConferenceVoucher.objects.get(
        user_id=schedule_item_1.submission.speaker_id
    )
    assert conference_voucher_1.voucher_code == "SPEAKER-ABC"
    assert conference_voucher_1.conference_id == conference.id
    assert conference_voucher_1.pretix_voucher_id == 123

    conference_voucher_2 = ConferenceVoucher.objects.get(
        user_id=schedule_item_2.submission.speaker_id
    )
    assert conference_voucher_2.voucher_code == "CODE2"
    assert conference_voucher_2.conference_id == conference.id
    assert conference_voucher_2.pretix_voucher_id is None


def test_mark_speakers_to_receive_vouchers_ignores_excluded_speakers(rf, mocker):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string",
        side_effect=[
            "CODE1",
            "CODE2",
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
        exclude_from_voucher_generation=True,
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 1

    conference_voucher_1 = ConferenceVoucher.objects.get(
        user_id=schedule_item_1.submission.speaker_id
    )
    assert conference_voucher_1.voucher_code == "CODE1"
    assert conference_voucher_1.conference_id == conference.id
    assert conference_voucher_1.pretix_voucher_id is None


def test_mark_speakers_to_receive_vouchers_ignores_excluded_speakers_multiple_items(
    rf, mocker
):
    mocker.patch(
        "conferences.models.conference_voucher.get_random_string",
        side_effect=[
            "CODE1",
            "CODE2",
        ],
    )
    mocker.patch("schedule.admin.messages")

    conference = ConferenceFactory(pretix_conference_voucher_quota_id=123)
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        submission=SubmissionFactory(conference=conference),
    )
    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        # Same speaker as 2, so 2 user_id 600 is excluded
        submission=SubmissionFactory(
            conference=conference, speaker_id=schedule_item_2.submission.speaker_id
        ),
        exclude_from_voucher_generation=True,
    )

    mark_speakers_to_receive_vouchers(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 1

    conference_voucher_1 = ConferenceVoucher.objects.get(
        user_id=schedule_item_1.submission.speaker_id
    )
    assert conference_voucher_1.voucher_code == "CODE1"
    assert conference_voucher_1.conference_id == conference.id
    assert conference_voucher_1.pretix_voucher_id is None


def test_send_schedule_invitation_to_all(rf, mocker):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = ConferenceFactory()
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=None,
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=None,
    )

    send_schedule_invitation_to_all(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    assert mock_send_invitation.delay.call_count == 2
    mock_send_invitation.delay.assert_has_calls(
        [
            call(
                schedule_item_id=schedule_item_1.id,
                is_reminder=False,
            ),
            call(
                schedule_item_id=schedule_item_2.id,
                is_reminder=False,
            ),
        ],
        any_order=True,
    )


def test_send_schedule_invitation_to_uninvited(rf, mocker):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = ConferenceFactory()
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=None,
    )
    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )

    send_schedule_invitation_to_uninvited(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    mock_send_invitation.delay.assert_called_once_with(
        schedule_item_id=schedule_item_1.id,
        is_reminder=False,
    )


def test_send_schedule_invitation_reminder_to_waiting(rf, mocker):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = ConferenceFactory()
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )
    ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=None,
    )

    send_schedule_invitation_reminder_to_waiting(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    mock_send_invitation.delay.assert_called_once_with(
        schedule_item_id=schedule_item_1.id,
        is_reminder=True,
    )


def test_send_schedule_invitation_reminder_to_all_waiting(rf, mocker):
    mock_send_invitation = mocker.patch("schedule.admin.send_schedule_invitation_email")
    mocker.patch("schedule.admin.messages")
    conference = ConferenceFactory()
    schedule_item_1 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )
    schedule_item_2 = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
        conference=conference,
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission=SubmissionFactory(conference=conference),
        speaker_invitation_sent_at=timezone.now(),
    )

    send_schedule_invitation_reminder_to_waiting(
        None,
        request=rf.get("/"),
        queryset=ScheduleItem.objects.filter(conference=conference).all(),
    )

    assert mock_send_invitation.delay.call_count == 2
    mock_send_invitation.delay.assert_has_calls(
        [
            call(
                schedule_item_id=schedule_item_1.id,
                is_reminder=True,
            ),
            call(
                schedule_item_id=schedule_item_2.id,
                is_reminder=True,
            ),
        ],
        any_order=True,
    )


def test_email_speakers(rf, admin_user, mocker):
    mock_send_comm = mocker.patch("schedule.admin.send_speaker_communication_email")
    user = UserFactory()
    conference = ConferenceFactory()

    ScheduleItemFactory(
        conference=conference, type=ScheduleItem.TYPES.talk, submission__speaker=user
    )

    admin = ScheduleItemAdmin(
        model=ScheduleItem,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post(
        "/",
        data={
            "conference": conference.id,
            "subject": "Subject",
            "body": "Body",
            "only_speakers_without_ticket": False,
        },
    )
    request.user = admin_user
    admin.email_speakers(request)

    mock_send_comm.delay.assert_has_calls(
        [
            call(
                user_id=user.id,
                conference_id=conference.id,
                subject="Subject",
                body="Body",
                only_speakers_without_ticket=False,
            )
        ],
        any_order=True,
    )
    admin.message_user.assert_called_once_with(
        request, "Scheduled 1 emails.", messages.SUCCESS
    )


def test_email_speakers_with_multiple_talks_is_only_notified_once(
    rf, admin_user, mocker
):
    mock_send_comm = mocker.patch("schedule.admin.send_speaker_communication_email")
    user = UserFactory()
    conference = ConferenceFactory()

    ScheduleItemFactory(
        conference=conference, type=ScheduleItem.TYPES.talk, submission__speaker=user
    )

    ScheduleItemFactory(
        conference=conference, type=ScheduleItem.TYPES.talk, submission__speaker=user
    )

    admin = ScheduleItemAdmin(
        model=ScheduleItem,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post(
        "/",
        data={
            "conference": conference.id,
            "subject": "Subject",
            "body": "Body",
            "only_speakers_without_ticket": False,
        },
    )
    request.user = admin_user
    admin.email_speakers(request)

    mock_send_comm.delay.assert_has_calls(
        [
            call(
                user_id=user.id,
                conference_id=conference.id,
                subject="Subject",
                body="Body",
                only_speakers_without_ticket=False,
            )
        ],
        any_order=True,
    )
    admin.message_user.assert_called_once_with(
        request, "Scheduled 1 emails.", messages.SUCCESS
    )


def test_email_speakers_with_co_speakers(rf, admin_user, mocker):
    mock_send_comm = mocker.patch("schedule.admin.send_speaker_communication_email")
    user = UserFactory()
    additional_speaker = UserFactory()
    conference = ConferenceFactory()

    schedule_item = ScheduleItemFactory(
        conference=conference, type=ScheduleItem.TYPES.talk, submission__speaker=user
    )
    ScheduleItemAdditionalSpeakerFactory(
        user=additional_speaker, scheduleitem=schedule_item
    )

    admin = ScheduleItemAdmin(
        model=ScheduleItem,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post(
        "/",
        data={
            "conference": conference.id,
            "subject": "Subject",
            "body": "Body",
            "only_speakers_without_ticket": False,
        },
    )
    request.user = admin_user
    admin.email_speakers(request)

    assert mock_send_comm.delay.call_count == 2
    mock_send_comm.delay.assert_has_calls(
        [
            call(
                user_id=user.id,
                conference_id=conference.id,
                subject="Subject",
                body="Body",
                only_speakers_without_ticket=False,
            ),
            call(
                user_id=additional_speaker.id,
                conference_id=conference.id,
                subject="Subject",
                body="Body",
                only_speakers_without_ticket=False,
            ),
        ],
        any_order=True,
    )
    admin.message_user.assert_called_once_with(
        request, "Scheduled 2 emails.", messages.SUCCESS
    )


def test_mark_as_confirmed_action(rf, mocker):
    mocker.patch("schedule.admin.messages")

    request = rf.get("/")
    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.waiting_confirmation,
    )
    unrelated_schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.waiting_confirmation,
    )

    mark_as_confirmed_action(
        None, request, ScheduleItem.objects.filter(id=schedule_item.id)
    )

    schedule_item.refresh_from_db()
    unrelated_schedule_item.refresh_from_db()

    assert schedule_item.status == ScheduleItem.STATUS.confirmed
    assert unrelated_schedule_item.status == ScheduleItem.STATUS.waiting_confirmation
