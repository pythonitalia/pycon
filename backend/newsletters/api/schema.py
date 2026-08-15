from strawberry.tools import create_type
from .mutations.subscribe_to_newsletter import subscribe_to_newsletter


NewsletterMutations = create_type(
    "NewsletterMutations",
    [
        subscribe_to_newsletter,
    ],
)
