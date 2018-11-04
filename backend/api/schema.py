import graphene

from users.schema import UsersQuery
from conferences.schema import ConferenceQuery

from talks.mutations import TalksMutations


class Query(UsersQuery, ConferenceQuery, graphene.ObjectType):
    pass


class Mutations(TalksMutations):
    pass


schema = graphene.Schema(query=Query, mutation=TalksMutations)
