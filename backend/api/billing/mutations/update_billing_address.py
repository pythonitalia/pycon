from typing import Annotated
from api.billing.types import BillingAddress
from api.types import BaseErrorType
from conferences.models.conference import Conference
import strawberry
from api.permissions import IsAuthenticated
from api.context import Info
from billing.models import BillingAddress as BillingAddressModel


@strawberry.type
class UpdateBillingAddressErrors(BaseErrorType):
    @strawberry.type
    class _UpdateBillingAddressErrors:
        conference: list[str] = strawberry.field(default_factory=list)
        is_business: list[str] = strawberry.field(default_factory=list)
        company_name: list[str] = strawberry.field(default_factory=list)
        user_name: list[str] = strawberry.field(default_factory=list)
        zip_code: list[str] = strawberry.field(default_factory=list)
        city: list[str] = strawberry.field(default_factory=list)
        address: list[str] = strawberry.field(default_factory=list)
        country: list[str] = strawberry.field(default_factory=list)
        vat_id: list[str] = strawberry.field(default_factory=list)
        fiscal_code: list[str] = strawberry.field(default_factory=list)
        sdi: list[str] = strawberry.field(default_factory=list)
        pec: list[str] = strawberry.field(default_factory=list)

    errors: _UpdateBillingAddressErrors = None


@strawberry.input
class UpdateBillingAddressInput:
    conference: str
    is_business: bool
    company_name: str
    user_name: str
    zip_code: str
    city: str
    address: str
    country: str
    vat_id: str
    fiscal_code: str
    sdi: str
    pec: str

    def validate(self) -> UpdateBillingAddressErrors:
        errors = UpdateBillingAddressErrors()

        return errors.if_has_errors


UpdateBillingAddressOutput = Annotated[
    BillingAddress | UpdateBillingAddressErrors,
    strawberry.union(name="UpdateBillingAddressOutput"),
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def update_billing_address(
    info: Info, input: UpdateBillingAddressInput
) -> UpdateBillingAddressOutput:
    if errors := input.validate():
        return errors

    user = info.context.request.user
    conference = Conference.objects.get(code=input.conference)
    billing_address, _ = BillingAddressModel.objects.update_or_create(
        user=user,
        organizer_id=conference.organizer_id,
        is_business=input.is_business,
        defaults={
            "company_name": input.company_name,
            "user_name": input.user_name,
            "zip_code": input.zip_code,
            "city": input.city,
            "address": input.address,
            "country": input.country,
            "vat_id": input.vat_id,
            "fiscal_code": input.fiscal_code,
            "sdi": input.sdi,
            "pec": input.pec,
        },
    )
    return BillingAddress.from_django_model(billing_address)
