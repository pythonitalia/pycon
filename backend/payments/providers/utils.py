from decimal import Decimal


def to_cents(amount):
    # I'm a bit scared here that we might call to_cents on a value
    # already in cents causing issues.
    # What can we do to make sure it does not happen?
    if not isinstance(amount, Decimal):
        raise ValueError(
            "Make sure the amount passed to `to_cents` is not already converted"
        )

    return int(amount * 100)
