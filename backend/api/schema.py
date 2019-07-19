import strawberry
from conferences.schema import ConferenceQuery
from payments.mutations import PaymentsMutations
from submissions.mutations import SubmissionsMutations
from users.mutations import UsersMutations
from users.schema import UsersQuery
from voting.mutations import VotesMutations


@strawberry.type
class Query(UsersQuery, ConferenceQuery):
    pass


@strawberry.type
class Mutation(UsersMutations, PaymentsMutations, SubmissionsMutations, VotesMutations):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
