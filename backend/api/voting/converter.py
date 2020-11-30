import dataclasses
from strawberry_forms.converter import convert_form_field

from .fields import VoteValueField


@convert_form_field.register(VoteValueField)
def convert_form_field_to_votevalue(field):
    return (int, dataclasses.field(default=field.initial))
