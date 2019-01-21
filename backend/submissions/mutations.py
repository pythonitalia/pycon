import graphene

from api.mutations import AuthOnlyDjangoFormMutation

from .types import SubmissionType, SubmissionTypeType

from .forms import SendSubmissionForm


class SendSubmission(AuthOnlyDjangoFormMutation):
    class Meta:
        form_class = SendSubmissionForm


class SubmissionsMutations(graphene.ObjectType):
    send_submission = SendSubmission.Field()
