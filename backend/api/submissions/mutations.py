import math

import strawberry
from strawberry import ID
from strawberry.types import Info

from api.permissions import IsAuthenticated
from api.types import BaseErrorType, MultiLingualInput
from conferences.models.conference import Conference
from domain_events.publisher import notify_new_submission
from i18n.strings import LazyI18nString
from languages.models import Language
from strawberry_forms.mutations import FormMutation
from submissions.models import Submission as SubmissionModel

from .forms import SendSubmissionCommentForm
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
    short_social_summary: list[str] = strawberry.field(default_factory=list)
    non_field_errors: list[str] = strawberry.field(default_factory=list)


class BaseSubmissionInput:
    def clean(self):
        self.title = self.title.clean(self.languages)
        self.elevator_pitch = self.elevator_pitch.clean(self.languages)
        self.abstract = self.abstract.clean(self.languages)

    def validate(self, conference: Conference):
        errors = SendSubmissionErrors()

        if not self.tags:
            errors.add_error("tags", "You need to add at least one tag")

        if not self.speaker_level:
            errors.add_error(
                "speaker_level", "You need to specify what is your speaker experience"
            )
        elif self.speaker_level not in SubmissionModel.SPEAKER_LEVELS:
            errors.add_error("speaker_level", "Select a valid choice")

        if not self.languages:
            errors.add_error("languages", "You need to add at least one language")

        fields = (
            "title",
            "abstract",
            "elevator_pitch",
        )

        max_lengths = {"title": 100, "elevator_pitch": 300, "abstract": 5000}
        to_text = {"it": "Italian", "en": "English"}

        allowed_languages = conference.languages.values_list("code", flat=True)

        for language in self.languages:
            if language not in allowed_languages:
                errors.add_error("languages", f"Language ({language}) is not allowed")
                continue

            for field in fields:
                value = getattr(getattr(self, field), language)
                max_length = max_lengths.get(field, math.inf)

                if not value:
                    errors.add_error(field, f"{to_text[language]}: Cannot be empty")
                    continue

                if len(value) > max_length:
                    errors.add_error(
                        field,
                        f"{to_text[language]}: Cannot be more than {max_length} chars",
                    )

        if len(self.notes) > 1000:
            errors.add_error(
                "notes",
                "Cannot be more than 1000 chars",
            )

        if len(self.short_social_summary) > 128:
            errors.add_error(
                "short_social_summary",
                "Cannot be more than 128 chars",
            )

        duration = conference.durations.filter(id=self.duration).first()

        if not conference.submission_types.filter(id=self.type).exists():
            errors.add_error("type", "Not allowed submission type")

        if not conference.topics.filter(id=self.topic).exists():
            errors.add_error("topic", "Not a valid topic")

        if not duration:
            errors.add_error(
                "duration",
                "Select a valid choice. That choice is not one of the available choices.",
            )
        elif not duration.allowed_submission_types.filter(id=self.type).exists():
            errors.add_error(
                "duration", "Duration is not an allowed for the submission type"
            )

        if not conference.audience_levels.filter(id=self.audience_level).exists():
            errors.add_error("audience_level", "Not a valid audience level")

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
    short_social_summary: str
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
    short_social_summary: str
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
                "non_field_errors", "You cannot edit this submission"
            )

        errors = input.validate(conference=instance.conference)

        if errors.has_errors:
            return errors

        input.clean()

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
        instance.short_social_summary = input.short_social_summary

        languages = Language.objects.filter(code__in=input.languages).all()
        instance.languages.set(languages)

        instance.tags.set(input.tags)

        instance.save()

        instance._type_definition = Submission._type_definition
        return instance

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_submission(
        self, info: Info, input: SendSubmissionInput
    ) -> SendSubmissionOutput:
        request = info.context.request

        conference = Conference.objects.filter(code=input.conference).first()

        if not conference:
            return SendSubmissionErrors.with_error("conference", "Invalid conference")

        errors = input.validate(conference=conference)

        if not conference.is_cfp_open:
            errors.add_error("non_field_errors", "The call for paper is not open!")

        if errors.has_errors:
            return errors

        input.clean()

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
            short_social_summary=input.short_social_summary,
        )

        languages = Language.objects.filter(code__in=input.languages).all()

        instance.languages.set(languages)
        instance.tags.set(input.tags)

        notify_new_submission(
            submission_id=instance.id,
            title=instance.title.localize("en"),
            elevator_pitch=instance.elevator_pitch.localize("en"),
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
