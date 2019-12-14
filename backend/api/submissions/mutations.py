import strawberry
from api.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from .forms import SendSubmissionForm, UpdateSubmissionForm
from .types import Submission


class SubmissionMutation:
    @classmethod
    def transform(cls, result):
        return Submission(
            id=result.id,
            conference=result.conference,
            title=result.title,
            elevator_pitch=result.elevator_pitch,
            notes=result.notes,
            abstract=result.abstract,
            speaker=result.speaker,
            slug=result.slug,
            topic=result.topic,
            languages=result.languages,
            type=result.type,
            duration=result.duration,
            audience_level=result.audience_level,
            tags=result.tags,
        )

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
