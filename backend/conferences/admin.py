from django.contrib import admin

from .models import Conference, Track


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'modified', )
    filter_horizontal = ('tracks', 'languages', )
    fieldsets = (
        ('Details', {
            'fields': (
                'name', 'slug',
            ),
        }),
        ('Conference', {
            'fields': (
                'tracks', 'languages',
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


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
