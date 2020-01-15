import strawberry
from api.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from .forms import SendVoteForm
from .types import VoteType


class SendVote(FormMutation):
    @classmethod
    def transform(cls, result):
        return VoteType(
            id=result.id,
            value=result.value,
            user=result.user,
            submission=result.submission,
        )

    class Meta:
        form_class = SendVoteForm
        permission_classes = (IsAuthenticated,)
        output_types = (VoteType,)


@strawberry.type
class VotesMutations:
    send_vote = SendVote.Mutation
