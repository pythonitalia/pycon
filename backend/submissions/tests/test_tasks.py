from notifications.models import EmailTemplateIdentifier
from notifications.tests.factories import EmailTemplateFactory
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
        slack_new_proposal_channel_id="C123456",
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


def test_send_proposal_rejected_email(sent_emails):
    submission = SubmissionFactory(
        conference__name=LazyI18nString({"en": "Conf"}),
        title=LazyI18nString({"en": "Title"}),
        speaker__full_name="Marco",
        status=Submission.STATUS.rejected,
    )

    EmailTemplateFactory(
        conference=submission.conference,
        identifier=EmailTemplateIdentifier.proposal_rejected,
    )

    send_proposal_rejected_email(
        proposal_id=submission.id,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.proposal_rejected
    assert sent_email.email_template.conference == submission.conference
    assert sent_email.recipient == submission.speaker
    assert sent_email.recipient_email == submission.speaker.email
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["proposal_title"] == "Title"
    assert sent_email.placeholders["proposal_type"] == submission.type.name
    assert sent_email.placeholders["conference_name"] == "Conf"
    assert sent_email.placeholders["speaker_name"] == "Marco"


def test_send_proposal_in_waiting_list_email(sent_emails):
    submission = SubmissionFactory(
        conference__name=LazyI18nString({"en": "Conf"}),
        title=LazyI18nString({"en": "Title"}),
        speaker__full_name="Marco",
        status=Submission.STATUS.waiting_list,
    )

    EmailTemplateFactory(
        conference=submission.conference,
        identifier=EmailTemplateIdentifier.proposal_in_waiting_list,
    )

    send_proposal_in_waiting_list_email(
        proposal_id=submission.id,
    )

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.proposal_in_waiting_list
    assert sent_email.email_template.conference == submission.conference
    assert sent_email.recipient == submission.speaker
    assert sent_email.recipient_email == submission.speaker.email
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["proposal_title"] == "Title"
    assert sent_email.placeholders["proposal_type"] == submission.type.name
    assert sent_email.placeholders["conference_name"] == "Conf"
    assert sent_email.placeholders["speaker_name"] == "Marco"
