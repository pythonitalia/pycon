from typing import List

import strawberry

from api.pretix.query import get_user_orders, get_user_tickets
from api.pretix.types import PretixOrder, PretixOrderPosition
from api.submissions.types import Submission
from conferences.models import Conference
from submissions.models import Submission as SubmissionModel


@strawberry.federation.type(keys=["id"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    email: str = strawberry.federation.field(external=True)
    isStaff: bool = strawberry.federation.field(external=True)

    @classmethod
    def resolve_reference(
        cls, id: strawberry.ID, email: str = "", isStaff: bool = False
    ):
        return cls(id=id, email=email, isStaff=isStaff)

    @strawberry.federation.field(requires=["email"])
    def orders(self, info, conference: str) -> List[PretixOrder]:
        conference = Conference.objects.get(code=conference)
        return get_user_orders(conference, self.email)

    @strawberry.federation.field(requires=["email"])
    def tickets(
        self, info, conference: str, language: str
    ) -> List[PretixOrderPosition]:
        conference = Conference.objects.get(code=conference)
        return get_user_tickets(conference, self.email, language)

    @strawberry.field
    def submissions(self, info, conference: str) -> List[Submission]:
        return SubmissionModel.objects.filter(
            speaker_id=self.id, conference__code=conference
        )

    @strawberry.federation.field(requires=["isStaff"])
    def can_edit_schedule(self) -> bool:
        return self.isStaff


@strawberry.type
class Country:
    code: str
    name: str
