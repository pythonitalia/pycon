from admin_views.admin import AdminViews
from django.contrib import admin, messages
from django.shortcuts import redirect
from notifications.aws import convert_users_to_endpoints, send_endpoints_to_pinpoint
from users.models import User

from .models import Email, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(AdminViews):
    list_display = ("email", "date_subscribed")
    admin_views = (("Export all users to Pinpoint", "export_all_users_to_pinpoint"),)

    def export_all_users_to_pinpoint(self, request, **kwargs):  # pragma: no cover
        users = User.objects.all()

        endpoints = convert_users_to_endpoints(users)
        send_endpoints_to_pinpoint(endpoints)

        self.message_user(
            request, "Exported all the users to Pinpoint", level=messages.SUCCESS
        )

        return redirect("admin:index")


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    ordering = ["status", "scheduled_date", "-pk"]
    list_display = (
        "subject",
        "recipients_type",
        "scheduled_date",
        "status",
        "email_actions",
    )
    readonly_fields = ("recipients", "email_actions")
