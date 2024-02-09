import strawberry


@strawberry.type
class Room:
    id: strawberry.ID
    name: str

    @classmethod
    def from_model(cls, room):
        return cls(id=room.id, name=room.name)
