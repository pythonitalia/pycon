import logging

from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo

from association_membership.domain.exceptions import AlreadySubscribed
from association_membership.domain.repository import AssociationMembershipRepository
from customers.domain.entities import UserID
from customers.domain.repository import CustomersRepository

logger = logging.getLogger(__name__)


async def subscribe_user_to_association(
    user: PastaportoUserInfo,
    *,
    customers_repository: CustomersRepository,
    association_repository: AssociationMembershipRepository
) -> str:
    user_id = UserID(user.id)
    customer = await customers_repository.get_for_user_id(user_id)

    if not customer:
        customer = await customers_repository.create_for_user(user_id, user.email)

    if customer.has_active_subscription():
        raise AlreadySubscribed()

    checkout_session_id = await association_repository.create_checkout_session(
        customer_id=customer.stripe_customer_id
    )
    return checkout_session_id
