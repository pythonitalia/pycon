import strawberry


@strawberry.type
class Country:
    id: strawberry.ID
    code: str
    name: str
