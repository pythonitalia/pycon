import graphene
from api.mutations import AuthOnlyDjangoFormMutation

from .forms import SendVoteForm


class SendVote(AuthOnlyDjangoFormMutation):
    class Meta:
        form_class = SendVoteForm


class VotesMutations(graphene.ObjectType):
    send_vote = SendVote.Field()
