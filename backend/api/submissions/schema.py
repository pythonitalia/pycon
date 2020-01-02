import typing

import strawberry
from submissions.models import Submission as SubmissionModel
from submissions.models import SubmissionTag as SubmissionTagModel

from .types import Submission, SubmissionTag


@strawberry.type
class SubmissionsQuery:
    @strawberry.field
    def submission(self, info, id: strawberry.ID) -> typing.Optional[Submission]:
        return SubmissionModel.objects.filter(id=id).first()

    @strawberry.field
    def submission_tags(self, info) -> typing.List[SubmissionTag]:
        return SubmissionTagModel.objects.all()
