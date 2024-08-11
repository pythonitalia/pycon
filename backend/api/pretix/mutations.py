import logging
from typing import Annotated, Union, Optional

import strawberry
from requests import HTTPError
from strawberry.types import Info

import pretix
from api.pretix.permissions import IsTicketOwner
from api.pretix.query import get_user_tickets
from api.pretix.types import (
    AttendeeTicket,
    UpdateAttendeeTicketErrors,
    UpdateAttendeeTicketInput,
)
from conferences.models.conference import Conference

logger = logging.getLogger(__name__)


@strawberry.type
class TicketReassigned:
    id: strawberry.ID
    # optional because AttendeeTicket.email is optional
    email: Optional[str]


@strawberry.type
class UpdateAttendeeTicketError:
    field: str
    message: str


UpdateAttendeeTicketResult = Annotated[
    Union[TicketReassigned, AttendeeTicket, UpdateAttendeeTicketErrors],
    strawberry.union(name="UpdateAttendeeTicketResult"),
]


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
        if errors := input.validate():
            return errors

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
    errors = UpdateAttendeeTicketErrors()

    if error := response.get("attendee_name"):
        errors.add_error("name", error[0])

    if error := response.get("attendee_email"):
        errors.add_error("email", error[0])

    if response_answers := response.get("answers"):
        for index, answer in enumerate(input.answers):
            answer_error = response_answers[index]

            if not answer_error:
                continue

            if answer_error := answer_error.get("answer"):
                errors.add_error(f"answers.{index}.answer", answer_error[0])

            if options_error := answer_error.get("options"):
                errors.add_error(
                    f"answers.{index}.{answer.question}",
                    options_error[0],
                )

    return errors
