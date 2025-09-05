from conferences.models.conference_voucher import ConferenceVoucher
from notifications.tests.factories import EmailTemplateFactory
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from googleapiclient.errors import HttpError
import numpy as np
from io import BytesIO
from django.core.files.storage import storages
from django.core.files.uploadedfile import InMemoryUploadedFile
from unittest import mock
from conferences.tests.factories import ConferenceFactory, ConferenceVoucherFactory
from i18n.strings import LazyI18nString
from datetime import datetime, timezone
from unittest.mock import ANY, patch
from django.test import override_settings

from schedule.tasks import (
    create_and_send_voucher_to_speaker,
    notify_new_schedule_invitation_answer_slack,
    process_schedule_items_videos_to_upload,
    send_schedule_invitation_email,
    send_schedule_invitation_plain_message,
    send_speaker_communication_email,
    send_submission_time_slot_changed_email,
    upload_schedule_item_video,
)
from schedule.tests.factories import (
    ScheduleItemAdditionalSpeakerFactory,
    ScheduleItemFactory,
    ScheduleItemSentForVideoUploadFactory,
)
from schedule.video_upload import get_thumbnail_file_name, get_video_file_name
from submissions.tests.factories import SubmissionFactory
import time_machine
from users.tests.factories import UserFactory
from schedule.models import ScheduleItem, ScheduleItemSentForVideoUpload
from notifications.models import EmailTemplateIdentifier

import pytest

pytestmark = pytest.mark.django_db


