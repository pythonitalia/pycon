from i18n.strings import LazyI18nString

from unittest.mock import patch
from conferences.tests.factories import ConferenceFactory
import pytest
from pythonit_toolkit.emails.templates import EmailTemplate
from submissions.tasks import notify_new_cfp_submission, send_proposal_rejected_email
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


def test_send_proposal_rejected_email(mocker):
    submission = SubmissionFactory(
        conference__name=LazyI18nString({"en": "Conf"}),
        title=LazyI18nString({"en": "Title"}),
        speaker__full_name="Marco",
    )
    mock_send_email = mocker.patch("submissions.tasks.send_email")

    send_proposal_rejected_email(
        proposal_id=submission.id,
    )

    mock_send_email.assert_called_once_with(
        template=EmailTemplate.SUBMISSION_REJECTED,
        to=submission.speaker.email,
        subject="[Conf] Update about your proposal",
        variables={
            "firstname": "Marco",
            "conferenceName": "Conf",
            "submissionTitle": "Title",
            "submissionType": submission.type.name,
        },
    )
