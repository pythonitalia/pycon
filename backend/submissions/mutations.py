import graphene

from api.mutations import AuthOnlyDjangoFormMutation

from .forms import SendSubmissionForm
from .types import SubmissionType, SubmissionTypeType


class SendSubmission(AuthOnlyDjangoFormMutation):
    class Meta:
        form_class = SendSubmissionForm


class SubmissionsMutations(graphene.ObjectType):
    send_submission = SendSubmission.Field()
