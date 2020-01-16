from django import forms
from newsletters.models import Subscription
from strawberry_forms.forms import FormWithContext


class SubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")
        subscription, _ = Subscription.objects.get_or_create(email=email)

        return subscription


class UnsubscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")

        Subscription.objects.get(email=email).delete()

        return True
