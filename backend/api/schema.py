import strawberry
from strawberry.extensions.tracing.sentry import SentryTracingExtensionSync

from api.users.types import User

from .blob.schema import BlobMutation
from .blog.schema import BlogQuery
from .checklist.query import ChecklistQuery
from .conferences.schema import ConferenceQuery
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
from .users.schema import CountryQuery
from .volunteers_notifications.mutations import VolunteersNotificationsMutation
from .volunteers_notifications.query import VolunteersNotificationsQuery
from .voting.mutations import VotesMutations


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
):
    pass


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[User],
    extensions=[SentryTracingExtensionSync],
)
