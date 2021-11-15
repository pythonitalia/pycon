from api.newsletters.forms import (
    SussbscribeToNewsletterForm,
    UnsubscribeToNewsletterForm,
)
from api.types import OperationResult
from strawberry_forms.mutations import FormMutation


class SubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = SussbscribeToNewsletterForm
        output_types = (OperationResult,)


class UnsubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = UnsubscribeToNewsletterForm
        output_types = (OperationResult,)
