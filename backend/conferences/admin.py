from django.contrib import admin

from .models import Conference, Topic, Deadline, AudienceLevel, Duration, TicketFare, Ticket


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


@admin.register(TicketFare)
class TicketFareAdmin(admin.ModelAdmin):
    list_display = ('conference', 'name',)
    list_filter = ('conference', )

    fieldsets = (
        ('Info', {
            "fields": (
                'conference', 'name', 'code', 'price', 'description',
            ),
        }),
        ('Deadline', {
            'fields': (
                'start', 'end',
            )
        })
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_fare_name', 'user_email')
    search_filters = ('user__email', 'conference__code',)

    def ticket_fare_name(self, obj):
        return obj.ticket_fare.name

    def user_email(self, obj):
        return obj.user.email
