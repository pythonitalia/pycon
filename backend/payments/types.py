import graphene


from graphene_django.forms.converter import convert_form_field


class CartItem(graphene.InputObjectType):
    id = graphene.ID()
    quantity = graphene.Int()


class PaymentPayload(graphene.InputObjectType):
    payment_method_id = graphene.String()


class PaymentFailed(graphene.ObjectType):
    # TOOD: Enum!
    reason = graphene.NonNull(graphene.String)


class PaymentResponse(graphene.Union):
    class Meta:
        types = (PaymentFailed,)