@override_settings(FRONTEND_URL="https://frontend/")
def test_send_schedule_invitation_email(sent_emails):
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

    EmailTemplateFactory(
        conference=schedule_item.conference,
        identifier=EmailTemplateIdentifier.proposal_scheduled,
    )
    EmailTemplateFactory(identifier=EmailTemplateIdentifier.proposal_scheduled)

    send_schedule_invitation_email(
        schedule_item_id=schedule_item.id,
        is_reminder=False,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.proposal_scheduled
    assert sent_email.email_template.conference == schedule_item.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["proposal_title"] == "Title Submission"
    assert sent_email.placeholders["conference_name"] == "Conf"
    assert sent_email.placeholders["invitation_url"] == f"https://frontend/schedule/invitation/{schedule_item.submission.hashid}"
    assert sent_email.placeholders["speaker_name"] == "Marco Acierno"
    assert sent_email.placeholders["is_reminder"] == False

    schedule_item.refresh_from_db()

    assert schedule_item.speaker_invitation_sent_at is not None


@override_settings(FRONTEND_URL="https://frontend/")
def test_send_schedule_invitation_email_reminder(sent_emails):
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

    EmailTemplateFactory(
        conference=schedule_item.conference,
        identifier=EmailTemplateIdentifier.proposal_scheduled,
    )
    EmailTemplateFactory(identifier=EmailTemplateIdentifier.proposal_scheduled)

    send_schedule_invitation_email(
        schedule_item_id=schedule_item.id,
        is_reminder=True,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.proposal_scheduled
    assert sent_email.email_template.conference == schedule_item.conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["proposal_title"] == "Title Submission"
    assert sent_email.placeholders["conference_name"] == "Conf"
    assert sent_email.placeholders["invitation_url"] == f"https://frontend/schedule/invitation/{schedule_item.submission.hashid}"
    assert sent_email.placeholders["speaker_name"] == "Marco Acierno"
    assert sent_email.placeholders["is_reminder"] == True


@override_settings(FRONTEND_URL="https://frontend/")
def test_send_submission_time_slot_changed_email(sent_emails):
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
    
    EmailTemplateFactory(
        conference=schedule_item.conference,
        identifier=EmailTemplateIdentifier.proposal_time_slot_changed,
    )

    send_submission_time_slot_changed_email(schedule_item_id=schedule_item.id)

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.proposal_time_slot_changed
    assert sent_email.email_template.conference == schedule_item.conference
    assert sent_email.recipient == schedule_item.submission.speaker
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["proposal_title"] == "Title Submission"
    assert sent_email.placeholders["speaker_name"] == "Marco Acierno"
    assert sent_email.placeholders["invitation_url"] == f"https://frontend/schedule/invitation/{schedule_item.submission.hashid}"
    assert sent_email.placeholders["conference_name"] == "Conf"


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


@override_settings(SPEAKERS_EMAIL_ADDRESS="reply")
@pytest.mark.parametrize("has_ticket", [True, False])
def test_send_speaker_communication_email_to_speakers_without_ticket(
    requests_mock, has_ticket, settings, sent_emails
):
    conference = ConferenceFactory()

    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.speaker_communication,
    )

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    send_speaker_communication_email(
        subject="test subject",
        body="test body",
        user_id=user.id,
        conference_id=conference.id,
        only_speakers_without_ticket=True,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    
    if not has_ticket:
        assert emails_sent.count() == 1
        
        sent_email = emails_sent.first()
        assert sent_email.email_template.identifier == EmailTemplateIdentifier.speaker_communication
        assert sent_email.email_template.conference == conference
        assert sent_email.recipient == user
        
        # Verify placeholders were processed correctly
        assert sent_email.placeholders["user_name"] == "Marco Acierno"
        assert sent_email.placeholders["conference_name"] == conference.name.localize("en")
        assert sent_email.placeholders["body"] == "test body"
        assert sent_email.placeholders["subject"] == "test subject"
    else:
        assert emails_sent.count() == 0


@override_settings(SPEAKERS_EMAIL_ADDRESS="reply")
@pytest.mark.parametrize("has_ticket", [True, False])
def test_send_speaker_communication_email_to_everyone(
    settings, requests_mock, has_ticket, sent_emails
):
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )
    conference = ConferenceFactory()
    
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.speaker_communication,
    )

    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": has_ticket},
    )

    send_speaker_communication_email(
        subject="test subject",
        body="test body",
        user_id=user.id,
        conference_id=conference.id,
        only_speakers_without_ticket=False,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.speaker_communication
    assert sent_email.email_template.conference == conference
    assert sent_email.recipient == user
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == "Marco Acierno"
    assert sent_email.placeholders["body"] == "test body"
    assert sent_email.placeholders["conference_name"] == conference.name.localize("en")
    assert sent_email.placeholders["subject"] == "test subject"


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


def test_process_schedule_items_videos_to_upload(mocker):
    mock_process = mocker.patch("schedule.tasks.upload_schedule_item_video")

    ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.failed,
    )

    # Never attempted - should be scheduled
    sent_for_upload_1 = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
    )

    # Recently attempted
    sent_for_upload_2 = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=datetime(2020, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        status=ScheduleItemSentForVideoUpload.Status.pending,
    )

    with time_machine.travel("2020-01-01 10:30:00Z", tick=False):
        process_schedule_items_videos_to_upload()

    mock_process.assert_called_once_with(
        sent_for_video_upload_state_id=sent_for_upload_1.id
    )
    mock_process.reset()

    # it has been an hour since upload 2 attempt, so it should be rescheduled
    with time_machine.travel("2020-01-01 11:20:00Z", tick=False):
        process_schedule_items_videos_to_upload()

    mock_process.assert_has_calls(
        [
            mock.call(sent_for_video_upload_state_id=sent_for_upload_1.id),
            mock.call(sent_for_video_upload_state_id=sent_for_upload_2.id),
        ],
        any_order=True,
    )


def test_process_schedule_items_videos_stops_processing_when_the_quota_is_finished(
    mocker,
):
    mock_process = mocker.patch(
        "schedule.tasks.upload_schedule_item_video",
        side_effect=NoGoogleCloudQuotaLeftError(),
    )

    sent_for_upload_1 = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
    )

    ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
    )

    with time_machine.travel("2020-01-01 10:30:00Z", tick=False):
        process_schedule_items_videos_to_upload()

    mock_process.assert_called_once_with(
        sent_for_video_upload_state_id=sent_for_upload_1.id
    )
    mock_process.reset()

    sent_for_upload_1.refresh_from_db()
    assert sent_for_upload_1.status == ScheduleItemSentForVideoUpload.Status.pending


