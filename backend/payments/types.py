from graphene import Int, ID, NonNull, InputObjectType, ObjectType, String, List

from conferences.types import TicketType
from orders.types import OrderType


class CartItem(InputObjectType):
    id = NonNull(ID)
    quantity = NonNull(Int)


class GenericPaymentError(ObjectType):
    message = NonNull(String)


class StripeClientSecret(ObjectType):
    client_secret = NonNull(String)
