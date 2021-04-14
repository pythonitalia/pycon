import logging

from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo

from association_membership.domain.entities import Subscription
from association_membership.domain.exceptions import CustomerNotAvailable
from customers.domain.repository import CustomersRepository

logger = logging.getLogger(__name__)


async def manage_user_association_subscription(
    user: PastaportoUserInfo,
    *,
    customers_repository: CustomersRepository,
) -> Subscription:
    """This service creates a CustomerPortalSession and returns its url"""
    customer = await customers_repository.get_for_user_id(user.id)

    if not customer.has_active_subscription():
        # TODO: subscription
        raise ValueError("No subscription")

    if not customer:
        raise CustomerNotAvailable()

    billing_portal_url = await customers_repository.create_stripe_portal_session_url(
        customer
    )
    return billing_portal_url
