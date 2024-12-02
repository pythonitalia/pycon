from dataclasses import asdict
from enum import Enum
from typing import Annotated, Union, Optional
from participants.models import Participant

from privacy_policy.record import record_privacy_policy_acceptance
import strawberry
from strawberry.types import Info
from django.db import transaction
from api.grants.types import (
    AgeGroup,
    Grant,
    GrantType,
    Occupation,
)
from api.permissions import IsAuthenticated
from api.types import BaseErrorType
from conferences.models.conference import Conference
from grants.tasks import (
    notify_new_grant_reply_slack,
)
from grants.models import Grant as GrantModel
from users.models import User
from grants.tasks import get_name
from notifications.models import EmailTemplate, EmailTemplateIdentifier


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

    errors: _GrantErrors = None


class BaseGrantInput:
    def validate(self, conference: Conference, user: User) -> GrantErrors:
        errors = GrantErrors()

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
        for field, max_length in max_length_fields.items():
            value = getattr(self, field, "")

            if value and len(value) > max_length:
                errors.add_error(
                    field,
                    f"{field}: Cannot be more than {max_length} chars",
                )

        non_empty_fields = (
            "full_name",
            "python_usage",
            "been_to_other_events",
            "why",
            "grant_type",
        )

        for field in non_empty_fields:
            value = getattr(self, field, "")

            if not value:
                errors.add_error(field, f"{field}: Cannot be empty")
                continue

        return errors


@strawberry.input
class SendGrantInput(BaseGrantInput):
    name: str
    full_name: str
    conference: strawberry.ID
    age_group: AgeGroup
    gender: str
    occupation: Occupation
    grant_type: list[GrantType]
    python_usage: str
    been_to_other_events: str
    community_contribution: str
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    why: str
    notes: str
    departure_country: str | None = None
    nationality: str
    departure_city: str | None = None

    participant_bio: str
    participant_website: str
    participant_twitter_handle: str
    participant_instagram_handle: str
    participant_linkedin_url: str
    participant_facebook_url: str
    participant_mastodon_handle: str

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
    age_group: AgeGroup
    gender: str
    occupation: Occupation
    grant_type: list[GrantType]
    python_usage: str
    been_to_other_events: str
    community_contribution: str
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    why: str
    notes: str
    departure_country: str | None = None
    nationality: str
    departure_city: str | None = None

    participant_bio: str
    participant_website: str
    participant_twitter_handle: str
    participant_instagram_handle: str
    participant_linkedin_url: str
    participant_facebook_url: str
    participant_mastodon_handle: str

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
                "age_group": input.age_group,
                "gender": input.gender,
                "occupation": input.occupation,
                "grant_type": input.grant_type,
                "python_usage": input.python_usage,
                "been_to_other_events": input.been_to_other_events,
                "community_contribution": input.community_contribution,
                "needs_funds_for_travel": input.needs_funds_for_travel,
                "need_visa": input.need_visa,
                "need_accommodation": input.need_accommodation,
                "why": input.why,
                "notes": input.notes,
                "departure_country": input.departure_country,
                "nationality": input.nationality,
                "departure_city": input.departure_city,
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

        # hack because we return django models
        instance.__strawberry_definition__ = Grant.__strawberry_definition__
        return instance

    @strawberry.mutation(permission_classes=[IsAuthenticated])
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

        for attr, value in asdict(input).items():
            setattr(instance, attr, value)
        instance.save()

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

        grant.status = input.status.to_grant_status()
        grant.save()

        admin_url = request.build_absolute_uri(grant.get_admin_url())
        notify_new_grant_reply_slack.delay(grant_id=grant.id, admin_url=admin_url)

        return Grant.from_model(grant)
