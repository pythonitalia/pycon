from api.context import Info
from sponsors.tasks import notify_new_sponsor_lead_via_slack, send_sponsor_brochure
from conferences.models.conference import Conference
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from typing import Annotated, Union
from api.types import BaseErrorType, OperationResult
from sponsors.models import SponsorLead
import strawberry


@strawberry.type
class SendSponsorLeadInputErrors(BaseErrorType):
    @strawberry.type
    class _SendSponsorLeadInput:
        fullname: list[str] = strawberry.field(default_factory=list)
        email: list[str] = strawberry.field(default_factory=list)
        company: list[str] = strawberry.field(default_factory=list)
        conference_code: list[str] = strawberry.field(default_factory=list)
        non_field_errors: list[str] = strawberry.field(default_factory=list)

    errors: _SendSponsorLeadInput = None


@strawberry.input
class SendSponsorLeadInput:
    fullname: str
    email: str
    company: str
    conference_code: str
    consent_to_contact_via_email: bool = False

    def validate(self):
        errors = SendSponsorLeadInputErrors()

        if not self.fullname:
            errors.add_error("fullname", "Required")

        if not self.email:
            errors.add_error("email", "Required")
        else:
            try:
                validate_email(self.email)
            except ValidationError:
                errors.add_error("email", "Invalid email address")

        if not self.company:
            errors.add_error("company", "Required")

        if not self.conference_code:
            errors.add_error("conference_code", "Required")
        else:
            if not Conference.objects.filter(code=self.conference_code).exists():
                errors.add_error("conference_code", "Invalid conference code")

        return errors.if_has_errors


SendSponsorLeadOutput = Annotated[
    Union[OperationResult, SendSponsorLeadInputErrors],
    strawberry.union(name="SendSponsorLeadOutput"),
]


@strawberry.type
class SponsorsMutation:
    @strawberry.field
    def send_sponsor_lead(
        self, info: Info, input: SendSponsorLeadInput
    ) -> SendSponsorLeadOutput:
        if errors := input.validate():
            return errors

        is_new_email = not SponsorLead.objects.filter(email=input.email).exists()
        conference_id = (
            Conference.objects.filter(code=input.conference_code)
            .values_list("id", flat=True)
            .first()
        )

        sponsor_lead, created = SponsorLead.objects.update_or_create(
            fullname=input.fullname,
            email=input.email,
            company=input.company,
            conference_id=conference_id,
            defaults={
                "consent_to_contact_via_email": input.consent_to_contact_via_email,
            },
        )

        if is_new_email and created:
            send_sponsor_brochure.delay(sponsor_lead_id=sponsor_lead.id)
            notify_new_sponsor_lead_via_slack.delay(
                sponsor_lead_id=sponsor_lead.id,
                admin_absolute_uri=info.context.request.build_absolute_uri("/"),
            )

        return OperationResult(ok=True)
