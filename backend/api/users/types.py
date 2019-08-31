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
    first_name: str
    last_name: str
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    date_birth: str
    business_name: Optional[str]
    fiscal_code: Optional[str]
    vat_number: Optional[str]
    recipient_code: Optional[str]
    pec_address: Optional[str]
    address: Optional[str]
    country: str
    phone_number: Optional[str]
    image: Optional[Image]

    # TODO: update this with pretix query
    @strawberry.field
    def tickets(self, info, conference: str) -> List["Ticket"]:
        return self.tickets.filter(ticket_fare__conference__code=conference).all()

    @strawberry.field
    def submissions(self, info, conference: str) -> List["Submission"]:
        return self.submissions.filter(conference__code=conference)

    @strawberry.field
    def image(self, info) -> Image:
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
    business_name: Optional[str]
    fiscal_code: Optional[str]
    vat_number: Optional[str]
    recipient_code: Optional[str]
    pec_address: Optional[str]
    address: Optional[str]
    country: str
    phone_number: Optional[str]
