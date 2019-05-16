from graphene import List
from graphene_django.forms.converter import convert_form_field

from .forms import PaymentPayloadField, CartField
from .types import PaymentPayload, CartItem


@convert_form_field.register(PaymentPayloadField)
def convert_form_field_to_payment_payload(field):
    return PaymentPayload(required=field.required)


@convert_form_field.register(CartField)
def convert_form_field_to_cart_item(field):
    return List(CartItem, required=field.required)
