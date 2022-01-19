from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.service_client import ServiceClient

from integrations import slack

USERS_NAMES_FROM_IDS = """query UserNamesFromIds($ids: [ID!]!) {
    usersByIds(ids: $ids) {
        id
        fullname
        name
        username
    }
}"""


def execute_service_client_query(query, variables):
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    return async_to_sync(client.execute)(query, variables)


def get_name(user_data):
    return (
        user_data["fullname"]
        or user_data["name"]
        or user_data["username"]
        or "<no name specified>"
    )


def handle_new_submission_comment(data):
    speaker_id = data["speaker_id"]
    submission_title = data["submission_title"]
    author_id = data["author_id"]
    admin_url = data["admin_url"]
    comment = data["comment"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id, author_id]}
    )
    users_by_id = {user["id"]: user for user in users_result.data["usersByIds"]}

    speaker_name = get_name(users_by_id[speaker_id])
    comment_author_name = get_name(users_by_id[author_id])

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New comment on submission {submission_title}",
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
                            "text": f"*<{admin_url}|Open admin>*\n"
                            f"*Comment*\n{comment}",
                        },
                        "fields": [
                            {"type": "mrkdwn", "text": "*Submission Author*"},
                            {"type": "mrkdwn", "text": "*Comment Author*"},
                            {"type": "plain_text", "text": speaker_name},
                            {"type": "plain_text", "text": comment_author_name},
                        ],
                    }
                ]
            }
        ],
        channel="submission-comments",
    )


def handle_new_cfp_submission(data):
    title = data["title"]
    elevator_pitch = data["elevator_pitch"]
    submission_type = data["submission_type"]
    admin_url = data["admin_url"]
    topic = data["topic"]
    duration = data["duration"]
    speaker_id = data["speaker_id"]

    user_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    user_data = user_result.data["usersByIds"][0]
    user_name = get_name(user_data)

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
        channel="cfp",
    )


HANDLERS = {
    "NewSubmissionComment": handle_new_submission_comment,
    "NewCFPSubmission": handle_new_cfp_submission,
}
