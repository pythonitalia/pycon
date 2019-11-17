import strawberry

from .blog.schema import BlogQuery
from .conferences.schema import ConferenceQuery
from .pages.schema import PagesQuery
from .payments.mutations import PaymentsMutations
from .submissions.mutations import SubmissionsMutations
from .submissions.schema import SubmissionsQuery
from .tickets.mutations import TicketsMutations
from .users.mutations import UsersMutations
from .users.schema import UsersQuery
from .voting.mutations import VotesMutations


@strawberry.type
class Query(UsersQuery, ConferenceQuery, BlogQuery, SubmissionsQuery, PagesQuery):
    pass


@strawberry.type
class Mutation(
    UsersMutations,
    PaymentsMutations,
    SubmissionsMutations,
    VotesMutations,
    TicketsMutations,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
