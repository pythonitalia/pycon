from api.newsletters.mutations import SubscribeToNewsletter, UnsubscribeToNewsletter


class NewsletterMutations:
    subscribe_to_newsletter = SubscribeToNewsletter.Mutation
    unsubscribe_to_newsletter = UnsubscribeToNewsletter.Mutation
