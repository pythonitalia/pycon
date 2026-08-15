import strawberry
import strawberry_django
from django.urls import reverse
from strawberry.types import Info

from billing.api.types import BillingAddress
from grants.api.types import Grant
from participants.api.types import Participant
from api.permissions import IsAuthenticated
from pretix.api.query import get_user_orders, get_user_tickets
from pretix.api.types import AttendeeTicket, PretixOrder, PretixOrderStatus
from schedule.api.types import ScheduleItem
from submissions.api.types import Submission
from visa.api.types import InvitationLetterRequest
from association_membership import models as association_membership_models
from badges.roles import ConferenceRole, get_conference_roles_for_user
from billing import models as billing_models
from conferences import models as conference_models
from grants import models as grant_models
from participants import models as participant_models
from pretix import user_has_admission_ticket
from pycon.signing import sign_path
from schedule import models as schedule_models
from submissions import models as submission_models
from users import models as user_models
from visa import models as visa_models

PRETIX_ORDERS_STATUS_ORDER = [
    PretixOrderStatus.PAID,
    PretixOrderStatus.PENDING,
    PretixOrderStatus.CANCELED,
    PretixOrderStatus.EXPIRED,
]


@strawberry.type
class OperationSuccess:
    ok: bool


@strawberry_django.type(user_models.User)
class User:
    id: strawberry.auto
    email: strawberry.auto
    fullname: str = strawberry_django.field(only=["full_name"])
    full_name: strawberry.auto
    name: strawberry.auto
    username: str = strawberry_django.field(only=["username"])
    gender: strawberry.auto
    open_to_recruiting: strawberry.auto
    open_to_newsletter: strawberry.auto
    date_birth: strawberry.auto
    country: strawberry.auto
    is_staff: strawberry.auto

    @strawberry_django.field(only=["id"])
    def hashid(self) -> str:
        return self.user_hashid()

    @strawberry_django.field(only=["id", "email"])
    def conference_roles(self, conference_code: str) -> list[ConferenceRole]:
        conference = conference_models.Conference.objects.get(code=conference_code)
        return get_conference_roles_for_user(
            conference=conference,
            user_id=self.id,
            user_email=self.email,
        )

    @strawberry_django.field(
        only=["id"],
        permission_classes=[IsAuthenticated],
    )
    def user_schedule_favourites_calendar_url(
        self, info: Info, conference: str
    ) -> str | None:
        conference_id = (
            conference_models.Conference.objects.filter(code=conference)
            .values_list("id", flat=True)
            .first()
        )

        if not conference_id:
            return

        return info.context.request.build_absolute_uri(
            sign_path(
                reverse(
                    "user-schedule-favourites-calendar",
                    kwargs={
                        "conference_id": conference_id,
                        "hash_user_id": self.user_hashid(),
                    },
                )
            )
        )

    @strawberry_django.field(only=["id"])
    def starred_schedule_items(self, conference: str) -> list[strawberry.ID]:
        stars = schedule_models.ScheduleItemStar.objects.filter(
            schedule_item__conference__code=conference, user_id=self.id
        ).values_list("schedule_item_id", flat=True)
        return stars

    @strawberry_django.field(permission_classes=[IsAuthenticated])
    def booked_schedule_items(self, conference: str) -> list[ScheduleItem]:
        return (
            schedule_models.ScheduleItem.objects.filter(
                conference__code=conference,
                attendees__user_id=self.id,
                slot__isnull=False,
            )
            .distinct()
            .order_by("slot__day__day", "slot__hour")
        )

    @strawberry_django.field
    def grant(self, conference: str) -> Grant | None:
        return grant_models.Grant.objects.filter(
            user_id=self.id,
            conference__code=conference,
        )

    @strawberry_django.field
    def participant(self, conference: str) -> Participant | None:
        return participant_models.Participant.objects.filter(
            user_id=self.id,
            conference__code=conference,
        )

    @strawberry.field
    def orders(self, conference: str) -> list[PretixOrder]:
        conference = conference_models.Conference.objects.get(code=conference)
        return sorted(
            get_user_orders(conference, self.email),
            key=lambda order: PRETIX_ORDERS_STATUS_ORDER.index(order.status),
        )

    @strawberry.field
    def tickets(self, conference: str, language: str) -> list[AttendeeTicket]:
        conference = conference_models.Conference.objects.get(code=conference)
        attendee_tickets = get_user_tickets(conference, self.email, language)
        return [ticket for ticket in attendee_tickets]

    @strawberry_django.field(only=["email"])
    def has_admission_ticket(self, conference: str) -> bool:
        conference = conference_models.Conference.objects.filter(
            code=conference
        ).first()

        if not conference:
            return False

        return user_has_admission_ticket(
            email=self.email,
            event_organizer=conference.pretix_organizer_id,
            event_slug=conference.pretix_event_id,
        )

    @strawberry_django.field(only=["id"])
    def submissions(self, conference: str) -> list[Submission]:
        return submission_models.Submission.objects.filter(
            speaker_id=self.id, conference__code=conference
        )

    @strawberry_django.field(only=["is_staff"])
    def can_edit_schedule(self) -> bool:
        return self.is_staff

    @strawberry_django.field(only=["id"])
    def is_python_italia_member(self) -> bool:
        return (
            association_membership_models.Membership.objects.active()
            .of_user(self.id)
            .exists()
        )

    @strawberry_django.field
    def billing_addresses(self, conference: str) -> list[BillingAddress]:
        return billing_models.BillingAddress.objects.of_user(
            self.id
        ).for_conference_code(conference)

    @strawberry_django.field
    def invitation_letter_request(
        self, conference: str
    ) -> InvitationLetterRequest | None:
        return (
            visa_models.InvitationLetterRequest.objects.for_conference_code(conference)
            .of_user(self.id)
            .filter(on_behalf_of=visa_models.InvitationLetterRequestOnBehalfOf.SELF)
        )
