import typing
from urllib.parse import urljoin

import strawberry
from conferences.models.conference import Conference
from django.conf import settings
from pretix import CreateOrderInput, create_order
from pretix.exceptions import PretixError


@strawberry.type
class CreateOrderResult:
    payment_url: str


@strawberry.type
class Error:
    message: str


@strawberry.type
class OrdersMutations:
    @strawberry.mutation
    def create_order(
        self, info, conference: str, input: CreateOrderInput
    ) -> typing.Union[CreateOrderResult, Error]:
        try:
            pretix_order = create_order(Conference.objects.get(code=conference), input)
        except PretixError as e:
            return Error(message=e.message)

        return_url = urljoin(
            settings.FRONTEND_URL,
            f"/{input.locale}/orders/{pretix_order.code}/confirmation",
        )

        payment_url = pretix_order.payment_url
        payment_url += f"?return_url={return_url}"

        return CreateOrderResult(payment_url=payment_url)
