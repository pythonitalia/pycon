from django.contrib import admin

from .models import HotelRoom, HotelRoomReservation


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("conference", "name", "price")
    list_filter = ("conference",)


@admin.register(HotelRoomReservation)
class HotelRoomReservationAdmin(admin.ModelAdmin):
    list_display = ("order_code", "room", "user", "checkin", "checkout")
    list_filter = ("order_code", "room__conference", "room")
