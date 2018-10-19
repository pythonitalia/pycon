from django.contrib import admin

from .models import Conference


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'modified', )
    fieldsets = (
        ('Details', {
            'fields': (
                'name', 'slug',
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
