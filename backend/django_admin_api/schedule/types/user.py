import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    fullname: str

    @classmethod
    def from_model(cls, user):
        return cls(id=user.id, fullname=user.fullname)
