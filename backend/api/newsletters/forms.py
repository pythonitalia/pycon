from django import forms

from newsletters.models import Subscription
from strawberry_forms.forms import FormWithContext


class SubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")
        subscription = Subscription.objects.get_or_create(email=email)[0]
        return subscription


class UnsubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")
        try:
            subscription = Subscription.objects.get(email=email)
        except Subscription.DoesNotExist:
            return True

        deleted, _ = subscription.delete()
        return deleted == 1
