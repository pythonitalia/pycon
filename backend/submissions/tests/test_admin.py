from unittest.mock import call
from conferences.tests.factories import ConferenceFactory
from notifications.tests.factories import EmailTemplateFactory
from notifications.models import EmailTemplateIdentifier, SentEmail
import pytest
from submissions.admin import (
    apply_and_notify_status_change,
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


def test_apply_and_notify_status_change(rf, mocker):
    mocker.patch("submissions.admin.messages")

    conference = ConferenceFactory()
    proposal_accepted_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_accepted,
        conference=conference,
    )
    proposal_rejected_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_rejected,
        conference=conference,
    )
    proposal_in_waiting_list_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_in_waiting_list,
        conference=conference,
    )

    accepted_submission = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.accepted,
        speaker__full_name="Marco",
    )

    rejected_submission = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.rejected,
        speaker__full_name="Jane",
    )

    waiting_list_proposal = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.waiting_list,
        speaker__full_name="John",
    )

    apply_and_notify_status_change(
        None,
        rf.post("/"),
        queryset=Submission.objects.filter(status=Submission.STATUS.proposed),
    )

    assert SentEmail.objects.filter(
        recipient=accepted_submission.speaker,
        email_template=proposal_accepted_template,
        conference=conference,
        placeholders={
            "conference_name": conference.name.localize("en"),
            "proposal_title": accepted_submission.title.localize("en"),
            "proposal_type": accepted_submission.type.name,
            "speaker_name": "Marco",
        },
    ).exists()

    assert SentEmail.objects.filter(
        recipient=rejected_submission.speaker,
        email_template=proposal_rejected_template,
        conference=conference,
        placeholders={
            "conference_name": conference.name.localize("en"),
            "proposal_title": rejected_submission.title.localize("en"),
            "proposal_type": rejected_submission.type.name,
            "speaker_name": "Jane",
        },
    ).exists()

    assert SentEmail.objects.filter(
        recipient=waiting_list_proposal.speaker,
        email_template=proposal_in_waiting_list_template,
        conference=conference,
        placeholders={
            "conference_name": conference.name.localize("en"),
            "proposal_title": waiting_list_proposal.title.localize("en"),
            "proposal_type": waiting_list_proposal.type.name,
            "speaker_name": "John",
        },
    ).exists()
