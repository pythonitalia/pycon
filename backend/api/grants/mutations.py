from dataclasses import asdict
from enum import Enum
from typing import Annotated, Optional, Union

import strawberry
from django.db import transaction
from strawberry.scalars import JSON
from strawberry.types import Info

from api.grants.types import AgeGroup, Grant, GrantType, Occupation
from api.permissions import IsAuthenticated
from api.types import BaseErrorType
from conferences.models.conference import Conference
from custom_admin.audit import (
    create_addition_admin_log_entry,
    create_change_admin_log_entry,
)
from generic_forms.models import Form, FormAnswer
from generic_forms.services import validate_answers, wrap_answers
from grants.models import Grant as GrantModel
from grants.tasks import (
    create_and_send_voucher_to_grantee,
    get_name,
    notify_new_grant_reply_slack,
)
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from participants.models import Participant
from privacy_policy.record import record_privacy_policy_acceptance
from users.models import User

# Soft questions live in the generic form once a conference configures one;
# these legacy input fields are then omitted by the frontend and the answers
# path never writes them. gender and occupation are NOT here: the grants
# summary aggregates their columns, so they stay structured inputs.
DYNAMIC_QUESTION_FIELDS = frozenset(
    {
        "age_group",
        "python_usage",
        "been_to_other_events",
        "community_contribution",
        "why",
        "notes",
    }
)

# Optional string inputs whose Grant columns are NOT NULL; omitted values
# are stored as empty strings, never None.
OMITTABLE_STRING_FIELDS = DYNAMIC_QUESTION_FIELDS | {"gender", "occupation"}


@strawberry.type
class GrantErrors(BaseErrorType):
    @strawberry.type
    class _GrantErrors:
        instance: list[str] = strawberry.field(default_factory=list)
        name: list[str] = strawberry.field(default_factory=list)
        full_name: list[str] = strawberry.field(default_factory=list)
        conference: list[str] = strawberry.field(default_factory=list)
        age_group: list[str] = strawberry.field(default_factory=list)
        gender: list[str] = strawberry.field(default_factory=list)
        occupation: list[str] = strawberry.field(default_factory=list)
        grant_type: list[str] = strawberry.field(default_factory=list)
        python_usage: list[str] = strawberry.field(default_factory=list)
        community_contribution: list[str] = strawberry.field(default_factory=list)
        been_to_other_events: list[str] = strawberry.field(default_factory=list)
        needs_funds_for_travel: list[str] = strawberry.field(default_factory=list)
        need_visa: list[str] = strawberry.field(default_factory=list)
        need_accommodation: list[str] = strawberry.field(default_factory=list)
        why: list[str] = strawberry.field(default_factory=list)
        notes: list[str] = strawberry.field(default_factory=list)
        departure_country: list[str] = strawberry.field(default_factory=list)
        nationality: list[str] = strawberry.field(default_factory=list)
        departure_city: list[str] = strawberry.field(default_factory=list)
        non_field_errors: list[str] = strawberry.field(default_factory=list)
        participant_bio: list[str] = strawberry.field(default_factory=list)
        participant_website: list[str] = strawberry.field(default_factory=list)
        participant_twitter_handle: list[str] = strawberry.field(default_factory=list)
        participant_instagram_handle: list[str] = strawberry.field(default_factory=list)
        participant_linkedin_url: list[str] = strawberry.field(default_factory=list)
        participant_facebook_url: list[str] = strawberry.field(default_factory=list)
        participant_mastodon_handle: list[str] = strawberry.field(default_factory=list)
        # {question_id: [messages]} for dynamic form answers; a JSON map
        # because question ids cannot be static fields on this class
        answers_errors: JSON = strawberry.field(default_factory=dict)

    errors: _GrantErrors = None

    def set_answers_errors(self, answer_errors: dict):
        # add_error() appends to list fields, so the JSON map is set directly
        self._has_errors = True
        if not self.errors:
            self.errors = self.__annotations__["errors"]()
        self.errors.answers_errors = answer_errors


