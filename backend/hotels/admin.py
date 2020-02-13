from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pretix.db import get_orders_status
from pretix.utils import order_status_to_text

from .models import HotelRoom, HotelRoomReservation


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("conference", "name", "price")
    list_filter = ("conference",)


@admin.register(HotelRoomReservation)
class HotelRoomReservationAdmin(admin.ModelAdmin):
    list_display = ("order_code", "order_status", "room", "user", "checkin", "checkout")
    list_filter = ("order_code", "room__conference", "room")

    def order_status(self, obj):
        if obj.order_code not in self._reservation_status:
            return _("Unknown")

        return order_status_to_text(self._reservation_status[obj.order_code])

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        codes = [reservation.order_code for reservation in queryset]
        self._reservation_status = get_orders_status(codes)
        return queryset
