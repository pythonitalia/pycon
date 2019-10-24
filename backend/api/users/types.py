from typing import List, Optional

import strawberry

from countries.types import Country

# TODO: merge Me User and User


@strawberry.type
class Image:
    url: str


@strawberry.type
class MeUser:
    id: strawberry.ID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    open_to_recruiting: Optional[bool]
    open_to_newsletter: Optional[bool]
    date_birth: Optional[str]
    country: Optional[str]
    image: Optional[Image]

    # TODO: update this with pretix query
    @strawberry.field
    def tickets(self, info, conference: str) -> List["Ticket"]:
        return self.tickets.filter(ticket_fare__conference__code=conference).all()

    @strawberry.field
    def submissions(self, info, conference: str) -> List["Submission"]:
        return self.submissions.filter(conference__code=conference)

    @strawberry.field
    def image(self, info) -> Optional[Image]:
        return self.image


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str
    full_name: str
    username: str
    first_name: str
    last_name: str
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    date_birth: str
    country: str


@strawberry.type
class Country:
    code: str
    name: str
