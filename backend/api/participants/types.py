from typing import TYPE_CHECKING, Annotated, Optional

from submissions.models import Submission as SubmissionModel
from strawberry.scalars import JSON
import strawberry
from strawberry import ID

from api.submissions.permissions import CanSeeSubmissionPrivateFields

if TYPE_CHECKING:
    from api.submissions.types import Submission


@strawberry.type
class Participant:
    id: ID
    bio: str
    website: str
    photo: str | None
    photo_id: str | None
    public_profile: bool
    twitter_handle: str
    instagram_handle: str
    linkedin_url: str
    facebook_url: str
    mastodon_handle: str
    fullname: str
    speaker_availabilities: JSON

    _speaker_level: strawberry.Private[str]
    _previous_talk_video: strawberry.Private[str]
    _conference_id: strawberry.Private[int]
    _user_id: strawberry.Private[int]

    @strawberry.field
    def proposals(
        self, info
    ) -> list[Annotated["Submission", strawberry.lazy("api.submissions.types")]]:
        return SubmissionModel.objects.for_conference(self._conference_id).filter(
            speaker_id=self._user_id,
            status=SubmissionModel.STATUS.accepted,
        )

    @strawberry.field
    def speaker_level(self, info) -> Optional[str]:
        if not CanSeeSubmissionPrivateFields().has_permission(self, info):
            return None

        return self._speaker_level

    @strawberry.field
    def previous_talk_video(self, info) -> Optional[str]:
        if not CanSeeSubmissionPrivateFields().has_permission(self, info):
            return None

        return self._previous_talk_video

    @classmethod
    def from_model(cls, instance):
        return cls(
            id=instance.hashid,
            fullname=instance.user.fullname,
            photo=instance.photo_url,
            photo_id=instance.photo_file_id,
            bio=instance.bio,
            website=instance.website,
            public_profile=instance.public_profile,
            twitter_handle=instance.twitter_handle,
            instagram_handle=instance.instagram_handle,
            linkedin_url=instance.linkedin_url,
            facebook_url=instance.facebook_url,
            mastodon_handle=instance.mastodon_handle,
            speaker_availabilities=instance.speaker_availabilities or {},
            _conference_id=instance.conference_id,
            _user_id=instance.user_id,
            _speaker_level=instance.speaker_level,
            _previous_talk_video=instance.previous_talk_video,
        )
