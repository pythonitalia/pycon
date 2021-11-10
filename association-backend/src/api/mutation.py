from strawberry.tools import create_type

from .mutations.manage_user_subscription import manage_user_subscription
from .mutations.subscribe_user_to_association import subscribe_user_to_association

Mutation = create_type(
    "Mutation", [subscribe_user_to_association, manage_user_subscription]
)
