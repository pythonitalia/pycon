import json

from decimal import Decimal

from django import forms
from django.utils.translation import ugettext_lazy as _

from api.forms import ContextAwareForm

from orders.models import Order, OrderItem
from orders.providers import PROVIDERS, get_provider, PROVIDER_STRIPE

from .models import TicketFare


class CommonPaymentItemsForm(ContextAwareForm):
    items = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()

        value = cleaned_data['items']
        items = json.loads(value)

        total_amount = Decimal(0)

        for index, item in enumerate(items):
            if 'id' not in item or 'quantity' not in item:
                raise forms.ValidationError(
                    _('Item #%(index)s does not follow the Item spec') % {'index': index}
                )

            item_id = item['id']
            # TODO: Add conference check

            try:
                fare = TicketFare.objects.get(id=item_id)
            except TicketFare.DoesNotExist:
                raise forms.ValidationError(
                    _('Row #%(index)s, item with id %(id)s does not exist') % {'index': index, 'id': item_id}
                )

            item['fare'] = fare
            total_amount = total_amount + fare.price

        cleaned_data['items'] = items
        cleaned_data['total_amount'] = total_amount

        return cleaned_data


class CreateStripeIntentForm(CommonPaymentItemsForm):
    payment_method_id = forms.CharField()

    def save(self):
        payment_method_id = self.cleaned_data.get('payment_method_id')
        total_amount = self.cleaned_data.get('total_amount')

        stripe_cls = get_provider(PROVIDER_STRIPE)
        stripe = stripe_cls()

        # We "force" the creation of an intent that
        # does not "confirm" so the user is forced to
        # run two requests. Technically we could create the
        # intent as soon as the user starts selecting something in the
        # buy ticket screen
        # and then expose another mutation to update the total if needed

        intent = stripe.create_intent(
            payment_method_id=payment_method_id,
            amount=total_amount
        )

        return {'payment_intent_id': intent.id}


class BuyTicketForm(CommonPaymentItemsForm):
    provider = forms.ChoiceField(choices=PROVIDERS)
    token = forms.CharField()

    def save(self):
        user = self.context.user

        provider = self.cleaned_data.get('provider')
        items = self.cleaned_data.get('items')
        total_amount = self.cleaned_data.get('total_amount')
        token = self.cleaned_data.get('token')

        order = Order.objects.create(
            user=user,
            provider=provider,
            amount=total_amount
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                description=item['fare'].name,
                unit_price=item['fare'].price,
                quantity=item['quantity']
            )

        order.charge(token)
        import pdb; pdb.set_trace()
        return True
        # return super().save()
