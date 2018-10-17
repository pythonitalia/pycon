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
            'fields': (('start', 'end'),),
        })
    )
