from graphene import Int, ID, NonNull, InputObjectType, ObjectType, String


class CartItem(InputObjectType):
    id = NonNull(ID)
    quantity = NonNull(Int)


class GenericPaymentFailedError(ObjectType):
    message = NonNull(String)
