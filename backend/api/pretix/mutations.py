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
    attendee_email: Optional[str]


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
            data = e.response.json()
            return convert_pretix_errors_to_graphql(data, input)

        # TODO: filter by orderposition in the Pretix API
        tickets = get_user_tickets(
            conference, info.context.request.user.email, language=language
        )

        ticket = next(filter(lambda ticket: str(ticket.id) == input.id, tickets), None)
        if ticket:
            return ticket

        # If the user has changed the email, the ticket will not be returned but
        # the mutation succeeded.
        return TicketReassigned(id=input.id, attendee_email=input.attendee_email)


def convert_pretix_errors_to_graphql(
    response, input: UpdateAttendeeTicketInput
) -> UpdateAttendeeTicketErrors:
    errors = UpdateAttendeeTicketErrors()

    if error := response.get("attendee_email"):
        errors.add_error("attendee_email", error[0])

    answers_errors_keys = ["options", "answer", "non_field_errors"]
    if response_answers := response.get("answers"):
        for index in range(len(input.answers)):
            answer_errors = response_answers[index]

            for key in answers_errors_keys:
                if error := answer_errors.get(key):
                    errors.add_error(f"answers.{index}.{key}", error[0])

    return errors
