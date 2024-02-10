import strawberry


@strawberry.type
class Room:
    id: strawberry.ID
    name: str
    type: str
