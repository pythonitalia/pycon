import logging

import strawberry
from strawberry.types import Info

import pretix
from api.permissions import IsAuthenticated
from api.pretix.query import get_user_tickets
from api.pretix.types import AttendeeTicket, UpdateAttendeeTicketInput
from conferences.models.conference import Conference

logger = logging.getLogger(__name__)


@strawberry.type
class UpdateAttendeeTicketError:
    message: str = ""


@strawberry.type
class TicketReassigned:
    id: strawberry.ID
    message: str = "Ticket was Successfully reassigned to {email}"


UpdateAttendeeTicketResult = strawberry.union(
    "UpdateAttendeeTicketResult",
    (TicketReassigned, AttendeeTicket, UpdateAttendeeTicketError),
)


@strawberry.type
class AttendeeTicketMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_attendee_ticket(
        self, info: Info, conference: str, input: UpdateAttendeeTicketInput
    ) -> UpdateAttendeeTicketResult:
        conference = Conference.objects.get(code=conference)

        try:
            pretix.update_ticket(conference, input)

            # TODO: filter by orderposition
            tickets = get_user_tickets(
                conference, info.context.request.user.email, language="en"
            )

            tickets = list(filter(lambda ticket: str(ticket.id) == input.id, tickets))
            if tickets:
                return tickets[0]

        except Exception as e:
            logger.error(
                "Unable to update the AttendeeTicket %s due to an error %s",
                input.id,
                e,
                exc_info=True,
            )
            return UpdateAttendeeTicketError(e)

        # If the user has changed the email, the ticket will not be returned but
        # the mutation succeeded.
        return TicketReassigned(
            id=input.id, message=TicketReassigned.message.format(email=input.email)
        )
