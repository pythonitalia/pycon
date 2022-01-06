from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.pastaporto.entities import Pastaporto
from pythonit_toolkit.service_client import ServiceClient

from conferences.models import Conference
from pretix.db import user_has_admission_ticket
from submissions.models import Submission

IS_USER_MEMBER_OF_PYTHON_ITALIA = """query($userId: ID!) {
    userIdIsMember(id: $userId)
}
"""


def pastaporto_user_info_can_vote(pastaporto: Pastaporto, conference: Conference):
    user_info = pastaporto.user_info

    # User is staff
    if user_info.is_staff:
        return True

    # User is a speaker
    if Submission.objects.filter(
        speaker_id=user_info.id, conference=conference
    ).exists():
        return True

    # User has admission ticket for the current conference
    if user_has_admission_ticket(user_info.email, conference.pretix_event_id):
        return True

    # User is a member of Python Italia
    if user_is_python_italia_member(user_info.id):
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
