from pythonit_toolkit.pastaporto.entities import Pastaporto

from conferences.models import Conference
from pretix.db import user_has_admission_ticket
from submissions.models import Submission


def pastaporto_user_info_can_vote(pastaporto: Pastaporto, conference: Conference):
    user_info = pastaporto.user_info

    if user_info.is_staff:
        return True

    if Submission.objects.filter(
        speaker_id=user_info.id, conference=conference
    ).exists():
        return True

    return user_has_admission_ticket(user_info.email, conference.pretix_event_id)
