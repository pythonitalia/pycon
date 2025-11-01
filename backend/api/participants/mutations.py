import re
from api.context import Info
import strawberry
from strawberry.tools import create_type
from api.permissions import IsAuthenticated
from api.types import BaseErrorType
from conferences.models.conference import Conference
from participants.models import Participant as ParticipantModel

from .types import Participant
from typing import Annotated, Union


FACEBOOK_LINK_MATCH = re.compile(r"^http(s)?:\/\/(www\.)?facebook\.com\/")
LINKEDIN_LINK_MATCH = re.compile(r"^http(s)?:\/\/(www\.)?linkedin\.com\/")
MASTODON_HANDLE_MATCH = re.compile(
    r"^(https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}\/@[a-zA-Z0-9_]+|@?[a-zA-Z0-9_]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})$"
)


@strawberry.type
class UpdateParticipantErrors(BaseErrorType):
    @strawberry.type
    class _UpdateParticipantErrors:
        bio: list[str] = strawberry.field(default_factory=list)
        photo: list[str] = strawberry.field(default_factory=list)
        website: list[str] = strawberry.field(default_factory=list)
        level: list[str] = strawberry.field(default_factory=list)
        twitter_handle: list[str] = strawberry.field(default_factory=list)
        instagram_handle: list[str] = strawberry.field(default_factory=list)
        linkedin_url: list[str] = strawberry.field(default_factory=list)
        facebook_url: list[str] = strawberry.field(default_factory=list)
        mastodon_handle: list[str] = strawberry.field(default_factory=list)

    errors: _UpdateParticipantErrors = None


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

        if self.mastodon_handle and not MASTODON_HANDLE_MATCH.match(
            self.mastodon_handle
        ):
            errors.add_error(
                "mastodon_handle",
                "Mastodon handle should be in format: username@instance.social or @username@instance.social or https://instance.social/@username",
            )

        return errors.if_has_errors


UpdateParticipantResult = Annotated[
    Union[Participant, UpdateParticipantErrors],
    strawberry.union(name="UpdateParticipantResult"),
]


@strawberry.field(permission_classes=[IsAuthenticated])
def update_participant(
    info: Info, input: UpdateParticipantInput
) -> UpdateParticipantResult:
    request = info.context.request

    if error_validation := input.validate():
        return error_validation

    conference = Conference.objects.get(code=input.conference)

    participant, _ = ParticipantModel.objects.update_or_create(
        user_id=request.user.id,
        conference=conference,
        defaults={
            "bio": input.bio,
            "photo_file_id": input.photo if input.photo else None,
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


ParticipantMutations = create_type("ParticipantMutations", (update_participant,))
