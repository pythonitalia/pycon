from typing import List

import strawberry

from countries.types import Country

# TODO: merge Me User and User


@strawberry.type
class MeUser:
    id: strawberry.ID
    email: str
    first_name: str
    last_name: str
    gender: str
    open_to_recruiting: bool
    date_birth: str
    business_name: str
    fiscal_code: str
    vat_number: str
    recipient_code: str
    pec_address: str
    address: str
    country: Country
    phone_number: str

    # TODO: update this with pretix query
    @strawberry.field
    def tickets(self, info, conference: str) -> List["Ticket"]:
        return self.tickets.filter(ticket_fare__conference__code=conference).all()

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
    first_name: str
    gender: str
    open_to_recruiting: bool
    date_birth: str
    business_name: str
    fiscal_code: str
    vat_number: str
    recipient_code: str
    pec_address: str
    address: str
    country: Country
    phone_number: str
