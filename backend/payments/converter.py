from typing import List

import strawberry
from strawberry_forms.converter import convert_form_field, type_or_optional_wrapped

from .fields import CartField
from .types import CartItem


@convert_form_field.register(CartField)
def convert_form_field_to_cart_item(field):
    return (
        type_or_optional_wrapped(List[CartItem], field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )
