from rest_framework import serializers


class PlainCustomerCardCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    externalId = serializers.CharField(required=False)


class PlainCustomerCardsSerializer(serializers.Serializer):
    cardKeys = serializers.ListField(
        child=serializers.CharField(),
        required=True,
    )
    customer = PlainCustomerCardCustomerSerializer(required=True)
