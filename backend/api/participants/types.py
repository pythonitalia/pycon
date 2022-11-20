import strawberry
from strawberry import ID


@strawberry.type
class Participant:
    id: ID
    bio: str
    website: str
    speaker_level: str
    photo: str
    previous_talk_video: str
    twitter_handle: str
    instagram_handle: str
    linkedin_url: str
    facebook_url: str
    mastodon_handle: str

    @classmethod
    def from_model(cls, instance):
        return cls(
            id=instance.id,
            photo=instance.photo,
            bio=instance.bio,
            website=instance.website,
            speaker_level=instance.speaker_level,
            previous_talk_video=instance.previous_talk_video,
            twitter_handle=instance.twitter_handle,
            instagram_handle=instance.instagram_handle,
            linkedin_url=instance.linkedin_url,
            facebook_url=instance.facebook_url,
            mastodon_handle=instance.mastodon_handle,
        )
