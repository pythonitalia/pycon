from graphene_django.forms.converter import convert_form_field

from .fields import VoteValueField
from .types import VoteValues


@convert_form_field.register(VoteValueField)
def convert_form_field_to_votevalue(field):
    return VoteValues(required=True, description=field.help_text)
