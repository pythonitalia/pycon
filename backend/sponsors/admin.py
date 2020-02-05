from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import Sponsor, SponsorLevel


@admin.register(SponsorLevel)
class SponsorLevelAdmin(OrderedModelAdmin):
    list_display = ("name", "conference", "move_up_down_links")
    readonly_fields = ("order",)


@admin.register(Sponsor)
class SponsorAdmin(OrderedModelAdmin):
    list_display = ("name", "move_up_down_links")
    readonly_fields = ("order",)
