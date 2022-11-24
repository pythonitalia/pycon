from typing import List, Optional

import strawberry
from strawberry.types import Info

from api.grants.types import GrantRequest
from api.participants.types import Participant
from api.pretix.query import get_user_orders, get_user_tickets
from api.pretix.types import AttendeeTicket, PretixOrder
from api.submissions.types import Submission
from conferences.models import Conference
from grants.models import Grant as GrantModel
from participants.models import Participant as ParticipantModel
from submissions.models import Submission as SubmissionModel


@strawberry.federation.type(keys=["id"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    email: str = strawberry.federation.field(external=True)
    isStaff: bool = strawberry.federation.field(external=True)

    @classmethod
    def resolve_reference(
        cls, id: strawberry.ID, email: str = "", isStaff: bool = False
    ):
        return cls(id=id, email=email, isStaff=isStaff)

    @strawberry.field
    def grant(self, info: Info, conference: str) -> Optional[GrantRequest]:
        grant = GrantModel.objects.filter(
            user_id=self.id, conference__code=conference
        ).first()
        return GrantRequest.from_model(grant) if grant else None

    @strawberry.field
    def participant(self, info, conference: str) -> Optional[Participant]:
        participant = ParticipantModel.objects.filter(
            user_id=self.id,
            conference__code=conference,
        ).first()
        return Participant.from_model(participant) if participant else None

    @strawberry.federation.field(requires=["email"])
    def orders(self, info, conference: str) -> List[PretixOrder]:
        conference = Conference.objects.get(code=conference)
        return get_user_orders(conference, self.email)

    @strawberry.federation.field(requires=["email"])
    def tickets(self, info, conference: str, language: str) -> List[AttendeeTicket]:
        conference = Conference.objects.get(code=conference)
        return get_user_tickets(conference, self.email, language)

    @strawberry.field
    def submissions(self, info, conference: str) -> List[Submission]:
        return SubmissionModel.objects.filter(
            speaker_id=self.id, conference__code=conference
        )

    @strawberry.federation.field(requires=["isStaff"])
    def can_edit_schedule(self) -> bool:
        return self.isStaff


@strawberry.type
class Country:
    code: str
    name: str
