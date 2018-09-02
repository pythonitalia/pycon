import graphene

from users.schema import UsersQuery


class Query(UsersQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
