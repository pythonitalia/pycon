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
        after: typing.Optional[str] = None,
        limit: typing.Optional[int] = 50,
    ) -> typing.Optional[typing.List[Submission]]:
        conference = ConferenceModel.objects.filter(code=code).first()

        if not conference or not CanSeeSubmissions().has_permission(conference, info):
            raise PermissionError("You need to have a ticket to see submissions")

        qs = conference.submissions.order_by("id").filter(
            status=SubmissionModel.STATUS.proposed
        )
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
    def voting_tags(
        self, info, conference: strawberry.ID
    ) -> typing.List[SubmissionTag]:
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
