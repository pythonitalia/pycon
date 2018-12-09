import graphene

from users.schema import UsersQuery
from conferences.schema import ConferenceQuery


class Query(UsersQuery, ConferenceQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
