from decimal import Decimal

from conferences.models import Conference, TicketFare
from django import forms
from django.utils.translation import ugettext_lazy as _
from orders.models import Order, OrderItem
from payments.errors import PaymentError
from strawberry_forms.forms import FormWithContext

from .fields import CartField
from .types import GenericPaymentError, StripeClientSecret


class CommonPaymentItemsForm(FormWithContext):
    items = CartField()
    conference = forms.ModelChoiceField(
        Conference.objects.all(), to_field_name="code", required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        conference = cleaned_data.get("conference")
        items = cleaned_data.get("items", [])

        if not items:
            raise forms.ValidationError({"items": _("The cart is empty")})

        total_amount = Decimal(0)

        for item in items:
            item_id = item["id"]

            try:
                fare = conference.ticket_fares.get(id=item_id)
            except TicketFare.DoesNotExist:
                raise forms.ValidationError(
                    {"items": _("Ticket %(id)s does not exist") % {"id": item_id}}
                )

            if not fare.is_available:
                raise forms.ValidationError(
                    {
                        "items": _("Ticket %(id)s is not available anymore")
                        % {"id": item_id}
                    }
                )

            item["fare"] = fare
            total_amount = total_amount + fare.price * item["quantity"]

        cleaned_data["items"] = items
        cleaned_data["total_amount"] = total_amount

        return cleaned_data

    def create_order(self, provider):
        user = self.context["request"].user

        total_amount = self.cleaned_data.get("total_amount")
        items = self.cleaned_data.get("items", [])

        order = Order.objects.create(user=user, provider=provider, amount=total_amount)

        for item in items:
            OrderItem.objects.create(
                order=order,
                description=item["fare"].order_description,
                unit_price=item["fare"].price,
                quantity=item["quantity"],
                item_object=item["fare"],
            )

        return order


class BuyTicketWithStripeForm(CommonPaymentItemsForm):
    def save(self):
        order = self.create_order("stripe")

        try:
            response = order.charge()
        except PaymentError as e:
            return GenericPaymentError(message=e.message)
        finally:
            order.save()

        return StripeClientSecret(client_secret=response.extras["client_secret"])
