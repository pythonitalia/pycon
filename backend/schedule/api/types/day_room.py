import strawberry


@strawberry.type
class DayRoom:
    id: strawberry.ID
    name: str
    type: str
    streaming_url: str
    slido_url: str