def test_failing_to_process_schedule_items_videos_to_upload_sets_failed_status(mocker):
    mock_process = mocker.patch(
        "schedule.tasks.upload_schedule_item_video",
        side_effect=ValueError("test error"),
    )

    sent_for_upload = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
    )

    with time_machine.travel("2020-01-01 10:30:00Z", tick=False):
        process_schedule_items_videos_to_upload()

    mock_process.assert_called_once_with(
        sent_for_video_upload_state_id=sent_for_upload.id
    )

    sent_for_upload.refresh_from_db()
    assert sent_for_upload.status == ScheduleItemSentForVideoUpload.Status.failed
    assert sent_for_upload.failed_reason == "test error"


def test_upload_schedule_item_video_flow(mocker):
    file_content = BytesIO(b"File")
    file_content.name = "test.mp4"
    file_content.seek(0)

    image_content = BytesIO(b"Image")
    image_content.name = "test.jpg"
    image_content.seek(0)

    local_storage = storages["localstorage"]
    conferencevideos_storage = storages["default"]

    conferencevideos_storage.save(
        "videos/test.mp4",
        InMemoryUploadedFile(
            file=file_content,
            field_name="file_field",
            name="test.txt",
            content_type="text/plain",
            size=file_content.getbuffer().nbytes,
            charset="utf-8",
            content_type_extra=None,
        ),
    )

    mock_yt_insert = mocker.patch(
        "schedule.tasks.youtube_videos_insert",
        autospec=True,
        return_value=[{"id": "vid_123"}],
    )
    mock_yt_set_thumbnail = mocker.patch(
        "schedule.tasks.youtube_videos_set_thumbnail", autospec=True
    )
    mocker.patch(
        "schedule.video_upload.cv2.VideoCapture.read",
        return_value=(True, np.array([1])),
    )

    sent_for_upload = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
        video_uploaded=False,
        thumbnail_uploaded=False,
        schedule_item__type=ScheduleItem.TYPES.talk,
        schedule_item__submission=None,
        schedule_item__title="Test Title",
        schedule_item__description="Test Description",
        schedule_item__video_uploaded_path=conferencevideos_storage.path(
            "videos/test.mp4"
        ),
        schedule_item__conference__video_title_template="{{ title }}",
        schedule_item__conference__video_description_template="{{ abstract }}",
    )
    upload_schedule_item_video(
        sent_for_video_upload_state_id=sent_for_upload.id,
    )

    mock_yt_insert.assert_called_with(
        title="Test Title",
        description="Test Description",
        tags="",
        file_path=mock.ANY,
    )
    mock_yt_set_thumbnail.assert_called_with(
        video_id="vid_123", thumbnail_path=mock.ANY
    )

    sent_for_upload.refresh_from_db()
    assert sent_for_upload.attempts == 1
    assert sent_for_upload.failed_reason == ""

    assert sent_for_upload.status == ScheduleItemSentForVideoUpload.Status.completed
    assert sent_for_upload.video_uploaded
    assert sent_for_upload.thumbnail_uploaded

    schedule_item = sent_for_upload.schedule_item
    schedule_item.refresh_from_db()
    assert schedule_item.youtube_video_id == "vid_123"

    # Make sure we cleanup files at the end
    assert not local_storage.exists(get_thumbnail_file_name(schedule_item.id))
    assert not local_storage.exists(get_video_file_name(schedule_item.id))


