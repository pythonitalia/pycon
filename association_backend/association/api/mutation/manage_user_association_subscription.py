import strawberry
from association.api.context import Info
from association.domain import services
from association.domain.entities.subscription_entities import UserData
from association.domain.exceptions import CustomerNotAvailable

# ===========
# Input
# ==========

# ===========
# Validation Errors
# ==========
@strawberry.type
class CustomerNotAvailableError:
    message: str = "Customer not available"


@strawberry.type
class CustomerPortalResponse:
    billing_portal_url: str


# ==========
# Output
# =========
CustomerPortalResult = strawberry.union(
    "CustomerPortalResult", (CustomerPortalResponse, CustomerNotAvailableError)
)


# ===========
# Mutation
# ==========
@strawberry.mutation
async def manage_user_association_subscription(info: Info) -> CustomerPortalResponse:
    # TODO ger UserData from authenticated User
    user_data = UserData(email="fake.user@pycon.it", user_id=12345)

    try:
        billing_portal_url = await services.manage_user_association_subscription(
            user_data, association_repository=info.context.association_repository
        )
        return CustomerPortalResponse(billing_portal_url=billing_portal_url)
    except CustomerNotAvailable:
        return CustomerNotAvailableError()
