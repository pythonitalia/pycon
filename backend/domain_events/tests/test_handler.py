from unittest.mock import patch

import respx
from django.conf import settings

from domain_events.handler import handle_new_cfp_submission


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
                    "user": {
                        "fullname": "Marco Acierno",
                        "name": "Marco",
                        "username": "marco",
                    }
                }
            }
        )
        handle_new_cfp_submission(data)

    slack_mock.send_message.assert_called_once()
    assert "Marco Acierno" in str(slack_mock.send_message.mock_calls[0])
