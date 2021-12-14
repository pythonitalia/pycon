import strawberry

from src.association_membership.domain.repository import AssociationMembershipRepository


@strawberry.federation.type(keys=["id"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    is_python_italia_member: bool

    @classmethod
    async def resolve_reference(cls, id: str):
        subscription = await AssociationMembershipRepository().get_user_subscription(
            int(id)
        )
        return cls(
            id=id,
            is_python_italia_member=subscription.is_active if subscription else False,
        )
