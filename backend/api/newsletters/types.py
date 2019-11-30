import strawberry


@strawberry.type
class Subscription:
    id: strawberry.ID
    email: str
