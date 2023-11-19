class WebhookError(Exception):
    """Base class for all known webhook errors"""


class NoCustomerFoundForEvent(WebhookError):
    """Raised when receiving an event for a customer that doesn't exist on our system"""


class NoSubscriptionFoundForEvent(WebhookError):
    """Raised when receiving a subscription event, but the subscription
    doesn't exist on our system"""


class NoUserFoundWithEmail(WebhookError):
    """Raised when no user matches the email"""


class NoConfirmedPaymentFound(WebhookError):
    """Raised when the pretix order doesn't contain a confirmed payment"""


class NotEnoughPaid(WebhookError):
    """Raised when the pretix order doesn't have enough payments
    to cover the whole position amount"""


class UserIsAlreadyAMember(WebhookError):
    """Raised when the user already has a membership"""


class UnsupportedMultipleMembershipInOneOrder(WebhookError):
    """Raised when we receive an order that contains multiple
    membership orders. This isn't supported"""
