from conferences.models import Conference
from pretix import user_has_admission_ticket
from users.models import User
from submissions.models import Submission
from association_membership.models import Membership


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
    return Membership.objects.active().of_user(user_id).exists()
