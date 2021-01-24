import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def me(self) -> int:
        return 5


# @strawberry.type
# class Mutation:
#     pass


schema = strawberry.federation.Schema(Query)
