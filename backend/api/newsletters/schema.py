from strawberry.tools import create_type
from .mutations import subscribe_to_newsletter, unsubscribe_to_newsletter


NewsletterMutations = create_type(
    "NewsletterMutations",
    (
        subscribe_to_newsletter,
        unsubscribe_to_newsletter,
    ),
)
