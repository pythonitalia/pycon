import graphene

from users.schema import UsersQuery
from conferences.schema import ConferenceQuery

from submissions.mutations import SubmissionsMutations
from conferences.mutations import ConferencesMutations


class Query(UsersQuery, ConferenceQuery, graphene.ObjectType):
    pass


class Mutations(SubmissionsMutations, ConferencesMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
