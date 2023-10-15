from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.service_client import ServiceClient

from conferences.models import Conference
from pretix import user_has_admission_ticket
from users.models import User
from submissions.models import Submission

IS_USER_MEMBER_OF_PYTHON_ITALIA = """query($userId: ID!) {
    userIdIsMember(id: $userId)
}
"""


def check_if_user_can_vote(user: User, conference: Conference):
    # User is staff
    if user.is_staff:
        return True

    # User is a speaker
    if Submission.objects.filter(speaker_id=user.id, conference=conference).exists():
        return True

    additional_events = [
        {
            "organizer_slug": included_voting_event.pretix_organizer_id,
            "event_slug": included_voting_event.pretix_event_id,
        }
        for included_voting_event in conference.included_voting_events.all()
    ]

    # User has admission ticket for the current conference
    # or for an included voting event
    if user_has_admission_ticket(
        email=user.email,
        event_organizer=conference.pretix_organizer_id,
        event_slug=conference.pretix_event_id,
        additional_events=additional_events,
    ):
        return True

    # User is a member of Python Italia
    if user_is_python_italia_member(user.id):
        return True

    return False


def user_is_python_italia_member(user_id: int) -> bool:
    client = ServiceClient(
        url=f"{settings.ASSOCIATION_BACKEND_SERVICE}/internal-api",
        service_name="association-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    result = client_execute(IS_USER_MEMBER_OF_PYTHON_ITALIA, {"userId": user_id})
    data = result.data
    return data["userIdIsMember"]
