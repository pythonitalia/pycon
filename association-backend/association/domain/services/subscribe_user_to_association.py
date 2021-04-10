import logging
from datetime import datetime

from association.domain.entities.stripe import StripeCheckoutSession
from association.domain.exceptions import (
    AlreadySubscribed,
    MultipleCustomerReturned,
    MultipleCustomerSubscriptionsReturned,
    StripeSubscriptionNotFound,
)
from association_membership.domain.entities import (  # Subscription,; SubscriptionState,
    UserData,
)
from association_membership.domain.repository import AssociationMembershipRepository
from customers.domain.entities import UserID
from customers.domain.repository import CustomersRepository

logger = logging.getLogger(__name__)


async def subscribe_user_to_association(
    user_data: UserData,
    *,
    customers_repository: CustomersRepository,
    association_repository: AssociationMembershipRepository
) -> StripeCheckoutSession:
    # TODO: Check if the user already has a subscription
    user_id = UserID(1)
    customer = await customers_repository.get_for_user_id(user_id)

    if not customer:
        customer = await customers_repository.create_for_user(
            user_id, "marcoaciernoemail@gmail.com"
        )

    checkout_session: StripeCheckoutSession = (
        await association_repository.create_checkout_session(
            customer_id=customer.stripe_customer_id
        )
    )
    return checkout_session
