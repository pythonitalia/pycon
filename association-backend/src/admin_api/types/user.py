import strawberry

from src.admin_api.types.subscription import MembershipSubscription
from src.customers.domain import entities
from src.customers.domain.repository import CustomersRepository


@strawberry.federation.type(keys=["id"], extend=True)
class User:
    id: strawberry.ID = strawberry.federation.field(external=True)
    is_python_italia_member: bool

    _customer: strawberry.Private[entities.Customer]

    @strawberry.field
    async def subscriptions(self) -> list[MembershipSubscription]:
        subscriptions = self._customer.subscriptions

        return [MembershipSubscription.from_domain(entity) for entity in subscriptions]

    @classmethod
    async def resolve_reference(cls, id: str):
        customer = await CustomersRepository().get_for_user_id(int(id))
        return cls(
            id=id,
            _customer=customer,
            is_python_italia_member=(
                customer.has_active_subscription() if customer else False
            ),
        )
