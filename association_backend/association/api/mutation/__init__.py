from ..builder import create_mutation_type
from .manage_user_association_subscription import manage_user_association_subscription
from .subscribe_user_to_association import subscribe_user_to_association

Mutation = create_mutation_type(
    "Mutation", [subscribe_user_to_association, manage_user_association_subscription]
)
