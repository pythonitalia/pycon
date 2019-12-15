import typing

import strawberry
from conferences.models.conference import Conference
from pretix import CreateOrderInput, create_order


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
        pretix_order = create_order(Conference.objects.get(code=conference), input)

        return CreateOrderResult(payment_url=pretix_order.payment_url)
