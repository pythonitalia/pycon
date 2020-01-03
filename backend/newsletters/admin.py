from django.contrib import admin

from .models import Email, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "date_subscribed")


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipients_types", "scheduled_date")
    readonly_fields = ("recipients",)
    actions = ["send_emails"]

    def send_emails(self, request, queryset):
        pass

        self.message_user(request, f"Successfully sent mails.")

    send_emails.short_description = "Send selected Emails"
