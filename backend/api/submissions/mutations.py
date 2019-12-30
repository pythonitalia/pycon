import strawberry
from api.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from .permissions import CanSendComment
from .forms import SendSubmissionForm, UpdateSubmissionForm, SendSubmissionCommentForm
from .types import Submission, SubmissionComment


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


class SendSubmissionComment(FormMutation):
    @classmethod
    def transform(cls, result):
        return SubmissionComment(
            id=result.id, text=result.text, author=result.author, created=result.created
        )

    class Meta(SubmissionMutation.Meta):
        form_class = SendSubmissionCommentForm
        output_types = (SubmissionComment,)
        permission_classes = (IsAuthenticated, CanSendComment)


@strawberry.type
class SubmissionsMutations:
    send_submission = SendSubmission.Mutation
    update_submission = UpdateSubmission.Mutation
    send_submission_comment = SendSubmissionComment.Mutation
