from strawberry.tools import create_type

from association_membership.api.mutations.manage_user_subscription import (
    manage_user_subscription,
)
from association_membership.api.mutations.subscribe_user_to_association import (
    subscribe_user_to_association,
)

AssociationMembershipMutation = create_type(
    "AssociationMembershipMutation",
    [manage_user_subscription, subscribe_user_to_association],
)
