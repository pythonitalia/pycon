import strawberry
from grants.forms import GrantForm
from strawberry_forms.mutations import FormMutation

from .types import GrantRequest


class SendGrantRequest(FormMutation):
    @classmethod
    def transform(cls, result):
        result._type_definition = GrantRequest._type_definition
        return result

    class Meta:
        output_types = (GrantRequest,)
        form_class = GrantForm


@strawberry.type
class GrantsMutations:
    send_grant_request = SendGrantRequest.Mutation