class BaseGrantInput:
    def validate(self, conference: Conference, user: User) -> GrantErrors:
        errors = GrantErrors()
        uses_answers = self.answers is not None

        if not conference:
            errors.add_error("conference", "Invalid conference")

        if conference and not conference.is_grants_open:
            errors.add_error("non_field_errors", "The grants form is not open!")

        max_length_fields = {
            "full_name": 300,
            "name": 300,
            "departure_country": 100,
            "nationality": 100,
            "departure_city": 100,
        }
        if not uses_answers:
            # legacy soft fields; superseded by validate_answers on the
            # answers path
            max_length_fields |= {
                "why": 1000,
                "python_usage": 700,
                "been_to_other_events": 500,
                "community_contribution": 900,
                "notes": 350,
            }
        for field, max_length in max_length_fields.items():
            value = getattr(self, field, "")

            if value and len(value) > max_length:
                errors.add_error(
                    field,
                    f"{field}: Cannot be more than {max_length} chars",
                )

        non_empty_fields = ["full_name", "grant_type"]
        if not uses_answers:
            non_empty_fields.extend(["python_usage", "been_to_other_events", "why"])
        if self.needs_funds_for_travel:
            non_empty_fields.extend(
                ["departure_country", "departure_city", "nationality"]
            )

        for field in non_empty_fields:
            value = getattr(self, field, "")

            if not value:
                errors.add_error(field, f"{field}: Cannot be empty")
                continue

        if uses_answers and conference:
            form = Form.objects.filter(
                conference=conference, purpose=Form.Purpose.GRANT
            ).first()
            if form is None:
                errors.add_error(
                    "non_field_errors",
                    "The grants form is not configured for this conference",
                )
            elif answer_errors := validate_answers(form, self.answers):
                errors.set_answers_errors(answer_errors)

        return errors


@strawberry.input
class SendGrantInput(BaseGrantInput):
    name: str
    full_name: str
    conference: strawberry.ID
    grant_type: list[GrantType]
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    nationality: str

    participant_bio: str
    participant_website: str
    participant_twitter_handle: str
    participant_instagram_handle: str
    participant_linkedin_url: str
    participant_facebook_url: str
    participant_mastodon_handle: str

    # soft questions: either these legacy fields (no generic form configured)
    # or the answers map — never both required
    age_group: AgeGroup | None = None
    gender: str | None = None
    occupation: Occupation | None = None
    python_usage: str | None = None
    been_to_other_events: str | None = None
    community_contribution: str | None = None
    why: str | None = None
    notes: str | None = None
    departure_country: str | None = None
    departure_city: str | None = None
    answers: JSON | None = None

    def validate(self, conference: Conference, user: User) -> GrantErrors | None:
        errors = super().validate(conference=conference, user=user)

        if GrantModel.objects.of_user(user).for_conference(conference).exists():
            errors.add_error("non_field_errors", "Grant already submitted!")

        return errors.if_has_errors


@strawberry.input
class UpdateGrantInput(BaseGrantInput):
    instance: strawberry.ID
    name: str
    full_name: str
    conference: strawberry.ID
    grant_type: list[GrantType]
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    nationality: str

    participant_bio: str
    participant_website: str
    participant_twitter_handle: str
    participant_instagram_handle: str
    participant_linkedin_url: str
    participant_facebook_url: str
    participant_mastodon_handle: str

    age_group: AgeGroup | None = None
    gender: str | None = None
    occupation: Occupation | None = None
    python_usage: str | None = None
    been_to_other_events: str | None = None
    community_contribution: str | None = None
    why: str | None = None
    notes: str | None = None
    departure_country: str | None = None
    departure_city: str | None = None
    answers: JSON | None = None

    def validate(self, conference: Conference, user: User) -> GrantErrors | None:
        return super().validate(conference=conference, user=user).if_has_errors


SendGrantResult = Annotated[
    Union[Grant, GrantErrors], strawberry.union(name="SendGrantResult")
]

UpdateGrantResult = Annotated[
    Union[Grant, GrantErrors], strawberry.union(name="UpdateGrantResult")
]


@strawberry.enum
class StatusOption(Enum):
    confirmed = "confirmed"
    refused = "refused"

    def to_grant_status(self) -> GrantModel.Status:
        return GrantModel.Status(self.name)


@strawberry.input
class SendGrantReplyInput:
    instance: strawberry.ID
    status: Optional[StatusOption]


@strawberry.type
class SendGrantReplyError:
    message: str


SendGrantReplyResult = Annotated[
    Union[Grant, SendGrantReplyError], strawberry.union(name="SendGrantReplyResult")
]


def _persist_form_answer(
    answers: dict | None, conference: Conference, user: User
) -> FormAnswer | None:
    if answers is None:
        return None

    # validate() already guaranteed the form exists
    form = Form.objects.get(conference=conference, purpose=Form.Purpose.GRANT)
    form_answer, _ = FormAnswer.objects.update_or_create(
        form=form,
        user_id=user.id,
        defaults={"answers": wrap_answers(answers)},
    )
    return form_answer


