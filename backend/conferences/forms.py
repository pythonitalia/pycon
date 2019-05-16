from decimal import Decimal

from django import forms
from django.utils.translation import ugettext_lazy as _

from api.forms import ContextAwareForm

from orders.models import Order, OrderItem

from payments.providers import PROVIDERS, get_provider, PROVIDER_STRIPE
from payments.forms import PaymentPayloadField, CartField
from payments.types import PaymentFailed
from payments.exceptions import Stripe3DVerificationException

from .models import TicketFare


class CommonPaymentItemsForm(ContextAwareForm):
    items = CartField()

    def clean(self):
        cleaned_data = super().clean()
        import pdb; pdb.set_trace()

        items = cleaned_data['items']

        total_amount = Decimal(0)

        for index, item in enumerate(items):
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


class BuyTicketForm(CommonPaymentItemsForm):
    provider = forms.ChoiceField(choices=PROVIDERS)
    payload = PaymentPayloadField()

    def save(self):
        user = self.context.user

        provider = self.cleaned_data.get('provider')
        items = self.cleaned_data.get('items')
        total_amount = self.cleaned_data.get('total_amount')
        payload = self.cleaned_data.get('payload')

        import pdb; pdb.set_trace()

        order = Order(
            user=user,
            provider=provider,
            amount=total_amount
        )

        for item in items:
            OrderItem(
                order=order,
                description=item['fare'].name,
                unit_price=item['fare'].price,
                quantity=item['quantity']
            )

        try:
            order.charge(payload)
        except Stripe3DVerificationException as e:
            return PaymentFailed(reason='test')
            # return {
            #     'required_action': True,
            #     'client_secret': e.client_secret
            # }

        import pdb; pdb.set_trace()
        return True
        # return super().save()
