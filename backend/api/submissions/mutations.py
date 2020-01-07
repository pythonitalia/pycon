import strawberry
from api.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from .forms import SendSubmissionForm, UpdateSubmissionForm
from .types import Submission


class SubmissionMutation:
    @classmethod
    def transform(cls, result):
        # lie to strawberry to make it think that the return value is a proper type
        result.field = Submission.field
        return result

    class Meta:
        output_types = (Submission,)
        permission_classes = (IsAuthenticated,)


class SendSubmission(FormMutation, SubmissionMutation):
    class Meta(SubmissionMutation.Meta):
        form_class = SendSubmissionForm


class UpdateSubmission(FormMutation, SubmissionMutation):
    class Meta(SubmissionMutation.Meta):
        form_class = UpdateSubmissionForm


@strawberry.type
class SubmissionsMutations:
    send_submission = SendSubmission.Mutation
    update_submission = UpdateSubmission.Mutation
