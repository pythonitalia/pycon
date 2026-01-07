from urllib.parse import urljoin
from django.conf import settings
from conferences.frontend import trigger_frontend_revalidate
from grants.tasks import get_name
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from strawberry.scalars import JSON

from django.db import transaction
import math
import re
from typing import Annotated, Union, Optional

from privacy_policy.record import record_privacy_policy_acceptance
import strawberry
from strawberry import ID
from strawberry.types import Info

from api.permissions import IsAuthenticated
from api.types import BaseErrorType, MultiLingualInput
from conferences.models.conference import Conference
from i18n.strings import LazyI18nString
from languages.models import Language
from participants.models import Participant
from submissions.models import ProposalMaterial, Submission as SubmissionModel
from submissions.tasks import notify_new_cfp_submission

from .types import Submission, SubmissionMaterialInput

FACEBOOK_LINK_MATCH = re.compile(r"^http(s)?:\/\/(www\.)?facebook\.com\/")
LINKEDIN_LINK_MATCH = re.compile(r"^http(s)?:\/\/(www\.)?linkedin\.com\/")


@strawberry.type
class ProposalMaterialErrors:
    file_id: list[str] = strawberry.field(default_factory=list)
    url: list[str] = strawberry.field(default_factory=list)
    id: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class SendSubmissionErrors(BaseErrorType):
    @strawberry.type
    class _SendSubmissionErrors:
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
        short_social_summary: list[str] = strawberry.field(default_factory=list)
        materials: list[ProposalMaterialErrors] = strawberry.field(default_factory=list)

        speaker_bio: list[str] = strawberry.field(default_factory=list)
        speaker_photo: list[str] = strawberry.field(default_factory=list)
        speaker_website: list[str] = strawberry.field(default_factory=list)
        speaker_level: list[str] = strawberry.field(default_factory=list)
        previous_talk_video: list[str] = strawberry.field(default_factory=list)
        speaker_twitter_handle: list[str] = strawberry.field(default_factory=list)
        speaker_instagram_handle: list[str] = strawberry.field(default_factory=list)
        speaker_linkedin_url: list[str] = strawberry.field(default_factory=list)
        speaker_facebook_url: list[str] = strawberry.field(default_factory=list)
        speaker_mastodon_handle: list[str] = strawberry.field(default_factory=list)

        non_field_errors: list[str] = strawberry.field(default_factory=list)

    errors: _SendSubmissionErrors = None


class BaseSubmissionInput:
    def clean(self):
        self.title = self.title.clean(self.languages)
        self.elevator_pitch = self.elevator_pitch.clean(self.languages)
        self.abstract = self.abstract.clean(self.languages)

    def multi_lingual_validation(
        self, errors: SendSubmissionErrors, conference: Conference
    ):
        multi_lingual_fields = (
            "title",
            "abstract",
            "elevator_pitch",
        )

        multi_lingual_max_lengths = {
            "title": 100,
            "elevator_pitch": 300,
            "abstract": 5000,
        }
        to_text = {"it": "Italian", "en": "English"}

        allowed_languages = conference.languages.values_list("code", flat=True)

        for language in self.languages:
            if language not in allowed_languages:
                errors.add_error("languages", f"Language ({language}) is not allowed")
                continue

            for field in multi_lingual_fields:
                value = getattr(getattr(self, field), language)
                max_length = multi_lingual_max_lengths.get(field, math.inf)

                if not value:
                    errors.add_error(field, f"{to_text[language]}: Cannot be empty")
                    continue

                if len(value) > max_length:
                    errors.add_error(
                        field,
                        f"{to_text[language]}: Cannot be more than {max_length} chars",
                    )

    def validate(self, conference: Conference):
        errors = SendSubmissionErrors()

        if not self.tags:
            errors.add_error("tags", "You need to add at least one tag")
        elif len(self.tags) > 3:
            errors.add_error("tags", "You can only add up to 3 tags")

        if not self.speaker_level:
            errors.add_error(
                "speaker_level", "You need to specify what is your speaker experience"
            )
        elif self.speaker_level not in SubmissionModel.SPEAKER_LEVELS:
            errors.add_error("speaker_level", "Select a valid choice")

        if not self.languages:
            errors.add_error("languages", "You need to add at least one language")

        self.multi_lingual_validation(errors, conference)

        max_lengths = {
            "speaker_bio": 2048,
            "notes": 1000,
            "short_social_summary": 128,
            "previous_talk_video": 2048,
            "speaker_website": 2048,
            "speaker_twitter_handle": 15,
            "speaker_instagram_handle": 30,
            "speaker_mastodon_handle": 2048,
            "speaker_linkedin_url": 2048,
            "speaker_facebook_url": 2048,
        }

        for field_name, max_length in max_lengths.items():
            field = getattr(self, field_name)
            if len(field) > max_length:
                errors.add_error(
                    field_name,
                    f"Cannot be more than {max_length} chars",
                )

        duration = conference.durations.filter(id=self.duration).first()

        if not conference.submission_types.filter(id=self.type).exists():
            errors.add_error("type", "Not allowed submission type")

        if self.topic and not conference.topics.filter(id=self.topic).exists():
            errors.add_error("topic", "Not a valid topic")

        if not duration:
            errors.add_error(
                "duration",
                (
                    "Select a valid choice. "
                    "That choice is not one of the available choices."
                ),
            )
        elif not duration.allowed_submission_types.filter(id=self.type).exists():
            errors.add_error(
                "duration", "Duration is not an allowed for the submission type"
            )

        if not conference.audience_levels.filter(id=self.audience_level).exists():
            errors.add_error("audience_level", "Not a valid audience level")

        if not self.speaker_photo:
            errors.add_error("speaker_photo", "This is required")

        if self.speaker_linkedin_url and not LINKEDIN_LINK_MATCH.match(
            self.speaker_linkedin_url
        ):
            errors.add_error(
                "speaker_linkedin_url", "Linkedin URL should be a linkedin.com link"
            )

        if self.speaker_facebook_url and not FACEBOOK_LINK_MATCH.match(
            self.speaker_facebook_url
        ):
            errors.add_error(
                "speaker_facebook_url", "Facebook URL should be a facebook.com link"
            )

        return errors


