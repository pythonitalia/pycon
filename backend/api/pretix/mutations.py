import logging
from typing import List

import strawberry
from requests import HTTPError
from strawberry.types import Info

import pretix
from api.pretix.permissions import IsTicketOwner
from api.pretix.query import get_user_tickets
from api.pretix.types import AttendeeTicket, UpdateAttendeeTicketInput
from conferences.models.conference import Conference

logger = logging.getLogger(__name__)


@strawberry.type
class TicketReassigned:
    id: strawberry.ID
    email: str


@strawberry.type
class UpdateAttendeeTicketError:
    field: str
    message: str


@strawberry.type
class UpdateAttendeeTicketErrors:
    id: strawberry.ID
    errors: List[UpdateAttendeeTicketError]


UpdateAttendeeTicketResult = strawberry.union(
    "UpdateAttendeeTicketResult",
    (TicketReassigned, AttendeeTicket, UpdateAttendeeTicketErrors),
)


@strawberry.type
class AttendeeTicketMutation:
    @strawberry.mutation(permission_classes=[IsTicketOwner])
    def update_attendee_ticket(
        self,
        info: Info,
        conference: str,
        input: UpdateAttendeeTicketInput,
        language: str = "en",
    ) -> UpdateAttendeeTicketResult:
        conference = Conference.objects.get(code=conference)
        try:
            pretix.update_ticket(conference, input)
        except HTTPError as e:
            logger.error(e, exc_info=True)
            data = e.response.json()
            return _get_update_tickets_errors(data, input)

        # TODO: filter by orderposition in the Pretix API
        tickets = get_user_tickets(
            conference, info.context.request.user.email, language=language
        )

        ticket = next(filter(lambda ticket: str(ticket.id) == input.id, tickets), None)
        if ticket:
            return ticket

        # If the user has changed the email, the ticket will not be returned but
        # the mutation succeeded.
        return TicketReassigned(id=input.id, email=input.email)


def _get_update_tickets_errors(
    response, input: UpdateAttendeeTicketInput
) -> UpdateAttendeeTicketErrors:
    errors = []
    for field in ("attendee_name", "attendee_email"):
        if response.get(field):
            errors.append(
                UpdateAttendeeTicketError(field=field, message=response[field][0])
            )

    if response.get("answers"):
        for index, answer in enumerate(input.answers):
            answer_error = response["answers"][index]
            if answer_error:
                for field in ("answer", "options"):
                    if answer_error.get(field):
                        error = UpdateAttendeeTicketError(
                            field=answer.question,
                            message=answer_error[field][0],
                        )
                        errors.append(error)

    return UpdateAttendeeTicketErrors(id=input.id, errors=errors)
