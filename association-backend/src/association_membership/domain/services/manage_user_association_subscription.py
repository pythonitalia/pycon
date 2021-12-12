import logging

from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo

from src.association_membership.domain.entities import Subscription
from src.association_membership.domain.exceptions import (
    CustomerNotAvailable,
    NoSubscriptionAvailable,
)

# from src.customers.domain.repository import CustomersRepository

logger = logging.getLogger(__name__)


async def manage_user_association_subscription(
    user: PastaportoUserInfo,
    *,
    customers_repository,
) -> Subscription:
    """This service creates a CustomerPortalSession and returns its url"""
    # customer = await customers_repository.get_for_user_id(user.id)

    # if not customer:
    #     raise CustomerNotAvailable()

    # if not customer.has_active_subscription():
    #     raise NoSubscriptionAvailable()

    # billing_portal_url = await customers_repository.create_stripe_portal_session_url(
    #     customer
    # )
    # return billing_portal_url
