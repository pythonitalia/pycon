import logging

from django import forms
import requests

from integrations.flodesk import SubscriptionResult, subscribe
from newsletters.models import Subscription
from strawberry_forms.forms import FormWithContext

logger = logging.getLogger(__name__)


class SubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")
        request = self.context.request

        try:
            return subscribe(email, ip=get_ip(request))
        except requests.exceptions.HTTPError as e:
            logger.error(
                "Unable to subscribe the user due to flodesk API error %s %s",
                e,
                e.response.text,
                exc_info=True,
            )
        except Exception as e:
            logger.error(
                "Unable to subscribe the user to flodesk due to an error %s",
                e,
                exc_info=True,
            )

        return SubscriptionResult.UNABLE_TO_SUBSCRIBE


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


def get_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(", ")[0]
    return request.META.get("REMOTE_ADDR")
