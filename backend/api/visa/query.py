from api.visa.queries.invitation_letter_document import invitation_letter_document
from strawberry.tools import create_type


VisaQuery = create_type(
    "VisaQuery",
    (invitation_letter_document,),
)