def test_upload_schedule_item_with_only_thumbnail_to_upload(mocker):
    file_content = BytesIO(b"File")
    file_content.name = "test.mp4"
    file_content.seek(0)

    image_content = BytesIO(b"Image")
    image_content.name = "test.jpg"
    image_content.seek(0)

    conferencevideos_storage = storages["default"]
    conferencevideos_storage.save(
        "videos/test.mp4",
        InMemoryUploadedFile(
            file=file_content,
            field_name="file_field",
            name="test.txt",
            content_type="text/plain",
            size=file_content.getbuffer().nbytes,
            charset="utf-8",
            content_type_extra=None,
        ),
    )

    mock_yt_insert = mocker.patch(
        "schedule.tasks.youtube_videos_insert",
        autospec=True,
        return_value=[{"id": "vid_123"}],
    )
    mock_yt_set_thumbnail = mocker.patch(
        "schedule.tasks.youtube_videos_set_thumbnail", autospec=True
    )
    mocker.patch(
        "schedule.video_upload.cv2.VideoCapture.read",
        return_value=(True, np.array([1])),
    )

    sent_for_upload = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
        video_uploaded=True,
        thumbnail_uploaded=False,
        schedule_item__type=ScheduleItem.TYPES.talk,
        schedule_item__submission=None,
        schedule_item__youtube_video_id="vid_10",
        schedule_item__title="Test Title",
        schedule_item__description="Test Description",
        schedule_item__video_uploaded_path=conferencevideos_storage.path(
            "videos/test.mp4"
        ),
        schedule_item__conference__video_title_template="{{ title }}",
        schedule_item__conference__video_description_template="{{ abstract }}",
    )
    upload_schedule_item_video(
        sent_for_video_upload_state_id=sent_for_upload.id,
    )

    mock_yt_insert.assert_not_called()
    mock_yt_set_thumbnail.assert_called_with(video_id="vid_10", thumbnail_path=mock.ANY)

    sent_for_upload.refresh_from_db()
    assert sent_for_upload.attempts == 1
    assert sent_for_upload.failed_reason == ""

    assert sent_for_upload.status == ScheduleItemSentForVideoUpload.Status.completed
    assert sent_for_upload.video_uploaded
    assert sent_for_upload.thumbnail_uploaded

    sent_for_upload.schedule_item.refresh_from_db()
    assert sent_for_upload.schedule_item.youtube_video_id == "vid_10"


@pytest.mark.parametrize(
    "status",
    [
        ScheduleItemSentForVideoUpload.Status.completed,
        ScheduleItemSentForVideoUpload.Status.failed,
        ScheduleItemSentForVideoUpload.Status.processing,
    ],
)
def test_upload_schedule_item_ignores_non_pending_jobs(status):
    sent_for_upload = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=status,
        schedule_item__type=ScheduleItem.TYPES.talk,
        schedule_item__submission=None,
        schedule_item__title="Test Title",
        schedule_item__description="Test Description",
        schedule_item__conference__video_title_template="{{ title }}",
        schedule_item__conference__video_description_template="{{ abstract }}",
    )
    upload_schedule_item_video(
        sent_for_video_upload_state_id=sent_for_upload.id,
    )

    assert sent_for_upload.status == status


