def handle_checkout_session_completed(event):
    # TODO: Create Subscription object
    pass


def handle_invoice_paid(event):
    # Called when the user pays for the subscription
    pass


def handle_invoice_payment_failed(event):
    # Called when the user subscription fails to renew
    pass


HANDLERS = {
    "checkout.session.completed": handle_checkout_session_completed,
    "invoice.paid": handle_invoice_paid,
    "invoice.payment_failed": handle_invoice_payment_failed,
}
