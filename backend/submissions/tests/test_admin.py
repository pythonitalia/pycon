from unittest.mock import call
import pytest
from submissions.admin import (
    send_proposal_in_waiting_list_email_action,
    send_proposal_rejected_email_action,
)
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db


def test_send_proposal_rejected_email_action(rf, mocker):
    mock_task = mocker.patch("submissions.admin.send_proposal_rejected_email")
    mocker.patch("submissions.admin.messages")

    submission = SubmissionFactory(status=Submission.STATUS.rejected)
    submission_2 = SubmissionFactory(
        conference=submission.conference, status=Submission.STATUS.rejected
    )
    SubmissionFactory(
        conference=submission.conference, status=Submission.STATUS.waiting_list
    )

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


def test_send_proposal_in_waiting_list_email_action(rf, mocker):
    mock_task = mocker.patch("submissions.admin.send_proposal_in_waiting_list_email")
    mocker.patch("submissions.admin.messages")

    submission = SubmissionFactory(status=Submission.STATUS.waiting_list)
    SubmissionFactory(
        conference=submission.conference, status=Submission.STATUS.accepted
    )
    SubmissionFactory(
        conference=submission.conference, status=Submission.STATUS.rejected
    )

    send_proposal_in_waiting_list_email_action(
        None, rf.post("/"), queryset=Submission.objects.all()
    )

    assert mock_task.delay.call_count == 1
    mock_task.delay.assert_has_calls(
        [
            call(submission.id),
        ],
        any_order=True,
    )
