import strawberry


@strawberry.type
class NewsletterSubscription:
    id: strawberry.ID
    email: str
