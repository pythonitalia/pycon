from unittest.mock import patch

import respx
from django.conf import settings

from domain_events.handler import (
    handle_new_cfp_submission,
    handle_new_submission_comment,
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


def test_handle_new_submission_comment():
    data = {
        "speaker_id": 20,
        "submission_title": "Test submission",
        "author_id": 10,
        "admin_url": "https://google.it",
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
        handle_new_submission_comment(data)

    slack_mock.send_message.assert_called_once()
    assert "Marco Acierno" in str(slack_mock.send_message.mock_calls[0])
    assert "Speaker Name" in str(slack_mock.send_message.mock_calls[0])
    assert "Test submission" in str(slack_mock.send_message.mock_calls[0])
