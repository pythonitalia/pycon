from typing import Optional

import strawberry
from strawberry import ID

from api.submissions.permissions import CanSeeSubmissionPrivateFields


@strawberry.type
class Participant:
    id: ID
    user_id: ID
    bio: str
    website: str
    photo: str
    public_profile: bool
    twitter_handle: str
    instagram_handle: str
    linkedin_url: str
    facebook_url: str
    mastodon_handle: str
    speaker_id: strawberry.Private[int]

    _speaker_level: strawberry.Private[str]
    _previous_talk_video: strawberry.Private[str]

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
            user_id=instance.user_id,
            speaker_id=instance.user_id,
            fullname=instance.user.fullname,
            photo=instance.photo,
            bio=instance.bio,
            website=instance.website,
            public_profile=instance.public_profile,
            _speaker_level=instance.speaker_level,
            _previous_talk_video=instance.previous_talk_video,
            twitter_handle=instance.twitter_handle,
            instagram_handle=instance.instagram_handle,
            linkedin_url=instance.linkedin_url,
            facebook_url=instance.facebook_url,
            mastodon_handle=instance.mastodon_handle,
        )
