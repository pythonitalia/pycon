import strawberry
from api.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from .forms import SendSubmissionCommentForm, SendSubmissionForm, UpdateSubmissionForm
from .permissions import CanSendComment
from .types import Submission, SubmissionComment, SubmissionCommentAuthor


class SubmissionMutation:
    @classmethod
    def transform(cls, result):
        # lie to strawberry to make it think that the return value is a proper type
        result._type_definition = Submission._type_definition
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
            id=result.id,
            text=result.text,
            submission=result.submission,
            author=SubmissionCommentAuthor(
                name="Speaker"
                if result.author == result.submission.speaker
                else result.author.name
            ),
            created=result.created,
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
