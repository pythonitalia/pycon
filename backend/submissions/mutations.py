import strawberry
from strawberry_forms.mutations import FormMutation

from .forms import SendSubmissionForm
from .permissions import IsAuthenticated
from .types import SubmissionType


class SendSubmission(FormMutation):
    @classmethod
    def transform(cls, result):
        return SubmissionType(
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
        )

    class Meta:
        form_class = SendSubmissionForm
        output_types = (SubmissionType,)
        permission_classes = (IsAuthenticated,)


@strawberry.type
class SubmissionsMutations:
    send_submission = SendSubmission.Mutation
