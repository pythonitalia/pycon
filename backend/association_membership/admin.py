from django.contrib import admin

from association_membership.models import (
    Payment,
    PretixPayment,
    Membership,
    StripeSubscriptionPayment,
)


@admin.register(PretixPayment)
class PretixPaymentAdmin(admin.ModelAdmin):
    fields = ("payment", "order_code", "event_organizer", "event_id")


@admin.register(StripeSubscriptionPayment)
class StripeSubscriptionPaymentAdmin(admin.ModelAdmin):
    fields = (
        "payment",
        "stripe_subscription_id",
        "stripe_invoice_id",
        "invoice_pdf",
    )


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = (
        "idempotency_key",
        "total",
        "payment_date",
        "period_start",
        "period_end",
        "status",
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "status")
    list_filter = ("status",)
    search_fields = ("user__email", "user__first_name", "user__last_name")
    autocomplete_fields = ("user",)
    inlines = [PaymentInline]
