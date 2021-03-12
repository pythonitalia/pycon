import pydantic


class StripeCheckoutSessionNotCreated(Exception):
    pass


class StripeCustomerSearchError(Exception):
    pass


class SubscriptionNotFound(Exception):
    pass


class SubscriptionNotUpdated(Exception):
    pass


class AlreadySubscribed(Exception):
    pass


class CustomerNotAvailable(Exception):
    pass


class InvalidCustomer(pydantic.ValidationError):
    pass


class InvalidCheckoutSession(pydantic.ValidationError):
    pass