@strawberry.type
class GrantMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def send_grant(self, info: Info, input: SendGrantInput) -> SendGrantResult:
        request = info.context.request

        conference = Conference.objects.filter(code=input.conference).first()

        if errors := input.validate(conference=conference, user=request.user):
            return errors

        instance = GrantModel.objects.create(
            **{
                "user_id": request.user.id,
                "conference": conference,
                "name": input.name,
                "full_name": input.full_name,
                # soft columns are NOT NULL; on the answers path they are
                # omitted from the input and stored empty
                "age_group": input.age_group or "",
                "gender": input.gender or "",
                "occupation": input.occupation or "",
                "grant_type": input.grant_type,
                "python_usage": input.python_usage or "",
                "been_to_other_events": input.been_to_other_events or "",
                "community_contribution": input.community_contribution or "",
                "needs_funds_for_travel": input.needs_funds_for_travel,
                "need_visa": input.need_visa,
                "need_accommodation": input.need_accommodation,
                "why": input.why or "",
                "notes": input.notes or "",
                "departure_country": input.departure_country,
                "nationality": input.nationality,
                "departure_city": input.departure_city,
                "form_answer": _persist_form_answer(
                    input.answers, conference, request.user
                ),
            }
        )

        record_privacy_policy_acceptance(
            info.context.request,
            conference,
            "grant",
        )

        Participant.objects.update_or_create(
            user_id=request.user.id,
            conference=instance.conference,
            defaults={
                "bio": input.participant_bio,
                "website": input.participant_website,
                "twitter_handle": input.participant_twitter_handle,
                "instagram_handle": input.participant_instagram_handle,
                "linkedin_url": input.participant_linkedin_url,
                "facebook_url": input.participant_facebook_url,
                "mastodon_handle": input.participant_mastodon_handle,
            },
        )

        email_template = EmailTemplate.objects.for_conference(
            conference
        ).get_by_identifier(EmailTemplateIdentifier.grant_application_confirmation)

        email_template.send_email(
            recipient=request.user,
            placeholders={
                "user_name": get_name(request.user, "there"),
            },
        )

        create_addition_admin_log_entry(request.user, instance, "Grant created.")

        # hack because we return django models
        instance.__strawberry_definition__ = Grant.__strawberry_definition__
        return instance

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
    def update_grant(self, info: Info, input: UpdateGrantInput) -> UpdateGrantResult:
        request = info.context.request

        instance = GrantModel.objects.get(id=input.instance)
        if not instance.can_edit(request.user):
            return GrantErrors.with_error(
                "non_field_errors", "You cannot edit this grant"
            )

        input.conference = instance.conference
        if errors := input.validate(conference=input.conference, user=request.user):
            return errors

        uses_answers = input.answers is not None
        skip_fields = {"answers"} | (DYNAMIC_QUESTION_FIELDS if uses_answers else set())

        for attr, value in asdict(input).items():
            if attr in skip_fields:
                continue
            if attr in OMITTABLE_STRING_FIELDS and value is None:
                # these columns are NOT NULL
                value = ""
            setattr(instance, attr, value)

        if uses_answers:
            instance.form_answer = _persist_form_answer(
                input.answers, instance.conference, request.user
            )

        instance.save()

        create_change_admin_log_entry(request.user, instance, "Grant updated.")

        Participant.objects.update_or_create(
            user_id=request.user.id,
            conference=instance.conference,
            defaults={
                "bio": input.participant_bio,
                "website": input.participant_website,
                "twitter_handle": input.participant_twitter_handle,
                "instagram_handle": input.participant_instagram_handle,
                "linkedin_url": input.participant_linkedin_url,
                "facebook_url": input.participant_facebook_url,
                "mastodon_handle": input.participant_mastodon_handle,
            },
        )

        instance.__strawberry_definition__ = Grant.__strawberry_definition__
        return instance

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_grant_reply(
        self, info: Info, input: SendGrantReplyInput
    ) -> SendGrantReplyResult:
        request = info.context.request

        grant = GrantModel.objects.get(id=input.instance)
        if not grant.can_edit(request.user):
            return SendGrantReplyError(message="You cannot reply to this grant")

        # Can't modify the status if the grant is still pending or was already rejected
        if grant.status in (GrantModel.Status.pending, GrantModel.Status.rejected):
            return SendGrantReplyError(message="You cannot reply to this grant")

        old_status = grant.status
        grant.status = input.status.to_grant_status()
        grant.save()

        if old_status != grant.status and grant.status == GrantModel.Status.confirmed:
            transaction.on_commit(
                lambda gid=grant.id: create_and_send_voucher_to_grantee.delay(
                    grant_id=gid
                )
            )

        create_change_admin_log_entry(
            request.user, grant, f"Grantee has replied with status {grant.status}."
        )

        admin_url = request.build_absolute_uri(grant.get_admin_url())
        notify_new_grant_reply_slack.delay(grant_id=grant.id, admin_url=admin_url)

        return Grant.from_model(grant)
