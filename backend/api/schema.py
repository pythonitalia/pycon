import graphene
from donations.api.schema import DonationsMutations


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'world'


class Mutation(
        DonationsMutations,
        graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
