import strawberry
from api.newsletters.mutations import SubscribeToNewsletter, UnsubscribeToNewsletter


@strawberry.type
class NewsletterMutations:
    subscribe_to_newsletter = SubscribeToNewsletter.Mutation
    unsubscribe_to_newsletter = UnsubscribeToNewsletter.Mutation
