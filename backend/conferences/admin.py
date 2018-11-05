from django.contrib import admin

from .models import Conference, Topic


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
                'topics', 'languages',
            ),
        }),
        ('Deadlines', {
            'fields': (
                ('start', 'end'),
                ('cfp_start', 'cfp_end'),
                ('voting_start', 'voting_end'),
                ('refund_start', 'refund_end'),
            ),
        })
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