def test_upload_schedule_item_video_with_failing_thumbnail_is_rescheduled(mocker):
    file_content = BytesIO(b"File")
    file_content.name = "test.mp4"
    file_content.seek(0)

    image_content = BytesIO(b"Image")
    image_content.name = "test.jpg"
    image_content.seek(0)

    conferencevideos_storage = storages["default"]
    conferencevideos_storage.save(
        "videos/test.mp4",
        InMemoryUploadedFile(
            file=file_content,
            field_name="file_field",
            name="test.txt",
            content_type="text/plain",
            size=file_content.getbuffer().nbytes,
            charset="utf-8",
            content_type_extra=None,
        ),
    )

    mock_yt_insert = mocker.patch(
        "schedule.tasks.youtube_videos_insert",
        autospec=True,
        return_value=[{"id": "vid_123"}],
    )
    mock_yt_set_thumbnail = mocker.patch(
        "schedule.tasks.youtube_videos_set_thumbnail",
        side_effect=HttpError(resp=mock.Mock(status=429), content=b""),
    )
    mocker.patch(
        "schedule.video_upload.cv2.VideoCapture.read",
        return_value=(True, np.array([1])),
    )

    sent_for_upload = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
        video_uploaded=False,
        thumbnail_uploaded=False,
        schedule_item__type=ScheduleItem.TYPES.talk,
        schedule_item__submission=None,
        schedule_item__title="Test Title",
        schedule_item__description="Test Description",
        schedule_item__video_uploaded_path=conferencevideos_storage.path(
            "videos/test.mp4"
        ),
        schedule_item__conference__video_title_template="{{ title }}",
        schedule_item__conference__video_description_template="{{ abstract }}",
    )
    upload_schedule_item_video(
        sent_for_video_upload_state_id=sent_for_upload.id,
    )

    mock_yt_insert.assert_called_with(
        title="Test Title",
        description="Test Description",
        tags="",
        file_path=mock.ANY,
    )
    mock_yt_set_thumbnail.assert_called_with(
        video_id="vid_123", thumbnail_path=mock.ANY
    )

    sent_for_upload.refresh_from_db()
    assert sent_for_upload.video_uploaded
    assert not sent_for_upload.thumbnail_uploaded
    assert sent_for_upload.status == ScheduleItemSentForVideoUpload.Status.pending

    sent_for_upload.schedule_item.refresh_from_db()
    assert sent_for_upload.schedule_item.youtube_video_id == "vid_123"

    local_storage = storages["localstorage"]
    # thumbnail is not deleted in this case, but the video is
    assert local_storage.exists(
        get_thumbnail_file_name(sent_for_upload.schedule_item.id)
    )
    assert not local_storage.exists(
        get_video_file_name(sent_for_upload.schedule_item.id)
    )


def test_upload_schedule_item_video_with_failing_thumbnail_upload_fails(mocker):
    file_content = BytesIO(b"File")
    file_content.name = "test.mp4"
    file_content.seek(0)

    image_content = BytesIO(b"Image")
    image_content.name = "test.jpg"
    image_content.seek(0)

    conferencevideos_storage = storages["default"]
    conferencevideos_storage.save(
        "videos/test.mp4",
        InMemoryUploadedFile(
            file=file_content,
            field_name="file_field",
            name="test.txt",
            content_type="text/plain",
            size=file_content.getbuffer().nbytes,
            charset="utf-8",
            content_type_extra=None,
        ),
    )

    mocker.patch(
        "schedule.tasks.youtube_videos_insert",
        autospec=True,
        return_value=[{"id": "vid_123"}],
    )
    mocker.patch(
        "schedule.tasks.youtube_videos_set_thumbnail",
        side_effect=HttpError(resp=mock.Mock(status=400), content=b""),
    )
    mocker.patch(
        "schedule.video_upload.cv2.VideoCapture.read",
        return_value=(True, np.array([1])),
    )

    sent_for_upload = ScheduleItemSentForVideoUploadFactory(
        last_attempt_at=None,
        status=ScheduleItemSentForVideoUpload.Status.pending,
        video_uploaded=False,
        thumbnail_uploaded=False,
        schedule_item__type=ScheduleItem.TYPES.talk,
        schedule_item__submission=None,
        schedule_item__title="Test Title",
        schedule_item__description="Test Description",
        schedule_item__video_uploaded_path=conferencevideos_storage.path(
            "videos/test.mp4"
        ),
        schedule_item__conference__video_title_template="{{ title }}",
        schedule_item__conference__video_description_template="{{ abstract }}",
    )

    with pytest.raises(HttpError):
        upload_schedule_item_video(
            sent_for_video_upload_state_id=sent_for_upload.id,
        )


def test_create_and_send_voucher_to_speaker(mocker):
    mock_create = mocker.patch(
        "conferences.vouchers.create_voucher", return_value={"id": 123}
    )
    mock_send_email = mocker.patch("schedule.tasks.send_conference_voucher_email")

    schedule_item = ScheduleItemFactory(type=ScheduleItem.TYPES.talk)
    create_and_send_voucher_to_speaker(schedule_item.id)

    assert (
        ConferenceVoucher.objects.for_conference(schedule_item.conference)
        .filter(
            user=schedule_item.submission.speaker,
            voucher_type=ConferenceVoucher.VoucherType.SPEAKER,
        )
        .exists()
    )

    mock_create.assert_called_once()
    mock_send_email.delay.assert_called_once()


