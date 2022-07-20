from unittest.mock import call, patch

import pytest
import respx
from django.conf import settings
from pythonit_toolkit.emails.templates import EmailTemplate

from domain_events.handler import (
    handle_new_cfp_submission,
    handle_new_schedule_invitation_answer,
    handle_new_submission_comment,
    handle_schedule_invitation_sent,
    handle_send_email_notification_for_new_submission_comment,
    handle_send_slack_notification_for_new_submission_comment,
    handle_speaker_voucher_email_sent,
    handle_submission_time_slot_changed,
)


@pytest.mark.django_db
def test_handle_new_cfp_submission(conference_factory):
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
        "speaker_id": 10,
        "conference_id": conference.id,
    }

    with patch("domain_events.handler.slack") as slack_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                        }
                    ]
                }
            }
        )
        handle_new_cfp_submission(data)

    slack_mock.send_message.assert_called_once()
    assert "Marco Acierno" in str(slack_mock.send_message.mock_calls[0])
    assert "https://456" in str(slack_mock.send_message.mock_calls[0])


def test_handle_new_submission_comment_triggers_more_actions():
    data = {
        "speaker_id": 20,
        "comment_id": 1,
    }

    with patch("domain_events.handler.publish_message") as mock_publish:
        handle_new_submission_comment(data)

        mock_publish.assert_has_calls(
            calls=[
                call(
                    "NewSubmissionComment/SlackNotification",
                    body=data,
                    deduplication_id="1",
                ),
                call(
                    "NewSubmissionComment/EmailNotification",
                    body=data,
                    deduplication_id="1",
                ),
            ],
            any_order=True,
        )


def test_handle_new_submission_comment_email_action():
    data = {
        "speaker_id": 20,
        "submission_title": "Test submission",
        "author_id": 10,
        "admin_url": "https://google.it",
        "submission_url": "https://twitter.it",
        "comment": "Comment here",
        "all_commenters_ids": [10, 20],
    }

    with patch(
        "domain_events.handler.send_email"
    ) as mock_email, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@email.it",
                        },
                        {
                            "id": 20,
                            "fullname": "Speaker Name",
                            "name": "Speaker",
                            "username": "Speaker",
                            "email": "speaker@email.it",
                        },
                    ]
                }
            }
        )

        handle_send_email_notification_for_new_submission_comment(data)

    assert mock_email.call_count == 1
    mock_email.assert_has_calls(
        calls=[
            call(
                template=EmailTemplate.NEW_COMMENT_ON_SUBMISSION,
                to="speaker@email.it",
                subject="[PyCon Italia 2022] New comment on Submission Test submission",
                variables={
                    "submissionTitle": "Test submission",
                    "userName": "Speaker Name",
                    "submissionlink": "https://twitter.it",
                },
            )
        ]
    )


def test_handle_new_submission_comment_email_action_with_multiple_people():
    data = {
        "speaker_id": 20,
        "submission_title": "Test submission",
        "author_id": 10,
        "admin_url": "https://google.it",
        "submission_url": "https://twitter.it",
        "comment": "Comment here",
        "all_commenters_ids": [10, 20, 30],
    }

    with patch(
        "domain_events.handler.send_email"
    ) as mock_email, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@email.it",
                        },
                        {
                            "id": 20,
                            "fullname": "Speaker Name",
                            "name": "Speaker",
                            "username": "Speaker",
                            "email": "speaker@email.it",
                        },
                        {
                            "id": 30,
                            "fullname": "Ester Beltrami",
                            "name": "Ester",
                            "username": "ester",
                            "email": "ester@email.it",
                        },
                    ]
                }
            }
        )

        handle_send_email_notification_for_new_submission_comment(data)

    assert mock_email.call_count == 2
    mock_email.assert_has_calls(
        calls=[
            call(
                template=EmailTemplate.NEW_COMMENT_ON_SUBMISSION,
                to="speaker@email.it",
                subject="[PyCon Italia 2022] New comment on Submission Test submission",
                variables={
                    "submissionTitle": "Test submission",
                    "userName": "Speaker Name",
                    "submissionlink": "https://twitter.it",
                },
            ),
            call(
                template=EmailTemplate.NEW_COMMENT_ON_SUBMISSION,
                to="ester@email.it",
                subject="[PyCon Italia 2022] New comment on Submission Test submission",
                variables={
                    "submissionTitle": "Test submission",
                    "userName": "Ester Beltrami",
                    "submissionlink": "https://twitter.it",
                },
            ),
        ],
        any_order=True,
    )


