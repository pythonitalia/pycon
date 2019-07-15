from django.contrib import admin

from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_fare_name', 'user_email')
    search_filters = ('user__email', 'conference__code',)

    def ticket_fare_name(self, obj):
        return obj.ticket_fare.name

    def user_email(self, obj):
        return obj.user.email
