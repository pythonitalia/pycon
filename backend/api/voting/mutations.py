from strawberry.tools import create_type
from voting.helpers import check_if_user_can_vote
from typing import Annotated, Union
from api.context import Info
from api.types import BaseErrorType
import strawberry

from api.permissions import IsAuthenticated
from submissions.models import Submission
from voting.models.vote import Vote

from .types import VoteType


@strawberry.type
class SendVoteErrors(BaseErrorType):
    @strawberry.type
    class _SendVoteErrorsErrors:
        value: list[str] = strawberry.field(default_factory=list)
        submission: list[str] = strawberry.field(default_factory=list)
        non_field_errors: list[str] = strawberry.field(default_factory=list)

    errors: _SendVoteErrorsErrors = None


@strawberry.input
class SendVoteInput:
    value: int
    submission: strawberry.ID

    def validate(self, info: Info, submission: Submission | None) -> SendVoteErrors:
        errors = SendVoteErrors()

        if not submission:
            return SendVoteErrors.with_error("submission", "Invalid submission")

        if self.value not in Vote.Values.values:
            errors.add_error("value", f"Value {self.value} is not a valid choice.")

        if submission.conference_id and not submission.conference.is_voting_open:
            errors.add_error("non_field_errors", "The voting session is not open!")

        user = info.context.request.user

        if not check_if_user_can_vote(user, submission.conference):
            errors.add_error("non_field_errors", "You cannot vote without a ticket")

        return errors.if_has_errors


SendVoteOutput = Annotated[
    Union[VoteType, SendVoteErrors],
    strawberry.union(name="SendVoteOutput"),
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def send_vote(info: Info, input: SendVoteInput) -> SendVoteOutput:
    try:
        submission = Submission.objects.get_by_hashid(input.submission)
    except Submission.DoesNotExist:
        submission = None

    if errors := input.validate(info, submission):
        return errors

    result, _ = Vote.objects.update_or_create(
        user_id=info.context.request.user.id,
        submission=submission,
        defaults={"value": input.value},
    )

    return VoteType(
        id=result.id,
        value=result.value,
        submission=result.submission,
    )


VotesMutations = create_type("VotesMutations", [send_vote])
