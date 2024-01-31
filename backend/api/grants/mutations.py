from dataclasses import asdict
from enum import Enum
from typing import Annotated, Union, Optional

import strawberry
from strawberry.types import Info

from api.grants.types import (
    AgeGroup,
    Grant,
    GrantType,
    InterestedInVolunteering,
    Occupation,
)
from api.permissions import IsAuthenticated
from api.types import BaseErrorType
from conferences.models.conference import Conference
from grants.tasks import send_new_plain_chat, notify_new_grant_reply_slack
from grants.models import Grant as GrantModel
from users.models import User


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
        interested_in_volunteering: list[str] = strawberry.field(default_factory=list)
        needs_funds_for_travel: list[str] = strawberry.field(default_factory=list)
        need_visa: list[str] = strawberry.field(default_factory=list)
        need_accommodation: list[str] = strawberry.field(default_factory=list)
        why: list[str] = strawberry.field(default_factory=list)
        notes: list[str] = strawberry.field(default_factory=list)
        travelling_from: list[str] = strawberry.field(default_factory=list)
        non_field_errors: list[str] = strawberry.field(default_factory=list)
        website: list[str] = strawberry.field(default_factory=list)
        twitter_handle: list[str] = strawberry.field(default_factory=list)
        github_handle: list[str] = strawberry.field(default_factory=list)
        linkedin_url: list[str] = strawberry.field(default_factory=list)
        mastodon_handle: list[str] = strawberry.field(default_factory=list)

    errors: _GrantErrors = None


class BaseGrantInput:
    def validate(self, conference: Conference, user: User) -> GrantErrors:
        errors = GrantErrors()

        if not conference:
            errors.add_error("conference", "Invalid conference")

        if conference and not conference.is_grants_open:
            errors.add_error("non_field_errors", "The grants form is not open!")

        max_length_fields = {
            "name": 300,
            "full_name": 300,
            "travelling_from": 200,
            "twitter_handle": 15,
            "github_handle": 39,
        }
        for field, max_length in max_length_fields.items():
            value = getattr(self, field, "")

            if len(value) > max_length:
                print(field)
                errors.add_error(
                    field,
                    f"{field}: Cannot be more than {max_length} chars",
                )

        non_empty_fields = (
            "full_name",
            "python_usage",
            "been_to_other_events",
            "why",
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
    grant_type: GrantType
    python_usage: str
    been_to_other_events: str
    community_contribution: str
    interested_in_volunteering: InterestedInVolunteering
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    why: str
    notes: str
    travelling_from: str
    website: str
    twitter_handle: str
    github_handle: str
    linkedin_url: str
    mastodon_handle: str

    def validate(self, conference: Conference, user: User) -> GrantErrors:
        errors = super().validate(conference=conference, user=user)

        if GrantModel.objects.filter(user_id=user.id).exists():
            errors.add_error("non_field_errors", "Grant already submitted!")

        return errors


@strawberry.input
class UpdateGrantInput(BaseGrantInput):
    instance: strawberry.ID
    name: str
    full_name: str
    conference: strawberry.ID
    age_group: AgeGroup
    gender: str
    occupation: Occupation
    grant_type: GrantType
    python_usage: str
    been_to_other_events: str
    community_contribution: str
    interested_in_volunteering: InterestedInVolunteering
    needs_funds_for_travel: bool
    need_visa: bool
    need_accommodation: bool
    why: str
    notes: str
    travelling_from: str
    website: str
    twitter_handle: str
    github_handle: str
    linkedin_url: str
    mastodon_handle: str


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
    need_info = "need_info"

    def to_grant_status(self) -> GrantModel.Status:
        return GrantModel.Status(self.name)


@strawberry.input
class SendGrantReplyInput:
    instance: strawberry.ID
    status: Optional[StatusOption]
    message: str


@strawberry.type
class SendGrantReplyError:
    message: str


SendGrantReplyResult = Annotated[
    Union[Grant, SendGrantReplyError], strawberry.union(name="SendGrantReplyResult")
]


@strawberry.type
class GrantMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_grant(self, info: Info, input: SendGrantInput) -> SendGrantResult:
        request = info.context.request

        conference = Conference.objects.filter(code=input.conference).first()

        errors = input.validate(conference=conference, user=request.user)
        if errors.has_errors:
            return errors

        instance = GrantModel.objects.create(
            **{
                **asdict(input),
                "user_id": request.user.id,
                "conference": conference,
            }
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
        errors = input.validate(conference=input.conference, user=request.user)
        if errors.has_errors:
            return errors

        for attr, value in asdict(input).items():
            setattr(instance, attr, value)
        instance.save()

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

        # do not update to need_info, otherwise we will lose the original status:
        # Approved, WaitingList
        if input.status != StatusOption.need_info:
            grant.status = input.status.to_grant_status()

        grant.applicant_message = input.message
        grant.save()

        admin_url = request.build_absolute_uri(grant.get_admin_url())
        notify_new_grant_reply_slack.delay(grant_id=grant.id, admin_url=admin_url)

        if grant.applicant_message:
            send_new_plain_chat.delay(grant_id=grant.id, message=input.message)

        return Grant.from_model(grant)
