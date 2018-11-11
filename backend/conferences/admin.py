from django.contrib import admin

from .models import Conference, Topic, Deadline


class DeadlineInline(admin.TabularInline):
    model = Deadline


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )
    filter_horizontal = ('topics', 'languages', )
    fieldsets = (
        ('Details', {
            'fields': (
                'name', 'code',
            ),
        }),
        ('Conference', {
            'fields': (
                ('start', 'end'),
                'topics',
                'languages',
            ),
        }),
    )
    inlines = [DeadlineInline, ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
