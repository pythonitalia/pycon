import strawberry
import stripe

from association.settings import SUBSCRIPTION_PRICE_ID


@strawberry.type
class CreateSubscriptionSuccess:
    checkout_session_id: str


CreateSubscriptionSessionResult = strawberry.union(
    "CreateSubscriptionSessionResult", (CreateSubscriptionSuccess,)
)


@strawberry.mutation
def create_subscription_session() -> CreateSubscriptionSessionResult:
    # TODO: Update URLs to use real url
    checkout_session = stripe.checkout.Session.create(
        success_url="https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://example.com/canceled.html",
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": SUBSCRIPTION_PRICE_ID, "quantity": 1}],
    )
    return CreateSubscriptionSuccess(checkout_session_id=checkout_session["id"])