@strawberry.input
class SendSubmissionInput(BaseSubmissionInput):
    conference: ID
    title: MultiLingualInput
    abstract: MultiLingualInput
    languages: list[ID]
    type: ID
    duration: ID
    elevator_pitch: MultiLingualInput
    notes: str
    audience_level: ID
    short_social_summary: str

    speaker_bio: str
    speaker_photo: str
    speaker_website: str
    speaker_level: str
    previous_talk_video: str
    speaker_twitter_handle: str
    speaker_instagram_handle: str
    speaker_linkedin_url: str
    speaker_facebook_url: str
    speaker_mastodon_handle: str
    speaker_availabilities: JSON

    topic: Optional[ID] = strawberry.field(default=None)
    tags: list[ID] = strawberry.field(default_factory=list)
    do_not_record: bool = strawberry.field(default=False)


@strawberry.input
class UpdateSubmissionInput(BaseSubmissionInput):
    instance: ID
    title: MultiLingualInput
    abstract: MultiLingualInput
    languages: list[ID]
    type: ID
    duration: ID
    elevator_pitch: MultiLingualInput
    notes: str
    audience_level: ID
    short_social_summary: str

    speaker_bio: str
    speaker_photo: str
    speaker_website: str
    speaker_level: str
    previous_talk_video: str
    speaker_twitter_handle: str
    speaker_instagram_handle: str
    speaker_linkedin_url: str
    speaker_facebook_url: str
    speaker_mastodon_handle: str
    speaker_availabilities: JSON

    topic: Optional[ID] = strawberry.field(default=None)
    tags: list[ID] = strawberry.field(default_factory=list)
    materials: list[SubmissionMaterialInput] = strawberry.field(default_factory=list)
    do_not_record: bool = strawberry.field(default=False)

    def validate(self, conference: Conference, submission: SubmissionModel):
        errors = super().validate(conference)

        # Check if CFP is closed and prevent editing of restricted fields
        # Exception: accepted submissions can still be edited
        if (
            not conference.is_cfp_open
            and submission.status != SubmissionModel.STATUS.accepted
        ):
            restricted_fields = (
                "title",
                "abstract",
                "elevator_pitch",
            )

            for field_name in restricted_fields:
                input_value = getattr(self, field_name)
                submission_value = getattr(submission, field_name)
                if LazyI18nString(input_value.to_dict()) != submission_value:
                    field_label = field_name.replace("_", " ")
                    errors.add_error(
                        field_name,
                        f"You cannot edit the {field_label} after the call for proposals deadline has passed.",
                    )

        if self.materials:
            if len(self.materials) > 3:
                errors.add_error(
                    "non_field_errors", "You can only add up to 3 materials"
                )
            else:
                for index, material in enumerate(self.materials):
                    with errors.with_prefix("materials", index):
                        material.validate(errors, submission)

        return errors


SendSubmissionOutput = Annotated[
    Union[Submission, SendSubmissionErrors],
    strawberry.union(name="SendSubmissionOutput"),
]

UpdateSubmissionOutput = Annotated[
    Union[Submission, SendSubmissionErrors],
    strawberry.union(name="UpdateSubmissionOutput"),
]


