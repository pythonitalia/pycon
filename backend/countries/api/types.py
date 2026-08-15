import strawberry


@strawberry.type
class Country:
    code: str
    name: str
