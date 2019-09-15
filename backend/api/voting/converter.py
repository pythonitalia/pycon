import strawberry
from strawberry_forms.converter import convert_form_field, type_or_optional_wrapped

from .fields import VoteValueField
from .types import VoteValues


@convert_form_field.register(VoteValueField)
def convert_form_field_to_votevalue(field):
    return (
        type_or_optional_wrapped(VoteValues, field.required),
        strawberry.field(description=field.help_text, is_input=True),
    )
