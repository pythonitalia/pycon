from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('conference', 'title', 'topic', 'language',)
    list_filter = ('conference',)
    search_fields = ('title', 'abstract',)
