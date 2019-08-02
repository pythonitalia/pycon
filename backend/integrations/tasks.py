from functools import wraps

from celery import shared_task
from django.conf import settings
from integrations import slack


def switchable_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if settings.USE_SCHEDULER:
            return func.delay(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper


@switchable_task
@shared_task
def notify_new_submission(
    title: str,
    elevator_pitch: str,
    submission_type: str,
    admin_url,
    topic: str,
    duration: int,
):
    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New _{submission_type}_ Submission",
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
                            {"type": "mrkdwn", "text": "*Topic*"},
                            {"type": "mrkdwn", "text": "*Duration*"},
                            {"type": "plain_text", "text": str(duration)},
                            {"type": "mrkdwn", "text": str(topic)},
                        ],
                    }
                ]
            }
        ],
    )
