from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from checklist.models import ChecklistItem


@admin.register(ChecklistItem)
class ChecklistAdmin(OrderedModelAdmin):
    list_display = ("text", "move_up_down_links")
