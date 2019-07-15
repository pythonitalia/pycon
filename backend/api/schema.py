import graphene

from users.schema import UsersQuery
from conferences.schema import ConferenceQuery

from submissions.mutations import SubmissionsMutations
from payments.mutations import PaymentsMutations


class Query(UsersQuery, ConferenceQuery, graphene.ObjectType):
    pass


class Mutations(SubmissionsMutations, PaymentsMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
