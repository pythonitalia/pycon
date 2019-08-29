import strawberry
from blog.schema import BlogQuery
from conferences.schema import ConferenceQuery
from pages.schema import PagesQuery
from payments.mutations import PaymentsMutations
from sponsors.schema import SponsorsQuery
from submissions.mutations import SubmissionsMutations
from users.mutations import UsersMutations
from users.schema import UsersQuery
from voting.mutations import VotesMutations


@strawberry.type
class Query(UsersQuery, ConferenceQuery, BlogQuery, PagesQuery, SponsorsQuery):
    pass


@strawberry.type
class Mutation(UsersMutations, PaymentsMutations, SubmissionsMutations, VotesMutations):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