@strawberry.type
class SubmissionsMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_submission(
        self, info: Info, input: UpdateSubmissionInput
    ) -> UpdateSubmissionOutput:
        request = info.context.request

        instance = SubmissionModel.objects.get_by_hashid(input.instance)
        if not instance.can_edit(info.context.request):
            return SendSubmissionErrors.with_error(
                "non_field_errors", "You cannot edit this submission"
            )

        conference = instance.conference

        errors = input.validate(conference=conference, submission=instance)

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
        instance.do_not_record = input.do_not_record

        languages = Language.objects.filter(code__in=input.languages).all()
        instance.languages.set(languages)

        instance.tags.set(input.tags)

        instance.save()

        materials_to_create = []
        materials_to_update = []

        existing_materials = {
            existing_material.id: existing_material
            for existing_material in instance.materials.all()
        }
        for material in input.materials:
            existing_material = (
                existing_materials.get(int(material.id)) if material.id else None
            )

            if existing_material:
                existing_material.name = material.name
                existing_material.url = material.url
                existing_material.file_id = material.file_id
                materials_to_update.append(existing_material)
            else:
                materials_to_create.append(
                    ProposalMaterial(
                        proposal=instance,
                        name=material.name,
                        url=material.url,
                        file_id=material.file_id,
                    )
                )

        if to_delete := [
            m.id for m in existing_materials.values() if m not in materials_to_update
        ]:
            ProposalMaterial.objects.filter(
                proposal=instance,
                id__in=to_delete,
            ).delete()

        if materials_to_create:
            ProposalMaterial.objects.bulk_create(materials_to_create)
        if materials_to_update:
            ProposalMaterial.objects.bulk_update(
                materials_to_update, fields=["name", "url", "file_id"]
            )

        Participant.objects.update_or_create(
            user_id=request.user.id,
            conference=conference,
            defaults={
                "bio": input.speaker_bio,
                "photo_file_id": input.speaker_photo,
                "website": input.speaker_website,
                "speaker_level": input.speaker_level,
                "previous_talk_video": input.previous_talk_video,
                "twitter_handle": input.speaker_twitter_handle,
                "instagram_handle": input.speaker_instagram_handle,
                "linkedin_url": input.speaker_linkedin_url,
                "facebook_url": input.speaker_facebook_url,
                "mastodon_handle": input.speaker_mastodon_handle,
                "speaker_availabilities": input.speaker_availabilities,
            },
        )

        trigger_frontend_revalidate(conference, instance)

        instance.__strawberry_definition__ = Submission.__strawberry_definition__
        return instance

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @transaction.atomic
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

        if (
            SubmissionModel.objects.of_user(request.user)
            .for_conference(conference)
            .non_cancelled()
            .count()
            >= 3
        ):
            errors.add_error(
                "non_field_errors", "You can only submit up to 3 proposals"
            )

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
            short_social_summary=input.short_social_summary,
            do_not_record=input.do_not_record,
        )

        languages = Language.objects.filter(code__in=input.languages).all()

        instance.languages.set(languages)
        instance.tags.set(input.tags)

        Participant.objects.update_or_create(
            user_id=request.user.id,
            conference=conference,
            defaults={
                "bio": input.speaker_bio,
                "photo_file_id": input.speaker_photo,
                "website": input.speaker_website,
                "speaker_level": input.speaker_level,
                "previous_talk_video": input.previous_talk_video,
                "twitter_handle": input.speaker_twitter_handle,
                "instagram_handle": input.speaker_instagram_handle,
                "linkedin_url": input.speaker_linkedin_url,
                "facebook_url": input.speaker_facebook_url,
                "mastodon_handle": input.speaker_mastodon_handle,
                "speaker_availabilities": input.speaker_availabilities,
            },
        )

        record_privacy_policy_acceptance(
            info.context.request,
            conference,
            "cfp",
        )

        email_template = EmailTemplate.objects.for_conference(
            conference
        ).get_by_identifier(EmailTemplateIdentifier.proposal_received_confirmation)

        proposal_url = urljoin(
            settings.FRONTEND_URL,
            f"/submission/{instance.hashid}",
        )

        email_template.send_email(
            recipient=request.user,
            placeholders={
                "user_name": get_name(request.user, "there"),
                "proposal_title": instance.title.localize("en"),
                "proposal_url": proposal_url,
            },
        )

        def _notify_new_submission():
            notify_new_cfp_submission.delay(
                submission_id=instance.id,
                conference_id=instance.conference_id,
                admin_url=request.build_absolute_uri(instance.get_admin_url()),
            )

        transaction.on_commit(_notify_new_submission)

        # hack because we return django models
        instance.__strawberry_definition__ = Submission.__strawberry_definition__
        return instance
