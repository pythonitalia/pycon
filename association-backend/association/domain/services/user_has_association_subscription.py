# import logging

# from association.domain.entities.subscriptions import SubscriptionState
# from association.domain.repositories import AssociationRepository

# logger = logging.getLogger(__name__)


# async def user_has_association_subscription(
#     user_id: int, association_repository: AssociationRepository
# ) -> bool:
#     """This service indicates if the user in session doesn't need
#     to create a checkout session in order to manage his Subscription"""
#     subscription = await association_repository.get_subscription_by_user_id(user_id)
#     if subscription and subscription.state in [
#         SubscriptionState.ACTIVE,
#         SubscriptionState.EXPIRED,
#     ]:
#         return True
#     else:
#         return False
