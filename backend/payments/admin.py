from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'status',
        'provider',
        'currency',
        'total',
    )
    list_filter = (
        'status',
        'provider',
        'currency',
    )


admin.site.register(Payment, PaymentAdmin)
