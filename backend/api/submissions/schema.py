import typing

import strawberry

from api.helpers.ids import decode_hashid
from api.permissions import CanSeeSubmissions, IsAuthenticated
from conferences.models import Conference as ConferenceModel
from submissions.models import Submission as SubmissionModel
from submissions.models import SubmissionTag as SubmissionTagModel

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
        self, info, code: str, after: typing.Optional[str] = None
    ) -> typing.Optional[typing.List[Submission]]:
        conference = ConferenceModel.objects.filter(code=code).first()

        if not conference or not CanSeeSubmissions().has_permission(conference, info):
            raise PermissionError("Cannot fetch submissions")

        qs = conference.submissions.order_by("id").all()
        if after:
            decoded_id = decode_hashid(after)
            qs = qs.filter(
                id__gt=decoded_id,
            )
        return qs[:50]

    @strawberry.field
    def submission_tags(self, info) -> typing.List[SubmissionTag]:
        return SubmissionTagModel.objects.all()
