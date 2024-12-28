from api.visa.mutations.update_invitation_letter_document import (
    update_invitation_letter_document,
)
from api.visa.mutations.request_invitation_letter import request_invitation_letter
from strawberry.tools import create_type

VisaMutation = create_type(
    "VisaMutation",
    (
        update_invitation_letter_document,
        request_invitation_letter,
    ),
)
