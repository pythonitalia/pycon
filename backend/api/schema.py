import strawberry
from strawberry.extensions.tracing.sentry import SentryTracingExtensionSync

from api.users.types import User
from api.participants.mutations import ParticipantMutations

from .blob.schema import BlobMutation
from .blog.schema import BlogQuery
from .checklist.query import ChecklistQuery
from .conferences.schema import ConferenceQuery
from .countries.schema import CountryQuery
from .grants.mutations import GrantMutation
from .job_board.schema import JobBoardQuery
from .newsletters.schema import NewsletterMutations
from .orders.mutations import OrdersMutations
from .orders.query import OrdersQuery
from .pages.schema import PagesQuery
from .pretix.mutations import AttendeeTicketMutation
from .schedule.mutations import ScheduleMutations
from .schedule.schema import ScheduleQuery
from .submissions.mutations import SubmissionsMutations
from .submissions.schema import SubmissionsQuery
from .volunteers_notifications.mutations import VolunteersNotificationsMutation
from .volunteers_notifications.query import VolunteersNotificationsQuery
from .voting.mutations import VotesMutations
from .participants.queries import ParticipantQueries


@strawberry.type
class Query(
    ConferenceQuery,
    BlogQuery,
    SubmissionsQuery,
    PagesQuery,
    CountryQuery,
    OrdersQuery,
    JobBoardQuery,
    ScheduleQuery,
    VolunteersNotificationsQuery,
    ChecklistQuery,
    ParticipantQueries,
):
    pass


@strawberry.type
class Mutation(
    SubmissionsMutations,
    VotesMutations,
    OrdersMutations,
    GrantMutation,
    NewsletterMutations,
    ScheduleMutations,
    AttendeeTicketMutation,
    VolunteersNotificationsMutation,
    BlobMutation,
    ParticipantMutations,
):
    pass


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[User],
    extensions=[SentryTracingExtensionSync],
)
