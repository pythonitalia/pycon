import strawberry


@strawberry.type
class LanguageType:
    id: strawberry.ID
    code: str
    name: str
