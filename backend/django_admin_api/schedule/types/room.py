import strawberry


@strawberry.type
class Room:
    id: strawberry.ID
    name: str
    type: str

    @classmethod
    def from_model(cls, room):
        return cls(id=room.id, name=room.name, type=room.type)
