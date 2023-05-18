import json
from typing import Optional
from django.conf import settings
import strawberry
from strawberry.tools import create_type
import pretix
from api.participants.types import Participant
from participants.models import Participant as ParticipantModel
from api.context import Info
from api.helpers.ids import decode_hashid, encode_hashid
from api.permissions import HasTokenPermission
from badges.roles import ConferenceRole, get_conference_roles_for_ticket_data
from users.client import get_user_by_email
from conferences.models import Conference


@strawberry.field
def participant(
    info: Info, user_id: strawberry.ID, conference: str
) -> Optional[Participant]:
    user = info.context.request.user
    decoded_id = decode_hashid(user_id, salt=settings.USER_ID_HASH_SALT, min_length=6)
    participant = ParticipantModel.objects.filter(
        conference__code=conference, user_id=decoded_id
    ).first()

    if not participant or (
        not participant.public_profile and (not user or participant.user_id != user.id)
    ):
        # Profile doesn't exist, or
        # Profile is not public, and the person requesting it is not the owner
        return None

    return Participant.from_model(participant)


@strawberry.field
def ticket_id_to_user_hashid(
    ticket_id: strawberry.ID, conference_code: str
) -> Optional[str]:
    conference = Conference.objects.filter(code=conference_code).first()
    decoded_ticket_id = decode_hashid(ticket_id)
    order_position = pretix.get_order_position(conference, decoded_ticket_id)

    if not order_position:
        return None

    attendee_email = order_position["attendee_email"]
    attendee_user = get_user_by_email(attendee_email)
    if not attendee_user:
        return None

    user_id = attendee_user["id"]
    return encode_hashid(int(user_id), salt=settings.USER_ID_HASH_SALT, min_length=6)


# TODO: move this to a badge app :)
@strawberry.type
class TicketDataConferenceRole:
    role: ConferenceRole
    ticket_hashid: str


@strawberry.field(permission_classes=[HasTokenPermission])
def conference_role_for_ticket_data(
    conference_code: str, raw_ticket_data: str
) -> TicketDataConferenceRole:
    conference = Conference.objects.filter(code=conference_code).first()
    assert conference

    ticket_data = json.loads(raw_ticket_data)
    attendee_email = ticket_data["attendee_email"]
    attendee_user = get_user_by_email(attendee_email)
    user_id = attendee_user["id"]

    roles = get_conference_roles_for_ticket_data(
        conference,
        user_id=user_id,
        data=ticket_data,
    )
    return TicketDataConferenceRole(
        role=roles[0],
        ticket_hashid=encode_hashid(
            ticket_data["id"],
        ),
    )


ParticipantQueries = create_type(
    "ParticipantQueries",
    (participant, ticket_id_to_user_hashid, conference_role_for_ticket_data),
)
