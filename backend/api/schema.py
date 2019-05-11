import graphene

from conferences.schema import ConferenceQuery
from submissions.mutations import SubmissionsMutations
from users.schema import UsersQuery


class Query(UsersQuery, ConferenceQuery, graphene.ObjectType):
    pass


class Mutations(SubmissionsMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
