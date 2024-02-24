from i18n.strings import LazyI18nString

from unittest.mock import patch
from conferences.tests.factories import ConferenceFactory
import pytest
from submissions.models import Submission
from submissions.tasks import (
    notify_new_cfp_submission,
    send_proposal_in_waiting_list_email,
    send_proposal_rejected_email,
)
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_handle_new_cfp_submission():
    user = UserFactory(
        full_name="Marco Acierno",
        email="marco@placeholder.it",
        name="Marco",
        username="marco",
    )

    conference = ConferenceFactory(
        slack_new_proposal_comment_incoming_webhook_url="https://123",
        slack_new_proposal_incoming_webhook_url="https://456",
    )

    submission = SubmissionFactory(
        conference=conference,
        speaker=user,
    )

    with patch("submissions.tasks.slack") as slack_mock:
        notify_new_cfp_submission(
            submission_id=submission.id,
            conference_id=conference.id,
            admin_url="https://admin/",
        )

    slack_mock.send_message.assert_called_once()
    assert "Marco Acierno" in str(slack_mock.send_message.mock_calls[0])
    assert "https://456" in str(slack_mock.send_message.mock_calls[0])


def test_send_proposal_rejected_email(sent_emails):
    submission = SubmissionFactory(
        conference__name=LazyI18nString({"en": "Conf"}),
        title=LazyI18nString({"en": "Title"}),
        speaker__full_name="Marco",
        status=Submission.STATUS.rejected,
    )

    send_proposal_rejected_email(
        proposal_id=submission.id,
    )

    assert len(sent_emails) == 1
    assert sent_emails[0]["to"] == submission.speaker.email
    assert sent_emails[0]["subject"] == "[Conf] Update about your proposal"
    assert sent_emails[0]["variables"]["firstname"] == "Marco"
    assert sent_emails[0]["variables"]["conferenceName"] == "Conf"
    assert sent_emails[0]["variables"]["submissionTitle"] == "Title"
    assert sent_emails[0]["variables"]["submissionType"] == submission.type.name


def test_send_proposal_in_waiting_list_email(sent_emails):
    submission = SubmissionFactory(
        conference__name=LazyI18nString({"en": "Conf"}),
        title=LazyI18nString({"en": "Title"}),
        speaker__full_name="Marco",
        status=Submission.STATUS.waiting_list,
    )

    send_proposal_in_waiting_list_email(
        proposal_id=submission.id,
    )

    assert len(sent_emails) == 1
    assert sent_emails[0]["to"] == submission.speaker.email
    assert sent_emails[0]["subject"] == "[Conf] Speakers Waiting List"
    assert sent_emails[0]["variables"]["firstname"] == "Marco"
    assert sent_emails[0]["variables"]["conferenceName"] == "Conf"
    assert sent_emails[0]["variables"]["submissionTitle"] == "Title"
    assert sent_emails[0]["variables"]["submissionType"] == submission.type.name
