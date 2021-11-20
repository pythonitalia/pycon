import logging

from django import forms

from integrations.mailchimp import subscribe
from newsletters.models import Subscription
from strawberry_forms.forms import FormWithContext

logger = logging.getLogger(__name__)


class SubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")

        try:
            return subscribe(email)
        except Exception as e:
            logger.error(
                "Unable to subscribe the user to mailchimp due to an error %s",
                e,
                exc_info=True,
            )
            return False


class UnsubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")

        try:
            Subscription.objects.get(email=email).delete()
        except Subscription.DoesNotExist:
            # We already do not know anything about the user
            # e.g maybe they are refreshing the page after
            # the unsubscribe
            # so let's just say yes for now
            pass

        return True
