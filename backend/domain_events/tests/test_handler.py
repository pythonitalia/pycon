from unittest.mock import call, patch

import respx
from django.conf import settings
from pythonit_toolkit.emails.templates import EmailTemplate

from domain_events.handler import (
    handle_new_cfp_submission,
    handle_new_submission_comment,
    handle_send_email_notification_for_new_submission_comment,
    handle_send_slack_notification_for_new_submission_comment,
)


def test_handle_new_cfp_submission():
    data = {
        "title": "test_title",
        "elevator_pitch": "test_elevator_pitch",
        "submission_type": "test_submission_type",
        "admin_url": "test_admin_url",
        "topic": "test_topic",
        "duration": "50",
        "speaker_id": 10,
    }

    with patch("domain_events.handler.slack") as slack_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE}/internal-api").respond(
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
        req_mock.post(f"{settings.USERS_SERVICE}/internal-api").respond(
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
                    "text": "Comment here",
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
        req_mock.post(f"{settings.USERS_SERVICE}/internal-api").respond(
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
                    "text": "Comment here",
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
                    "text": "Comment here",
                    "submissionlink": "https://twitter.it",
                },
            ),
        ],
        any_order=True,
    )


def test_handle_new_submission_comment_slack_action():
    data = {
        "speaker_id": 20,
        "submission_title": "Test submission",
        "author_id": 10,
        "admin_url": "https://google.it",
        "submission_url": "https://twitter.it",
        "comment": "Comment here",
    }

    with patch("domain_events.handler.slack") as slack_mock, respx.mock as req_mock:
        req_mock.post(f"{settings.USERS_SERVICE}/internal-api").respond(
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
