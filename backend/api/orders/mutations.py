from urllib.parse import urljoin

from api.context import Info
from privacy_policy.record import record_privacy_policy_acceptance
import strawberry
from django.conf import settings

from api.permissions import IsAuthenticated
from api.pretix.types import CreateOrderErrors, CreateOrderInput
from conferences.models.conference import Conference
from pretix import create_order
from pretix.exceptions import PretixError
from billing.models import BillingAddress as BillingAddressModel


@strawberry.type
class CreateOrderResult:
    payment_url: str


@strawberry.type
class Error:
    message: str


@strawberry.type
class OrdersMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_order(
        self, info: Info, conference: str, input: CreateOrderInput
    ) -> CreateOrderResult | CreateOrderErrors:
        conference_obj = Conference.objects.get(code=conference)

        if errors := input.validate(conference_obj):
            return errors

        BillingAddressModel.objects.update_or_create(
            user=info.context.request.user,
            organizer_id=conference_obj.organizer_id,
            is_business=input.invoice_information.is_business,
            defaults={
                "company_name": input.invoice_information.company,
                "user_given_name": input.invoice_information.given_name,
                "user_family_name": input.invoice_information.family_name,
                "zip_code": input.invoice_information.zipcode,
                "city": input.invoice_information.city,
                "address": input.invoice_information.street,
                "country": input.invoice_information.country,
                "vat_id": input.invoice_information.vat_id,
                "fiscal_code": input.invoice_information.fiscal_code or "",
                "sdi": input.invoice_information.sdi or "",
                "pec": input.invoice_information.pec or "",
            },
        )

        try:
            pretix_order = create_order(conference_obj, input)
        except PretixError as e:
            return CreateOrderErrors.with_error("non_field_errors", str(e))

        record_privacy_policy_acceptance(
            info.context.request, conference_obj, "checkout-order"
        )

        return_url = urljoin(
            settings.FRONTEND_URL,
            f"/{input.locale}/orders/{pretix_order.code}/confirmation",
        )

        if pretix_order.payment_url is None:
            return CreateOrderResult(payment_url=return_url)

        payment_url = pretix_order.payment_url
        payment_url += f"?return_url={return_url}"

        return CreateOrderResult(payment_url=payment_url)
