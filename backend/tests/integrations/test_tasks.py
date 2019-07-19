from unittest.mock import MagicMock, patch

from django.test import override_settings
from integrations.tasks import notify_new_submission, switchable_task


def test_notify_new_submission():
    with patch("integrations.slack.send_message") as m1:
        notify_new_submission(
            "test_title",
            "test_elevator_pitch",
            "test_submission_type",
            "test_admin_url",
            "test_topic",
            42,
        )

    blocks = m1.call_args[0][0]
    attachments = m1.call_args[0][1]

    assert blocks[0]["text"]["text"] == "New _test_submission_type_ Submission"
    assert (
        attachments[0]["blocks"][0]["text"]["text"]
        == "*<test_admin_url|Test_title>*\n*"
        "Elevator Pitch*\ntest_elevator_pitch"
    )
    assert attachments[0]["blocks"][0]["fields"][2]["text"] == "42"
    assert attachments[0]["blocks"][0]["fields"][3]["text"] == "test_topic"


@override_settings(USE_SCHEDULER=True)
def test_switchable_task():
    def dummy_task():
        pass

    dummy_task.delay = MagicMock()
    switchable_dummy_task = switchable_task(dummy_task)

    switchable_dummy_task()

    assert dummy_task.delay.called
