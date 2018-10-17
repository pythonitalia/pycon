from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('conference', 'name',)
    list_filter = ('conference', )

    fieldsets = (
        ('Info', {
            "fields": (
                'conference', 'name', 'code', 'price', 'description',
            ),
        }),
        ('Deadline', {
            'fields': (
                'start', 'end',
            )
        })
    )
