import strawberry


@strawberry.input
class CartItem:
    id: strawberry.ID
    quantity: int


@strawberry.type
class GenericPaymentError:
    message: str


@strawberry.type
class StripeClientSecret:
    client_secret: str
