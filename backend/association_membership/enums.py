from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def as_choices(cls):
        return [(e.value, e.name) for e in list(cls)]


class MembershipStatus(str, ChoiceEnum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)


class PaymentStatus(str, ChoiceEnum):
    PAID = "paid"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)
