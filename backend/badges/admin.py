from django.contrib import admin
from badges.models import AttendeeConferenceRole


@admin.register(AttendeeConferenceRole)
class AttendeeConferenceRoleAdmin(admin.ModelAdmin):
    pass
