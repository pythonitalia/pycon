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
        self, info, input: CreateOrderInput
    ) -> typing.Union[CreateOrderResult, Error]:
        # TODO:
        conference = Conference.objects.first()

        pretix_order = create_order(conference, input)

        return CreateOrderResult(payment_url=pretix_order.payment_url)
