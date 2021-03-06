import pydantic


class StripeCheckoutSessionNotCreated(Exception):
    pass


class StripeCustomerSearchError(Exception):
    pass


class SubscriptionNotCreated(Exception):
    pass


class SubscriptionNotFound(Exception):
    pass


class SubscriptionNotUpdated(Exception):
    pass


class AlreadySubscribed(Exception):
    def __init__(self, *args, **kwargs):
        self.expiration_date = kwargs.pop("expiration_date")
        super().__init__(*args, **kwargs)


class CustomerNotAvailable(Exception):
    pass


class InvalidCustomer(pydantic.ValidationError):
    pass


class InvalidCheckoutSession(pydantic.ValidationError):
    pass
