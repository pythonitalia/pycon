from enum import IntEnum


class PaymentState(IntEnum):
    NEW = 1
    PROCESSING = 2
    COMPLETE = 3
    FAILED = -1

    @classmethod
    def choices(cls):
        return tuple((s.value, "{}".format(PaymentState(s.value).name)) for s in cls)