def test_create_and_send_voucher_to_speaker_to_speaker_and_co_speakers(mocker):
    mock_create = mocker.patch(
        "conferences.vouchers.create_voucher", return_value={"id": 123}
    )
    mock_send_email = mocker.patch("schedule.tasks.send_conference_voucher_email")

    schedule_item = ScheduleItemFactory(
        type=ScheduleItem.TYPES.talk,
    )
    additional_speaker_1 = ScheduleItemAdditionalSpeakerFactory(
        scheduleitem=schedule_item
    ).user
    additional_speaker_2 = ScheduleItemAdditionalSpeakerFactory(
        scheduleitem=schedule_item
    ).user

    create_and_send_voucher_to_speaker(schedule_item.id)

    speaker_voucher = (
        ConferenceVoucher.objects.for_conference(schedule_item.conference)
        .filter(
            user=schedule_item.submission.speaker,
            voucher_type=ConferenceVoucher.VoucherType.SPEAKER,
        )
        .get()
    )

    co_speaker_voucher = (
        ConferenceVoucher.objects.for_conference(schedule_item.conference)
        .filter(
            user=additional_speaker_1,
            voucher_type=ConferenceVoucher.VoucherType.CO_SPEAKER,
        )
        .get()
    )

    assert not (
        ConferenceVoucher.objects.for_conference(schedule_item.conference)
        .filter(
            user=additional_speaker_2,
            voucher_type=ConferenceVoucher.VoucherType.CO_SPEAKER,
        )
        .exists()
    )

    assert mock_create.call_count == 2
    mock_send_email.delay.assert_has_calls(
        [
            mock.call(conference_voucher_id=speaker_voucher.id),
            mock.call(conference_voucher_id=co_speaker_voucher.id),
        ],
        any_order=True,
    )


def test_create_and_send_voucher_to_speaker_works_if_existing_voucher_is_for_different_conf(
    mocker,
):
    mock_create = mocker.patch(
        "conferences.vouchers.create_voucher", return_value={"id": 123}
    )
    mock_send_email = mocker.patch("schedule.tasks.send_conference_voucher_email")

    schedule_item = ScheduleItemFactory(type=ScheduleItem.TYPES.talk)

    ConferenceVoucherFactory(
        user=schedule_item.submission.speaker,
    )

    create_and_send_voucher_to_speaker(schedule_item.id)

    assert (
        ConferenceVoucher.objects.for_conference(schedule_item.conference)
        .filter(
            user=schedule_item.submission.speaker,
            voucher_type=ConferenceVoucher.VoucherType.SPEAKER,
        )
        .exists()
    )

    mock_create.assert_called_once()
    mock_send_email.delay.assert_called_once()


def test_create_and_send_voucher_to_speaker_does_nothing_if_voucher_exists(mocker):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("schedule.tasks.send_conference_voucher_email")

    schedule_item = ScheduleItemFactory(type=ScheduleItem.TYPES.talk)

    ConferenceVoucherFactory(
        conference=schedule_item.conference,
        user=schedule_item.submission.speaker,
    )

    create_and_send_voucher_to_speaker(schedule_item.id)

    mock_create.assert_not_called()
    mock_send_email.delay.assert_not_called()


def test_create_and_send_voucher_to_speaker_does_nothing_if_schedule_item_does_not_hav_speakers(
    mocker,
):
    mock_create = mocker.patch("conferences.vouchers.create_voucher")
    mock_send_email = mocker.patch("schedule.tasks.send_conference_voucher_email")

    schedule_item = ScheduleItemFactory(type=ScheduleItem.TYPES.talk, submission=None)

    create_and_send_voucher_to_speaker(schedule_item.id)

    mock_create.assert_not_called()
    mock_send_email.delay.assert_not_called()
