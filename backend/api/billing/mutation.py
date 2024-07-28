from strawberry.tools import create_type

from api.billing.mutations.update_billing_address import update_billing_address

BillingMutation = create_type(
    "BillingMutation",
    [update_billing_address],
)
