import graphene

from django import forms

from decimal import Decimal

from django import forms
from django.utils.translation import ugettext_lazy as _

from graphene_form.forms import FormWithContext

from conferences.models import TicketFare, Conference
from orders.models import Order, OrderItem

from .providers.stripe.types import Stripe3DValidationRequired
from .providers.stripe.exceptions import Stripe3DVerificationException

from .exceptions import PaymentFailed
from .fields import CartField
from .types import GenericPaymentFailedError


class CommonPaymentItemsForm(FormWithContext):
    items = CartField()
    conference = forms.ModelChoiceField(
        Conference.objects.all(),
        to_field_name='code',
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        conference = cleaned_data.get('conference', None)

        if not conference:
            return

        items = cleaned_data['items']

        total_amount = Decimal(0)

        for item in items:
            item_id = item['id']

            try:
                fare = conference.ticket_fares.get(id=item_id)
            except TicketFare.DoesNotExist:
                raise forms.ValidationError({
                    'items': _('Ticket %(id)s does not exist') % {'id': item_id}
                })

            if not fare.is_available:
                raise forms.ValidationError({
                    'items': _('Ticket #%(id)s is not available anymore') % {'id': item_id}
                })

            item['fare'] = fare
            total_amount = total_amount + fare.price

        cleaned_data['items'] = items
        cleaned_data['total_amount'] = total_amount

        return cleaned_data

    def create_order(self):
        user = self.context.user

        items = self.cleaned_data.get('items')
        total_amount = self.cleaned_data.get('total_amount')

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

        return order


class BuyTicketWithStripeForm(CommonPaymentItemsForm):
    payment_method_id = forms.CharField(required=False)
    payment_intent_id = forms.CharField(required=False)

    def save(self):
        order = self.create_order()

        payload = {
            'payment_method_id': self.cleaned_data.get('payment_method_id', None),
            'payment_intent_id': self.cleaned_data.get('payment_intent_id', None),
        }

        try:
            order.charge(payload)
        except Stripe3DVerificationException as e:
            return Stripe3DValidationRequired(client_secret=e.client_secret)
        except PaymentFailed as e:
            return GenericPaymentFailedError(message=e.message)

        # payment completed with success
        order.save()
        # register ticket?
        return True
