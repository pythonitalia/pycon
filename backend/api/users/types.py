from typing import List, Optional

import strawberry
from api.pretix.query import get_user_orders
from api.pretix.types import PretixOrder
from conferences.models import Conference

# TODO: merge Me User and User


@strawberry.type
class MeUser:
    id: strawberry.ID
    email: str
    name: Optional[str]
    full_name: Optional[str]
    gender: Optional[str]
    open_to_recruiting: Optional[bool]
    open_to_newsletter: Optional[bool]
    date_birth: Optional[str]
    country: Optional[str]

    @strawberry.field
    def orders(self, info, conference: str) -> List[PretixOrder]:
        conference = Conference.objects.get(code=conference)

        return get_user_orders(conference, self.email)

    @strawberry.field
    def submissions(self, info, conference: str) -> List["Submission"]:
        return self.submissions.filter(conference__code=conference)


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str
    full_name: str
    username: str
    name: str
    full_name: str
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    date_birth: str
    country: str


@strawberry.type
class Country:
    code: str
    name: str
