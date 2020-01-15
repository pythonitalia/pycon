import strawberry
from strawberry_forms.converter import convert_form_field

from .fields import VoteValueField


@convert_form_field.register(VoteValueField)
def convert_form_field_to_votevalue(field):
    return (int, strawberry.field(description=field.help_text, is_input=True))
