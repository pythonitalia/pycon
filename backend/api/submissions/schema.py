import typing

import strawberry
from submissions.models import Submission as SubmissionModel

from .types import Submission


@strawberry.type
class SubmissionsQuery:
    @strawberry.field
    def submission(self, info, id: strawberry.ID) -> typing.Optional[Submission]:
        user = info.context["request"].user

        if not user.is_authenticated:
            return None

        return SubmissionModel.objects.filter(speaker=user, id=id).first()
