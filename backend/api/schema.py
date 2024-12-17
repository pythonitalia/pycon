import strawberry

from api.participants.mutations import ParticipantMutations
from .users.mutations import UsersMutations
from .files_upload.schema import FilesUploadMutation
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
from .schedule.schema import ScheduleQuery, ScheduleMutations
from .submissions.mutations import SubmissionsMutations
from .submissions.schema import SubmissionsQuery
from .volunteers_notifications.mutations import VolunteersNotificationsMutation
from .volunteers_notifications.query import VolunteersNotificationsQuery
from .voting.mutations import VotesMutations
from .badge_scanner.schema import BadgeScannerQuery, BadgeScannerMutation
from .participants.queries import ParticipantQueries
from .users.queries import UserQuery
from .association_membership.mutation import AssociationMembershipMutation
from .cms.schema import CMSQuery
from .sponsors.schema import SponsorsMutation
from .visa.queries import VisaQuery
from .visa.mutations import VisaMutation


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
    BadgeScannerQuery,
    UserQuery,
    CMSQuery,
    VisaQuery,
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
    FilesUploadMutation,
    BadgeScannerMutation,
    ParticipantMutations,
    UsersMutations,
    AssociationMembershipMutation,
    SponsorsMutation,
    VisaMutation,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
