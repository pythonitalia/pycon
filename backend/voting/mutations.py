import graphene
from api.mutations import AuthOnlyDjangoModelFormMutation

from .forms import SendVoteForm


class SendVote(AuthOnlyDjangoModelFormMutation):
    class Meta:
        form_class = SendVoteForm


class VotesMutations(graphene.ObjectType):
    send_vote = SendVote.Field()
