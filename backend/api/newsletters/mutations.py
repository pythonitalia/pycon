import strawberry

from api.newsletters.forms import SubscribeToNewsletterForm, UnsubscribeToNewsletterForm
from api.types import OperationResult
from integrations.mailchimp import SubscriptionResult as MailchimpSubscriptionResult
from strawberry_forms.mutations import FormMutation

NewsletterMembershipStatus = strawberry.enum(
    MailchimpSubscriptionResult, name="NewsletterSubscriptionResult"
)


@strawberry.type
class NewsletterSubscribeResult:
    status: NewsletterMembershipStatus


class SubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return NewsletterSubscribeResult(status=NewsletterMembershipStatus(result))

    class Meta:
        form_class = SubscribeToNewsletterForm
        output_types = (NewsletterSubscribeResult,)


class UnsubscribeToNewsletter(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = UnsubscribeToNewsletterForm
        output_types = (OperationResult,)
