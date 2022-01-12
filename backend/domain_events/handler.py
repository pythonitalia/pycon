from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.service_client import ServiceClient

from integrations import slack

USER_NAME_FROM_ID = """query UserNameFromId($userId: ID!) {
    user(id: $userId) {
        fullname
        name
        username
    }
}"""


def handle_new_cfp_submission(data):
    title = data["title"]
    elevator_pitch = data["elevator_pitch"]
    submission_type = data["submission_type"]
    admin_url = data["admin_url"]
    topic = data["topic"]
    duration = data["duration"]
    speaker_id = data["speaker_id"]

    client = ServiceClient(
        url=f"{settings.USERS_SERVICE}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    user_result = client_execute(USER_NAME_FROM_ID, {"userId": speaker_id})
    user_data = user_result.data
    user_name = (
        user_data["user"]["fullname"]
        or user_data["user"]["name"]
        or user_data["user"]["username"]
        or "<no name specified>"
    )

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New _{submission_type}_ Submission by {user_name}",
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
                            {"type": "mrkdwn", "text": str(topic)},
                            {"type": "plain_text", "text": str(duration)},
                        ],
                    }
                ]
            }
        ],
    )


HANDLERS = {"NewCFPSubmission": handle_new_cfp_submission}
