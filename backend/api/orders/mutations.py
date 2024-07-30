import typing
from urllib.parse import urljoin

from api.context import Info
from pretix import CreateOrderErrors
import strawberry
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.permissions import IsAuthenticated
from conferences.models.conference import Conference
from hotels.models import HotelRoom, HotelRoomReservation
from pretix import (
    CreateOrderHotelRoom,
    CreateOrderInput,
    Order,
    create_order,
)
from pretix.exceptions import PretixError
from billing.models import BillingAddress as BillingAddressModel


@strawberry.type
class CreateOrderResult:
    payment_url: str


@strawberry.type
class Error:
    message: str


@strawberry.type
class OrdersMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_order(
        self, info: Info, conference: str, input: CreateOrderInput
    ) -> typing.Union[CreateOrderResult, CreateOrderErrors]:
        conference_obj = Conference.objects.get(code=conference)

        if errors := input.validate():
            return errors

        BillingAddressModel.objects.update_or_create(
            user=info.context.request.user,
            organizer_id=conference_obj.organizer_id,
            is_business=input.invoice_information.is_business,
            defaults={
                "company_name": input.invoice_information.company,
                "user_name": input.invoice_information.name,
                "zip_code": input.invoice_information.zipcode,
                "city": input.invoice_information.city,
                "address": input.invoice_information.street,
                "country": input.invoice_information.country,
                "vat_id": input.invoice_information.vat_id,
                "fiscal_code": input.invoice_information.fiscal_code or "",
                "sdi": input.invoice_information.sdi or "",
                "pec": input.invoice_information.pec or "",
            },
        )

        try:
            pretix_order = create_order(conference_obj, input)
        except PretixError as e:
            return CreateOrderErrors.with_error("non_field_errors", str(e))

        if len(input.hotel_rooms) > 0:
            create_hotel_reservations(
                pretix_order, input.hotel_rooms, user_id=info.context.request.user.id
            )

        return_url = urljoin(
            settings.FRONTEND_URL,
            f"/{input.locale}/orders/{pretix_order.code}/confirmation",
        )

        if pretix_order.payment_url is None:
            return CreateOrderResult(payment_url=return_url)

        payment_url = pretix_order.payment_url
        payment_url += f"?return_url={return_url}"

        return CreateOrderResult(payment_url=payment_url)


def validate_hotel_rooms(hotel_rooms: typing.List[CreateOrderHotelRoom], *, conference):
    count_rooms = {}

    conference_start = conference.start.date()
    conference_end = conference.end.date()

    for order_room in hotel_rooms:
        try:
            room = HotelRoom.objects.get(id=order_room.room_id, conference=conference)
        except HotelRoom.DoesNotExist:
            return Error(
                message=_("Room %(id)s not found") % {"id": order_room.room_id}
            )

        if room.is_sold_out:
            return Error(
                message=_("Room %(id)s is sold out") % {"id": order_room.room_id}
            )

        count = count_rooms.get(room.pk, 0)

        if count + 1 > room.capacity_left:
            return Error(message=_("Too many rooms") % {"id": order_room.room_id})

        count_rooms[room.pk] = count + 1

        if order_room.checkin < conference_start or order_room.checkin > conference_end:
            return Error(message=_("Invaild check-in date"))

        if (
            order_room.checkout < conference_start
            or order_room.checkout > conference_end
            or order_room.checkin > order_room.checkout
        ):
            return Error(message=_("Invaild check-out date"))

        if not room.available_bed_layouts.filter(id=order_room.bed_layout_id).exists():
            return Error(message=_("Invaild bed layout"))


def create_hotel_reservations(
    pretix_order: Order, hotel_rooms: typing.List[CreateOrderHotelRoom], user_id: int
):
    for room in hotel_rooms:
        HotelRoomReservation.objects.create(
            room_id=room.room_id,
            order_code=pretix_order.code,
            checkin=room.checkin,
            checkout=room.checkout,
            user_id=user_id,
            bed_layout_id=room.bed_layout_id,
        )