@pytest.mark.django_db
def test_handle_new_submission_comment_slack_action(conference_factory):
    conference = conference_factory(
        slack_new_proposal_comment_incoming_webhook_url="https://123",
        slack_new_proposal_incoming_webhook_url="https://456",
    )
    data = {
        "speaker_id": 20,
        "submission_title": "Test submission",
        "author_id": 10,
        "admin_url": "https://google.it",
        "submission_url": "https://twitter.it",
        "comment": "Comment here",
        "conference_id": conference.id,
    }

    with patch("domain_events.handler.slack") as slack_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                        },
                        {
                            "id": 20,
                            "fullname": "Speaker Name",
                            "name": "Speaker",
                            "username": "Speaker",
                        },
                    ]
                }
            }
        )
        handle_send_slack_notification_for_new_submission_comment(data)

    slack_mock.send_message.assert_called_once()
    assert "Marco Acierno" in str(slack_mock.send_message.mock_calls[0])
    assert "Speaker Name" in str(slack_mock.send_message.mock_calls[0])
    assert "Test submission" in str(slack_mock.send_message.mock_calls[0])
    assert "https://123" in str(slack_mock.send_message.mock_calls[0])


def test_handle_schedule_invitation_sent():
    data = {
        "speaker_id": 10,
        "invitation_url": "https://url",
        "submission_title": "Title title",
    }

    with patch(
        "domain_events.handler.send_email"
    ) as email_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@placeholder.it",
                        },
                    ]
                }
            }
        )

        handle_schedule_invitation_sent(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to="marco@placeholder.it",
        subject="[PyCon Italia 2022] Your submission was accepted!",
        variables={
            "submissionTitle": "Title title",
            "firstname": "Marco Acierno",
            "invitationlink": "https://url",
        },
    )


def test_handle_schedule_invitation_sent_reminder():
    data = {
        "speaker_id": 10,
        "invitation_url": "https://url",
        "submission_title": "Title title",
        "is_reminder": True,
    }

    with patch(
        "domain_events.handler.send_email"
    ) as email_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@placeholder.it",
                        },
                    ]
                }
            }
        )

        handle_schedule_invitation_sent(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to="marco@placeholder.it",
        subject="[PyCon Italia 2022] Reminder: Your submission was accepted, confirm your presence",
        variables={
            "submissionTitle": "Title title",
            "firstname": "Marco Acierno",
            "invitationlink": "https://url",
        },
    )


def test_handle_submission_time_slot_changed():
    data = {
        "speaker_id": 10,
        "invitation_url": "https://url",
        "submission_title": "Title title",
    }

    with patch(
        "domain_events.handler.send_email"
    ) as email_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@placeholder.it",
                        },
                    ]
                }
            }
        )

        handle_submission_time_slot_changed(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_SCHEDULE_TIME_CHANGED,
        to="marco@placeholder.it",
        subject="[PyCon Italia 2022] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": "Title title",
            "firstname": "Marco Acierno",
            "invitationlink": "https://url",
        },
    )


def test_handle_new_schedule_invitation_answer(settings):
    settings.SPEAKERS_EMAIL_ADDRESS = "speakers@placeholder.com"

    data = {
        "speaker_id": 10,
        "submission_title": "Title title",
        "answer": "Yellow",
        "speaker_notes": "Sub",
        "time_slot": "2020-10-10 13:00",
        "invitation_admin_url": "https://admin",
        "schedule_item_admin_url": "https://schedule",
    }

    with patch(
        "domain_events.handler.send_email"
    ) as email_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@placeholder.it",
                        },
                    ]
                }
            }
        )

        handle_new_schedule_invitation_answer(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.NEW_SCHEDULE_INVITATION_ANSWER,
        to="speakers@placeholder.com",
        subject="[PyCon Italia 2022] Schedule Invitation Answer: Title title",
        variables={
            "submissionTitle": "Title title",
            "speakerName": "Marco Acierno",
            "speakerEmail": "marco@placeholder.it",
            "timeSlot": "2020-10-10 13:00",
            "answer": "Yellow",
            "notes": "Sub",
            "invitationAdminUrl": "https://admin",
            "scheduleItemAdminUrl": "https://schedule",
        },
        reply_to=["marco@placeholder.it"],
    )


def test_handle_speaker_voucher_email_sent(settings):
    settings.SPEAKERS_EMAIL_ADDRESS = "speakers@placeholder.com"

    data = {
        "speaker_id": 10,
        "voucher_code": "ABC123",
    }

    with patch(
        "domain_events.handler.send_email"
    ) as email_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "email": "marco@placeholder.it",
                        },
                    ]
                }
            }
        )

        handle_speaker_voucher_email_sent(data)

    email_mock.assert_called_once_with(
        template=EmailTemplate.SPEAKER_VOUCHER_CODE,
        to="marco@placeholder.it",
        subject="[PyCon Italia 2022] Your Speaker Voucher Code",
        variables={"firstname": "Marco Acierno", "voucherCode": "ABC123"},
        reply_to=["speakers@placeholder.com"],
    )
