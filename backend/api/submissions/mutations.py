import strawberry

from strawberry_forms.mutations import FormMutation

from .forms import SendSubmissionForm, SendTagForm
from .permissions import IsAuthenticated
from .types import Submission, SubmissionTag


class SendSubmission(FormMutation):
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
        form_class = SendSubmissionForm
        output_types = (Submission,)
        permission_classes = (IsAuthenticated,)


class SendTag(FormMutation):
    @classmethod
    def transform(cls, result):
        return SubmissionTag(id=result.id, name=result.name)

    class Meta:
        form_class = SendTagForm
        output_types = (SubmissionTag,)
        permission_classes = (IsAuthenticated,)


@strawberry.type
class SubmissionsMutations:
    send_submission = SendSubmission.Mutation
    send_tag = SendTag.Mutation
