import json
from unittest.mock import ANY, patch

import pytest

from domain_events.publisher import (
    notify_new_submission,
    publish_message,
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
    send_schedule_invitation_email,
    send_speaker_voucher_email,
)
from grants.models import Grant
from schedule.models import ScheduleItem


def test_publish_message(settings):
    settings.SQS_QUEUE_URL = "sqs://fake-queue"

    with patch("domain_events.publisher.boto3") as mock_boto:
        publish_message("MessageType", {"body": "123"}, deduplication_id="idid")

    mock_boto.resource().Queue.assert_called_with(settings.SQS_QUEUE_URL)
    mock_boto.resource().Queue().send_message.assert_called_once_with(
        MessageBody=json.dumps({"body": "123"}),
        MessageAttributes={
            "MessageType": {"StringValue": "MessageType", "DataType": "String"}
        },
        MessageDeduplicationId="MessageType-idid",
        MessageGroupId="MessageType",
    )


def test_notify_new_submission():
    with patch("domain_events.publisher.publish_message") as mock_publish:
        notify_new_submission(
            1,
            "test_title",
            "test_elevator_pitch",
            "test_submission_type",
            "test_admin_url",
            42,
            "test_topic",
            10,
            123,
            "a,b",
        )

    mock_publish.assert_called_once_with(
        "NewCFPSubmission",
        {
            "title": "test_title",
            "elevator_pitch": "test_elevator_pitch",
            "submission_type": "test_submission_type",
            "admin_url": "test_admin_url",
            "topic": "test_topic",
            "duration": "42",
            "speaker_id": 10,
            "conference_id": 123,
            "tags": "a,b",
        },
        deduplication_id="1",
    )


@pytest.mark.django_db
def test_send_schedule_invitation_email_reminder(
    schedule_item_factory, submission_factory, settings
):
    settings.FRONTEND_URL = "https://pycon.it"
    schedule_item = schedule_item_factory(
        type=ScheduleItem.TYPES.talk, submission=submission_factory()
    )
    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_schedule_invitation_email(schedule_item, is_reminder=True)

    mock_publish.assert_called_once_with(
        "ScheduleInvitationReminderSent",
        body={
            "speaker_id": schedule_item.submission.speaker_id,
            "submission_title": schedule_item.submission.title,
            "invitation_url": f"https://pycon.it/schedule/invitation/{schedule_item.submission.hashid}",
            "is_reminder": True,
        },
        deduplication_id=str(schedule_item.id),
    )


@pytest.mark.django_db
def test_send_schedule_invitation_email(
    schedule_item_factory, submission_factory, settings
):
    settings.FRONTEND_URL = "https://pycon.it"
    schedule_item = schedule_item_factory(
        type=ScheduleItem.TYPES.talk, submission=submission_factory()
    )
    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_schedule_invitation_email(schedule_item, is_reminder=False)

    mock_publish.assert_called_once_with(
        "ScheduleInvitationSent",
        body={
            "speaker_id": schedule_item.submission.speaker_id,
            "submission_title": schedule_item.submission.title,
            "invitation_url": f"https://pycon.it/schedule/invitation/{schedule_item.submission.hashid}",
            "is_reminder": False,
        },
        deduplication_id=str(schedule_item.id),
    )


@pytest.mark.django_db
def test_send_speaker_voucher_email(speaker_voucher_factory):
    speaker_voucher = speaker_voucher_factory(
        user_id=123,
        voucher_code="ABC123",
        pretix_voucher_id=2,
    )

    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_speaker_voucher_email(speaker_voucher)

    mock_publish.assert_called_once_with(
        "SpeakerVoucherEmailSent",
        body={
            "speaker_id": 123,
            "voucher_code": "ABC123",
        },
        deduplication_id=str(speaker_voucher.id),
    )


@pytest.mark.django_db
def test_send_grant_reply_approved_email(grant_factory):
    grant = grant_factory(status=Grant.Status.approved)
    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_grant_reply_approved_email(grant)

    mock_publish.assert_called_once_with(
        "GrantReplyApprovedSent",
        body={
            "grant_id": grant.id,
            "is_reminder": False,
        },
        deduplication_id=ANY,
    )


@pytest.mark.django_db
def test_send_grant_reply_approved_email_reminder(grant_factory):
    grant = grant_factory(status=Grant.Status.approved)
    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_grant_reply_approved_email(grant, is_reminder=True)

    mock_publish.assert_called_once_with(
        "GrantReplyApprovedReminderSent",
        body={
            "grant_id": grant.id,
            "is_reminder": True,
        },
        deduplication_id=ANY,
    )


@pytest.mark.django_db
def test_send_grant_reply_waiting_list_email(grant_factory):
    grant = grant_factory(status=Grant.Status.waiting_list)
    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_grant_reply_waiting_list_email(grant)

    mock_publish.assert_called_once_with(
        "GrantReplyWaitingListSent",
        body={
            "grant_id": grant.id,
        },
        deduplication_id=str(grant.id),
    )


@pytest.mark.django_db
def test_send_grant_reply_rejected_email(grant_factory):
    grant = grant_factory(status=Grant.Status.rejected)
    with patch("domain_events.publisher.publish_message") as mock_publish:
        send_grant_reply_rejected_email(grant)

    mock_publish.assert_called_once_with(
        "GrantReplyRejectedSent",
        body={
            "grant_id": grant.id,
        },
        deduplication_id=str(grant.id),
    )
