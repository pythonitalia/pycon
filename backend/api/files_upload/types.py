import strawberry


@strawberry.type
class File:
    id: strawberry.ID
    url: str
    virus: bool | None

    @classmethod
    def from_model(cls, model):
        return cls(
            id=str(model.id),
            url=model.url,
            virus=model.virus,
        )
