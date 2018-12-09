from django.contrib import admin

from .models import Conference, Topic, Deadline, AudienceLevel, Duration


class DeadlineInline(admin.TabularInline):
    model = Deadline


class DurationInline(admin.TabularInline):
    model = Duration


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
    inlines = [DeadlineInline, DurationInline, ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(AudienceLevel)
class AudienceLevelAdmin(admin.ModelAdmin):
    pass
