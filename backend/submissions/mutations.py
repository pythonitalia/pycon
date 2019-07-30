import strawberry

from strawberry_forms.mutations import FormMutation

from .forms import SendSubmissionForm
from .permissions import IsAuthenticated
from .types import Submission


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
            # helpers=result.#,
            topic=result.topic,
            type=result.type,
            duration=result.duration,
            audience_level=result.audience_level,
        )

    class Meta:
        form_class = SendSubmissionForm
        output_types = (Submission,)
        permission_classes = (IsAuthenticated,)


@strawberry.type
class SubmissionsMutations:
    send_submission = SendSubmission.Mutation
