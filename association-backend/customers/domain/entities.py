from typing import NewType

import ormar

from database.db import BaseMeta

UserID = NewType("UserID", int)


class Customer(ormar.Model):
    class Meta(BaseMeta):
        tablename = "customers"

    id: int = ormar.Integer(primary_key=True)
    user_id: UserID = ormar.Integer(unique=True)
    stripe_customer_id: str = ormar.String(max_length=256, unique=True)
