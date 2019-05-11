import graphene

from api.mutations import AuthOnlyDjangoModelFormMutation

from .types import SubmissionType, SubmissionTypeType

from .forms import SendSubmissionForm


class SendSubmission(AuthOnlyDjangoModelFormMutation):
    class Meta:
        form_class = SendSubmissionForm


class SubmissionsMutations(graphene.ObjectType):
    send_submission = SendSubmission.Field()
