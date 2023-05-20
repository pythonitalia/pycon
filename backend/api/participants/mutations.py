import re
from api.context import Info
from api.helpers.ids import encode_hashid
from django.conf import settings
import strawberry
from strawberry.tools import create_type
from api.permissions import IsAuthenticated
from api.types import BaseErrorType
from blob.confirmation import confirm_blob_upload_usage
from blob.enum import BlobContainer
from blob.url_parsing import verify_azure_storage_url
from conferences.models.conference import Conference
from participants.models import Participant as ParticipantModel

from .types import Participant


FACEBOOK_LINK_MATCH = re.compile(r"^http(s)?:\/\/(www\.)?facebook\.com\/")
LINKEDIN_LINK_MATCH = re.compile(r"^http(s)?:\/\/(www\.)?linkedin\.com\/")


@strawberry.type
class UpdateParticipantErrors(BaseErrorType):
    bio: list[str] = strawberry.field(default_factory=list)
    photo: list[str] = strawberry.field(default_factory=list)
    website: list[str] = strawberry.field(default_factory=list)
    level: list[str] = strawberry.field(default_factory=list)
    twitter_handle: list[str] = strawberry.field(default_factory=list)
    instagram_handle: list[str] = strawberry.field(default_factory=list)
    linkedin_url: list[str] = strawberry.field(default_factory=list)
    facebook_url: list[str] = strawberry.field(default_factory=list)
    mastodon_handle: list[str] = strawberry.field(default_factory=list)


@strawberry.input
class UpdateParticipantInput:
    conference: str
    bio: str
    public_profile: bool
    photo: str
    website: str
    speaker_level: str
    previous_talk_video: str
    twitter_handle: str
    instagram_handle: str
    linkedin_url: str
    facebook_url: str
    mastodon_handle: str

    def validate(self) -> UpdateParticipantErrors:
        errors = UpdateParticipantErrors()
        max_lengths = {
            "bio": 2048,
            "website": 2048,
            "twitter_handle": 15,
            "instagram_handle": 30,
            "mastodon_handle": 2048,
            "linkedin_url": 2048,
            "facebook_url": 2048,
        }

        for field_name, max_length in max_lengths.items():
            field = getattr(self, field_name)
            if len(field) > max_length:
                errors.add_error(
                    field_name,
                    f"Cannot be more than {max_length} chars",
                )

        if self.linkedin_url and not LINKEDIN_LINK_MATCH.match(self.linkedin_url):
            errors.add_error(
                "linkedin_url", "Linkedin URL should be a linkedin.com link"
            )

        if self.facebook_url and not FACEBOOK_LINK_MATCH.match(self.facebook_url):
            errors.add_error(
                "facebook_url", "Facebook URL should be a facebook.com link"
            )

        if self.photo and not verify_azure_storage_url(
            url=self.photo,
            allowed_containers=[
                BlobContainer.TEMPORARY_UPLOADS,
                BlobContainer.PARTICIPANTS_AVATARS,
            ],
        ):
            errors.add_error("photo", "Invalid photo")

        return errors


@strawberry.type
class UpdateParticipantValidationError:
    errors: UpdateParticipantErrors


UpdateParticipantResult = strawberry.union(
    "UpdateParticipantResult", (Participant, UpdateParticipantValidationError)
)


@strawberry.field(permission_classes=[IsAuthenticated])
def update_participant(
    info: Info, input: UpdateParticipantInput
) -> UpdateParticipantResult:
    request = info.context.request
    errors = input.validate()

    if errors.has_errors:
        return UpdateParticipantValidationError(errors=errors)

    conference = Conference.objects.get(code=input.conference)

    photo = input.photo
    if photo and verify_azure_storage_url(
        url=photo, allowed_containers=[BlobContainer.TEMPORARY_UPLOADS]
    ):
        photo = confirm_blob_upload_usage(
            photo,
            blob_name=_participant_avatar_blob_name(
                conference=conference, user_id=request.user.id
            ),
        )

    participant, _ = ParticipantModel.objects.update_or_create(
        user_id=request.user.id,
        conference=conference,
        defaults={
            "bio": input.bio,
            "photo": photo,
            "website": input.website,
            "public_profile": input.public_profile,
            "speaker_level": input.speaker_level,
            "previous_talk_video": input.previous_talk_video,
            "twitter_handle": input.twitter_handle,
            "instagram_handle": input.instagram_handle,
            "linkedin_url": input.linkedin_url,
            "facebook_url": input.facebook_url,
            "mastodon_handle": input.mastodon_handle,
        },
    )
    return Participant.from_model(participant)


def _participant_avatar_blob_name(conference: Conference, user_id: int) -> str:
    hashed_id = encode_hashid(user_id, salt=settings.USER_ID_HASH_SALT, min_length=6)
    return f"{conference.code}/{hashed_id}.jpg"


ParticipantMutations = create_type("ParticipantMutations", (update_participant,))
