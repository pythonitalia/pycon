from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django
from strawberry.scalars import JSON

from api.context import Info
from submissions.api.permissions import CanSeeSubmissionPrivateFields
from participants import models
from submissions import models as submission_models

if TYPE_CHECKING:
    from submissions.api.types import Submission


@strawberry_django.type(models.Participant)
class Participant:
    id: strawberry.ID

    @strawberry_django.field(only=["id"])
    def id(self) -> strawberry.ID:
        return self.hashid

    bio: strawberry.auto
    website: strawberry.auto

    photo_id: str | None

    @strawberry_django.field(only=["photo_file_id"])
    def photo_id(self) -> str | None:
        return str(self.photo_file_id) if self.photo_file_id else None

    public_profile: strawberry.auto
    twitter_handle: strawberry.auto
    instagram_handle: strawberry.auto
    linkedin_url: strawberry.auto
    facebook_url: strawberry.auto
    mastodon_handle: strawberry.auto

    @strawberry_django.field(
        only=["user__full_name"],
        select_related=["user"],
    )
    def fullname(self) -> str:
        return self.user.fullname

    @strawberry_django.field(only=["conference_id", "user_id"])
    def proposals(
        self,
    ) -> list[Annotated["Submission", strawberry.lazy("submissions.api.types")]]:
        return submission_models.Submission.objects.for_conference(
            self.conference_id
        ).filter(
            speaker_id=self.user_id,
            status=submission_models.Submission.STATUS.accepted,
        )

    @strawberry_django.field(only=["speaker_availabilities", "user_id"])
    def speaker_availabilities(self, info: Info) -> JSON | None:
        if not CanSeeSubmissionPrivateFields().has_permission(self, info):
            return None

        return self.speaker_availabilities

    @strawberry_django.field(only=["speaker_level", "user_id"])
    def speaker_level(self, info: Info) -> str | None:
        if not CanSeeSubmissionPrivateFields().has_permission(self, info):
            return None

        return self.speaker_level

    @strawberry_django.field(only=["previous_talk_video", "user_id"])
    def previous_talk_video(self, info: Info) -> str | None:
        if not CanSeeSubmissionPrivateFields().has_permission(self, info):
            return None

        return self.previous_talk_video

    @strawberry_django.field(
        only=["photo", "photo_file__file"],
        select_related=["photo_file"],
    )
    def photo(self, size: str = "default") -> str | None:
        if size == "small":
            return self.photo_small_url

        return self.photo_url
