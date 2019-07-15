from graphene import Int, ID, NonNull, InputObjectType, ObjectType, String


class CartItem(InputObjectType):
    id = NonNull(ID)
    quantity = NonNull(Int)


class GenericPaymentError(ObjectType):
    message = NonNull(String)


class StripeClientSecret(ObjectType):
    client_secret = NonNull(String)
