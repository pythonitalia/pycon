from django.contrib import admin

from .models import BedLayout, HotelRoom


@admin.register(BedLayout)
class BedLayoutAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("conference", "name", "price")
    list_filter = ("conference",)
