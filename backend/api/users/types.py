from logging import getLogger
from typing import List, Optional

import strawberry
from strawberry.types import Info

from api.grants.types import Grant
from api.participants.types import Participant
from api.pretix.query import get_user_orders, get_user_tickets
from api.pretix.types import AttendeeTicket, PretixOrder, PretixOrderStatus
from api.submissions.types import Submission
from conferences.models import Conference
from grants.models import Grant as GrantModel
from participants.models import Participant as ParticipantModel
from schedule.models import ScheduleItemStar as ScheduleItemStarModel
from submissions.models import Submission as SubmissionModel

logger = getLogger(__name__)
PRETIX_ORDERS_STATUS_ORDER = [
    PretixOrderStatus.PAID,
    PretixOrderStatus.PENDING,
    PretixOrderStatus.CANCELED,
    PretixOrderStatus.EXPIRED,
]


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
    def starred_schedule_items(self, info, conference: str) -> List[strawberry.ID]:
        stars = ScheduleItemStarModel.objects.filter(
            schedule_item__conference__code=conference, user_id=self.id
        ).values_list("schedule_item_id", flat=True)
        return stars

    @strawberry.field
    def grant(self, info: Info, conference: str) -> Optional[Grant]:
        grant = GrantModel.objects.filter(
            user_id=self.id, conference__code=conference
        ).first()
        logger.info(
            "Grant: user_id: %s, conference: %s, grant: %s", self.id, conference, grant
        )
        return Grant.from_model(grant) if grant else None

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
        return sorted(
            get_user_orders(conference, self.email),
            key=lambda order: PRETIX_ORDERS_STATUS_ORDER.index(order.status),
        )

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
