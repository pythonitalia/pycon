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


class StripeSubscriptionNotFound(Exception):
    """Raised when the System cannot find the requested subscription on Stripe
    It could be raised by subscribeUserToAssociation mutation"""

    pass


class InconsistentStateTransitionError(Exception):
    """Raised when the system tries to change the status of an active or already paid (at least once) subscription to `INCOMPLETE_EXPIRED`
    It could be raised by webhook event `customer.subscription.update`"""

    pass


class WebhookSecretMissing(Exception):
    """Raised when the Stripe webhook is called
    but STRIPE_WEBHOOK_SIGNATURE_SECRET has not been set in your .env variables"""

    pass


class MultipleCustomerReturned(Exception):
    """Raised when the System tries to retrieve a Customer from Stripe passing his email
    It's a case that should never happen, and if a user has two customers we should investigate on it.
    Otherwise, we might end up choosing the wrong customer and subscribe the wrong person
    It could be raised by subscribeUserToAssociation mutation"""

    pass


class MultipleCustomerSubscriptionsReturned(Exception):
    """Raised when the System tries to retrieve a Subsciption from Stripe passing his customer (customer_id)
    It's a case that should never happen, and if a customer has two subscriptions we should investigate on it.
    Otherwise, we might end up choosing the wrong subscription and update the wrong one
    It could be raised by subscribeUserToAssociation mutation"""

    pass
