from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import ScheduleItem


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('conference', 'topic', 'start', 'end', 'type', 'title', 'submission')
    ordering = ('conference', 'topic', 'start',)
    fieldsets = (
        (_('Event'), {
            'fields': ('conference', 'type', 'title', 'description', 'submission')
        }),
        (_('Schedule'), {
            'fields': ('start', 'end', 'topic')
        }),
    )
    autocomplete_fields = ('submission',)
