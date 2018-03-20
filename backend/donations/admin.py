from django.contrib import admin

from .models import Donation

from django.utils.translation import ugettext_lazy as _


class DonationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Donation, DonationAdmin)
