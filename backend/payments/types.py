from graphene import Int, ID, NonNull, InputObjectType


class CartItem(InputObjectType):
    id = NonNull(ID)
    quantity = NonNull(Int)
