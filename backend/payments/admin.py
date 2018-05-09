from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Payment


def refund(modeladmin, request, queryset):
    for payment in queryset:
        payment.refund()
refund.short_description = _("Refund the payment")


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('provider',)
    list_display = (
        'id',
        'created',
        'status',
        'provider',
        'currency',
        'amount',
    )
    list_filter = (
        'status',
        'provider',
        'currency',
    )
    actions = [refund]


admin.site.register(Payment, PaymentAdmin)
