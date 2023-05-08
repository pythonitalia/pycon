from typing import Optional
from django.conf import settings
import strawberry
from strawberry.tools import create_type

from api.participants.types import Participant
from participants.models import Participant as ParticipantModel
from api.context import Info
from api.helpers.ids import decode_hashid


@strawberry.field
def participant(
    info: Info, user_id: strawberry.ID, conference: str
) -> Optional[Participant]:
    user = info.context.request.user
    decoded_id = decode_hashid(user_id, salt=settings.USER_ID_HASH_SALT, min_length=6)
    participant = ParticipantModel.objects.filter(
        conference__code=conference, user_id=decoded_id
    ).first()

    if (
        not participant
        or not participant.public_profile
        and participant.user_id != user.id
    ):
        # Profile doesn't exist, or
        # Profile is not public, and the person requesting it is not the owner
        return None

    return Participant.from_model(participant)


ParticipantQueries = create_type("ParticipantQueries", (participant,))
