from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pretix.db import get_orders_status
from pretix.utils import order_status_to_text

from .models import BedLayout, HotelRoom, HotelRoomReservation


@admin.register(BedLayout)
class BedLayoutAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("conference", "name", "price")
    list_filter = ("conference",)


class HotelRoomReservationForm(forms.ModelForm):
    class Meta:
        model = HotelRoomReservation
        fields = ["order_code", "room", "checkin", "checkout"]


@admin.register(HotelRoomReservation)
class HotelRoomReservationAdmin(admin.ModelAdmin):
    form = HotelRoomReservationForm
    list_display = (
        "order_code",
        "order_status",
        "room",
        "user_display_name",
        "checkin",
        "checkout",
    )
    list_filter = ("room__conference", "room")
    user_fk = "user_id"
    readonly_fields = (
        "user_info",
        "checkin",
        "checkout",
        "order_code",
    )

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def user_display_name(self, obj):
        return obj.user.display_name

    @admin.display(
        description="User",
    )
    def user_info(self, obj):
        display_name = obj.user.display_name
        email = obj.user.email
        id = obj.user_id
        return f"{display_name} ({email}) #{id}"

    def order_status(self, obj):
        if obj.order_code not in self._reservation_status:
            return _("Unknown")

        return order_status_to_text(self._reservation_status[obj.order_code])

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        codes = [reservation.order_code for reservation in queryset]
        self._reservation_status = get_orders_status(codes)
        return queryset
