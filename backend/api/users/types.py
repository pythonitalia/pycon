from typing import List

import strawberry


@strawberry.type
class MeUser:
    id: strawberry.ID
    email: str

    @strawberry.field
    def tickets(self, info, conference: str) -> List["Ticket"]:
        return self.tickets.filter(ticket_fare__conference__code=conference).all()


@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str
    full_name: str
    username: str
