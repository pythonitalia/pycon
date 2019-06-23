import graphene

from conferences.schema import ConferenceQuery
from payments.mutations import PaymentsMutations
from submissions.mutations import SubmissionsMutations
from users.schema import UsersQuery
from voting.mutations import VotesMutations


class Query(UsersQuery, ConferenceQuery, graphene.ObjectType):
    pass


class Mutations(SubmissionsMutations, PaymentsMutations, VotesMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
