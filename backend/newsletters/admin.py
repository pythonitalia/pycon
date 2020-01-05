from django.contrib import admin, messages

from .models import Email, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "date_subscribed")


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipients_type", "scheduled_date")
    readonly_fields = ("recipients",)
    actions = ["send_emails"]

    def send_emails(self, request, queryset):

        results = []
        for email in queryset:
            results.append(email.send_email())

        if all(results):
            self.message_user(request, f"Successfully sent mails.")
        else:
            self.message_user(
                request, "Mmmm... Something went wrong :(", level=messages.ERROR
            )

    send_emails.short_description = "Send selected Emails"
