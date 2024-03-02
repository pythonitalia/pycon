from conferences.models.conference import Conference
from integrations.permissions import IsPlainAuthenticated, PlainAuthentication
from integrations.plain_cards import create_grant_card
from integrations.serializers import PlainCustomerCardsSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import status
from rest_framework.response import Response
from users.models import User


@api_view(["POST"])
@permission_classes([IsPlainAuthenticated])
@authentication_classes([PlainAuthentication])
def plain_customer_cards(request):
    conference_id = request.headers.get("Conference-Id")
    serializer = PlainCustomerCardsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    customer_email = data["customer"]["email"]
    card_keys = data["cardKeys"]

    conference = Conference.objects.filter(id=conference_id).first()
    if not conference:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=customer_email).first()

    if not user:
        return Response(status=status.HTTP_404_NOT_FOUND)

    cards = []
    if "grant" in card_keys:
        cards.append(create_grant_card(request, user, conference))

    return Response({"cards": cards})
