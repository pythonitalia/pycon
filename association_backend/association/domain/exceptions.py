class AlreadySubscribed(Exception):
    """Raised when the system tries to associate a new subscription to an already subscribed user
    It could be raised by subscribeUserToAssociation mutation"""

    pass


class CustomerNotAvailable(Exception):
    """Raised when a user requests to access his customer portal, but the system has not yet associated the session user with the customer.
    The webhook has probably not been called yet or the user has never completed the subscription procedure
    It could be raised by manageUserAssociationSubscription mutation"""

    pass


class SubscriptionNotFound(Exception):
    """Raised when the system cannot find the requested subscription for retrieve/update purpose
    It could be raised by all webhook events"""

    pass


class InconsistentStateTransitionError(Exception):
    """Raised when the system tries to change the status of an already paid (at least once) subscription to `FIRST_PAYMENT_EXPIRED`
    It could be raised by webhook event `customer.subscription.update`"""

    pass


class WebhookSecretMissing(Exception):
    """Raised when the Stripe webhook is called
    but STRIPE_WEBHOOK_SIGNATURE_SECRET has not been set in your .env variables"""

    pass


class MultipleCustomerReturned(Exception):
    """Raised when the System tries to retrieve a Customer from Stripe passing his email
    It's a case that should never happen, and if it happens that a user has two customer profiles and we should investigate.
    Otherwise, we might end up choosing the wrong customer and subscribe the wrong person
    It could be raised by subscribeUserToAssociation mutation"""

    pass
