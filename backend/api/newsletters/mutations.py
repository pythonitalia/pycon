from api.newsletters.forms import SubscribeToNewsletterForm, UnsubscribeToNewsletterForm
from api.newsletters.types import Subscription
from api.types import OperationResult
from strawberry_forms.mutations import FormMutation


class SubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return Subscription(id=result.id, email=result.email)

    class Meta:
        form_class = SubscribeToNewsletterForm
        output_types = (Subscription,)


class UnsubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = UnsubscribeToNewsletterForm
        output_types = (OperationResult,)
