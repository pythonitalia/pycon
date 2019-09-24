from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start", "end", "conference")
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "title",
                    "slug",
                    "content",
                    "conference",
                    "start",
                    "end",
                    "image",
                )
            },
        ),
        ("Location", {"fields": ("latitude", "longitude", "map_link")}),
    )
