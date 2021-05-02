from typing import List, Optional

import strawberry
from api.pretix.query import get_user_orders
from api.pretix.types import PretixOrder
from api.submissions.types import Submission
from conferences.models import Conference
from submissions.models import Submission as SubmissionModel


@strawberry.federation.type(keys=["id email"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    email: str = strawberry.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberry.ID, email: str):
        return cls(id=id, email=email)

    @strawberry.field
    def orders(self, info, conference: str) -> List[PretixOrder]:
        # TODO remove this
        return []
        conference = Conference.objects.get(code=conference)

        return get_user_orders(conference, self.email)

    @strawberry.field
    def submissions(self, info, conference: str) -> List[Submission]:
        return SubmissionModel.objects.filter(
            speaker_id=self.id, conference__code=conference
        )

    @strawberry.field
    def can_edit_schedule(self, info) -> bool:
        # return self.is_staff or self.is_superuser
        # todo implement
        return False


@strawberry.type
class Country:
    code: str
    name: str
