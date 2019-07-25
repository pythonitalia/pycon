import strawberry


@strawberry.type
class Language:
    id: strawberry.ID
    code: str
    name: str
