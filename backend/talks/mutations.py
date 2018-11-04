import graphene

from graphene_django.forms import mutation

from .forms import ProposeTalkForm


class ProposeTalk(mutation.DjangoModelFormMutation):
    class Meta:
        form_class = ProposeTalkForm


class TalksMutations(graphene.ObjectType):
    propose_talk = ProposeTalk.Field()
