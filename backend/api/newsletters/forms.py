from django import forms
from newsletters.models import Subscription
from strawberry_forms.forms import FormWithContext
from integrations.mailchimp import subscribe


class SussbscribeToNewsletterForm(FormWithContext):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data.get("email")

        return subscribe(email)


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
