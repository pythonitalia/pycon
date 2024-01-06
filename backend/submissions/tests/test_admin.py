from unittest.mock import call
import pytest
from submissions.admin import send_proposal_rejected_email_action
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db


def test_send_proposal_rejected_email_action(rf, mocker):
    mock_task = mocker.patch("submissions.admin.send_proposal_rejected_email")
    mocker.patch("submissions.admin.messages")

    submission = SubmissionFactory()
    submission_2 = SubmissionFactory()

    send_proposal_rejected_email_action(
        None, rf.post("/"), queryset=Submission.objects.all()
    )

    assert mock_task.delay.call_count == 2
    mock_task.delay.assert_has_calls(
        [
            call(submission.id),
            call(submission_2.id),
        ],
        any_order=True,
    )
