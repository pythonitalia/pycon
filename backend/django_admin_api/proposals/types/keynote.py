import strawberry


@strawberry.type
class Keynote:
    id: strawberry.ID
    title: str
    name: str

    @classmethod
    def from_model(cls, keynote):
        return cls(
            id=keynote.id,
            title=keynote.title,
            name=keynote.speakers.first().name,
        )
