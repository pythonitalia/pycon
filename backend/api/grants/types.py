import strawberry

from grants.models import Grant


@strawberry.type
class Grant:
    id: strawberry.ID

    @classmethod
    def from_model(cls, grant: Grant):
        return cls(id=grant.id)
