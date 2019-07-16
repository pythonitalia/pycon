from graphene import List
from graphene_form.converter import convert_form_field

from .fields import CartField
from .types import CartItem


@convert_form_field.register(CartField)
def convert_form_field_to_cart_item(field):
    return List(CartItem, required=field.required)
