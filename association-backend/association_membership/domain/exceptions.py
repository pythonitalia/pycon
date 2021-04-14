class AlreadySubscribed(Exception):
    """Raised when the system tries to associate a new subscription to an already subscribed user
    It could be raised by subscribeUserToAssociation mutation"""

    pass


class CustomerNotAvailable(Exception):
    """Raised when a user requests to access his customer portal, but the system has not yet associated the session user with the customer.
    The webhook has probably not been called yet or the user has never completed the subscription procedure
    It could be raised by manageUserAssociationSubscription mutation"""

    pass
