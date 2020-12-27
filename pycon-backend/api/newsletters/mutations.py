from api.newsletters.forms import SubscribeToNewsletterForm, UnsubscribeToNewsletterForm
from api.newsletters.types import NewsletterSubscription
from api.types import OperationResult
from strawberry_forms.mutations import FormMutation


class SubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return NewsletterSubscription(id=result.id, email=result.email)

    class Meta:
        form_class = SubscribeToNewsletterForm
        output_types = (NewsletterSubscription,)


class UnsubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = UnsubscribeToNewsletterForm
        output_types = (OperationResult,)
