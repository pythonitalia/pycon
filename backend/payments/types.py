import graphene

from graphene import String, Int, ID, NonNull


class CartItem(graphene.InputObjectType):
    id = NonNull(ID)
    quantity = NonNull(Int)


class PaymentPayload(graphene.InputObjectType):
    payment_method_id = String()


class Stripe3DValidationRequired(graphene.ObjectType):
    client_secret = NonNull(String)
