from notifications.models import EmailTemplate, EmailTemplateIdentifier
from integrations import slack
from grants.tasks import get_name
from users.models import User
import logging

from pycon.celery import app

logger = logging.getLogger(__name__)


@app.task
def notify_new_cfp_submission(*, submission_id, conference_id, admin_url):
    from conferences.models import Conference
    from submissions.models import Submission

    conference = Conference.objects.get(id=conference_id)
    submission = Submission.objects.get(id=submission_id)

    title = submission.title.localize("en")
    elevator_pitch = submission.elevator_pitch.localize("en")
    submission_type = submission.type.name

    speaker_id = submission.speaker_id
    tags = ",".join(submission.tags.values_list("name", flat=True))

    speaker = User.objects.get(id=speaker_id)
    user_name = get_name(speaker)

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New _{submission_type}_ proposal by {user_name}",
                    "type": "mrkdwn",
                },
            }
        ],
        [
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*<{admin_url}|{title.capitalize()}>*\n"
                            f"*Elevator Pitch*\n{elevator_pitch}",
                        },
                        "fields": [
                            {"type": "mrkdwn", "text": "*Tags*"},
                            {"type": "plain_text", "text": str(tags)},
                        ],
                    }
                ]
            }
        ],
        oauth_token=conference.get_slack_oauth_token(),
        channel_id=conference.slack_new_proposal_channel_id,
    )


@app.task
def send_proposal_rejected_email(proposal_id):
    from submissions.models import Submission

    proposal = Submission.objects.get(id=proposal_id)
    proposal_speaker = proposal.speaker

    conference = proposal.conference
    language_code = proposal.languages.first().code
    conference_name = proposal.conference.name

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.proposal_rejected
    )
    email_template.send_email(
        recipient=proposal_speaker,
        placeholders={
            "proposal_title": proposal.title.localize(language_code),
            "proposal_type": proposal.type.name,
            "conference_name": conference_name,
            "speaker_name": get_name(proposal_speaker, "there"),
        },
    )

    logger.info("Sending email to speaker for rejected proposal %s", proposal.id)


@app.task
def send_proposal_in_waiting_list_email(proposal_id):
    from submissions.models import Submission

    proposal = Submission.objects.get(id=proposal_id)
    proposal_speaker = proposal.speaker

    conference = proposal.conference
    language_code = proposal.languages.first().code
    conference_name = proposal.conference.name

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.proposal_in_waiting_list
    )

    email_template.send_email(
        recipient=proposal_speaker,
        placeholders={
            "proposal_title": proposal.title.localize(language_code),
            "proposal_type": proposal.type.name,
            "conference_name": conference_name,
            "speaker_name": get_name(proposal_speaker, "there"),
        },
    )

    logger.info("Sending email to speaker in waiting list for proposal %s", proposal.id)
