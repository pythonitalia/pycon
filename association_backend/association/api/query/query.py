import strawberry

from association.api.context import Info
from association.domain.entities import SubscriptionState
from association.settings import TEST_USER_ID


@strawberry.type
class HasAssociationSubscriptionResponse:
    has_association_subscription: bool


@strawberry.type
class Query:
    @strawberry.field()  # permission_classes=[IsJWTAvailable])
    async def has_association_subscription(
        self, info: Info
    ) -> HasAssociationSubscriptionResponse:
        user_id = TEST_USER_ID
        subscription = (
            await info.context.association_repository.get_subscription_by_user_id(
                user_id
            )
        )
        if subscription and subscription.state in [
            SubscriptionState.ACTIVE,
            SubscriptionState.EXPIRED,
        ]:
            has_association_subscription = True
        else:
            has_association_subscription = False
        return HasAssociationSubscriptionResponse(
            has_association_subscription=has_association_subscription
        )
