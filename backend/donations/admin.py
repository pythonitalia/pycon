from django.contrib import admin

from .models import Donation


class DonationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Donation, DonationAdmin)
