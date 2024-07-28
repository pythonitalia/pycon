from countries import countries
from typing import Annotated
from api.billing.types import BillingAddress
from api.types import BaseErrorType
from billing.validation import (
    validate_cap_code,
    validate_fiscal_code,
    validate_italian_partita_iva,
    validate_sdi_code,
)
from billing.exceptions import (
    CapCodeValidationError,
    FiscalCodeValidationError,
    PartitaIvaValidationError,
    SdiValidationError,
)
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

        if not self.user_name:
            errors.add_error("user_name", "User name is required")

        if not self.address:
            errors.add_error("address", "Address is required")

        if not self.country:
            errors.add_error("country", "Country is required")
        elif not countries.is_valid(self.country):
            errors.add_error("country", "Invalid country code")

        if not self.city:
            errors.add_error("city", "City is required")

        if not self.zip_code:
            errors.add_error("zip_code", "Zip code is required")
        elif self.country == "IT":
            self.validate_cap_code(errors)

        if not self.vat_id:
            errors.add_error("vat_id", "VAT ID is required")

        if self.country == "IT":
            if self.is_business and not self.sdi:
                errors.add_error("sdi", "SDI is required")
            else:
                self.validate_sdi(errors)

            if self.is_business and not self.vat_id:
                errors.add_error("vat_id", "VAT ID is required")
            elif self.vat_id:
                self.validate_partita_iva(errors)

            if not self.is_business and not self.fiscal_code:
                errors.add_error("fiscal_code", "Fiscal code is required")
            elif self.fiscal_code:
                self.validate_fiscal_code(errors)

        if self.is_business and not self.company_name:
            errors.add_error("company_name", "Company name is required")

        return errors.if_has_errors

    def validate_fiscal_code(self, errors: UpdateBillingAddressErrors):
        try:
            validate_fiscal_code(self.fiscal_code)
        except FiscalCodeValidationError as exc:
            errors.add_error("fiscal_code", str(exc))

    def validate_partita_iva(self, errors: UpdateBillingAddressErrors):
        try:
            validate_italian_partita_iva(self.vat_id)
        except PartitaIvaValidationError as exc:
            errors.add_error("vat_id", str(exc))

    def validate_cap_code(self, errors: UpdateBillingAddressErrors):
        try:
            validate_cap_code(self.zip_code)
        except CapCodeValidationError as exc:
            errors.add_error("zip_code", str(exc))

    def validate_sdi(self, errors: UpdateBillingAddressErrors):
        try:
            validate_sdi_code(self.sdi)
        except SdiValidationError as exc:
            errors.add_error("sdi", str(exc))


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
