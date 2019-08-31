from django.contrib import admin

from .models import Sponsor, SponsorLevel


@admin.register(SponsorLevel)
class SponsorLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "conference")


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass
