import strawberry
from strawberry import ID
from strawberry.types import Info

from api.permissions import IsAuthenticated
from conferences.models.conference import Conference
from domain_events.publisher import notify_new_submission
from languages.models import Language
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
                id=result.author_id,
                is_speaker=result.author_id == result.submission.speaker_id,
            ),
            created=result.created,
        )

    class Meta(SubmissionMutation.Meta):
        form_class = SendSubmissionCommentForm
        output_types = (SubmissionComment,)
        permission_classes = (IsAuthenticated, CanSendComment)


@strawberry.input
class MultiLingualInput:
    en: str
    it: str


@strawberry.input
class SendSubmissionInput:
    conference: ID
    title: MultiLingualInput
    abstract: MultiLingualInput
    topic: ID
    languages: list[ID]
    type: ID
    duration: ID
    elevator_pitch: MultiLingualInput
    notes: str
    audience_level: ID
    tags: list[ID]
    speaker_level: str
    previous_talk_video: str


@strawberry.type
class SendSubmissionErrors:
    title: list[str]
    abstract: list[str]
    topic: list[str]
    languages: list[str]
    conference: list[str]
    type: list[str]
    duration: list[str]
    elevatorPitch: list[str]
    notes: list[str]
    audienceLevel: list[str]
    tags: list[str]
    speakerLevel: list[str]
    previousTalkVideo: list[str]
    nonFieldErrors: list[str]


SendSubmissionOutput = strawberry.union(
    "SendSubmissionOutput",
    (
        Submission,
        SendSubmissionErrors,
    ),
)


@strawberry.type
class SubmissionsMutations:
    update_submission = UpdateSubmission.Mutation
    send_submission_comment = SendSubmissionComment.Mutation

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_submission(
        self, info: Info, input: SendSubmissionInput
    ) -> SendSubmissionOutput:
        request = info.context.request

        conference = Conference.objects.filter(code=input.conference).first()
        languages = Language.objects.filter(code__in=input.languages).values_list(
            "id", flat=True
        )

        instance = Submission.objects.create(
            speaker_id=request.user.id,
            conference=conference,
            title=input.title,
            abstract=input.abstract,
            topic=input.topic,
            languages=languages,
            type=input.type,
            duration=input.duration,
            elevator_pitch=input.elevator_pitch,
            notes=input.notes,
            audience_level=input.audience_level,
            tags=input.tags,
            speaker_level=input.speaker_level,
            previous_talk_video=input.previous_talk_video,
        )

        notify_new_submission(
            submission_id=instance.id,
            title=instance.title,
            elevator_pitch=instance.elevator_pitch,
            submission_type=instance.type.name,
            admin_url=request.build_absolute_uri(instance.get_admin_url()),
            duration=instance.duration.duration,
            topic=instance.topic.name,
            speaker_id=instance.speaker_id,
            conference_id=instance.conference_id,
        )

        return instance
