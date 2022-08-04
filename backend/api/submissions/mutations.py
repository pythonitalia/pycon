import math
from typing import Optional

import strawberry
from strawberry import ID
from strawberry.types import Info

from api.permissions import IsAuthenticated
from conferences.models.conference import Conference
from domain_events.publisher import notify_new_submission
from i18n.strings import LazyI18nString
from languages.models import Language
from strawberry_forms.mutations import FormMutation
from submissions.models import Submission as SubmissionModel

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

    def to_dict(self) -> dict:
        return {"en": self.en, "it": self.it}


class BaseErrorType:
    _has_errors: strawberry.Private[bool] = False

    def add_error(self, field: str, message: str):
        self._has_errors = True

        existing_errors = getattr(self, field, [])
        existing_errors.append(message)
        setattr(self, field, existing_errors)

    @property
    def has_errors(self) -> bool:
        return self._has_errors

    @classmethod
    def with_error(cls, field: str, message: str):
        instance = cls()
        setattr(instance, field, [message])
        return instance


@strawberry.type
class SendSubmissionErrors(BaseErrorType):
    instance: list[str] = strawberry.field(default_factory=list)
    title: list[str] = strawberry.field(default_factory=list)
    abstract: list[str] = strawberry.field(default_factory=list)
    topic: list[str] = strawberry.field(default_factory=list)
    languages: list[str] = strawberry.field(default_factory=list)
    conference: list[str] = strawberry.field(default_factory=list)
    type: list[str] = strawberry.field(default_factory=list)
    duration: list[str] = strawberry.field(default_factory=list)
    elevator_pitch: list[str] = strawberry.field(default_factory=list)
    notes: list[str] = strawberry.field(default_factory=list)
    audience_level: list[str] = strawberry.field(default_factory=list)
    tags: list[str] = strawberry.field(default_factory=list)
    speaker_level: list[str] = strawberry.field(default_factory=list)
    previous_talk_video: list[str] = strawberry.field(default_factory=list)
    non_field_errors: list[str] = strawberry.field(default_factory=list)


class BaseSubmissionInput:
    def validate(self, conference: Optional[Conference], languages: list[str]):
        errors = SendSubmissionErrors()

        if not conference:
            errors.add_error("conference", "Invalid conference")
            return errors

        if not self.tags:
            errors.add_error("tags", "You need to add at least one tag")

        if not self.speaker_level:
            errors.add_error(
                "speaker_level", "You need to specify what is your speaker experience"
            )

        if not languages:
            errors.add_error("languages", "You need to add at least one language")

        fields = (
            "title",
            "abstract",
            "elevator_pitch",
        )
        max_lengths = {"title": 100, "elevator_pitch": 300, "abstract": 5000}
        to_text = {"it": "Italian", "en": "English"}

        for language in ("it", "en"):
            for field in fields:
                value = getattr(getattr(self, field), language)
                max_length = max_lengths.get(field, math.inf)

                if language not in languages:
                    continue

                if not value:
                    errors.add_error(field, f"{to_text[language]}: Cannot be empty")
                    continue

                if len(value) > max_length:
                    errors.add_error(
                        field,
                        f"{to_text[language]}: Cannot be more than {max_length} chars",
                    )

        return errors


@strawberry.input
class SendSubmissionInput(BaseSubmissionInput):
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
    speaker_level: str
    previous_talk_video: str
    tags: list[ID] = strawberry.field(default_factory=list)


@strawberry.input
class UpdateSubmissionInput(BaseSubmissionInput):
    instance: ID
    title: MultiLingualInput
    abstract: MultiLingualInput
    topic: ID
    languages: list[ID]
    type: ID
    duration: ID
    elevator_pitch: MultiLingualInput
    notes: str
    audience_level: ID
    speaker_level: str
    previous_talk_video: str
    tags: list[ID] = strawberry.field(default_factory=list)


SendSubmissionOutput = strawberry.union(
    "SendSubmissionOutput",
    (
        Submission,
        SendSubmissionErrors,
    ),
)

UpdateSubmissionOutput = strawberry.union(
    "UpdateSubmissionOutput",
    (
        Submission,
        SendSubmissionErrors,
    ),
)


@strawberry.type
class SubmissionsMutations:
    send_submission_comment = SendSubmissionComment.Mutation

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_submission(
        self, info: Info, input: UpdateSubmissionInput
    ) -> UpdateSubmissionOutput:
        instance = SubmissionModel.objects.get_by_hashid(input.instance)
        if not instance.can_edit(info.context.request):
            return SendSubmissionErrors.with_error(
                "instance", "You cannot edit this submission"
            )

        conference = instance.conference
        languages = Language.objects.filter(code__in=input.languages).all()

        errors = input.validate(
            conference=conference, languages=languages.values_list("code", flat=True)
        )

        if errors.has_errors:
            return errors

        instance.title = LazyI18nString(input.title.to_dict())
        instance.abstract = LazyI18nString(input.abstract.to_dict())
        instance.topic_id = input.topic
        instance.type_id = input.type
        instance.duration_id = input.duration
        instance.elevator_pitch = LazyI18nString(input.elevator_pitch.to_dict())
        instance.notes = input.notes
        instance.audience_level_id = input.audience_level
        instance.speaker_level = input.speaker_level
        instance.previous_talk_video = input.previous_talk_video
        instance.save()

        instance._type_definition = Submission._type_definition
        return instance

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_submission(
        self, info: Info, input: SendSubmissionInput
    ) -> SendSubmissionOutput:
        request = info.context.request

        conference = Conference.objects.filter(code=input.conference).first()
        languages = Language.objects.filter(code__in=input.languages).all()

        errors = input.validate(
            conference=conference, languages=languages.values_list("code", flat=True)
        )

        if errors.has_errors:
            return errors

        instance = SubmissionModel.objects.create(
            speaker_id=request.user.id,
            conference=conference,
            title=LazyI18nString(input.title.to_dict()),
            abstract=LazyI18nString(input.abstract.to_dict()),
            topic_id=input.topic,
            type_id=input.type,
            duration_id=input.duration,
            elevator_pitch=LazyI18nString(input.elevator_pitch.to_dict()),
            notes=input.notes,
            audience_level_id=input.audience_level,
            speaker_level=input.speaker_level,
            previous_talk_video=input.previous_talk_video,
        )
        instance.languages.set(languages)
        instance.tags.set(input.tags)

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

        # hack because we return django models
        instance._type_definition = Submission._type_definition
        return instance
