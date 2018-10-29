from django.contrib import admin

from .models import Conference, Track


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'modified', )
    filter_horizontal = ('tracks',)
    fieldsets = (
        ('Details', {
            'fields': (
                'name', 'slug', 'tracks',
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
