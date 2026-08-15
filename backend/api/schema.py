import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from participants.api.mutations import ParticipantMutations
from users.api.mutations import UsersMutations
from files_upload.api.schema import FilesUploadMutation
from checklist.api.query import ChecklistQuery
from conferences.api.schema import ConferenceQuery
from countries.api.schema import CountryQuery
from grants.api.mutations import GrantMutation
from job_board.api.schema import JobBoardQuery
from newsletters.api.schema import NewsletterMutations
from .orders.mutations import OrdersMutations
from .orders.query import OrdersQuery
from pages.api.schema import PagesQuery
from pretix.api.mutations import AttendeeTicketMutation
from schedule.api.schema import ScheduleQuery, ScheduleMutations
from submissions.api.mutations import SubmissionsMutations
from submissions.api.schema import SubmissionsQuery
from volunteers_notifications.api.mutations import VolunteersNotificationsMutation
from volunteers_notifications.api.query import VolunteersNotificationsQuery
from voting.api.mutations import VotesMutations
from badge_scanner.api.schema import BadgeScannerQuery, BadgeScannerMutation
from participants.api.queries import ParticipantQueries
from users.api.queries import UserQuery
from association_membership.api.mutation import AssociationMembershipMutation
from cms.api.schema import CMSQuery
from sponsors.api.schema import SponsorsMutation
from visa.api.query import VisaQuery
from visa.api.mutation import VisaMutation


@strawberry.type
class Query(
    ConferenceQuery,
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


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DjangoOptimizerExtension],
)
