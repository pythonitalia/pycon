from datetime import date
from logging import getLogger
from typing import List, Optional
from django.conf import settings

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
from api.helpers.ids import encode_hashid
from badges.roles import ConferenceRole, get_conference_roles_for_user
from schedule.models import ScheduleItemStar as ScheduleItemStarModel
from submissions.models import Submission as SubmissionModel

logger = getLogger(__name__)

PRETIX_ORDERS_STATUS_ORDER = [
    PretixOrderStatus.PAID,
    PretixOrderStatus.PENDING,
    PretixOrderStatus.CANCELED,
    PretixOrderStatus.EXPIRED,
]


@strawberry.type
class OperationSuccess:
    ok: bool


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    fullname: str
    full_name: str
    name: str
    username: str
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    date_birth: Optional[date]
    country: str
    is_staff: bool

    @strawberry.field
    def hashid(self, info: Info) -> str:
        return encode_hashid(
            int(self.id), salt=settings.USER_ID_HASH_SALT, min_length=6
        )

    @strawberry.field
    def conference_roles(
        self, info: Info, conference_code: str
    ) -> List[ConferenceRole]:
        conference = Conference.objects.get(code=conference_code)
        return get_conference_roles_for_user(
            conference=conference,
            user_id=self.id,
            user_email=self.email,
        )

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

    @strawberry.field
    def orders(self, info, conference: str) -> List[PretixOrder]:
        conference = Conference.objects.get(code=conference)
        return sorted(
            get_user_orders(conference, self.email),
            key=lambda order: PRETIX_ORDERS_STATUS_ORDER.index(order.status),
        )

    @strawberry.field
    def tickets(self, info, conference: str, language: str) -> List[AttendeeTicket]:
        conference = Conference.objects.get(code=conference)
        attendee_tickets = get_user_tickets(conference, self.email, language)
        return [ticket for ticket in attendee_tickets]

    @strawberry.field
    def submissions(self, info, conference: str) -> List[Submission]:
        return SubmissionModel.objects.filter(
            speaker_id=self.id, conference__code=conference
        )

    @strawberry.field
    def can_edit_schedule(self) -> bool:
        return self.is_staff

    @strawberry.field
    def is_python_italia_member(self) -> bool:
        # TODO: Implement is_python_italia_member
        return False

    @classmethod
    def from_django_model(cls, user):
        return cls(
            id=user.id,
            email=user.email,
            fullname=user.full_name,
            full_name=user.full_name,
            name=user.name,
            username=user.username,
            gender=user.gender,
            open_to_recruiting=user.open_to_recruiting,
            open_to_newsletter=user.open_to_newsletter,
            date_birth=user.date_birth,
            country=user.country,
            is_staff=user.is_staff,
        )
