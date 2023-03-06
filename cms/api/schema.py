import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"

    @strawberry.field
    def page(self) -> str:
        breakpoint()
        return "Page"


schema = strawberry.Schema(query=Query)
