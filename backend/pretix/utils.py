ORDER_STATUS_TO_TEXT = {"n": "Pending", "p": "Paid", "e": "Expired", "c": "Canceled"}


def order_status_to_text(status):
    return ORDER_STATUS_TO_TEXT[status]
