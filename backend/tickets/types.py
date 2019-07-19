import strawberry
from conferences.types import TicketFareType
from users.types import UserType


@strawberry.type
class TicketType:
    id: strawberry.ID
    user: UserType
    ticket_fare: TicketFareType
