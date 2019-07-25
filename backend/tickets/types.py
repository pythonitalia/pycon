import strawberry
from conferences.types import TicketFare
from users.types import UserType


@strawberry.type
class TicketType:
    id: strawberry.ID
    user: UserType
    ticket_fare: TicketFare
