from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pretix.db import get_orders_status
from pretix.utils import order_status_to_text
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin

from .models import HotelRoom, HotelRoomReservation


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("conference", "name", "price")
    list_filter = ("conference",)


class HotelRoomReservationForm(forms.ModelForm):
    class Meta:
        model = HotelRoomReservation
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = ["order_code", "room", "checkin", "checkout"]


@admin.register(HotelRoomReservation)
class HotelRoomReservationAdmin(AdminUsersMixin):
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
    readonly_fields = ("user_info", "checkin", "checkout", "order_code", "room")

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def user_display_name(self, obj):
        return self.get_user_display_name(obj.user_id)

    def user_info(self, obj):
        user_data = self.get_user_data(obj.user_id)
        display_name = user_data["displayName"]
        email = user_data["email"]
        id = user_data["id"]
        return f"{display_name} ({email}) #{id}"

    user_info.short_description = "User"

    def order_status(self, obj):
        if obj.order_code not in self._reservation_status:
            return _("Unknown")

        return order_status_to_text(self._reservation_status[obj.order_code])

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        codes = [reservation.order_code for reservation in queryset]
        self._reservation_status = get_orders_status(codes)
        return queryset
