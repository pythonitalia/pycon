class WebhookError(Exception):
    """Base class for all known webhook errors"""


class NoCustomerFoundForEvent(WebhookError):
    """Raised when receiving an event for a customer that doesn't exist on our system"""


class NoSubscriptionFoundForEvent(WebhookError):
    """Raised when receiving a subscription event, but the subscription
    doesn't exist on our system"""


class NoUserFoundWithEmail(WebhookError):
    """Raised when no user matches the email"""
