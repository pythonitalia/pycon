from typing import NewType

import ormar

from src.database.db import BaseMeta

UserID = NewType("UserID", int)


class Customer(ormar.Model):
    class Meta(BaseMeta):
        tablename = "customers"

    id: int = ormar.Integer(primary_key=True)
    user_id: UserID = ormar.Integer(unique=True)
    stripe_customer_id: str = ormar.String(max_length=256, unique=True)

    def has_active_subscription(self) -> bool:
        return any([subscription.is_active for subscription in self.subscriptions])
