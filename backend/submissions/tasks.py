from pythonit_toolkit.emails.templates import EmailTemplate
from notifications.emails import send_email
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
        token=conference.slack_new_proposal_incoming_webhook_url,
    )


@app.task
def send_proposal_rejected_email(proposal_id):
    from submissions.models import Submission

    submission = Submission.objects.get(id=proposal_id)
    submission_speaker = submission.speaker

    language_code = submission.languages.first().code
    conference_name = submission.conference.name.localize(language_code)

    send_email(
        template=EmailTemplate.SUBMISSION_REJECTED,
        to=submission_speaker.email,
        subject=f"[{conference_name}] Update about your proposal",
        variables={
            "firstname": get_name(submission_speaker, "there"),
            "conferenceName": conference_name,
            "submissionTitle": submission.title.localize(language_code),
            "submissionType": submission.type.name,
        },
    )
    logger.info("Sending email to speaker for rejected proposal %s", submission.id)


@app.task
def send_proposal_in_waiting_list_email(proposal_id):
    from submissions.models import Submission

    submission = Submission.objects.get(id=proposal_id)
    submission_speaker = submission.speaker

    language_code = submission.languages.first().code
    conference_name = submission.conference.name.localize(language_code)

    send_email(
        template=EmailTemplate.SUBMISSION_IN_WAITING_LIST,
        to=submission_speaker.email,
        subject=f"[{conference_name}] Speakers Waiting List",
        variables={
            "firstname": get_name(submission_speaker, "there"),
            "conferenceName": conference_name,
            "submissionTitle": submission.title.localize(language_code),
            "submissionType": submission.type.name,
        },
    )
    logger.info(
        "Sending email to speaker in waiting list for proposal %s", submission.id
    )
