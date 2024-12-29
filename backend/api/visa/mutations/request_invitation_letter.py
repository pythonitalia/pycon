from django.db import transaction
from datetime import date
from typing import Annotated
from api.types import BaseErrorType, FormNotAvailable, NoAdmissionTicket
from api.utils import validate_email
from api.visa.types import InvitationLetterOnBehalfOf, InvitationLetterRequest
from api.extensions import RateLimit
from conferences.models.deadline import Deadline
from privacy_policy.record import record_privacy_policy_acceptance
from visa.models import (
    InvitationLetterRequest as InvitationLetterRequestModel,
    InvitationLetterRequestOnBehalfOf,
)
from api.permissions import IsAuthenticated
from api.context import Context
from api.conferences.types import Conference
from conferences.models import Conference as ConferenceModel
from pretix import user_has_admission_ticket
import strawberry

MAX_LENGTH_FIELDS = {
    "email": 254,
    "full_name": 300,
    "nationality": 100,
    "address": 300,
    "passport_number": 20,
    "embassy_name": 300,
}


@strawberry.type
class InvitationLetterAlreadyRequested:
    message: str = "Invitation letter has already been requested for this conference"


@strawberry.type
class RequestInvitationLetterErrors(BaseErrorType):
    @strawberry.type
    class _RequestInvitationLetterErrors:
        conference: list[str] = strawberry.field(default_factory=list)
        on_behalf_of: list[str] = strawberry.field(default_factory=list)
        email: list[str] = strawberry.field(default_factory=list)
        full_name: list[str] = strawberry.field(default_factory=list)
        date_of_birth: list[str] = strawberry.field(default_factory=list)
        nationality: list[str] = strawberry.field(default_factory=list)
        address: list[str] = strawberry.field(default_factory=list)
        passport_number: list[str] = strawberry.field(default_factory=list)
        embassy_name: list[str] = strawberry.field(default_factory=list)

    errors: _RequestInvitationLetterErrors = None


@strawberry.input
class RequestInvitationLetterInput:
    conference: str
    on_behalf_of: InvitationLetterOnBehalfOf
    email: str
    full_name: str
    nationality: str
    address: str
    passport_number: str
    embassy_name: str
    date_of_birth: date

    def validate(self, conference: Conference) -> RequestInvitationLetterErrors | None:
        errors = RequestInvitationLetterErrors()

        required_fields = [
            "conference",
            "on_behalf_of",
            "full_name",
            "nationality",
            "address",
            "passport_number",
            "embassy_name",
            "date_of_birth",
        ]

        if self.on_behalf_of == InvitationLetterOnBehalfOf.OTHER:
            required_fields.append("email")

        for field_name in required_fields:
            if not getattr(self, field_name):
                errors.add_error(field_name, "This field is required")

        for field_name, max_length in MAX_LENGTH_FIELDS.items():
            value = getattr(self, field_name)

            if value and len(value) > max_length:
                errors.add_error(
                    field_name,
                    f"Ensure this field has no more than {max_length} characters",
                )

        if self.email and not validate_email(self.email):
            errors.add_error("email", "Invalid email address")

        if not conference:
            errors.add_error("conference", "Conference not found")

        return errors.if_has_errors


RequestInvitationLetterResult = Annotated[
    InvitationLetterRequest
    | RequestInvitationLetterErrors
    | NoAdmissionTicket
    | InvitationLetterAlreadyRequested
    | FormNotAvailable,
    strawberry.union(name="RequestInvitationLetterResult"),
]


@strawberry.mutation(
    permission_classes=[IsAuthenticated],
    extensions=[RateLimit("5/m")],
)
def request_invitation_letter(
    info: strawberry.Info[Context], input: RequestInvitationLetterInput
) -> RequestInvitationLetterResult:
    conference = ConferenceModel.objects.filter(code=input.conference).first()

    if errors := input.validate(conference):
        return errors

    if not conference.is_deadline_active(Deadline.TYPES.invitation_letter_request):
        return FormNotAvailable()

    user = info.context.request.user

    if input.on_behalf_of == InvitationLetterOnBehalfOf.SELF:
        input.email = ""

        if not user_has_admission_ticket(
            email=info.context.request.user.email,
            event_organizer=conference.pretix_organizer_id,
            event_slug=conference.pretix_event_id,
        ):
            return NoAdmissionTicket()

        if (
            InvitationLetterRequestModel.objects.for_conference(conference)
            .of_user(user)
            .filter(
                on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
            )
            .exists()
        ):
            return InvitationLetterAlreadyRequested()

    with transaction.atomic():
        invitation_letter, created = InvitationLetterRequestModel.objects.get_or_create(
            conference=conference,
            requester=user,
            on_behalf_of=InvitationLetterRequestOnBehalfOf(input.on_behalf_of.name),
            full_name=input.full_name,
            email_address=input.email,
            nationality=input.nationality,
            address=input.address,
            date_of_birth=input.date_of_birth,
            passport_number=input.passport_number,
            embassy_name=input.embassy_name,
        )

        if created:
            record_privacy_policy_acceptance(
                info.context.request,
                conference,
                "invitation_letter",
            )

    return InvitationLetterRequest.from_model(invitation_letter)
