from unittest.mock import patch

from domain_events.handler import handle_new_cfp_submission


def test_handle_new_cfp_submission():
    data = {
        "title": "test_title",
        "elevator_pitch": "test_elevator_pitch",
        "submission_type": "test_submission_type",
        "admin_url": "test_admin_url",
        "topic": "test_topic",
        "duration": "50",
    }

    with patch("domain_events.handler.slack") as slack_mock:
        handle_new_cfp_submission(data)

    slack_mock.send_message.assert_called_once()
