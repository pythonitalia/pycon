import logging

import strawberry
from strawberry.types import Info

import pretix
from api.pretix.permissions import IsTicketOwner
from api.pretix.query import get_user_tickets
from api.pretix.types import AttendeeTicket, UpdateAttendeeTicketInput
from conferences.models.conference import Conference

logger = logging.getLogger(__name__)


@strawberry.type
class UpdateAttendeeTicketError:
    message: str = "Something went wrong while updating the ticket, please try again."


@strawberry.type
class TicketReassigned:
    id: strawberry.ID
    email: str


UpdateAttendeeTicketResult = strawberry.union(
    "UpdateAttendeeTicketResult",
    (TicketReassigned, AttendeeTicket, UpdateAttendeeTicketError),
)


@strawberry.type
class AttendeeTicketMutation:
    @strawberry.mutation(permission_classes=[IsTicketOwner])
    def update_attendee_ticket(
        self, info: Info, conference_code: str, input: UpdateAttendeeTicketInput
    ) -> UpdateAttendeeTicketResult:
        conference = Conference.objects.get(code=conference_code)
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
            return UpdateAttendeeTicketError(message=str(e))

        # If the user has changed the email, the ticket will not be returned but
        # the mutation succeeded.
        return TicketReassigned(id=input.id, email=input.email)
