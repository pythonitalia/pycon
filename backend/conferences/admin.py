from django.contrib import admin

from .models import Conference, Topic, Deadline, AudienceLevel


class DeadlineInline(admin.TabularInline):
    model = Deadline


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )
    filter_horizontal = ('topics', 'languages', 'audience_levels', )
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
                'audience_levels',
                'languages',
            ),
        }),
    )
    inlines = [DeadlineInline, ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(AudienceLevel)
class AudienceLevelAdmin(admin.ModelAdmin):
    pass
