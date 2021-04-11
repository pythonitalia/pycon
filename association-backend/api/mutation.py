from pythonit_toolkit.api.builder import create_root_type

from .mutations.manage_user_association_subscription import (
    manage_user_association_subscription,
)
from .mutations.subscribe_user_to_association import subscribe_user_to_association

Mutation = create_root_type(
    [subscribe_user_to_association, manage_user_association_subscription]
)
