import graphene

from django import forms

from decimal import Decimal

from django import forms
from django.utils.translation import ugettext_lazy as _

from graphene_form.forms import FormWithContext

from conferences.models import TicketFare
from orders.models import Order, OrderItem

from .fields import CartField
from .types import Stripe3DValidationRequired
from .exceptions import Stripe3DVerificationException


class CommonPaymentItemsForm(FormWithContext):
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


class BuyTicketWithStripeForm(CommonPaymentItemsForm):
    payment_method_id = forms.CharField(required=False)
    payment_intent_id = forms.CharField(required=False)

    def save(self):
        user = self.context.user

        items = self.cleaned_data.get('items')
        total_amount = self.cleaned_data.get('total_amount')

        import pdb; pdb.set_trace()

        order = Order(
            user=user,
            provider='stripe',
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
            order.charge(self.cleaned_data)
        except Stripe3DVerificationException as e:
            return Stripe3DValidationRequired(client_secret=e.client_secret)

        import pdb; pdb.set_trace()
        return True
