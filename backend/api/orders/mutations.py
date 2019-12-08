import typing

import strawberry
from conferences.models.conference import Conference
from pretix import CreateOrderData, create_order


@strawberry.input
class CreateOrderTicket:
    ticketId: str
    total: int


@strawberry.input
class CreateOrderInput:
    payment_provider: str
    tickets: typing.List[CreateOrderTicket]


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

        pretix_order = create_order(
            conference,
            CreateOrderData(
                email="patrick.arminio@gmail.com",
                locale="en",
                payment_provider="stripe",
            ),
        )  # noqa

        return CreateOrderResult(payment_url=pretix_order.payment_url)
