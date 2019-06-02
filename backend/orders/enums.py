from enum import Enum


class PaymentState(Enum):
    FAILED = 0
    COMPLETED = 1
    MANUAL = 2
