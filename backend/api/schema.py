import graphene


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, args, context, info):
        return 'world'


schema = graphene.Schema(query=Query)
