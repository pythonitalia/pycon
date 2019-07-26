from typing import List

import strawberry


@strawberry.type
class MeUserType:
    id: strawberry.ID
    email: str

    @strawberry.field
    def tickets(self, info, conference: str) -> List["TicketType"]:
        return self.tickets.filter(ticket_fare__conference__code=conference).all()


@strawberry.type
class UserType:
    id: strawberry.ID
    email: str
    name: str
    username: str
