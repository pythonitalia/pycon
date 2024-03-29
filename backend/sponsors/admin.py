from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import Sponsor, SponsorLead, SponsorLevel


@admin.register(Sponsor)
class SponsorAdmin(OrderedModelAdmin):
    list_display = ("name", "move_up_down_links")
    list_filter = (
        "levels__conference",
        "levels__name",
    )
    readonly_fields = ("order",)


@admin.register(SponsorLevel)
class SponsorLevelAdmin(OrderedModelAdmin):
    list_display = ("name", "conference", "move_up_down_links")
    readonly_fields = ("order",)


@admin.register(SponsorLead)
class SponsorLeadAdmin(admin.ModelAdmin):
    list_display = (
        "fullname",
        "email",
        "company",
        "brochure_viewed",
        "consent_to_contact_via_email",
        "conference",
    )
    search_fields = (
        "fullname",
        "email",
        "company",
    )
    list_filter = ("conference",)
