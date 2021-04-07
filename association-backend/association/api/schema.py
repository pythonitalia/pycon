import strawberry

from association.api.mutation import Mutation


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello"


schema = strawberry.Schema(query=Query, mutation=Mutation)
