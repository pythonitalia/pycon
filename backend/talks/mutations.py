import graphene

from graphql import GraphQLError

from api.mutations import ContextAwareDjangoModelFormMutation

from .types import TalkType  # noqa

from .forms import ProposeTalkForm


class ProposeTalk(ContextAwareDjangoModelFormMutation):
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('User not logged in')

        return super().mutate_and_get_payload(root, info, **input)

    class Meta:
        form_class = ProposeTalkForm


class TalksMutations(graphene.ObjectType):
    propose_talk = ProposeTalk.Field()
