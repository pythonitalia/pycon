import strawberry


@strawberry.type
class File:
    id: strawberry.ID
    url: str
    virus: bool | None
