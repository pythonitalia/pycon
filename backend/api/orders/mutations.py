import strawberry
from conferences.models.conference import Conference
from pretix import CreateOrderData, create_order


@strawberry.type
class OrdersMutations:
    @strawberry.mutation
    def create_order(self, info) -> str:
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

        return pretix_order.payment_url
