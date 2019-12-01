from pretix import get_items as _get_items
from pretix import get_user_orders as _get_user_orders

from .types import PretixOrder


def get_user_orders(conference, email):
    orders = _get_user_orders(conference, email)

    if orders["count"] == 0:
        return []

    items = _get_items(conference)
    return [PretixOrder(order, all_items=items) for order in orders["results"]]
