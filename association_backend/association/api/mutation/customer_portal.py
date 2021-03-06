import pydantic
import strawberry
from association.api.context import Info
from association.domain import services
from association.domain.exceptions import CustomerNotAvailable


# ===========
# Input
# ==========
class UserData(pydantic.BaseModel):
    email: str
    user_id: int


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
async def customer_portal(info: Info) -> CustomerPortalResponse:
    # TODO ger UserData from authenticated User
    user_data = UserData(email="fake.user@pycon.it", user_id=12345)

    try:
        billing_portal_url = await services.customer_portal(
            user_data, association_repository=info.context.association_repository
        )
        return CustomerPortalResponse(billing_portal_url=billing_portal_url)
    except CustomerNotAvailable:
        return CustomerNotAvailableError()
