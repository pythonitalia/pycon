import strawberry
from strawberry.types import Info

from api.permissions import IsAuthenticated
from api.pretix.types import UpdateAttendeeTicketInput
from api.types import OperationResult
from conferences.models.conference import Conference
from pretix import update_ticket


@strawberry.type
class AttendeeTicketMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_attendee_ticket(
        self, info: Info, conference: str, input: UpdateAttendeeTicketInput
    ) -> OperationResult:
        print("update_attendee_ticket")
        print(input)
        conference = Conference.objects.get(code=conference)

        update_ticket(conference, input)
        return OperationResult(ok=True)
