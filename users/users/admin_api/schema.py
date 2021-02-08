import strawberry

from users.admin_api.mutation import Mutation


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "hello"


schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
