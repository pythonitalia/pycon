from django.contrib import admin

from .models import Conference, Topic, Deadline, AudienceLevel, Duration


class DeadlineInline(admin.TabularInline):
    model = Deadline


class DurationInline(admin.StackedInline):
    model = Duration
    filter_horizontal = ('allowed_submission_types', )


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )
    filter_horizontal = ('topics', 'languages', 'audience_levels', 'submission_types', )
    fieldsets = (
        ('Details', {
            'fields': (
                'name', 'code', 'timezone',
            ),
        }),
        ('Conference', {
            'fields': (
                ('start', 'end'),
                'submission_types',
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
