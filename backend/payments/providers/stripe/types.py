import graphene

from graphene import String, Int, ID, NonNull, ObjectType


class Stripe3DValidationRequired(ObjectType):
    client_secret = NonNull(String)
