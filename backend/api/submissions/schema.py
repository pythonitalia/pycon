import typing

import strawberry

from api.helpers.ids import decode_hashid
from api.permissions import CanSeeSubmissions, IsAuthenticated
from conferences.models import Conference as ConferenceModel
from submissions.models import (
    Submission as SubmissionModel,
    SubmissionTag as SubmissionTagModel,
)

from .types import Submission, SubmissionTag


@strawberry.type
class SubmissionsQuery:
    @strawberry.field
    def submission(self, info, id: strawberry.ID) -> typing.Optional[Submission]:
        try:
            return SubmissionModel.objects.get_by_hashid(id)
        except SubmissionModel.DoesNotExist:
            return None

    @strawberry.field(permission_classes=[IsAuthenticated])
    def submissions(
        self,
        info,
        code: str,
        language: typing.Optional[str] = None,
        voted: typing.Optional[bool] = None,
        tags: typing.Optional[list[str]] = None,
        type: typing.Optional[str] = None,
        audience_level: typing.Optional[str] = None,
        after: typing.Optional[str] = None,
        limit: typing.Optional[int] = 50,
    ) -> typing.Optional[typing.List[Submission]]:
        request = info.context.request
        conference = (
            ConferenceModel.objects.filter(code=code).first()
        )

        if not conference or not CanSeeSubmissions().has_permission(conference, info):
            raise PermissionError("You need to have a ticket to see submissions")

        info.context._user_can_vote = True

        qs = (
            conference.submissions.prefetch_related(
                "type",
                "duration",
                "schedule_items",
                "languages",
                "audience_level",
                "tags",
            )
            .order_by("id")
            .filter(status=SubmissionModel.STATUS.proposed)
        )

        if language:
            qs = qs.filter(languages__code=language)

        if tags:
            qs = qs.filter(tags__id__in=tags)

        if voted:
            qs = qs.filter(votes__user_id=request.user.id)
        elif voted is not None:
            qs = qs.exclude(
                id__in=[s.id for s in qs.filter(votes__user_id=request.user.id)]
            )

        if type:
            qs = qs.filter(type__id=type)

        if audience_level:
            qs = qs.filter(audience_level__id=audience_level)

        qs = qs.distinct()

        if after:
            decoded_id = decode_hashid(after)
            qs = qs.filter(
                id__gt=decoded_id,
            )
        return qs[:limit]

    @strawberry.field
    def submission_tags(self, info) -> typing.List[SubmissionTag]:
        return SubmissionTagModel.objects.order_by("name").all()

    @strawberry.field
    def voting_tags(self, info, conference: str) -> typing.List[SubmissionTag]:
        used_tags = (
            SubmissionModel.objects.filter(
                conference__code=conference,
            )
            .values_list("tags__id", flat=True)
            .distinct()
        )
        return (
            SubmissionTagModel.objects.filter(id__in=used_tags).order_by("name").all()
        )
